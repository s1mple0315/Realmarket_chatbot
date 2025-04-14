
from fastapi import APIRouter, HTTPException, Depends
import openai

from app.models.assistant import Assistant, AssistantConfig, AssistantMongoModel
from fastapi import Request

from app.services.assitant_service import add_message, create_assistant, get_assistant, run_chat, start_new_chat
from app.services.auth_service import verify_token

router = APIRouter()

@router.post("/", response_model=Assistant)
async def create_new_assistant(assistant_config: AssistantConfig, request: Request, user_id: str = Depends(verify_token)):
    user_id = request.state.user_id
    
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    assistant = create_assistant(
        client=openai,  
        name=assistant_config.name,
        description=assistant_config.description,
        instructions=assistant_config.instructions,
        tools=assistant_config.tools,
    )
    
    if isinstance(assistant, str): 
        raise HTTPException(status_code=500, detail=assistant)
    
    assistant_data = AssistantMongoModel(
        user_id=user_id,
        assistant_id=assistant.id,
        name=assistant_config.name,
        instructions=assistant_config.instructions,
        tone=assistant_config.tone,
        website_data=assistant_config.website_data,
    )
    assistant_data.save()
    
    return assistant_data

@router.post("/{assistant_id}/query", response_model=str)
async def query_assistant_route(assistant_id: str, user_query: str):
    assistant = get_assistant(client=openai, assistant_id=assistant_id)
    
    if isinstance(assistant, str):  
        raise HTTPException(status_code=404, detail=assistant)
    
    thread = start_new_chat(client=openai)
    
    if isinstance(thread, str): 
        raise HTTPException(status_code=500, detail=thread)
    
    message = add_message(client=openai, thread=thread, content=user_query)
    
    if isinstance(message, str):  
        raise HTTPException(status_code=500, detail=message)
    
    run = run_chat(client=openai, thread=thread, assistant=assistant)
    
    if isinstance(run, str):  
        raise HTTPException(status_code=500, detail=run)
    
    return {"response": run["choices"][0]["message"]["content"]}
