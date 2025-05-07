import DropBox from "../../icons/DropBox";
import FooterDzen from "../../icons/FooterDzen";
import FooterInstagram from "../../icons/FooterInstagram";
import FooterLogo from "../../icons/FooterLogo";
import FooterMastercard from "../../icons/FooterMastercard";
import FooterMir from "../../icons/FooterMir";
import FooterMtc from "../../icons/FooterMtc";
import FooterTelegram from "../../icons/FooterTelegram";
import FooterVisa from "../../icons/FooterVisa";
import FooterVK from "../../icons/FooterVK";
import FooterWhatsupp from "../../icons/FooterWhatsupp";
import styles from "./Footer.module.css";

const Footer = () => {
  const services = [
    { count: "347", title: "UX/UI", subtitle: "Создание сайтов" },
    { count: "64", title: "Смо", subtitle: "Реальный маркетинг" },
    { count: "284", title: "Сра", subtitle: "Рекламные агентства" },
    { count: "147", title: "Kit", subtitle: "Разработка ИТ" },
    { count: "104", title: "App", subtitle: "Мобильное приложение" },
    { count: "82", title: "Ai", subtitle: "Бизнесе ИИ" },
    { count: "new", title: "Game", subtitle: "Игровой студии" },
    { count: "demb", title: "B2B", subtitle: "Обучение на Twitch" },
    { count: "78", title: "B2C", subtitle: "Компьютор доходы" },
    { count: "51", title: "Roi", subtitle: "Сколько маркетинга" },
    { count: "01001", title: "Abc", subtitle: "Маркетинга" },
    { count: "Gpt", title: "Gpt", subtitle: "Реальный" },
    { count: "3847", title: "Art", subtitle: "Искусство работы" },
    { count: "1", title: "Sale", subtitle: "Паске привет" },
    { count: "8 min", title: "Zoom", subtitle: "Обучения 3 года" },
    { count: "47", title: "Work", subtitle: "Работа дома" },
    { count: "2010", title: "Hi", subtitle: "История компании" },
  ];

  return (
    <footer className={`${styles.footer} d-flex flex-column`}>
      <img
        className={styles.footerBack1}
        src="assets/images/Background/footer_back1.svg"
        alt=""
      />
      <img
        className={styles.footerBack2}
        src="assets/images/Background/footer_back2.svg"
        alt=""
      />
      <div className={`${styles.footerTop} d-flex`}>
        <div className={`${styles.footerTopLogoContainer} d-flex flex-column`}>
          <div className={styles.footerTopLogo}>
            <FooterLogo />
          </div>
          <div className={`${styles.footerTopLogoInfo} d-flex flex-column`}>
            <div className={styles.socials}>
              <h3>8 (800) 302-02-84</h3>{" "}
              <div>
                <FooterTelegram /> <FooterWhatsupp />
              </div>
            </div>
            <div className={styles.email}>
              <a href="mailto:help@business-factory.site">
                Email: help@business-factory.site
              </a>
            </div>
          </div>
        </div>
        <div className={styles.footerTopServices}>
          {services.map((service, index) => (
            <div key={index} className={styles.footerTopService}>
              <span className={styles.count}>{service.count}</span>
              <button className={styles.arrowButton}>
                <svg
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M7 17L17 7M17 7H7M17 7V17"
                    stroke="white"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </button>
              <div className={styles.serviceText}>
                <h3 className={styles.serviceTitle}>{service.title}</h3>
                <p className={styles.serviceSubtitle}>{service.subtitle}</p>
              </div>
            </div>
          ))}
        </div>
        <div className={styles.footerTopForm}>
          <div className={styles.footerTopFormTitle}>
            <h3>Есть рабочие материалы для обсуждения?</h3>
          </div>
          <div className={styles.footerTopFormText}>
            <p>Присылайте файлы, изучим и свяжемся с Вами.</p>
            <span>
              *вся информация используется только для ознакомления с проектом
            </span>
          </div>
          <div className={styles.filePicker}>
            <DropBox /> <h3>Dropbox</h3>
          </div>
          <div className={styles.footerTopFormInput}>
            <input type="text" placeholder="+7 (___) ___-__-__" />
          </div>
          <div className={styles.footerTopFormButton}>
            <button>Отправить</button>
          </div>
        </div>
      </div>
      <div className={styles.footerBottom}>
        <div className={styles.footerBottomSocialIcons}>
          <FooterVK />
          <FooterDzen />
          <FooterInstagram />
        </div>
        <div className={styles.footerBottomText}>
          <p>ООО «БИЗНЕСФАБРИКА» © 2022</p>
          <p>Пользовательское соглашение</p>
          <p>Политика конфиденциальности.</p>
          <p>Оферта</p>
        </div>
        <div className={styles.footerBottomCardIcons}>
          <FooterVisa />
          <FooterMastercard />
          <FooterMir />
          <FooterMtc />
        </div>
      </div>
    </footer>
  );
};

export default Footer;
