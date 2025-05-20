import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api/v1",
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export const fetchAssistants = () => api.get("/assistants");
export const createAssistant = (data) => api.post("/assistants", data);
export const deleteAssistant = (id) => api.delete(`/assistants/${id}`);
export const fetchContent = (assistantId, contentType) =>
  api.get(`/assistants/${assistantId}/content`, {
    params: { content_type: contentType },
  });
export const uploadContent = (assistantId, data) =>
  api.post(`/assistants/${assistantId}/content`, data);
export const uploadFile = (assistantId, formData) =>
  api.post("/files/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
    params: { assistant_id: assistantId },
  });
export const crawlWebsite = (assistantId, data) =>
  api.post("/crawler/crawl", { ...data, assistant_id: assistantId });
export const fetchCrawlHistory = (assistantId) =>
  api.get("/crawler/history", { params: { assistant_id: assistantId } });
export const fetchConversations = (page = 1) =>
  api.get("/assistants/conversations", {
    params: { skip: (page - 1) * 50, limit: 50 },
  });

export default api;
