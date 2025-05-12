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

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize OpenAI client
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
    instructions: Optional[str] = (
        "You are a helpful assistant for an e-commerce chatbot."
    )
    model: Optional[str] = "gpt-4o-mini"
    tools: Optional[List[Tool]] = None
    tool_resources: Optional[Dict[str, Any]] = None


class UpdateAssistantRequest(BaseModel):
    name: Optional[str] = None
    instructions: Optional[str] = None


@router.post("/assistants/")
async def create_assistant(
    request: CreateAssistantRequest, user_id: str = Depends(verify_token)
):
    logger.info(f"Received request to create assistant: {request.dict()}")
    try:
        assistant_name = request.name or f"Assistant for {user_id}"
        tools = [tool.dict() for tool in request.tools] if request.tools else []
        if len(tools) > 128:
            raise HTTPException(status_code=400, detail="Maximum 128 tools allowed")

        # Prepare tool_resources conditionally
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
        else:
            tool_resources = None  # Exclude tool_resources if no valid file_ids

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
            "created_at": datetime.utcnow(),
        }
        await db.assistants.insert_one(assistant_data)

        # Add the assistant_id to the user's assistants array
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


@router.get("/assistants/")
async def list_assistants(user_id: str = Depends(verify_token)):
    assistants = await db.assistants.find({"user_id": user_id}).to_list(length=100)
    for assistant in assistants:
        assistant.pop("_id", None)
    return {"assistants": assistants}


@router.put("/assistants/{assistant_id}")
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


@router.delete("/assistants/{assistant_id}")
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

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize OpenAI client
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
    instructions: Optional[str] = (
        "You are a helpful assistant for an e-commerce chatbot."
    )
    model: Optional[str] = "gpt-4o-mini"
    tools: Optional[List[Tool]] = None
    tool_resources: Optional[Dict[str, Any]] = None


class UpdateAssistantRequest(BaseModel):
    name: Optional[str] = None
    instructions: Optional[str] = None


@router.post("/assistants/")
async def create_assistant(
    request: CreateAssistantRequest, user_id: str = Depends(verify_token)
):
    logger.info(f"Received request to create assistant: {request.dict()}")
    try:
        assistant_name = request.name or f"Assistant for {user_id}"
        tools = [tool.dict() for tool in request.tools] if request.tools else []
        if len(tools) > 128:
            raise HTTPException(status_code=400, detail="Maximum 128 tools allowed")

        # Prepare tool_resources conditionally
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
        else:
            tool_resources = None  # Exclude tool_resources if no valid file_ids

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
            "created_at": datetime.utcnow(),
        }
        await db.assistants.insert_one(assistant_data)

        # Add the assistant_id to the user's assistants array
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


@router.get("/assistants/")
async def list_assistants(user_id: str = Depends(verify_token)):
    assistants = await db.assistants.find({"user_id": user_id}).to_list(length=100)
    for assistant in assistants:
        assistant.pop("_id", None)
    return {"assistants": assistants}


@router.put("/assistants/{assistant_id}")
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


@router.delete("/assistants/{assistant_id}")
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


@router.websocket("/assistants/{assistant_id}/ws")
async def chat_with_assistant(websocket: WebSocket, assistant_id: str, token: str):

    await websocket.accept()
    try:
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
        await websocket.close()
    except Exception as e:
        await websocket.send_json({"error": f"Connection failed: {str(e)}"})
        await websocket.close()
