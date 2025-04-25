import ScriptIntegration from "../../../components/ScriptIntegration/ScriptIntegration";
import IntegrationsCopy from "../../../icons/IntegrationsCopy";
import styles from "./IntegrationPage.module.css";

const IntegrationPage = () => {
  return (
    <div className={styles.integrationPage}>
      <div className={styles.integrationPageTitle}>
        <h3>Интеграции</h3>
        <div
          className={`${styles.integrationPageTitleButton} d-flex align-items-center gap-2`}
        >
          <button>Сгенерировать код</button>
          <button>
            <IntegrationsCopy /> Скопировать код
          </button>
        </div>
      </div>
      <div className={styles.integrationPageContent}>
        <ScriptIntegration />
      </div>
      <div className={`${styles.integrationPageText} d-flex flex-column gap-3`}>
        <h3>Заголовок текстовой информации</h3>
        <p>
          Lorem Ipsum is simply dummy text of the printing and typesetting
          industry. Lorem Ipsum has been the industry's standard dummy text ever
          since the 1500s, when an unknown printer took a galley of type and
          scrambled it to make a type specimen book. It has survived not only
          five centuries, but also the leap into electronic typesetting,
          remaining essentially unchanged. It was popularised in the 1960s with
          the release of Letraset sheets containing Lorem Ipsum passages, and
          more recently with desktop publishing software like Aldus PageMaker
          including versions of Lorem Ipsum.
        </p>
      </div>
    </div>
  );
};

export default IntegrationPage;
