from database.connection import engine
from database.models import Base

# Import all model files
import models.master_data
import models.procurement
import models.inventory
import models.rules
import models.ai_models
import models.system


def create_database():
    print("=" * 60)
    print("Creating Database Tables...")
    print("=" * 60)

    Base.metadata.create_all(bind=engine)

    print("\n✅ All tables created successfully!")


if __name__ == "__main__":
    create_database()