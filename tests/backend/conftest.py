import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import database, main
from app.config import settings
from app.database import Base
from app.deps import get_db
from app.main import app

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_database():
    original_session_local = database.SessionLocal
    original_main_session_local = main.SessionLocal
    original_run_migrations = settings.RUN_MIGRATIONS_ON_STARTUP
    settings.RUN_MIGRATIONS_ON_STARTUP = False

    database.SessionLocal = TestingSessionLocal  # type: ignore[assignment]
    main.SessionLocal = TestingSessionLocal  # type: ignore[assignment]

    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

    database.SessionLocal = original_session_local  # type: ignore[assignment]
    main.SessionLocal = original_main_session_local  # type: ignore[assignment]
    settings.RUN_MIGRATIONS_ON_STARTUP = original_run_migrations


@pytest.fixture()
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.pop(get_db, None)
