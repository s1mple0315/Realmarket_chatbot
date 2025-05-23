import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  useInfiniteQuery,
  useMutation,
  useQueryClient,
} from "@tanstack/react-query";
import {
  fetchConversations,
  markConversationRead,
} from "../../../config/api/api";
import DashboardControls from "../../../components/DashboardControls/DashboardControls";
import DialogItem from "../../../components/DialogItem/DialogItem";
import Loader from "../../../components/Loader/Loader";
import styles from "./DialogsPage.module.css";

const DialogsPage = () => {
  const [activeTab, setActiveTab] = useState("today");
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading,
    error,
  } = useInfiniteQuery({
    queryKey: ["conversations", activeTab],
    queryFn: ({ pageParam = 1 }) =>
      fetchConversations({ page: pageParam, tab: activeTab }),
    getNextPageParam: (lastPage, allPages) =>
      lastPage.data.conversations.length === 50
        ? allPages.length + 1
        : undefined,
    retry: 1,
  });

  const readMutation = useMutation({
    mutationFn: markConversationRead,
    onSuccess: () =>
      queryClient.invalidateQueries(["conversations", activeTab]),
    onError: (error) =>
      console.error("Failed to mark conversation as read:", error),
  });

  const conversations =
    data?.pages.flatMap((page) => page.data.conversations) || [];
  const totalDialogs = conversations.length;
  const newDialogs = conversations.filter((conv) => conv.unread).length;

  const handleDialogClick = (userId, threadId) => {
    readMutation.mutate(threadId);
    navigate(`/dialog/${userId}`);
  };

  return (
    <div className={styles.dialogsPage}>
      <div
        className={`${styles.dialogsPageTitle} d-flex align-items-center justify-content-between`}
      >
        <h2 className={styles.title}>Диалоги</h2>
        <DashboardControls onTabChange={setActiveTab} />
      </div>

      <div className={styles.dialogsPageContent}>
        <h3>
          Диалогов: {totalDialogs} / Новых: {newDialogs}
        </h3>
        {isLoading && <Loader />}
        {error && (
          <p className={styles.error}>
            {error.response?.status === 401
              ? "Не авторизован. Пожалуйста, войдите снова."
              : error.response?.status === 404
              ? "Диалоги не найдены."
              : `Ошибка: ${error.message}`}
          </p>
        )}
        {conversations.length === 0 && !isLoading && <p>Диалогов нет</p>}
        {conversations.map((dialog) => (
          <DialogItem
            key={dialog.thread_id}
            userId={dialog.user_id}
            message={
              dialog.messages[dialog.messages.length - 1]?.content ||
              "Нет сообщений"
            }
            timestamp={new Date(dialog.created_at).toLocaleString("ru-RU", {
              day: "2-digit",
              month: "2-digit",
              year: "2-digit",
              hour: "2-digit",
              minute: "2-digit",
            })}
            readStatus={dialog.readStatus}
            readTime={
              dialog.read_at
                ? new Date(dialog.read_at).toLocaleString("ru-RU", {
                    hour: "2-digit",
                    minute: "2-digit",
                  })
                : null
            }
            unread={dialog.unread}
            onArrowClick={() =>
              handleDialogClick(dialog.user_id, dialog.thread_id)
            }
          />
        ))}
        {hasNextPage && (
          <button
            onClick={() => fetchNextPage()}
            disabled={isFetchingNextPage}
            className={styles.loadMoreButton}
          >
            {isFetchingNextPage ? "Загрузка..." : "Загрузить еще"}
          </button>
        )}
      </div>
    </div>
  );
};

export default DialogsPage;
