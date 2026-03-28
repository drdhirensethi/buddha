from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def log_audit_event(
    db: Session,
    action: str,
    entity_type: str,
    entity_id: int | None = None,
    user_id: int | None = None,
    old_value: dict | None = None,
    new_value: dict | None = None,
    ip_address: str | None = None,
) -> AuditLog:
    log = AuditLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        old_value_json=old_value,
        new_value_json=new_value,
        ip_address=ip_address,
    )
    db.add(log)
    return log

