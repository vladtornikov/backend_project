from src.utils.database_cntxt_mngr import DBManager


class BaseService:
    db: DBManager | None

    def __init__(self, db: DBManager | None) -> None:
        self.db = db