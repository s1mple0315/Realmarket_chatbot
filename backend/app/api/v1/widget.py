from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordBearer
from app.database import db
import logging
from jose import JWTError, jwt
from app.services.auth_service import SECRET_KEY, ALGORITHM

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# OAuth2 scheme for Bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Configuration (adjust for production)
BACKEND_WS_URL = "ws://localhost:8000/api/v1/assistants/assistant_id/ws"

# Widget JavaScript template
WIDGET_SCRIPT = """
(function () {
  // Ensure DOM is ready
  function initWidget() {
    console.log("Initializing chat widget");

    // Create widget container
    let widgetDiv = document.getElementById("chatbot-widget-root");
    if (!widgetDiv) {
      console.log("Creating chatbot-widget-root");
      widgetDiv = document.createElement("div");
      widgetDiv.id = "chatbot-widget-root";
      document.body.appendChild(widgetDiv);
    }

    // Inject widget HTML
    widgetDiv.innerHTML = `
      <div id="chat-widget" style="display: none;">
        <div class="chat-header">
          <button id="close-chat-btn" aria-label="Toggle chatbot">X</button>
          <div class="chat-title">
            <img src="/static/logo.png" alt="Logo" width="30" />
            <div>
              <h3>ИИ-ассистент</h3>
              <p>Онлайн</p>
            </div>
          </div>
        </div>
        <div class="chat-body">
          <div class="welcome-message">
            <img src="/static/bot-icon.png" alt="Bot" width="20" />
            <p>Привет! Меня зовут Realbot, я ИИ ассистент студии разработки RealBrand. Чем могу вам помочь?</p>
          </div>
          <div class="common-questions">
            <h4>Частые вопросы</h4>
            <div class="question-btn" data-message="Сколько стоят ваши услуги?">Сколько стоят ваши услуги?</div>
            <div class="question-btn" data-message="Что можно настроить с помощью бота?">Что можно настроить с помощью бота?</div>
            <div class="question-btn" data-message="Какие интеграции поддерживает бот?">Какие интеграции поддерживает бот?</div>
          </div>
          <div class="chat-messages" id="chat-messages"></div>
          <div class="chat-input">
            <input type="text" id="message-input" placeholder="Задайте любой вопрос" />
            <button id="send-message-btn" aria-label="Send message">➤</button>
          </div>
        </div>
      </div>
      <button id="chat-toggle" style="position: fixed; bottom: 20px; right: 20px; width: 60px; height: 60px; background: #6945ed; border-radius: 50%; border: none; cursor: pointer;">
        <img src="/static/logo.png" alt="Chat" width="30" />
      </button>
    `;

    // Inject CSS
    const style = document.createElement("style");
    style.textContent = `
      #chat-widget {
        min-width: 375px;
        background: linear-gradient(232.68deg, #ffffff 5.05%, #e9e5ff 107.06%);
        border-radius: 30px;
        position: fixed;
        bottom: 90px;
        right: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        z-index: 1000;
      }
      .chat-header {
        display: flex;
        align-items: center;
        padding: 15px;
        border-bottom: 1.5px solid #6945ed;
      }
      .chat-header button {
        background: none;
        border: none;
        cursor: pointer;
        font-size: 18px;
      }
      .chat-title {
        display: flex;
        align-items: center;
        gap: 15px;
      }
      .chat-title h3 {
        color: #6945ed;
        margin: 0;
        font-size: 18px;
      }
      .chat-title p {
        color: #09c993;
        margin: 0;
        font-size: 15px;
      }
      .chat-body {
        padding: 15px;
      }
      .welcome-message {
        display: flex;
        gap: 10px;
        background: #ffffff;
        padding: 15px;
        border-radius: 25px 25px 25px 0;
      }
      .welcome-message p {
        margin: 0;
        font-size: 13px;
      }
      .common-questions {
        margin: 20px 0;
      }
      .common-questions h4 {
        font-size: 13px;
        margin: 0 0 10px;
      }
      .common-questions .question-btn {
        background: #ffffff;
        padding: 10px;
        border-radius: 30px;
        cursor: pointer;
        margin: 5px 0;
        text-align: center;
      }
      .chat-messages {
        max-height: 200px;
        overflow-y: auto;
        margin-bottom: 10px;
      }
      .chat-messages div {
        margin: 5px 0;
      }
      .chat-input {
        display: flex;
        gap: 10px;
        background: #ffffff;
        padding: 10px;
        border-radius: 17px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.13);
      }
      .chat-input input {
        border: none;
        outline: none;
        flex: 1;
        font-size: 13px;
      }
      .chat-input button {
        background: none;
        border: none;
        cursor: pointer;
      }
    `;
    document.head.appendChild(style);

    // Client-side JavaScript
    let ws = null;
    const token = window.chatWidgetToken || "${__TOKEN__}";
    const selectedAssistantId = "${__SELECTED_BOT_ID__}";

    window.toggleChat = function () {
      console.log("toggleChat called");
      const widget = document.getElementById("chat-widget");
      if (widget) {
        console.log("Current display:", widget.style.display);
        widget.style.display = widget.style.display === "none" ? "block" : "none";
        console.log("New display:", widget.style.display);
      } else {
        console.error("chat-widget element not found");
      }
    };

    window.sendMessage = function (message) {
      console.log("sendMessage called with:", message);
      const input = document.getElementById("message-input");
      const text = message || input.value.trim();
      if (!text) {
        console.log("No message to send");
        return;
      }
      if (!ws || ws.readyState !== WebSocket.OPEN) {
        addMessage("System", "Not connected to assistant. Please try again.");
        console.error("WebSocket not connected");
        return;
      }
      addMessage("User", text);
      ws.send(JSON.stringify({ message: text }));
      if (!message) input.value = "";
    };

    function connectWebSocket() {
      console.log("Connecting WebSocket");
      if (!selectedAssistantId || !token) {
        addMessage("System", "Error: Assistant ID or token missing.");
        console.error("Missing assistant ID or token");
        return;
      }
      ws = new WebSocket(`${BACKEND_WS_URL}${selectedAssistantId}/ws?token=${token}`);
      ws.onopen = () => {
        addMessage("System", "Connected to assistant!");
        console.log("WebSocket connected");
      };
      ws.onmessage = (event) => {
        console.log("WebSocket message received:", event.data);
        const data = JSON.parse(event.data);
        if (data.error) {
          addMessage("System", "Error: " + data.error);
        } else if (data.status) {
          addMessage("System", "Status: " + data.status);
        } else if (data.response) {
          addMessage("Assistant", data.response);
        }
      };
      ws.onclose = () => {
        addMessage("System", "Disconnected from assistant.");
        console.log("WebSocket disconnected");
      };
      ws.onerror = (error) => {
        addMessage("System", "WebSocket error: " + error);
        console.error("WebSocket error:", error);
      };
    }

    function addMessage(sender, content) {
      console.log("Adding message:", sender, content);
      const messages = document.getElementById("chat-messages");
      const msgDiv = document.createElement("div");
      msgDiv.innerHTML = `<strong>${sender}:</strong> ${content}`;
      messages.appendChild(msgDiv);
      messages.scrollTop = messages.scrollHeight;
    }

    // Set up event listeners
    const toggleBtn = document.getElementById("chat-toggle");
    const closeBtn = document.getElementById("close-chat-btn");
    const sendBtn = document.getElementById("send-message-btn");
    const messageInput = document.getElementById("message-input");
    const questionButtons = document.querySelectorAll(".question-btn");

    if (toggleBtn) {
      toggleBtn.addEventListener("click", () => {
        console.log("Toggle button clicked");
        window.toggleChat();
      });
    } else {
      console.error("chat-toggle button not found");
    }

    if (closeBtn) {
      closeBtn.addEventListener("click", () => {
        console.log("Close button clicked");
        window.toggleChat();
      });
    } else {
      console.error("close-chat-btn not found");
    }

    if (sendBtn) {
      sendBtn.addEventListener("click", () => {
        console.log("Send button clicked");
        window.sendMessage();
      });
    } else {
      console.error("send-message-btn not found");
    }

    if (messageInput) {
      messageInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
          console.log("Enter key pressed in input");
          window.sendMessage();
        }
      });
    } else {
      console.error("message-input not found");
    }

    questionButtons.forEach(button => {
      button.addEventListener("click", () => {
        const message = button.getAttribute("data-message");
        console.log("Question button clicked:", message);
        window.sendMessage(message);
      });
    });

    // Auto-connect to WebSocket
    connectWebSocket();
  }

  // Run initWidget when DOM is ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initWidget);
  } else {
    initWidget();
  }
})();
"""


