
FROM node:20 AS frontend-builder
WORKDIR /app
COPY frontend/package.json frontend/yarn.lock ./
RUN yarn install
COPY frontend ./
RUN yarn build 


FROM python:3.10-slim
WORKDIR /app
COPY backend/requirements.txt ./
RUN pip install -r requirements.txt
COPY backend ./
COPY --from=frontend-builder /app/dist ./frontend_dist  # ➜ копируем в backend

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
