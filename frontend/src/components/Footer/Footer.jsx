import FooterLogo from "../../icons/FooterLogo";
import FooterTelegram from "../../icons/FooterTelegram";
import FooterWhatsupp from "../../icons/FooterWhatsupp";
import styles from "./Footer.module.css";

const Footer = () => {
  return (
    <footer className={`${styles.footer} d-flex flex-column`}>
      <div className={`${styles.footerTop} d-flex`}>
        <div className={`${styles.footerTopLogoContainer} d-flex flex-column`}>
          <div className={styles.footerTopLogo}>
            <FooterLogo />
          </div>
          <div className={`${styles.footerTopLogoInfo} d-flex flex-column`}>
            <div className={styles.socials}>
              <h3>8 (800) 302-02-84</h3> <FooterTelegram /> <FooterWhatsupp />
            </div>
            <div className={styles.email}>
              <a href="mailto:help@business-factory.site">
                Email: help@business-factory.site
              </a>
            </div>
          </div>
        </div>
        <div className={styles.footerTopServices}>
          <div className={styles.footerTopService}></div>
        </div>
        <div></div>
      </div>
      <div className={styles.footerBottom}>
        <div></div>
        <div></div>
        <div></div>
      </div>
    </footer>
  );
};

export default Footer;
