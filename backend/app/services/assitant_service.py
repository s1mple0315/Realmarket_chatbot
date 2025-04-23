import time
from dotenv import load_dotenv
import openai
import os
from app.models.assistant import AssistantConfig
from app.models.assistant import AssistantMongoModel
from app.database import db
from app.config import redis_client

load_dotenv()


openai.api_key = os.getenv("OPENAI_API_KEY")



def create_assistant(
    client, name, description, instructions, tools=[], model="gpt-4o-mini"
):
    """Create and save a new assistant linked to a user"""
    try:
        assistant = client.beta.assistants.create(
            name=name,
            description=description,
            instructions=instructions,
            tools=tools,
            model=model,
        )
        return assistant
    except Exception as e:
        return f"Error occurred during assistant creation: {str(e)}"


def get_assistant(client, assistant_id):
    """Retrieve an already created assistant"""
    try:
        assistant = client.beta.assistants.retrieve(assistant_id)
        return assistant
    except Exception as e:
        return f"Error occurred during assistant retrieval: {str(e)}"


def start_new_chat(client):
    """Start a new chat (thread) with an assistant"""
    try:
        empty_thread = client.beta.threads.create()
        return empty_thread
    except Exception as e:
        return f"Error occurred during chat creation: {str(e)}"


def get_chat(client, thread_id):
    """Retrieve the chat thread's details by ID"""
    try:
        thread = client.beta.threads.retrieve(thread_id)
        return thread
    except Exception as e:
        return f"Error occurred during thread retrieval: {str(e)}"


def add_message(client, thread, content):
    """Add a message to an existing thread"""
    try:
        thread_message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=content,
        )
        return thread_message
    except Exception as e:
        return f"Error occurred while adding message: {str(e)}"


def get_messages_in_chat(client, thread):
    """Retrieve all messages in a specific chat thread"""
    try:
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        return messages
    except Exception as e:
        return f"Error occurred while retrieving messages: {str(e)}"


def run_chat(client, thread, assistant):
    """Run the assistant with the current thread and wait for completion."""
    try:
        cache_key = f"chat:{thread.id}:{assistant.id}"
        cached_response = redis_client.get(cache_key)
        if cached_response:
            return cached_response.decode("utf-8")

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id, run_id=run.id
            )
            if run_status.status in ["completed", "failed", "cancelled"]:
                break
            time.sleep(1)
        if run_status.status != "completed":
            return f"Run failed with status: {run_status.status}"

        messages = client.beta.threads.messages.list(thread_id=thread.id)
        for message in messages.data:
            if message.role == "assistant":
                response = message.content[0].text.value
                redis_client.setex(cache_key, 3600, response)
                return response
        return "No assistant response found"
    except Exception as e:
        return f"Error occurred while running chat: {str(e)}"
