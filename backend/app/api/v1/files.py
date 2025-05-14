from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.services.auth_service import verify_token
from app.database import db
from openai import OpenAI
import os
import csv
import io
import PyPDF2
import logging
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize OpenAI client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise HTTPException(status_code=500, detail="OpenAI API key is not configured")

client = OpenAI(api_key=OPENAI_API_KEY)


class FileUploadRequest(BaseModel):
    purpose: str = "assistants"
    content_type: Optional[str] = None
    assistant_id: str


def extract_csv_content(file_content: bytes) -> list:
    try:
        text = file_content.decode("utf-8")
        csv_file = io.StringIO(text)
        reader = csv.DictReader(csv_file)
        return [dict(row) for row in reader]
    except Exception as e:
        logger.error(f"Failed to extract CSV content: {str(e)}")
        return []


def extract_pdf_content(file_content: bytes) -> list:
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        # Split into pseudo-items for simplicity
        return [{"text": text[:500]}]  # Limit for context
    except Exception as e:
        logger.error(f"Failed to extract PDF content: {str(e)}")
        return []


def extract_txt_content(file_content: bytes) -> list:
    try:
        text = file_content.decode("utf-8")
        return [{"text": text[:500]}]  # Limit for context
    except Exception as e:
        logger.error(f"Failed to extract TXT content: {str(e)}")
        return []


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    purpose: str = "assistants",
    content_type: Optional[str] = None,
    assistant_id: str = None,
    user_id: str = Depends(verify_token),
):
    logger.info(f"Uploading file for user_id: {user_id}, assistant_id: {assistant_id}")

    # Validate inputs
    if purpose not in ["assistants", "vision"]:
        raise HTTPException(
            status_code=400, detail="Purpose must be 'assistants' or 'vision'"
        )
    if not assistant_id:
        raise HTTPException(status_code=400, detail="Assistant ID is required")

    # Verify assistant
    assistant = await db.assistants.find_one(
        {"assistant_id": assistant_id, "user_id": user_id}
    )
    if not assistant:
        raise HTTPException(
            status_code=404, detail="Assistant not found or not authorized"
        )

    try:
        # Upload file to OpenAI
        file_content = await file.read()
        openai_file = client.files.create(
            file=(file.filename, file_content), purpose=purpose
        )

        # Extract content based on file type
        extracted_data = []
        if file.filename.endswith(".csv"):
            extracted_data = extract_csv_content(file_content)
        elif file.filename.endswith(".pdf"):
            extracted_data = extract_pdf_content(file_content)
        elif file.filename.endswith(".txt"):
            extracted_data = extract_txt_content(file_content)

        # Store file metadata
        file_metadata = {
            "file_id": openai_file.id,
            "assistant_id": assistant_id,
            "filename": file.filename,
            "purpose": purpose,
            "content_type": content_type,
            "created_at": datetime.utcnow(),
        }
        await db.assistant_files.insert_one(file_metadata)

        # Store extracted content in assistant_content
        if extracted_data and content_type:
            content_data = {
                "assistant_id": assistant_id,
                "content_type": content_type,
                "data": extracted_data,
                "source": "file",
                "file_id": openai_file.id,
                "created_at": datetime.utcnow(),
            }
            await db.assistant_content.replace_one(
                {
                    "assistant_id": assistant_id,
                    "content_type": content_type,
                    "source": "file",
                },
                content_data,
                upsert=True,
            )

        return {
            "file_id": openai_file.id,
            "filename": file.filename,
            "content_type": content_type,
            "extracted_data": extracted_data,
        }
    except Exception as e:
        logger.error(f"Failed to upload file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")


@router.get("/")
async def list_files(assistant_id: str, user_id: str = Depends(verify_token)):
    logger.info(f"Listing files for assistant_id: {assistant_id}")
    assistant = await db.assistants.find_one(
        {"assistant_id": assistant_id, "user_id": user_id}
    )
    if not assistant:
        raise HTTPException(
            status_code=404, detail="Assistant not found or not authorized"
        )

    files = await db.assistant_files.find({"assistant_id": assistant_id}).to_list(
        length=100
    )
    for file in files:
        file.pop("_id", None)
    return {"files": files}
