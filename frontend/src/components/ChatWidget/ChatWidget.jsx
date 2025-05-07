import BackButton from "../../icons/Widget/BackButton";
import ChatBotIndicator from "../../icons/Widget/ChatBotIndicator";
import QuestionMark from "../../icons/Widget/QuestionMark";
import SendQuestion from "../../icons/Widget/SendQuestion";
import Services from "../../icons/Widget/Services";
import WidgetLogo from "../../icons/Widget/WidgetLogo";
import styles from "./ChatWidget.module.css";

const ChatWidget = () => {
  return (
    <div className={styles.chatWidget}>
      <div className={styles.chatWidgetHeader}>
        <BackButton />
        <div className={styles.chatWidgetTitle}>
          <WidgetLogo />
          <div>
            <h3>ИИ-ассистент</h3>
            <p>Онлайн</p>
          </div>
        </div>
      </div>
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
                <div>
                  <p>Сколько стоят ваши услуги?</p>
                </div>
                <div>
                  <p>Что можно настроить с помощью бота?</p>
                </div>
                <div>
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

          <div className={styles.chatWidgetInput}>
            <input placeholder="Задайте любой вопрос" type="text" />
            <SendQuestion onClick={null} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatWidget;
