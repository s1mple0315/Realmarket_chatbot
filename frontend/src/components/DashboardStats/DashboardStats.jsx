import { useState, useEffect } from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import StatsContainer from "../StatsContainer/StatsContainer";
import styles from "./DashboardStats.module.css";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const DashboardStats = ({ activeTab }) => {
  const [statsData, setStatsData] = useState({
    dialogs: { labels: [], dialogs: [], messages: [] },
    widgetViews: { labels: [], views: [] },
    calls: { labels: [], calls: [] },
    conversion: { labels: [], conversion: [] },
    newDialogs: [],
  });

  useEffect(() => {
    const mockData = {
      today: {
        dialogs: {
          labels: [
            "14.04",
            "16.04",
            "17.04",
            "18.04",
            "19.04",
            "20.04",
            "21.04",
          ],
          dialogs: [35, 20, 5, 10, 5, 5, 5],
          messages: [40, 25, 15, 20, 15, 10, 10],
        },
        widgetViews: {
          labels: [
            "14.04",
            "16.04",
            "17.04",
            "18.04",
            "19.04",
            "20.04",
            "21.04",
          ],
          views: [40, 20, 5, 30, 5, 5, 5],
        },
        calls: {
          labels: [
            "14.04",
            "16.04",
            "17.04",
            "18.04",
            "19.04",
            "20.04",
            "21.04",
          ],
          calls: [35, 15, 5, 25, 5, 5, 5],
        },
        conversion: {
          labels: [
            "14.04",
            "16.04",
            "17.04",
            "18.04",
            "19.04",
            "20.04",
            "21.04",
          ],
          conversion: [30, 10, 5, 20, 5, 5, 5],
        },
        newDialogs: [
          {
            id: 1,
            user: "User-73",
            message: "Как мне зайти в личный кабинет если я забыл п...",
            time: "18:02",
            status: "done",
          },
          {
            id: 2,
            user: "User-71",
            message: "Спасибо за ваш запрос я передал ваши контакты...",
            time: "18:02",
            status: "done",
          },
          {
            id: 3,
            user: "User-25",
            message: "Кастомный доступ только для пользователя с 80 lvl",
            time: "17:42",
            status: "pending",
          },
        ],
      },
      week: {
        dialogs: {
          labels: ["Week 1", "Week 2", "Week 3", "Week 4"],
          dialogs: [50, 40, 30, 20],
          messages: [60, 50, 40, 30],
        },
        widgetViews: {
          labels: ["Week 1", "Week 2", "Week 3", "Week 4"],
          views: [60, 50, 40, 30],
        },
        calls: {
          labels: ["Week 1", "Week 2", "Week 3", "Week 4"],
          calls: [30, 20, 15, 10],
        },
        conversion: {
          labels: ["Week 1", "Week 2", "Week 3", "Week 4"],
          conversion: [25, 35, 15, 10],
        },
        newDialogs: [
          {
            id: 4,
            user: "User-10",
            message: "Разработка сайта...",
            time: "13:04",
            status: "done",
          },
          {
            id: 5,
            user: "User-15",
            message: "Продвижение в соцсетях...",
            time: "14:04",
            status: "pending",
          },
        ],
      },
      month: {
        dialogs: {
          labels: ["Jan", "Feb", "Mar", "Apr"],
          dialogs: [100, 80, 60, 40],
          messages: [120, 100, 80, 60],
        },
        widgetViews: {
          labels: ["Jan", "Feb", "Mar", "Apr"],
          views: [120, 100, 80, 60],
        },
        calls: {
          labels: ["Jan", "Feb", "Mar", "Apr"],
          calls: [50, 40, 30, 20],
        },
        conversion: {
          labels: ["Jan", "Feb", "Mar", "Apr"],
          conversion: [30, 40, 20, 10],
        },
        newDialogs: [
          {
            id: 6,
            user: "User-20",
            message: "Настройка директ...",
            time: "17:42",
            status: "pending",
          },
        ],
      },
    };

    setStatsData(mockData[activeTab]);
  }, [activeTab]);

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "bottom",
        align: "start",
        labels: {
          boxWidth: 16,
          boxHeight: 16,
          useBorderRadius: true,
          borderRadius: 4,
          font: {
            family: "var(--montserrat-font)",
            size: 14,
          },
        },
      },
    },
    scales: {
      x: {
        grid: {
          display: false,
        },
        ticks: {
          font: {
            family: "var(--montserrat-font)",
            size: 12,
          },
          color: "#707991",
        },
      },
      y: {
        beginAtZero: true,
        max: 40,
        ticks: {
          stepSize: 10,
          font: {
            family: "var(--montserrat-font)",
            size: 12,
          },
          color: "#707991",
        },
        grid: {
          color: "rgba(112, 121, 145, 0.2)",
        },
      },
    },
  };

  return (
    <div className={styles.statsGrid}>
      <StatsContainer
        title="Количество диалогов и сообщений"
        className={styles.largeChart}
      >
        <Bar
          data={{
            labels: statsData.dialogs.labels,
            datasets: [
              {
                label: "Диалоги",
                data: statsData.dialogs.dialogs,
                backgroundColor: "#6945ed",
                borderRadius: 15,
              },
              {
                label: "Сообщения",
                data: statsData.dialogs.messages,
                backgroundColor: "#75B4FC",
                borderRadius: 15,
              },
            ],
          }}
          options={chartOptions}
        />
      </StatsContainer>

      <StatsContainer title="Просмотры виджета">
        <Bar
          data={{
            labels: statsData.widgetViews.labels,
            datasets: [
              {
                label: "Просмотры виджета за сутки",
                data: statsData.widgetViews.views,
                backgroundColor: "#6945ed",
                borderRadius: 15,
              },
            ],
          }}
          options={chartOptions}
        />
      </StatsContainer>

      <StatsContainer title="Новые диалоги">
        <ul className={styles.dialogList}>
          {statsData.newDialogs.map((dialog) => (
            <li key={dialog.id} className={styles.dialogItem}>
              <span className={styles.user}>{dialog.user}</span>
              <span className={styles.message}>{dialog.message}</span>
              <span className={styles.time}>{dialog.time}</span>
              <span className={styles.status}>
                {dialog.status === "done" ? (
                  <svg
                    width="16"
                    height="16"
                    viewBox="0 0 16 16"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M3 8L6 11L13 4"
                      stroke="#00c853"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                ) : (
                  "⏳"
                )}
              </span>
            </li>
          ))}
        </ul>
        <button className={styles.viewAllButton}>Смотреть все диалоги</button>
      </StatsContainer>

      {/* Second Row */}
      <StatsContainer title="Количество звонков">
        <Bar
          data={{
            labels: statsData.calls.labels,
            datasets: [
              {
                label: "Количество звонков за сутки",
                data: statsData.calls.calls,
                backgroundColor: "#6945ed",
                borderRadius: 15,
              },
            ],
          }}
          options={chartOptions}
        />
      </StatsContainer>

      <StatsContainer title="Конверсия в звонки">
        <Bar
          data={{
            labels: statsData.conversion.labels,
            datasets: [
              {
                label: "Конверсия в звонки за сутки",
                data: statsData.conversion.conversion,
                backgroundColor: "#6945ed",
                borderRadius: 15,
              },
            ],
          }}
          options={chartOptions}
        />
      </StatsContainer>

      <StatsContainer title="Новые звонки">
        <ul className={styles.dialogList}>
          {[
            {
              id: 1,
              user: "Разработка сайта",
              message: "Статус заявки: входящая",
              time: "13.04.25",
              status: "done",
            },
            {
              id: 2,
              user: "Продвижение в соцсетях",
              message: "Статус заявки: входящая",
              time: "14.04.25",
              status: "pending",
            },
            {
              id: 3,
              user: "Настройка директ",
              message: "Статус заявки: отправлено добро",
              time: "17:42",
              status: "pending",
            },
          ].map((call) => (
            <li key={call.id} className={styles.dialogItem}>
              <span className={styles.user}>{call.user}</span>
              <span className={styles.message}>{call.message}</span>
              <span className={styles.time}>{call.time}</span>
              <span className={styles.status}>
                {call.status === "done" ? (
                  <svg
                    width="16"
                    height="16"
                    viewBox="0 0 16 16"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M3 8L6 11L13 4"
                      stroke="#00c853"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                ) : (
                  "⏳"
                )}
              </span>
            </li>
          ))}
        </ul>
        <button className={styles.viewAllButton}>Смотреть все заявки</button>
      </StatsContainer>
    </div>
  );
};

export default DashboardStats;
