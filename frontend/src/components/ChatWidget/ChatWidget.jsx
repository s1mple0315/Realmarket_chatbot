import React, { useState, useEffect, useRef } from "react";
import BackButton from "../../icons/Widget/BackButton";
import ChatBotIndicator from "../../icons/Widget/ChatBotIndicator";
import QuestionMark from "../../icons/Widget/QuestionMark";
import SendQuestion from "../../icons/Widget/SendQuestion";
import Services from "../../icons/Widget/Services";
import WidgetLogo from "../../icons/Widget/WidgetLogo";
import styles from "./ChatWidget.module.css";

const ChatWidget = () => {
  const [token, setToken] = useState(null);
  const [assistants, setAssistants] = useState([]);
  const [selectedAssistantId, setSelectedAssistantId] = useState("");
  const [messages, setMessages] = useState([]);
  const [messageInput, setMessageInput] = useState("");
  const [isOpen, setIsOpen] = useState(false);
  const ws = useRef(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    const config = window.chatbotConfig || {};
    const apiKey = config.apiKey;

    if (!apiKey) {
      setMessages([
        {
          sender: "System",
          content:
            "Error: API key is required. Please provide it in window.chatbotConfig.apiKey.",
        },
      ]);
      return;
    }

    setToken(apiKey);
  }, []);

  useEffect(() => {
    if (!token) return;

    const fetchAssistants = async () => {
      try {
        const response = await fetch(
          "http://localhost:8000/api/v1/assistants/",
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        const data = await response.json();
        if (data.assistants) {
          setAssistants(data.assistants);
        } else {
          setMessages((prev) => [
            ...prev,
            { sender: "System", content: "Error: Unable to fetch assistants." },
          ]);
        }
      } catch (error) {
        setMessages((prev) => [
          ...prev,
          {
            sender: "System",
            content: "Error fetching assistants: " + error.message,
          },
        ]);
      }
    };

    fetchAssistants();
  }, [token]);

  useEffect(() => {
    if (!selectedAssistantId || !token) return;

    ws.current = new WebSocket(
      `ws://localhost:8000/api/v1/assistants/${selectedAssistantId}/ws?token=${token}`
    );

    ws.current.onopen = () => {
      setMessages((prev) => [
        ...prev,
        { sender: "System", content: "Connected to assistant!" },
      ]);
    };

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.error) {
        setMessages((prev) => [
          ...prev,
          { sender: "System", content: "Error: " + data.error },
        ]);
      } else if (data.status) {
        setMessages((prev) => [
          ...prev,
          { sender: "System", content: "Status: " + data.status },
        ]);
      } else if (data.response) {
        setMessages((prev) => [
          ...prev,
          { sender: "Assistant", content: data.response },
        ]);
      }
    };

    ws.current.onclose = () => {
      setMessages((prev) => [
        ...prev,
        { sender: "System", content: "Disconnected from assistant." },
      ]);
      setSelectedAssistantId("");
    };

    ws.current.onerror = (error) => {
      setMessages((prev) => [
        ...prev,
        { sender: "System", content: "WebSocket error: " + error },
      ]);
    };

    return () => {
      if (ws.current) ws.current.close();
    };
  }, [selectedAssistantId, token]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = () => {
    if (
      !messageInput.trim() ||
      !ws.current ||
      ws.current.readyState !== WebSocket.OPEN
    ) {
      if (!messageInput.trim()) {
        setMessages((prev) => [
          ...prev,
          { sender: "System", content: "Please enter a message." },
        ]);
      } else {
        setMessages((prev) => [
          ...prev,
          {
            sender: "System",
            content: "Not connected to an assistant. Please select one.",
          },
        ]);
      }
      return;
    }

    setMessages((prev) => [...prev, { sender: "User", content: messageInput }]);
    ws.current.send(JSON.stringify({ message: messageInput }));
    setMessageInput("");
  };

  const toggleChatbot = () => {
    setIsOpen(!isOpen);
  };

  const handleQuestionClick = (question) => {
    setMessageInput(question);
    sendMessage();
  };

  return (
    <div className={styles.chatWidget}>
      <div className={styles.chatWidgetHeader}>
        <BackButton onClick={toggleChatbot} />
        <div className={styles.chatWidgetTitle}>
          <WidgetLogo />
          <div>
            <h3>ИИ-ассистент</h3>
            <p>Онлайн</p>
          </div>
        </div>
      </div>
      {isOpen && (
        <div className={styles.chatWidgetBody}>
          <div className={styles.chatWidgetBotMessage}>
            <ChatBotIndicator />
            <div className={styles.chatWidgetBotMessageContainer}>
              <p>
                Привет! Меня зовут Realbot, я ИИ ассистент студии разработки
                RealBrand. Чем могу вам помочь?
              </p>
            </div>

            <div className={styles.chatWidgetPreviewMessages}>
              <div className={styles.commonQuestions}>
                <div className={styles.commonQuestionsTitle}>
                  <QuestionMark />
                  <h3>Частые вопросы</h3>
                </div>
                <div className={styles.commonQuestionsList}>
                  <div
                    onClick={() =>
                      handleQuestionClick("Сколько стоят ваши услуги?")
                    }
                  >
                    <p>Сколько стоят ваши услуги?</p>
                  </div>
                  <div
                    onClick={() =>
                      handleQuestionClick("Что можно настроить с помощью бота?")
                    }
                  >
                    <p>Что можно настроить с помощью бота?</p>
                  </div>
                  <div
                    onClick={() =>
                      handleQuestionClick("Какие интеграции поддерживает бот?")
                    }
                  >
                    <p>Какие интеграции поддерживает бот?</p>
                  </div>
                </div>
              </div>
              <div className={styles.services}>
                <div className={styles.servicesTitle}>
                  <Services />
                  <h3>Услуги</h3>
                </div>
                <div className={styles.servicesList}>
                  <div>
                    <p>ИИ-сотрудник</p>
                  </div>
                  <div>
                    <p>ИИ-сотрудник</p>
                  </div>
                  <div>
                    <p>ИИ-сотрудник</p>
                  </div>
                  <div>
                    <p>ИИ-сотрудник</p>
                  </div>
                  <div>
                    <p>ИИ-сотрудник</p>
                  </div>
                  <div>
                    <p>ИИ-сотрудник</p>
                  </div>
                </div>
              </div>
            </div>

            <div className={styles.chatWidgetMessages}>
              {messages.map((msg, index) => (
                <div key={index} className={styles.chatWidgetMessage}>
                  <strong>{msg.sender}:</strong> {msg.content}
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>

            <div className={styles.chatWidgetInput}>
              <input
                placeholder="Задайте любой вопрос"
                type="text"
                value={messageInput}
                onChange={(e) => setMessageInput(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && sendMessage()}
              />
              <SendQuestion onClick={sendMessage} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatWidget;
