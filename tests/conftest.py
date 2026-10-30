# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# from debt_api.db.models import Base
# from tests.factories import DebtorFactory


# @pytest.fixture
# def db_session():
#     # 1. Create a fast, in-memory SQLite database for testing
#     engine = create_engine("sqlite:///:memory:")
#     Base.metadata.create_all(engine)

#     SessionLocal = sessionmaker(bind=engine)
#     session = SessionLocal()

#     DebtorFactory._meta.sqlalchemy_session = session

#     yield session  # 3. Pass the session to the tests

#     session.close()
#     Base.metadata.drop_all(engine)
