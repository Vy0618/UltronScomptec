"""Allocate stable human-readable codes for domain entities."""
from sqlalchemy import select
from sqlalchemy.orm import Session
from database.models import CodeSequence


def next_code(db: Session, model, prefix: str) -> str:
    """Generate a readable code without reusing one after a deletion."""
    if db.bind.dialect.name == "mysql":
        from sqlalchemy.dialects.mysql import insert
        existing_numbers = [int(code[len(prefix):]) for code in db.scalars(select(model.code)) if code.startswith(prefix) and code[len(prefix):].isdigit()]
        stmt = insert(CodeSequence).values(prefix=prefix, last_number=max(existing_numbers, default=0) + 1)
        db.execute(stmt.on_duplicate_key_update(last_number=CodeSequence.last_number + 1))
        number = db.scalar(select(CodeSequence.last_number).where(CodeSequence.prefix == prefix).with_for_update())
        return f"{prefix}{number:03d}"
    sequence = db.get(CodeSequence, prefix)
    if not sequence:
        existing_numbers = [
            int(code.removeprefix(prefix))
            for code in db.scalars(select(model.code))
            if code.startswith(prefix) and code.removeprefix(prefix).isdigit()
        ]
        sequence = CodeSequence(prefix=prefix, last_number=max(existing_numbers, default=0))
        db.add(sequence)

    sequence.last_number += 1
    db.flush()
    return f"{prefix}{sequence.last_number:03d}"

