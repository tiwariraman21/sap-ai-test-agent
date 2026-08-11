from repositories.base_repository import BaseRepository

from models.rules import BusinessRule


class RuleRepository(BaseRepository):

    def get_active_rules(self):

        return (
            self.db.query(BusinessRule)
            .filter(
                BusinessRule.is_active == True
            )
            .all()
        )

    def get_rules(self):
        """
        Returns all active business rules.
        """
        return self.get_active_rules()