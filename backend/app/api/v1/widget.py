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
        <hr class="chat-divider">
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
            <button id="send-message-btn" aria-label="Send message"><svg width="34" height="34" viewBox="0 0 34 34" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect width="34" height="34" rx="8" fill="#6945ED"/>
              <path d="M24.0205 13.5087L15.4605 9.22867C9.71046 6.34867 7.35046 8.70867 10.2305 14.4587L11.1005 16.1987C11.3505 16.7087 11.3505 17.2987 11.1005 17.8087L10.2305 19.5387C7.35046 25.2887 9.70046 27.6487 15.4605 24.7687L24.0205 20.4887C27.8605 18.5687 27.8605 15.4287 24.0205 13.5087ZM20.7905 17.7487H15.3905C14.9805 17.7487 14.6405 17.4087 14.6405 16.9987C14.6405 16.5887 14.9805 16.2487 15.3905 16.2487H20.7905C21.2005 16.2487 21.5405 16.5887 21.5405 16.9987C21.5405 17.4087 21.2005 17.7487 20.7905 17.7487Z" fill="white"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
      <button id="chat-toggle" style="position: fixed; bottom: 20px; right: 20px; border: none; cursor: pointer;">
        <svg width="34" height="34" viewBox="0 0 34 34" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M10.75 12.3125H23.25" stroke="white" stroke-width="2.5" stroke-linecap="round"/>
          <path d="M10.75 17.7812H19.3438" stroke="white" stroke-width="2.5" stroke-linecap="round"/>
          <path d="M19.7064 32.2652L20.5534 30.8342L18.5364 29.6403L17.6894 31.0714L19.7064 32.2652ZM13.4465 30.8342L14.2936 32.2652L16.3105 31.0714L15.4634 29.6403L13.4465 30.8342ZM17.6894 31.0714C17.3883 31.5802 16.6117 31.5802 16.3105 31.0714L14.2936 32.2652C15.5023 34.3073 18.4977 34.3073 19.7064 32.2652L17.6894 31.0714ZM14.6562 2.54688H19.3438V0.203125H14.6562V2.54688ZM31.4531 14.6562V16.2188H33.7969V14.6562H31.4531ZM2.54688 16.2188V14.6562H0.203125V16.2188H2.54688ZM0.203125 16.2188C0.203125 18.0228 0.202485 19.4345 0.280172 20.5731C0.358594 21.7223 0.520672 22.6787 0.887016 23.5631L3.05236 22.6663C2.82402 22.115 2.68877 21.4434 2.6185 20.4136C2.54752 19.3733 2.54688 18.0548 2.54688 16.2188H0.203125ZM10.4414 26.7525C8.47978 26.7186 7.45192 26.5939 6.64623 26.2602L5.74933 28.4255C7.00709 28.9464 8.43966 29.062 10.401 29.0958L10.4414 26.7525ZM0.887016 23.5631C1.79888 25.7645 3.54791 27.5136 5.74933 28.4255L6.64623 26.2602C5.01909 25.5861 3.72634 24.2934 3.05236 22.6663L0.887016 23.5631ZM31.4531 16.2188C31.4531 18.0548 31.4525 19.3733 31.3816 20.4136C31.3113 21.4434 31.1759 22.115 30.9477 22.6663L33.113 23.5631C33.4794 22.6787 33.6414 21.7223 33.7198 20.5731C33.7975 19.4345 33.7969 18.0228 33.7969 16.2188H31.4531ZM23.5989 29.0958C25.5603 29.062 26.993 28.9464 28.2506 28.4255L27.3538 26.2602C26.5481 26.5939 25.5202 26.7186 23.5586 26.7525L23.5989 29.0958ZM30.9477 22.6663C30.2736 24.2934 28.9809 25.5861 27.3538 26.2602L28.2506 28.4255C30.452 27.5136 32.2011 25.7645 33.113 23.5631L30.9477 22.6663ZM19.3438 2.54688C21.9237 2.54688 23.7766 2.54811 25.2217 2.68552C26.6495 2.82127 27.558 3.08161 28.2822 3.52544L29.5069 1.52706C28.3523 0.819641 27.0428 0.50436 25.4436 0.352297C23.8617 0.201891 21.8784 0.203125 19.3438 0.203125V2.54688ZM33.7969 14.6562C33.7969 12.1216 33.7981 10.1383 33.6477 8.55642C33.4956 6.95713 33.1803 5.64758 32.473 4.49317L30.4745 5.71778C30.9184 6.44205 31.1788 7.35053 31.3145 8.77827C31.4519 10.2234 31.4531 12.0762 31.4531 14.6562H33.7969ZM28.2822 3.52544C29.1758 4.073 29.927 4.82425 30.4745 5.71778L32.473 4.49317C31.7322 3.28428 30.7158 2.26788 29.5069 1.52706L28.2822 3.52544ZM14.6562 0.203125C12.1216 0.203125 10.1383 0.201891 8.55642 0.352297C6.95713 0.50436 5.64758 0.819641 4.49317 1.52706L5.71778 3.52544C6.44205 3.08161 7.35053 2.82127 8.77827 2.68552C10.2234 2.54811 12.0762 2.54688 14.6562 2.54688V0.203125ZM2.54688 14.6562C2.54688 12.0762 2.54811 10.2234 2.68552 8.77827C2.82127 7.35053 3.08161 6.44205 3.52544 5.71778L1.52706 4.49317C0.819641 5.64758 0.50436 6.95713 0.352297 8.55642C0.201891 10.1383 0.203125 12.1216 0.203125 14.6562H2.54688ZM4.49317 1.52706C3.28428 2.26788 2.26788 3.28428 1.52706 4.49317L3.52544 5.71778C4.073 4.82425 4.82425 4.073 5.71778 3.52544L4.49317 1.52706ZM15.4634 29.6403C15.1462 29.1044 14.8678 28.6314 14.597 28.2598C14.3117 27.8686 13.9847 27.5163 13.531 27.2523L12.3527 29.2784C12.4268 29.3214 12.5277 29.4 12.7029 29.6403C12.8925 29.9006 13.1068 30.2602 13.4465 30.8342L15.4634 29.6403ZM10.401 29.0958C11.0871 29.1077 11.5217 29.1164 11.8529 29.153C12.1625 29.1873 12.2825 29.2375 12.3527 29.2784L13.531 27.2523C13.0736 26.9862 12.5976 26.8773 12.1109 26.8234C11.6459 26.772 11.084 26.7636 10.4414 26.7525L10.401 29.0958ZM20.5534 30.8342C20.8931 30.2602 21.1073 29.9006 21.297 29.6403C21.4722 29.4 21.5731 29.3214 21.6472 29.2784L20.4689 27.2523C20.0153 27.5163 19.6881 27.8686 19.403 28.2598C19.1322 28.6314 18.8537 29.1044 18.5364 29.6403L20.5534 30.8342ZM23.5586 26.7525C22.9159 26.7636 22.3541 26.772 21.8891 26.8234C21.4023 26.8773 20.9264 26.9862 20.4689 27.2523L21.6472 29.2784C21.7175 29.2375 21.8375 29.1873 22.147 29.153C22.4783 29.1164 22.9128 29.1077 23.5989 29.0958L23.5586 26.7525Z" fill="white"/>
        </svg>
        <p>
          Мгновенная
          консультация
        </p>
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
      #chat-widget::before {
        content: "";
        position: absolute;
        inset: 0;
        border-radius: 25px;
        padding: 2px;
        background: linear-gradient(
          232.68deg,
          rgba(105, 69, 237, 0.3), /* Lightened */
          rgba(199, 189, 255, 0.3) /* Lightened */
        );
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        z-index: -1;
      }
      .chat-header {
        display: flex;
        align-items: center;
        padding: 15px;
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
        display: flex;
        align-items: center; 
        font-family: "Unbounded";
        color: #09c993;
        margin: 0;
        font-size: 15px;
      }
      .chat-title p::before {
        content: "";
        display: inline-block; 
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: #09C993; 
        margin-right: 5px;
      }

      .chat-divider {
        height: 1px; 
        border: none;
        background: conic-gradient(
          from 180deg at 50% 50%,
          rgba(58, 173, 255, 0.3) 0deg, 
          rgba(69, 77, 237, 0.3) 83.08deg,
          rgba(105, 69, 237, 0.3) 167.88deg,
          rgba(160, 28, 186, 0.3) 275.19deg,
          rgba(58, 173, 255, 0.3) 360deg
        );
        margin: 0;
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
        # width: 40px;
        border-radius: 6px;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 7.5px;
        background-color: #ffffff;
      }
      .bot-message-text {
        flex: 1;
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
      .user-message {
        display: flex;
        flex-direction: row;
        align-items: flex-end;
        padding: 0px;
        gap: 9px;
      }
      .user-message-text {
        display: flex;
        flex-direction: row;
        # align-items: flex-end;
        padding: 18px 20px;
        gap: 10px;
        background: #6945ED;
        border-radius: 25px 25px 0px 25px;
        flex: 1;
      }
      .user-message-text p {
        font-family: 'Montserrat';
        font-style: normal;
        font-weight: 400;
        font-size: 13px;
        line-height: 18px;
        color: #FFFFFF;
      }
      .user-message-avatar {
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        padding: 0px;
        gap: 4.91px;
        width: 30px;
        height: 30px;
        background: #6945ED;
        box-shadow: 0px 1.96226px 1.96226px rgba(0, 0, 0, 0.05);
        border-radius: 6px;
      }      
      .common-questions {
        margin: 20px 0;
      }
      .common-questions h4 {
        font-family: 'Unbounded';
        font-style: normal;
        font-weight: 500;
        font-size: 13px;
        line-height: 16px;
        color: #3F3F3F;
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
      #chat-toggle {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #6945ED;
        border-radius: 15px;
        padding: 16px;
        gap: 8px;
      }
      
      #chat-toggle > p{
        width: 104px;
        font-family: 'Unbounded';
        font-size: 15px;
        line-height: 19px;
        color: #FFFFFF;
        text-align: left;
        margin: 0;
      }
    `;
    document.head.appendChild(style);
    // Client-side JavaScript
    let ws = null;
    window.toggleChat = function () {
      const widget = document.getElementById("chat-widget");
      const toggleBtn = document.getElementById("chat-toggle");
      if (widget && toggleBtn) {
        const isVisible = widget.style.display !== "none";
        widget.style.display = isVisible ? "none" : "block";
        toggleBtn.style.display = isVisible ? "flex" : "none"; // Hide toggle when widget is open
      } else {
        console.error("chat-widget or chat-toggle element not found");
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
      console.log("Adding message:", sender, content);
      const messages = document.getElementById("chat-messages");
      if (!messages) {
        console.error("chat-messages element not found");
        return;
      }
      const msgDiv = document.createElement("div");
      if (sender === "Assistant") {
        msgDiv.className = "bot-message";
        msgDiv.innerHTML = `
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
          <div class="bot-message-text">
            <p>${content}</p>
          </div>
        `;
      } else if (sender === "User") {
        msgDiv.className = "user-message";
        msgDiv.innerHTML = `
          <div class="user-message-text">
            <p>${content}</p>
          </div>
          <div class="user-message-avatar">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M5.33334 4.00001C5.33334 4.70725 5.61429 5.38553 6.11439 5.88563C6.61449 6.38573 7.29277 6.66668 8.00001 6.66668C8.70725 6.66668 9.38553 6.38573 9.88563 5.88563C10.3857 5.38553 10.6667 4.70725 10.6667 4.00001C10.6667 3.29277 10.3857 2.61449 9.88563 2.11439C9.38553 1.6143 8.70725 1.33334 8.00001 1.33334C7.29277 1.33334 6.61449 1.6143 6.11439 2.11439C5.61429 2.61449 5.33334 3.29277 5.33334 4.00001Z" fill="white"/>
              <path d="M13.3333 11.6667C13.3333 13.3235 13.3333 14.6667 7.99999 14.6667C2.66666 14.6667 2.66666 13.3235 2.66666 11.6667C2.66666 10.0098 5.05447 8.66666 7.99999 8.66666C10.9455 8.66666 13.3333 10.0098 13.3333 11.6667Z" fill="white"/>
            </svg>
          </div>            
        `;
      }
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
