import DashboardControls from "../../../components/DashboardControls/DashboardControls";
import ToggleSwitch from "../../../components/ToggleSwitch/ToggleSwitch";
import BotData from "../../../icons/BotData";
import QuestionMark from "../../../icons/QuestionMark";
import Plus from "../../../icons/Plus";

import styles from "./MyRealbotPage.module.css";
import DropdownButton from "../../../components/DropdownButton/DropdownButton";

const MyRealbotPage = () => {
  return (
    <div className={styles.myRealbotPage}>
      <div className={`${styles.myRealbotPageTitle} d-flex flex-column`}>
        <h3>Мой RealBot</h3>
        <DashboardControls />
      </div>
      <div className={`${styles.myRealbotPageContent} d-flex`}>
        <div className={styles.knowledgeBase}>
          <div className={`${styles.knowledgeBaseTitle} d-flex flex-column`}>
            <h3>База знаний RealBot</h3>
            <p>Вся информация, на основе которой ИИ создаёт ответы</p>
          </div>
          <div className={styles.knowledgeBaseInputfield}>
            <textarea
              name="knowledgeBase"
              id=""
              placeholder="Ваш текст"
            ></textarea>
          </div>
          <div className={styles.imagePicker}>
            <BotData /> <p>Прикрепить файл (.doc,.pdf,.word,.txt,.cvc,.xslx)</p>
          </div>
        </div>
        <div className={styles.suggestions}>
          <div className={`${styles.suggestionsTitle}`}>
            <h3>Подсказки </h3>
            <p>Пользователи будут видеть их при открытии чата</p>
          </div>
          <div
            className={`${styles.suggestionsToggle} d-flex align-items-center`}
          >
            <ToggleSwitch /> <h3>Динамические подсказки</h3> <QuestionMark />
          </div>
          <div className={`${styles.suggestionItems}`}>
            <div className={`${styles.suggestionItem}`}>
              <p>Разработка сайта</p>
            </div>
            <div className={`${styles.suggestionItem}`}>
              <p>Настройка директа</p>
            </div>
            <div className={`${styles.suggestionItem}`}>
              <p>Логотип и фирменный стиль</p>
            </div>
            <div className={`${styles.suggestionItem}`}>
              <p>Маркетинг</p>
            </div>
            <div className={`${styles.suggestionItem}`}>
              <p>Социальные сети</p>
            </div>
          </div>
          <div className={styles.addSuggestion}>
            <input
              type="text"
              name="addSuggestion"
              // value={suggestion}
              // onChange={handleAddValue}
              placeholder="Добавьте свое"
            />
            <Plus />
          </div>
        </div>
        <div className={`${styles.dataSelection} d-flex flex-column`}>
          <div className={`${styles.dataSelectionTitle} d-flex flex-column`}>
            <h3>Выбор данных</h3>
            <p>Данные, которые бот будет собирать у пользователя</p>
          </div>
          <div className={`${styles.dataSelectionItems}`}>
            <div className={styles.dataSelectionItem}>
              <p>Имя</p>
            </div>
            <div className={styles.dataSelectionItem}>
              <p>Номер телефона</p>
            </div>
            <div className={styles.dataSelectionItem}>
              <p>Имя и фамилия</p>
            </div>
            <div className={styles.dataSelectionItem}>
              <p>Адрес доставки</p>
            </div>
          </div>
          <div className={`${styles.dataSelectionAddItem}`}>
            <input type="text" name="addData" placeholder="Добавьте свое" />
            <Plus />
          </div>
        </div>
        <div className={`${styles.target} d-flex flex-column`}>
          <div className={styles.targetTitle}>
            <h3>Цель RealBot</h3>
            <p>Цель в которую нужно конвертировать пользователя</p>
          </div>
          <div className={styles.targetSelect}>
            <DropdownButton />
          </div>
        </div>
      </div>
      <div className={styles.saveButton}>
        <button>Применить изменения</button>
      </div>
    </div>
  );
};

export default MyRealbotPage;