async def validate_assistant(assistant_id: str, user_id: str):
    """
    Validate that the assistant_id exists and is accessible to the user.
    """
    logger.info(f"Validating assistant_id: {assistant_id} for user_id: {user_id}")

    assistant = await db.assistants.find_one({"assistant_id": assistant_id})
    if not assistant:
        logger.error(f"Assistant not found: {assistant_id}")
        raise HTTPException(status_code=400, detail="Invalid assistant ID")

    if assistant.get("user_id") != user_id:
        logger.error(f"User {user_id} not authorized for assistant {assistant_id}")
        raise HTTPException(status_code=403, detail="Unauthorized access to assistant")

    logger.info(f"Assistant found: {assistant}")
    return assistant


async def verify_token(token: str = Depends(oauth2_scheme)):
    """
    Verify JWT token from Authorization header.
    """
    logger.info(f"Verifying token: {token[:10]}...")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            logger.error("Token missing 'sub' field")
            raise HTTPException(
                status_code=401, detail="Token is invalid or missing user ID"
            )
        logger.info(f"Token validated for user_id: {user_id}")
        return user_id
    except JWTError as e:
        logger.error(f"JWTError: {str(e)}")
        raise HTTPException(
            status_code=401, detail=f"Token is invalid or expired: {str(e)}"
        )


@router.get("/widget.js", response_class=PlainTextResponse)
async def serve_widget(
    selectedbotid: str = Query(...), user_id: str = Depends(verify_token)
):
    logger.info(f"Serving widget for selectedbotid: {selectedbotid}")

    await validate_assistant(selectedbotid, user_id)

    script = WIDGET_SCRIPT.replace("__TOKEN__", "window.chatWidgetToken").replace(
        "__SELECTED_BOT_ID__", selectedbotid
    )
    return PlainTextResponse(script, media_type="application/javascript")
