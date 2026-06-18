FROM python:3.12-slim

# uv をインストール
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# 依存関係のインストール（ソースコードより先にキャッシュ効率化）
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev

COPY . .

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
