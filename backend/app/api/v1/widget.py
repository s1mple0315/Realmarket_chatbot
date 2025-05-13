from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordBearer
from app.database import db
import logging
from jose import JWTError, jwt
from app.services.auth_service import SECRET_KEY, ALGORITHM

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

BACKEND_WS_URL = "ws://localhost:8000/api/v1/assistants/assistants"

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
          <button id="close-chat-btn" aria-label="Toggle chatbot">
            <svg width="24" height="25" viewBox="0 0 24 25" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M9.57 6.43L3.5 12.5L9.57 18.57" stroke="#6945ED" stroke-width="1.5" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M20.5 12.5H3.67001" stroke="#6945ED" stroke-width="1.5" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <div class="chat-title">
            <svg width="48" height="49" viewBox="0 0 48 49" fill="none" xmlns="http://www.w3.org/2000/svg">
              <g clip-path="url(#clip0_102_3776)">
              <rect y="3.76923" width="44.2353" height="45.2308" rx="8" fill="#6945ED"/>
              <path d="M43.6263 1.43537C45.3124 1.43545 46.7063 2.79703 46.7063 4.52131V11.202C46.7063 12.8937 45.3203 14.2878 43.6263 14.2879H36.9661C35.2798 14.2879 33.886 12.9264 33.886 11.202V4.52131C33.8861 2.83735 35.2396 1.43537 36.9661 1.43537H43.6263Z" fill="#6945ED" stroke="white" stroke-width="2"/>
              </g>
              <defs>
              <clipPath id="clip0_102_3776">
              <rect width="48" height="49" fill="white"/>
              </clipPath>
              </defs>
            </svg>
            <div>
              <h3>ИИ-ассистент</h3>
              <p>Онлайн</p>
            </div>
          </div>
        </div>
        <div class="chat-body">
          <div class="bot-message">
            <div class="bot-message-avatar">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <g clip-path="url(#clip0_102_3766)">
                <rect x="0.5" y="1.65384" width="13.8235" height="13.8462" rx="3" fill="#6945ED"/>
                <path d="M14.1338 0.745605C14.7535 0.745697 15.2832 1.23879 15.2832 1.88428V3.9292C15.2832 4.56325 14.7574 5.06778 14.1338 5.06787H12.0527C11.4329 5.06787 10.9023 4.57475 10.9023 3.9292V1.88428C10.9023 1.25402 11.4174 0.745605 12.0527 0.745605H14.1338Z" fill="#6945ED" stroke="white"/>
                </g>
                <defs>
                <clipPath id="clip0_102_3766">
                <rect width="15" height="15" fill="white" transform="translate(0.5 0.5)"/>
                </clipPath>
                </defs>
              </svg>
            </div>
            <div class="bot-message-text"> <p>Привет! Меня зовут Realbot, я ИИ ассистент студии разработки RealBrand. Чем могу вам помочь?</p></div>
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
      @import url('https://fonts.googleapis.com/css2?family=Montserrat :ital@0;1&display=swap');
      @import url('https://fonts.googleapis.com/css2?family=Unbounded :wght@200..900&display=swap');
      #chat-widget {
        max-width: 375px;
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
        display: flex;
        justify-content: center;
        align-items: center;
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
        font-family: "Unbounded";
        color: #09c993;
        margin: 0;
        font-size: 15px;
      }
      .chat-body {
        padding: 15px;
      }
      .bot-message {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        gap: 10px;
      }
      .bot-message-avatar {
        width: 40px;
        border-radius: 6px;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 7.5px;
        background-color: #ffffff;
      }
      .bot-message-text {
        padding: 15px;
        display: flex;
        flex-direction: column;
        background: #ffffff;
        border-radius: 25px 25px 25px 0;
      }
      .bot-message-text p {
        margin: 0;
        font-size: 13px;
      }
      .common-questions {
        margin: 20px 0;
      }
      .common-questions h4 {
        font-size: 13px;
        margin: 0 0 10px;
        text-align: center;
      }
      .common-questions .question-btn {
        background: #ffffff;
        padding: 10px;
        border-radius: 30px;
        cursor: pointer;
        margin: 5px 0;
        text-align: center;
        font-family: 'Montserrat';
        font-weight: 500;
        font-size: 13px;
        line-height: 16px;
        color: #3E3E3E;
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
        justify-content: space-between;
        gap: 10px;
        background: #ffffff;
        padding: 10px;
        border-radius: 17px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.13);
      }
      .chat-input input {
        flex: 1;
        border: none;
        outline: none;
        font-size: 13px;
        font-family: 'Montserrat';
        font-style: normal;
        font-weight: 600;
        line-height: 16px;
        color: #6945ED !important;
      }
      .chat-input input::placeholder {
        color: #6945ED !important;
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
    window.toggleChat = function () {
      const widget = document.getElementById("chat-widget");
      if (widget) {
        widget.style.display = widget.style.display === "none" ? "block" : "none";
      } else {
        console.error("chat-widget element not found");
      }
    };
    window.sendMessage = function (message) {
      const input = document.getElementById("message-input");
      const text = message || input.value.trim();
      if (!text) {
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
      if (!assistantId || !token) {
        addMessage("System", "Error: Assistant ID or token missing.");
        console.error("Missing assistant ID or token");
        return;
      }
      const BACKEND_WS_URL = "ws://localhost:8000/api/v1/assistants/";
      ws = new WebSocket(`${BACKEND_WS_URL}${assistantId}/ws?token=${token}`);
      ws.onopen = () => {
        addMessage("System", "Connected to assistant!");
      };
      ws.onmessage = (event) => {
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
      };
      ws.onerror = (error) => {
        addMessage("System", "WebSocket error: " + error);
        console.error("WebSocket error:", error);
      };
    }
    function addMessage(sender, content) {
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
        window.toggleChat();
      });
    } else {
      console.error("chat-toggle button not found");
    }
    if (closeBtn) {
      closeBtn.addEventListener("click", () => {
        window.toggleChat();
      });
    } else {
      console.error("close-chat-btn not found");
    }
    if (sendBtn) {
      sendBtn.addEventListener("click", () => {
        window.sendMessage();
      });
    } else {
      console.error("send-message-btn not found");
    }
    if (messageInput) {
      messageInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
          window.sendMessage();
        }
      });
    } else {
      console.error("message-input not found");
    }
    questionButtons.forEach(button => {
      button.addEventListener("click", () => {
        const message = button.getAttribute("data-message");
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
