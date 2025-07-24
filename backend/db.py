from sqlmodel import SQLModel, create_engine

DATABASE_URL = "postgresql://reconrebels_1:Loknath%404044@recons.postgres.database.azure.com/postgres"  # Update if needed

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
