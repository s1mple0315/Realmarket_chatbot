import Header from "../../components/Header/Header";
import Footer from "../../components/Footer/Footer";

import styles from "./HomePage.module.css";
import Chat from "../../icons/Chat";
import CRM from "../../icons/CRM";
import Branching from "../../icons/Branching";
import Testing from "../../icons/Testing";
import Rocket from "../../icons/Rocket";
import Brain from "../../icons/Brain";
import Chip from "../../icons/Chip";
import Accordion from "../../components/Accordion/Accordion";

const HomePage = () => {
  return (
    <div>
      <Header />
      <section className={styles.homePageTitle}>
        <div className={styles.homePageTitleText}>
          <h1>ИИ⁠-⁠сотрудник</h1>
          <h3>для вашего бизнеса</h3>
        </div>
        <div className={styles.homePageTitleStats}>
          <p className={styles.homePageTitleStatsText}>
            Ловит потенциальных клиентов в воронку прогрева, квалифицирует
            входящие заявки
          </p>
          <p className={styles.homePageTitleStatsText}>
            и доводит до покупки без менеджеров в чате
          </p>
          <div className={styles.homePageTitleStatsItems}>
            <div className={styles.homePageTitleStatsItem}>
              <h3>80%</h3>
              <p>Экономия на зарплате сотрудникам</p>
            </div>
            <div className={styles.homePageTitleStatsItem}>
              <h3>+30%</h3>
              <p>К конверсии и выручке вашей компании</p>
            </div>
            <div className={styles.homePageTitleStatsItem}>
              <h3>{">"}20</h3>
              <p>Часов в неделю экономит вам ИИ-сотрудник</p>
            </div>
          </div>
        </div>
        <div className={styles.homePageTitleButton}>
          <button>Попробовать бесплатно</button>
        </div>
        <img
          className={styles.homePageTitleBack}
          src="/assets/images/Background/custom_back.svg"
          alt=""
        />
      </section>

      <section className={styles.homePageInfo}>
        <div className={styles.homePageInfoText}>
          <h1>
            Наймите <span>ИИ-сотрудника</span>
          </h1>
        </div>
        <p className={styles.homePageInfoItemsText}>
          который выучит весь ваш ассортимент, будет на связи с клиентом 24/7 и
          профессионально продавать ваш продукт
        </p>
        <div className={styles.homePageInfoItems}>
          <div className={styles.homePageInfoItem}>
            <h3>Консультация</h3>
            <div className={styles.homePageInfoItemText}>
              <p>за 5 минут создадим ИИ⁠-⁠ассистента под ваши задачи</p>
              <p>настроим его в соответствии с вашими целями и вкусами</p>
              <p>покажем весь функционал и научим им пользоваться</p>
            </div>
          </div>
          <div className={styles.homePageInfoItem}>
            <h3>Тестирование</h3>
            <div className={styles.homePageInfoItemText}>
              <p>за 5 минут создадим ИИ⁠-⁠ассистента под ваши задачи</p>
              <p>настроим его в соответствии с вашими целями и вкусами</p>
              <p>покажем весь функционал и научим им пользоваться</p>
            </div>
          </div>
          <div className={styles.homePageInfoItem}>
            <h3>Включайте в работу</h3>
            <div className={styles.homePageInfoItemText}>
              <p>за 5 минут создадим ИИ⁠-⁠ассистента под ваши задачи</p>
              <p>настроим его в соответствии с вашими целями и вкусами</p>
              <p>покажем весь функционал и научим им пользоваться</p>
            </div>
          </div>
        </div>
        <div className={styles.homePageInfoReturn}>
          <p>Вернем 100% средств, если вам что-то не понравится</p>
        </div>
      </section>

      <section className={styles.homePageTime}>
        <div className={styles.homePageTimeText}>
          <h1>Сколько времени вы высвобождаете</h1>
          <h2>с ИИ-сотрудником в неделю?</h2>
          <p>
            Нстроив один раз ИИ-сотрудника вы высвобождаете себе, РОПу и HR от
            20 часов в неделю и более, которые можно потратить на развитие
            компании
          </p>
        </div>
        <div className={styles.homePageTimeItems}>
          <div>
            <h3>10 часов</h3>
            <p>На поиск и найм менеджеров и технических специалистов</p>
          </div>
          <div>
            <h3>2 часа</h3>
            <p>На собеседование и введение в должность каждого менеджера</p>
          </div>
          <div>
            <h3>5 часов</h3>
            <p>На обучении и регулярных планерках</p>
          </div>
          <div>
            <h3>3 часа</h3>
            <p>
              На контроле звонков, соблюдения скриптов, сбору обратной связи
            </p>
          </div>
        </div>
        <div className={styles.homePageTimeReturn}>
          <p>Нстроив один раз ИИ-сотрудника вы высвобождаете себе, РОПу и HR</p>
          <h3>
            от 20 часов <span>в неделю</span>
          </h3>
          <p>которые можно потратить на развитие компании</p>
        </div>
      </section>

      <section className={styles.homePageAdvantages}>
        <img
          className={styles.homePageAdvantagesBack}
          src="assets/images/Background/homepageAdvantages_back.svg"
          alt=""
        />
        <h1>
          ИИ-сотрудник продает <span>лучше человека</span>
        </h1>
        <div className={styles.homePageAdvantagesItems}>
          <div className={styles.homePageAdvantagesItem}>
            <h3>Человек</h3>
            <div className={styles.homePageAdvantagesItemText}>
              <p>не успевает отвечать в потоке клиентов</p>
              <p>отходит от скрипта и продает «по-своему»</p>
              <p>берет отпуска, больничные, выходные</p>
              <p>отвечает только в рабочее время</p>
              <p>
                зависит от своего состояния — не проявляет инициативу, срывается
                на клиентов
              </p>
            </div>
          </div>
          <div className={styles.homePageAdvantagesItem}>
            <h3>ИИ-сотрудник</h3>
            <div className={styles.homePageAdvantagesItemText}>
              <p>
                сам ловит пользователя в диалог и ведет одновременно более 50
                000 диалогов
              </p>
              <p>
                четко следует инструкциям и в продаже исходит из запроса клиента
              </p>
              <p>не болеет и не нуждается в отдыхе</p>
              <p>эффективен круглосуточно и даже на выходных</p>
              <p>
                отвечает за полсекунды — дружелюбно общается, самообучается
                на собственных диалогах
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className={styles.homePageFeatures}>
        <h1>
          Один в поле <span>эффективный воин</span>
        </h1>
        <p>Все для усиления и автоматизации продаж в одном сервисе</p>
        <div className={styles.homePageFeaturesItems}>
          <div>
            <Chat />
            <h3>Персональные ответы</h3>
            <p>
              Помощник считывает запрос клиента и продает с позиции его выгод,
              а не по общему скрипту
            </p>
          </div>
          <div>
            <Branching />
            <h3>Адаптивные сценарии</h3>
            <p>
              Скрипты ИИ⁠-⁠менеджера подстраиваются под социальный портрет, опыт
              и потребности клиента автоматически
            </p>
          </div>
          <div>
            <CRM />
            <h3>Интеграция с CRM</h3>
            <p>
              Отслеживает статус лида и подстраивает диалоги под этап в воронке
              продаж, на котором находится клиент
            </p>
          </div>
          <div>
            <Testing />
            <h3>A/B-тестирование</h3>
            <p>
              Самостоятельно тестирует разные сценарии и отбирает наиболее
              эффективные из них для работы
            </p>
          </div>
        </div>
        <div className={styles.homePageFeaturesDashboard}>
          <img
            src="assets/images/dashboard_screen.png"
            alt="Respresentation of the dashboard"
          />
          <div className={styles.homePageFeaturesDashboardText}>
            <h3>Удобный личный кабинет с аналитикой и настройками</h3>
            <p>
              Весь процесс интеграции ИИ⁠-⁠ассистента Solo в бизнес, включая
              настройки, занимает около 10 минут и сопровождается вашим
              персональным ассистентом, а все последующие изменения через
              кабинет на платформе вступают в силу уже через несколько секунд
              после отправки.
            </p>
          </div>
        </div>
        <div className={styles.homePageFeaturesItems}>
          <div>
            <Chat />
            <h3>Повышение вовлечённости</h3>
            <p>
              Сам прогревает клиента, предоставляя ему ценные материалы и
              специальные условия из вашей базы
            </p>
          </div>
          <div>
            <Chat />
            <h3>Круглосуточная поддержка</h3>
            <p>
              Работает 24/7, без перерывов и выходных. Будет вести клиента,
              отвечая за секунду даже ночью
            </p>
          </div>
          <div>
            <Chat />
            <h3>Передача диалога менеджеру</h3>
            <p>
              В ситуации вне базы данных ИИ⁠-⁠менеджера клиент передается живому
              менеджеру вместе с ревью и историей их общения
            </p>
          </div>
          <div>
            <Chat />
            <h3>Мгновенная реакция на запросы</h3>
            <p>
              Помощник обрабатывает запрос клиента за секунды и дает
              качественный ответ даже в периоды пиковых нагрузок
            </p>
          </div>
        </div>
      </section>

      <section className={styles.homePageHowItWorks}>
        <img
          className={styles.homePageHowItWorksBack}
          src="assets/images/Background/homepageHowItWorks_back.svg"
          alt=""
        />
        <div className={styles.homePageHowItWorksTitle}>
          <h1>
            Чем вам поможет <span>ИИ-сотрудник?</span>
          </h1>
          <p>
            который выучит весь ваш ассортимент, будет на связи с клиентом 24/7
            и профессионально продавать ваш продукт
          </p>
        </div>
        <div className={styles.homePageHowItWorksItems}>
          <div>
            <h3>
              Для отдела продаж <br /> <span>и привлечения</span>
            </h3>
            <p>
              Умный алгоритм ИИ⁠-⁠ассистента для бизнеса привлекает до 30%
              дополнительных лидов с сайта на том же трафике, квалифицирует их и
              прогревает в заявку, параллельно увеличивая конверсию лидформ на
              сайте компании.
            </p>
          </div>
          <div>
            <h3>
              Для отдела технической
              <br /> <span>поддержки</span>
            </h3>
            <p>
              AI⁠-⁠технологии позволяют консультировать текущих клиентов по
              техническим вопросам, а также решать до 85% стандартных
              технических проблем: возврат оплат, перенос записей и продуктов,
              повышение тарифа и другие.
            </p>
          </div>
          <div>
            <h3>
              Для малого <br />
              <span> бизнеса</span>
            </h3>
            <p>
              Нейросеть заменяет целый штат менеджеров продаж и технических
              специалистов, позволяя оптимизировать затраты. Одно готовое
              решение обеспечит вам стабильный поток заявок с сайта, продажи в
              социальных сетях и техническую поддержку внутри продукта.
            </p>
          </div>
        </div>
      </section>

      <section className={styles.homePageFaq}>
        <img
          className={styles.homePageFaqBack}
          src="assets/images/Background/homepageFaq_back.svg"
          alt=""
        />
        <div className={styles.homePageFaqItems}>
          <Accordion
            title={"Сколько стоит?"}
            content={
              "Код написан с учетом всех пунктов законодательства РФ, активно применяется в крупных компаниях больше года и поддерживается командой разработчиков, которые защищают его от взломов, утечки данных и других последствий кибератак. "
            }
          />
          <Accordion
            title={"Насколько это безопасно?"}
            content={
              "Код написан с учетом всех пунктов законодательства РФ, активно применяется в крупных компаниях больше года и поддерживается командой разработчиков, которые защищают его от взломов, утечки данных и других последствий кибератак. "
            }
          />
          <Accordion
            title={"Что можно настроить?"}
            content={
              "Код написан с учетом всех пунктов законодательства РФ, активно применяется в крупных компаниях больше года и поддерживается командой разработчиков, которые защищают его от взломов, утечки данных и других последствий кибератак. "
            }
          />
          <Accordion
            title={"Интегрируется ли Solo с моей CRM-системой?"}
            content={
              "Код написан с учетом всех пунктов законодательства РФ, активно применяется в крупных компаниях больше года и поддерживается командой разработчиков, которые защищают его от взломов, утечки данных и других последствий кибератак. "
            }
          />
          <Accordion
            title={"Подходит ли Solo для моего бизнеса?"}
            content={
              "Код написан с учетом всех пунктов законодательства РФ, активно применяется в крупных компаниях больше года и поддерживается командой разработчиков, которые защищают его от взломов, утечки данных и других последствий кибератак. "
            }
          />
        </div>
        <div className={styles.homePageFaqForm}>
          <div className={styles.homePageFaqFormTitle}>
            <h3>
              Протестируйте ИИ-сотрудника бесплатно
              <span>
                и начните получать на 30% больше конверсий уже сегодня
              </span>
            </h3>
            <p>
              95% наших клиентов отмечают рост статистики даже за 2 пробные
              недели
            </p>
          </div>
          <div className={styles.homePageFaqFormInputs}>
            <div className={styles.homePageFaqFormInputsTop}>
              <div>
                <input type="text" placeholder="Ваше имя" />
              </div>
              <div>
                <input type="text" placeholder="+7 (___) ___-__-__" />
              </div>
              <div>
                <input type="text" placeholder="Сайт или Инстаграм" />
              </div>
            </div>
            <div className={styles.homePageFaqFormInputsBottom}>
              <input type="text" placeholder="Комментарий" />
            </div>
            <button>Круто! Хочу получить пробный период</button>
          </div>
        </div>
      </section>

      <section>
        <div>
          <h1></h1>
        </div>
        <div>
          <div></div>
          <div></div>
          <div></div>
        </div>
      </section>

      <section className={styles.homePageAbilities}>
        <h1>
          Собственные <span>разработки</span>
        </h1>
        <div className={styles.homePageAbilitiesItems}>
          <div>
            <Rocket />
            <h3>
              Realbot <br /> <span>leadbooster™</span>
            </h3>
            <p>
              Помощник считывает запрос клиента и продает с позиции его выгод,
              а не по общему скрипту
            </p>
          </div>
          <div>
            <Testing />
            <h3>
              Realbot <br /> <span>intelligence™</span>
            </h3>
            <p>
              Помощник считывает запрос клиента и продает с позиции его выгод,
              а не по общему скрипту
            </p>
          </div>
          <div>
            <Chat />
            <h3>
              Realbot <br /> <span>perfomance™</span>
            </h3>
            <p>
              Помощник считывает запрос клиента и продает с позиции его выгод,
              а не по общему скрипту
            </p>
          </div>
          <div>
            <Brain />
            <h3>
              Realbot <br /> <span>education™</span>
            </h3>
            <p>
              Помощник считывает запрос клиента и продает с позиции его выгод,
              а не по общему скрипту
            </p>
          </div>
          <div>
            <Chip />
            <h3>
              Realbot <br /> <span>navitechnology™</span>
            </h3>
            <p>
              Помощник считывает запрос клиента и продает с позиции его выгод,
              а не по общему скрипту
            </p>
          </div>
        </div>
      </section>
      <Footer />
    </div>
  );
};

export default HomePage;
