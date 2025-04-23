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
    views: { labels: [], views: [] },
    calls: { labels: [], calls: [] },
    conversion: { labels: [], conversion: [] },
    newDialogs: [],
  });

  useEffect(() => {
    const mockData = {
      today: {
        dialogs: {
          labels: ["14.04", "16.04", "18.04", "20.04"],
          dialogs: [30, 20, 15, 10],
          messages: [35, 25, 20, 15],
        },
        views: {
          labels: ["14.04", "16.04", "18.04", "20.04"],
          views: [40, 30, 20, 10],
        },
        calls: {
          labels: ["14.04", "16.04", "18.04", "20.04"],
          calls: [25, 15, 10, 5],
        },
        conversion: {
          labels: ["14.04", "16.04", "18.04", "20.04"],
          conversion: [20, 30, 10, 5],
        },
        newDialogs: [
          {
            id: 1,
            user: "User-73",
            message: "Как мне зайти в личный кабинет...",
            time: "18:02",
            status: "done",
          },
          {
            id: 2,
            user: "User-71",
            message: "Спасибо за ваш вопрос! Передавайте...",
            time: "18:02",
            status: "done",
          },
          {
            id: 3,
            user: "User-25",
            message: "Кастомизация доступна только для годового...",
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
        views: {
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
        views: {
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
    plugins: {
      legend: { position: "bottom" },
    },
  };

  return (
    <div className={styles.statsGrid}>
      <div className={styles.chart}>
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
          options={{
            maintainAspectRatio: false,
            responsive: true,
            plugins: {
              legend: {
                align: "start",
                position: "bottom",
                labels: {
                  boxWidth: 16,
                  boxHeight: 16,
                  useBorderRadius: true,
                  borderRadius: 4,
                },
              },
            },
          }}
        />
      </div>

      <StatsContainer title="Просмотры визитки">
        <Bar
          data={{
            labels: statsData.views.labels,
            datasets: [
              {
                label: "Просмотры визитки за сутки",
                data: statsData.views.views,
                backgroundColor: "#6945ed",
              },
            ],
          }}
          options={{ maintainAspectRatio: false, responsive: true }}
        />
      </StatsContainer>
      <StatsContainer title="Количество звонков">
        <Bar
          data={{
            labels: statsData.calls.labels,
            datasets: [
              {
                label: "Количество звонков за сутки",
                data: statsData.calls.calls,
                backgroundColor: "#6945ed",
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
                {dialog.status === "done" ? "✔️" : "⏳"}
              </span>
            </li>
          ))}
        </ul>
        <button className={styles.viewAllButton}>Смотреть все диалоги</button>
      </StatsContainer>
    </div>
  );
};

export default DashboardStats;
