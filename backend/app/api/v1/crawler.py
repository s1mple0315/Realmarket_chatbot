from fastapi import APIRouter, Depends, HTTPException
from app.services.auth_service import verify_token
from app.database import db
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


class CrawlRequest(BaseModel):
    url: str
    content_type: str
    assistant_id: str


def clean_text(text: str) -> str:
    """Clean scraped text by removing extra whitespace and invalid characters."""
    return re.sub(r"\s+", " ", text.strip()) if text else ""


def extract_products(soup: BeautifulSoup) -> list:
    """Extract product data from common e-commerce page structures."""
    products = []
    # Common product containers (adjust selectors based on real-world testing)
    product_elements = soup.select("div.product, article.product, div.item, li.product")
    for elem in product_elements:
        name = elem.select_one("h2, h3, .product-title, .item-name")
        price = elem.select_one(".price, .product-price, .amount")
        description = elem.select_one(".description, .product-description, p")
        product = {
            "name": clean_text(name.text) if name else "Unknown Product",
            "price": clean_text(price.text) if price else "N/A",
            "description": clean_text(description.text) if description else "",
        }
        products.append(product)
    return products


def extract_articles(soup: BeautifulSoup) -> list:
    """Extract article data from blog or news pages."""
    articles = []
    # Common article containers
    article_elements = soup.select("article, div.post, div.article, .blog-post")
    for elem in article_elements:
        title = elem.select_one("h1, h2, .post-title, .article-title")
        body = elem.select_one(".content, .post-content, .article-body, p")
        articles.append(
            {
                "title": clean_text(title.text) if title else "Untitled Article",
                "body": clean_text(body.text) if body else "",
            }
        )
    return articles


@router.post("/crawl")
async def crawl_website(request: CrawlRequest, user_id: str = Depends(verify_token)):
    logger.info(f"Crawling URL: {request.url} for assistant_id: {request.assistant_id}")

    # Verify assistant
    assistant = await db.assistants.find_one(
        {"assistant_id": request.assistant_id, "user_id": user_id}
    )
    if not assistant:
        raise HTTPException(
            status_code=404, detail="Assistant not found or not authorized"
        )

    # Validate URL
    if not request.url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="Invalid URL format")

    try:
        # Fetch webpage
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(request.url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract data based on content_type
        data = []
        if request.content_type == "products":
            data = extract_products(soup)
        elif request.content_type == "articles":
            data = extract_articles(soup)
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported content_type. Use 'products' or 'articles'.",
            )

        if not data:
            logger.warning(f"No {request.content_type} found at {request.url}")
            raise HTTPException(
                status_code=404,
                detail=f"No {request.content_type} found at the provided URL",
            )

        # Store extracted data
        content_data = {
            "assistant_id": request.assistant_id,
            "content_type": request.content_type,
            "data": data,
            "source": "crawler",
            "url": request.url,
            "created_at": datetime.utcnow(),
        }
        await db.assistant_content.replace_one(
            {
                "assistant_id": request.assistant_id,
                "content_type": request.content_type,
                "source": "crawler",
            },
            content_data,
            upsert=True,
        )

        # Store crawl history
        crawl_history = {
            "assistant_id": request.assistant_id,
            "url": request.url,
            "content_type": request.content_type,
            "created_at": datetime.utcnow(),
        }
        await db.crawler_history.insert_one(crawl_history)

        return {
            "message": f"Successfully crawled {request.url} for {request.content_type}",
            "data": data,
        }
    except requests.RequestException as e:
        logger.error(f"Failed to fetch URL: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch URL: {str(e)}")
    except Exception as e:
        logger.error(f"Failed to crawl website: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to crawl website: {str(e)}"
        )


@router.get("/history")
async def get_crawl_history(assistant_id: str, user_id: str = Depends(verify_token)):
    logger.info(f"Fetching crawl history for assistant_id: {assistant_id}")
    assistant = await db.assistants.find_one(
        {"assistant_id": assistant_id, "user_id": user_id}
    )
    if not assistant:
        raise HTTPException(
            status_code=404, detail="Assistant not found or not authorized"
        )

    history = await db.crawler_history.find({"assistant_id": assistant_id}).to_list(
        length=100
    )
    for item in history:
        item.pop("_id", None)
    return {"history": history}
