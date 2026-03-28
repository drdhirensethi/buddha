from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import get_password_hash
from app.db.base import *
from app.db.session import Base, SessionLocal, engine
from app.models.role import Role
from app.models.user import User


def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)

    settings = get_settings()
    db: Session = SessionLocal()
    try:
        roles = ["admin", "doctor", "nurse", "reception"]
        existing_roles = {role.name for role in db.query(Role).all()}
        for role_name in roles:
            if role_name not in existing_roles:
                db.add(Role(name=role_name))
        db.commit()

        admin = db.query(User).filter(User.email == settings.first_admin_email).first()
        if not admin:
            admin_role = db.query(Role).filter(Role.name == "admin").one()
            db.add(
                User(
                    email=settings.first_admin_email,
                    full_name="System Administrator",
                    password_hash=get_password_hash(settings.first_admin_password),
                    role_id=admin_role.id,
                    is_active=True,
                )
            )
            db.commit()
    finally:
        db.close()

