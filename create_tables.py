from database.database import engine, Base
from database.models import GoldPrice

Base.metadata.create_all(bind=engine)

print("Database created successfully")