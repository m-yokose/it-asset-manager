# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

IT資産管理Webアプリケーション。FastAPI + Jinja2 + HTMX + Tailwind CSS/DaisyUI 構成。
管理対象: ハードウェア、ソフトウェアライセンス、ネットワーク機器、消耗品・備品。

## Commands

```bash
# --- 環境構築（初回のみ、backend/ ディレクトリで実行）---

# 依存関係インストール（.venv を自動作成）
uv sync

# 開発用依存関係（pytest 等）も含む場合
uv sync --dev

# --- 以降はすべて backend/ から実行 ---

# 初回: 管理者アカウント作成
uv run python -m scripts.create_admin

# 開発サーバー起動
uv run uvicorn app.main:app --reload

# マイグレーション
uv run alembic upgrade head
uv run alembic revision --autogenerate -m "description"
uv run alembic downgrade -1

# テスト
uv run pytest
uv run pytest tests/test_assets.py
uv run pytest -k "test_create"

# Docker で起動 (プロジェクトルートで実行)
docker compose up --build
```

## Architecture

```
it-asset-manager/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI初期化・ルーター登録・セキュリティヘッダー・slowapi
│   │   ├── core/
│   │   │   ├── config.py        # pydantic-settings (DATABASE_URL, SECRET_KEY 等)
│   │   │   ├── database.py      # SQLAlchemy engine / SessionLocal / Base
│   │   │   ├── security.py      # JWT発行・検証・パスワードハッシュ
│   │   │   └── limiter.py       # slowapi レート制限インスタンス
│   │   ├── models/              # SQLAlchemy ORMモデル
│   │   ├── schemas/             # Pydantic スキーマ (Create/Update/Response)
│   │   ├── services/            # DBロジック (router から呼び出す)
│   │   └── api/v1/              # FastAPI ルーター (画面+フォーム処理)
│   ├── alembic/                 # マイグレーション
│   ├── scripts/create_admin.py  # 初期管理者作成
│   └── pyproject.toml           # 依存関係定義 (uv で管理)
└── frontend/
    ├── templates/               # Jinja2 テンプレート (base.html + カテゴリ別)
    ├── static/                  # CSS / JS
    └── components/              # 再利用可能な Jinja2 マクロ (予定)
```

### データフロー

`Router → Service → SQLAlchemy Model → SQLite/PostgreSQL`

### 認証フロー (JWT + httpOnly Cookie)

1. `POST /auth/login` でフォーム送信 → JWT を httpOnly + SameSite=strict Cookie にセット
2. 以降のリクエストで Cookie を自動送信
3. `api/deps.py` の `get_current_account()` で Cookie を検証、Account モデルを返す
4. 未認証時は `/auth/login` にリダイレクト (401ハンドラ)
5. ログインには 5回/分 のレート制限あり (slowapi)

### 権限モデル

`accounts.role` で制御:
- `"admin"` — CRUD 全操作可。`require_admin` 依存関数で保護。
- `"viewer"` — 閲覧のみ。テンプレートで編集・削除ボタンを非表示。

`accounts` テーブル = ログイン用 (IT管理者・監査担当)
`users` テーブル = 資産の割り当て先 (従業員)

### テンプレート構造

`base.html` が共通レイアウト (DaisyUI Drawer サイドバー)。各ページは `{% extends "base.html" %}` で継承。
フォームの登録・編集は同一テンプレート (`form.html`) で `asset` が None かどうかで切り替え。
`current_account.role == 'admin'` で編集・削除ボタンの表示を制御。

### テンプレートディレクトリの解決

`core/config.py` の `templates_dir` / `static_dir` で制御。
ローカル実行時は `backend/` からの相対パスで `../frontend/templates` に自動解決。
Docker では環境変数 `TEMPLATES_DIR=/frontend/templates` でオーバーライド。

## Tech Stack

| 用途 | ライブラリ |
|------|-----------|
| Web フレームワーク | FastAPI |
| ORM | SQLAlchemy 2.0 |
| マイグレーション | Alembic |
| DB | SQLite (開発) / PostgreSQL (本番) |
| テンプレート | Jinja2 |
| 動的UI | HTMX |
| CSS | Tailwind CSS + DaisyUI (CDN) |
| 認証 | python-jose (JWT) + passlib (bcrypt) |
| レート制限 | slowapi |
| 設定管理 | pydantic-settings |
| インポート | openpyxl, pandas |
| テスト | pytest, httpx (TestClient) |
| パッケージ管理 | uv |
