
FROM node:20 AS frontend-builder

WORKDIR /frontend
COPY frontend/package.json frontend/yarn.lock ./
RUN yarn install
COPY frontend ./
RUN yarn build



FROM python:3.10-slim


WORKDIR /app
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY backend ./backend


COPY --from=frontend-builder /frontend/dist ./frontend_dist


CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
