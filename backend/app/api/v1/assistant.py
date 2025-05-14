from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    WebSocket,
    WebSocketDisconnect,
)
from app.services.auth_service import verify_token
from app.database import db
import os
from openai import OpenAI, AuthenticationError
from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="OpenAI API key is not configured",
    )

client = OpenAI(api_key=OPENAI_API_KEY)


# Request models
class Tool(BaseModel):
    type: str = Field(
        ..., description="Tool type, e.g., 'code_interpreter' or 'file_search'"
    )

    @validator("type")
    def validate_tool_type(cls, v):
        allowed_types = ["code_interpreter", "file_search", "function"]
        if v not in allowed_types:
            raise ValueError(f"Tool type must be one of {allowed_types}")
        return v


class CreateAssistantRequest(BaseModel):
    name: Optional[str] = None
    instructions: Optional[str] = "You are a helpful assistant for a website."
    model: Optional[str] = "gpt-4o-mini"
    tools: Optional[List[Tool]] = None
    tool_resources: Optional[Dict[str, Any]] = None


class UpdateAssistantRequest(BaseModel):
    name: Optional[str] = None
    instructions: Optional[str] = None


class ConfigureAssistantRequest(BaseModel):
    system_prompt: str = Field(
        ..., description="System prompt defining the assistant's role and behavior"
    )
    tone: str = Field("casual", description="Tone of responses, e.g., casual, formal")
    language: str = Field("ru", description="Primary language, e.g., ru, en")
    data_collection: Optional[Dict[str, bool]] = Field(
        None, description="Fields to collect, e.g., {'email': true, 'name': false}"
    )


class UserDataRequest(BaseModel):
    user_id: str
    name: Optional[str] = None
    email: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None


class ContentRequest(BaseModel):
    content_type: str = Field(
        ..., description="Type of content, e.g., 'products', 'articles', 'services'"
    )
    data: List[Dict[str, Any]] = Field(
        ...,
        description="List of content items, e.g., [{'name': 'Phone', 'price': 599}, ...]",
    )


