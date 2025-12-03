"""
Pytest configuration for backend tests

Author: MiniMax Agent
"""

import os
import pytest
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base

# Configure test database
TEST_DATABASE_URL = os.getenv('TEST_DATABASE_URL', 'sqlite:///./test.db')

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def test_engine():
    """Create a test database engine"""
    engine = create_engine(TEST_DATABASE_URL, echo=False)
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    yield engine
    
    # Cleanup
    Base.metadata.drop_all(engine)
    engine.dispose()

@pytest.fixture
def test_session(test_engine):
    """Create a test database session"""
    Session = sessionmaker(bind=test_engine)
    session = Session()
    
    yield session
    
    session.rollback()
    session.close()

# Configure environment for tests
@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment variables"""
    # Ensure we're using a test database
    os.environ.setdefault('DATABASE_URL', 'sqlite:///./test.db')
    yield
    # Cleanup after tests if needed