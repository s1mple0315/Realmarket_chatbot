import { useState } from "react";
import styles from "./Accordion.module.css";
import ChevronDownIcon from "../../icons/ChevronDownIcon";

const Accordion = ({ title, content }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleAccordion = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className={styles.accordion}>
      <div className={styles.header} onClick={toggleAccordion}>
        <h2 className={styles.accordionTitle}>{title}</h2>
        <ChevronDownIcon />
      </div>
      {isOpen && (
        <div className={styles.contentWrapper}>
          <p className={styles.accordionContent}>{content}</p>
        </div>
      )}
    </div>
  );
};

export default Accordion;