@router.post("/")
async def create_assistant(
    request: CreateAssistantRequest, user_id: str = Depends(verify_token)
):
    logger.info(f"Received request to create assistant: {request.dict()}")
    try:
        assistant_name = request.name or f"Assistant for {user_id}"
        tools = [tool.dict() for tool in request.tools] if request.tools else []
        if len(tools) > 128:
            raise HTTPException(status_code=400, detail="Maximum 128 tools allowed")

        tool_resources = request.tool_resources or {}
        if (
            "code_interpreter" in [tool["type"] for tool in tools]
            and "code_interpreter" in tool_resources
        ):
            file_ids = tool_resources["code_interpreter"].get("file_ids", [])
            if not file_ids or len(file_ids) > 20:
                raise HTTPException(
                    status_code=400,
                    detail="At least one valid file ID is required for code_interpreter, and maximum 20 files allowed.",
                )
        elif (
            "file_search" in [tool["type"] for tool in tools]
            and "file_search" in tool_resources
        ):
            file_ids = tool_resources["file_search"].get("file_ids", [])
            if not file_ids or len(file_ids) > 20:
                raise HTTPException(
                    status_code=400,
                    detail="At least one valid file ID is required for file_search, and maximum 20 files allowed.",
                )
        else:
            tool_resources = None

        assistant = client.beta.assistants.create(
            name=assistant_name,
            instructions=request.instructions,
            model=request.model,
            tools=tools,
            tool_resources=tool_resources,
        )

        assistant_data = {
            "assistant_id": assistant.id,
            "user_id": user_id,
            "name": assistant_name,
            "instructions": request.instructions,
            "model": request.model,
            "tools": tools,
            "tool_resources": tool_resources,
            "config": {
                "system_prompt": request.instructions,
                "tone": "casual",
                "language": "ru",
                "data_collection": {"email": True, "name": False},
            },
            "created_at": datetime.utcnow(),
        }
        await db.assistants.insert_one(assistant_data)

        user = await db.users.find_one({"email": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        assistants = user.get("assistants", [])
        assistants.append(assistant.id)
        await db.users.update_one(
            {"email": user_id}, {"$set": {"assistants": assistants}}
        )

        return {
            "message": f"Assistant {assistant.id} created by {user_id}",
            "assistant_id": assistant.id,
        }
    except AuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid OpenAI API key"
        )
    except Exception as e:
        logger.error(f"Error creating assistant: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create assistant: {str(e)}",
        )


@router.get("/")
async def list_assistants(user_id: str = Depends(verify_token)):
    assistants = await db.assistants.find({"user_id": user_id}).to_list(length=100)
    for assistant in assistants:
        assistant.pop("_id", None)
    return {"assistants": assistants}


@router.put("/{assistant_id}")
async def update_assistant(
    assistant_id: str,
    request: UpdateAssistantRequest,
    user_id: str = Depends(verify_token),
):
    assistant = await db.assistants.find_one(
        {"assistant_id": assistant_id, "user_id": user_id}
    )
    if not assistant:
        raise HTTPException(
            status_code=404, detail="Assistant not found or not authorized"
        )

    try:
        updated_assistant = client.beta.assistants.update(
            assistant_id=assistant_id,
            name=request.name or assistant["name"],
            instructions=request.instructions or assistant["instructions"],
        )

        update_data = {
            "name": updated_assistant.name,
            "instructions": updated_assistant.instructions,
            "updated_at": datetime.utcnow(),
        }
        await db.assistants.update_one(
            {"assistant_id": assistant_id}, {"$set": update_data}
        )

        return {"message": f"Assistant {assistant_id} updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update assistant: {str(e)}"
        )


@router.delete("/{assistant_id}")
async def delete_assistant(assistant_id: str, user_id: str = Depends(verify_token)):
    assistant = await db.assistants.find_one(
        {"assistant_id": assistant_id, "user_id": user_id}
    )
    if not assistant:
        raise HTTPException(
            status_code=404, detail="Assistant not found or not authorized"
        )

    try:
        client.beta.assistants.delete(assistant_id=assistant_id)
        await db.assistants.delete_one({"assistant_id": assistant_id})
        await db.conversations.delete_many({"assistant_id": assistant_id})
        return {"message": f"Assistant {assistant_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete assistant: {str(e)}"
        )


@router.put("/{assistant_id}/configure")
async def configure_assistant(
    assistant_id: str,
    request: ConfigureAssistantRequest,
    user_id: str = Depends(verify_token),
):
    logger.info(f"Configuring assistant_id: {assistant_id} for user_id: {user_id}")
    assistant = await db.assistants.find_one(
        {"assistant_id": assistant_id, "user_id": user_id}
    )
    if not assistant:
        raise HTTPException(
            status_code=404, detail="Assistant not found or not authorized"
        )

    try:
        update_data = {
            "config": request.dict(),
            "updated_at": datetime.utcnow(),
        }
        await db.assistants.update_one(
            {"assistant_id": assistant_id}, {"$set": update_data}
        )
        return {"message": f"Assistant {assistant_id} configuration updated"}
    except Exception as e:
        logger.error(f"Error configuring assistant: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to configure assistant: {str(e)}"
        )


@router.get("/{assistant_id}/configure")
async def get_assistant_config(assistant_id: str, user_id: str = Depends(verify_token)):
    logger.info(f"Fetching config for assistant_id: {assistant_id}")
    assistant = await db.assistants.find_one(
        {"assistant_id": assistant_id, "user_id": user_id}
    )
    if not assistant:
        raise HTTPException(
            status_code=404, detail="Assistant not found or not authorized"
        )
    config = assistant.get(
        "config",
        {
            "system_prompt": "You are a helpful assistant for a website.",
            "tone": "casual",
            "language": "ru",
            "data_collection": {"email": True, "name": False},
        },
    )
    return {"config": config}


@router.post("/{assistant_id}/collect")
async def collect_user_data(
    assistant_id: str, request: UserDataRequest, user_id: str = Depends(verify_token)
):
    logger.info(f"Collecting user data for assistant_id: {assistant_id}")
    assistant = await db.assistants.find_one(
        {"assistant_id": assistant_id, "user_id": user_id}
    )
    if not assistant:
        raise HTTPException(
            status_code=404, detail="Assistant not found or not authorized"
        )

    try:
        user_data = {
            "assistant_id": assistant_id,
            "user_id": request.user_id,
            "name": request.name,
            "email": request.email,
            "preferences": request.preferences,
            "timestamp": datetime.utcnow(),
        }
        await db.user_data.insert_one(user_data)
        return {"message": "User data collected successfully"}
    except Exception as e:
        logger.error(f"Error collecting user data: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to collect user data: {str(e)}"
        )


@router.post("/{assistant_id}/content")
async def upload_content(
    assistant_id: str, request: ContentRequest, user_id: str = Depends(verify_token)
):
    logger.info(f"Uploading content for assistant_id: {assistant_id}")
    assistant = await db.assistants.find_one(
        {"assistant_id": assistant_id, "user_id": user_id}
    )
    if not assistant:
        raise HTTPException(
            status_code=404, detail="Assistant not found or not authorized"
        )

    try:
        content_data = {
            "assistant_id": assistant_id,
            "content_type": request.content_type,
            "data": request.data,
            "source": "json",
            "created_at": datetime.utcnow(),
        }
        await db.assistant_content.replace_one(
            {
                "assistant_id": assistant_id,
                "content_type": request.content_type,
                "source": "json",
            },
            content_data,
            upsert=True,
        )
        return {
            "message": f"Content '{request.content_type}' uploaded for assistant {assistant_id}"
        }
    except Exception as e:
        logger.error(f"Error uploading content: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to upload content: {str(e)}"
        )


@router.get("/{assistant_id}/content")
async def get_content(
    assistant_id: str,
    content_type: Optional[str] = None,
    user_id: str = Depends(verify_token),
):
    logger.info(f"Fetching content for assistant_id: {assistant_id}")
    assistant = await db.assistants.find_one(
        {"assistant_id": assistant_id, "user_id": user_id}
    )
    if not assistant:
        raise HTTPException(
            status_code=404, detail="Assistant not found or not authorized"
        )

    query = {"assistant_id": assistant_id}
    if content_type:
        query["content_type"] = content_type

    contents = await db.assistant_content.find(query).to_list(length=100)
    for content in contents:
        content.pop("_id", None)
    return {"contents": contents}


@router.websocket("/{assistant_id}/ws")
async def chat_with_assistant(websocket: WebSocket, assistant_id: str):
    await websocket.accept()
    try:
        # First message must contain token
        data = await websocket.receive_json()
        token = data.get("token")
        if not token:
            await websocket.send_json({"error": "Token is required"})
            await websocket.close()
            return

        user_id = verify_token(token)
        assistant = await db.assistants.find_one(
            {"assistant_id": assistant_id, "user_id": user_id}
        )
        if not assistant:
            await websocket.send_json(
                {"error": "Assistant not found or not authorized"}
            )
            await websocket.close()
            return

        thread = client.beta.threads.create()
        thread_id = thread.id

        # Add system prompt and content
        config = assistant.get(
            "config",
            {
                "system_prompt": "You are a helpful assistant for a website.",
                "tone": "casual",
                "language": "ru",
            },
        )
        system_prompt = config.get("system_prompt")

        # Fetch content (JSON, file-based, crawled)
        contents = await db.assistant_content.find(
            {"assistant_id": assistant_id}
        ).to_list(length=10)
        content_context = []
        for content in contents:
            content_type = content.get("content_type")
            data = content.get("data", [])
            source = content.get("source", "unknown")
            file_id = content.get("file_id")
            url = content.get("url")
            content_str = f"Content type: {content_type}\nSource: {source}\nData: {json.dumps(data, ensure_ascii=False)}"
            if file_id:
                content_str += f"\nFile ID: {file_id}"
            if url:
                content_str += f"\nURL: {url}"
            content_context.append(content_str)

        # Fetch file metadata
        files = await db.assistant_files.find({"assistant_id": assistant_id}).to_list(
            length=10
        )
        file_context = [
            f"File: {f['filename']} (ID: {f['file_id']}, Type: {f['content_type']})"
            for f in files
        ]

        # Fetch crawl history
        crawls = await db.crawler_history.find({"assistant_id": assistant_id}).to_list(
            length=10
        )
        crawl_context = [
            f"Crawled URL: {c['url']} (Type: {c['content_type']})" for c in crawls
        ]

        content_message = (
            "\n\n".join(content_context)
            if content_context
            else "No specific content available."
        )
        file_message = (
            "\n\n".join(file_context) if file_context else "No files available."
        )
        crawl_message = (
            "\n\n".join(crawl_context)
            if crawl_context
            else "No crawled URLs available."
        )
        full_prompt = f"{system_prompt}\n\nAvailable content:\n{content_message}\n\nAvailable files:\n{file_message}\n\nCrawled URLs:\n{crawl_message}"

        client.beta.threads.messages.create(
            thread_id=thread_id, role="system", content=full_prompt
        )

        await websocket.send_json({"status": "connected", "thread_id": thread_id})

        while True:
            data = await websocket.receive_json()
            message = data.get("message")
            if not message:
                await websocket.send_json({"error": "Message is required"})
                continue

            try:
                client.beta.threads.messages.create(
                    thread_id=thread_id, role="user", content=message
                )

                run = client.beta.threads.runs.create(
                    thread_id=thread_id, assistant_id=assistant_id
                )
                await websocket.send_json({"status": "queued"})

                while run.status in ["queued", "in_progress"]:
                    run = client.beta.threads.runs.retrieve(
                        thread_id=thread_id, run_id=run.id
                    )
                    await websocket.send_json({"status": run.status})

                if run.status != "completed":
                    await websocket.send_json(
                        {"error": f"Run failed with status: {run.status}"}
                    )
                    continue

                messages = client.beta.threads.messages.list(thread_id=thread_id)
                assistant_response = next(
                    (
                        msg.content[0].text.value
                        for msg in messages.data
                        if msg.role == "assistant"
                    ),
                    "No response from assistant",
                )

                conversation = {
                    "thread_id": thread_id,
                    "assistant_id": assistant_id,
                    "user_id": user_id,
                    "messages": [
                        {
                            "role": "user",
                            "content": message,
                            "timestamp": datetime.utcnow(),
                        },
                        {
                            "role": "assistant",
                            "content": assistant_response,
                            "timestamp": datetime.utcnow(),
                        },
                    ],
                    "created_at": datetime.utcnow(),
                }
                await db.conversations.insert_one(conversation)

                await websocket.send_json({"response": assistant_response})
            except AuthenticationError:
                await websocket.send_json({"error": "Invalid OpenAI API key"})
                await websocket.close()
                break
            except Exception as e:
                await websocket.send_json({"error": f"Chat failed: {str(e)}"})
                continue

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
        await websocket.close()
    except Exception as e:
        logger.error(f"Connection failed: {str(e)}")
        await websocket.send_json({"error": f"Connection failed: {str(e)}"})
        await websocket.close()
