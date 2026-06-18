"""初期管理者アカウントを作成するスクリプト。
使い方: python -m scripts.create_admin
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import SessionLocal, engine, Base
from app.core.security import hash_password
from app.models.account import Account
import app.models  # noqa: F401


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        username = input("管理者ユーザー名: ").strip()
        email = input("メールアドレス: ").strip()
        password = input("パスワード: ").strip()

        if len(password) < 8:
            print("エラー: パスワードは8文字以上にしてください")
            return

        if db.query(Account).filter(Account.username == username).first():
            print(f"エラー: ユーザー名 '{username}' は既に存在します")
            return

        account = Account(
            username=username,
            email=email,
            hashed_password=hash_password(password),
            is_active=True,
            role="admin",
        )
        db.add(account)
        db.commit()
        print(f"✅ 管理者アカウント '{username}' を作成しました (role=admin)")
    finally:
        db.close()


if __name__ == "__main__":
    main()
