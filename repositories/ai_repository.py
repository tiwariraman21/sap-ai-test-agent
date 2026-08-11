from repositories.base_repository import BaseRepository

from models.ai_models import (
    TestSuite,
    TestCase,
    TestExecution,
    TestResult,
)

class AIRepository(BaseRepository):

    def get_test_suites(self):

        return self.db.query(
            TestSuite
        ).all()

    def get_test_cases(self):

        return self.db.query(
            TestCase
        ).all()

    def save_execution(self, execution):

        self.add(execution)

        self.commit()

        return execution