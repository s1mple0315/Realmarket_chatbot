from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.services.auth_service import verify_token
from openai import OpenAI
import os

router = APIRouter()

# Initialize OpenAI client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise HTTPException(status_code=500, detail="OpenAI API key is not configured")

client = OpenAI(api_key=OPENAI_API_KEY)


@router.post("/files/upload")
async def upload_file(
    file: UploadFile = File(...),
    purpose: str = "assistants",
    user_id: str = Depends(verify_token),
):
    try:
        # Validate purpose
        if purpose not in ["assistants", "vision"]:
            raise HTTPException(
                status_code=400, detail="Purpose must be 'assistants' or 'vision'"
            )

        # Upload file to OpenAI
        file_content = await file.read()
        openai_file = client.files.create(
            file=(file.filename, file_content), purpose=purpose
        )

        return {"file_id": openai_file.id, "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")
