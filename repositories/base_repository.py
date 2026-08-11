from sqlalchemy.orm import Session


class BaseRepository:

    def __init__(self, db: Session):
        self.db = db

    def add(self, obj):
        self.db.add(obj)
        return obj

    def add_all(self, objects):
        self.db.add_all(objects)

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def refresh(self, obj):
        self.db.refresh(obj)

    def flush(self):
        self.db.flush()