# IT資産管理システム

PC・モニタ・スマホなどのハードウェア資産、ソフトウェアライセンス、利用者（従業員）を一元管理するWebアプリケーション。

## 機能

- **ハードウェア資産管理** — 種別・メーカー・型番・シリアル番号・購入日・ステータス・担当者・備考
- **ソフトウェアライセンス管理** — ライセンスキー・有効期限・ライセンス数量（席数）、30日前期限切れアラート
- **利用者管理** — 従業員の氏名・部署・メールアドレス
- **役割ベースアクセス制御** — `admin`（CRUD）/ `viewer`（閲覧のみ）
- **JWT認証** — httpOnly Cookie + SameSite=strict

## 技術スタック

| 用途 | ライブラリ |
|------|-----------|
| Web フレームワーク | FastAPI |
| ORM | SQLAlchemy 2.0 |
| マイグレーション | Alembic |
| DB | SQLite（開発）/ PostgreSQL（本番） |
| テンプレート | Jinja2 + HTMX |
| CSS | Tailwind CSS + DaisyUI |
| 認証 | python-jose (JWT) + passlib (bcrypt) |
| パッケージ管理 | uv |

## セットアップ

### 前提条件

- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

```bash
# uv のインストール
# Windows
winget install --id=astral-sh.uv
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### ローカル開発

```bash
git clone https://github.com/m-yokose/it-asset-manager.git
cd it-asset-manager/backend

# 依存関係のインストール（.venv を自動作成）
uv sync

# 環境変数の設定
cp .env.example .env
# .env を編集して SECRET_KEY を変更

# 初回: 管理者アカウントを作成
uv run python -m scripts.create_admin

# 開発サーバーを起動
uv run uvicorn app.main:app --reload
```

ブラウザで [http://localhost:8000](http://localhost:8000) を開く。

### Docker で起動

```bash
# プロジェクトルートで実行
cp backend/.env.example backend/.env  # .env を設定してから
docker compose up --build
```

## 環境変数

`backend/.env.example` をコピーして `backend/.env` を作成。

| 変数 | 説明 | デフォルト |
|------|------|-----------|
| `DATABASE_URL` | DB接続文字列 | `sqlite:///./dev.db` |
| `SECRET_KEY` | JWT署名キー（**本番では必ず変更**） | `change-me-in-production` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | トークン有効期限（分） | `480` |

## 権限

| ロール | 権限 |
|--------|------|
| `admin` | 登録・編集・削除・閲覧すべて可 |
| `viewer` | 閲覧のみ（編集・削除ボタン非表示） |

管理者アカウントは `uv run python -m scripts.create_admin` で作成。

## 開発コマンド

```bash
# テスト
uv run pytest

# DBマイグレーション
uv run alembic upgrade head
uv run alembic revision --autogenerate -m "description"

# 開発用依存関係も含めてインストール
uv sync --dev
```

## ディレクトリ構成

```
it-asset-manager/
├── backend/
│   ├── app/
│   │   ├── main.py        # FastAPI初期化
│   │   ├── core/          # 設定・DB・JWT・レート制限
│   │   ├── models/        # SQLAlchemyモデル
│   │   ├── schemas/       # Pydanticスキーマ
│   │   ├── services/      # CRUDロジック
│   │   └── api/v1/        # ルーター（画面+フォーム処理）
│   ├── alembic/           # マイグレーション
│   ├── scripts/           # 管理者作成スクリプト
│   └── pyproject.toml
├── frontend/
│   ├── templates/         # Jinja2テンプレート
│   └── static/
└── docker-compose.yml
```
