from database.database import Base, engine
from database.models import GoldPrice

Base.metadata.create_all(bind=engine)

print("Database created successfully.")