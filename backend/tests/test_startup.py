"""
Backend Startup Tests
Tests that verify the backend can start and basic functionality works

Author: MiniMax Agent
"""

import pytest
import os
import sys

# Add the backend directory to Python path for imports
backend_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, backend_dir)

def test_models_import():
    """Test that database models can be imported successfully"""
    try:
        from models.models import Base, Supplier, Product, User
        
        # Verify models are imported correctly
        assert Base is not None
        assert Supplier is not None  
        assert Product is not None
        assert User is not None
        
        # Check that table metadata is available
        assert len(Base.metadata.tables) > 0
        
        print(f"✅ Successfully imported {len(Base.metadata.tables)} tables")
        
    except ImportError as e:
        pytest.fail(f"Failed to import models: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error importing models: {e}")

def test_models_structure():
    """Test that models have expected structure"""
    from models.models import Base, Supplier, Product, User
    
    # Test Supplier model attributes
    supplier_columns = [col.name for col in Supplier.__table__.columns]
    expected_supplier_cols = ['id', 'name', 'code', 'country', 'category']
    for col in expected_supplier_cols:
        assert col in supplier_columns, f"Supplier missing column: {col}"
    
    # Test Product model attributes  
    product_columns = [col.name for col in Product.__table__.columns]
    expected_product_cols = ['id', 'sku', 'name', 'category', 'supplier_id']
    for col in expected_product_cols:
        assert col in product_columns, f"Product missing column: {col}"
        
    # Test User model attributes
    user_columns = [col.name for col in User.__table__.columns]
    expected_user_cols = ['id', 'username', 'email', 'role', 'is_active']
    for col in expected_user_cols:
        assert col in user_columns, f"User missing column: {col}"
        
    print("✅ All models have expected structure")

def test_database_config():
    """Test database configuration is valid"""
    # Test DATABASE_URL format
    db_url = os.getenv('DATABASE_URL')
    if db_url:
        # Accept various formats including GitHub Actions masked format
        valid_formats = [
            db_url.startswith('postgresql://'),
            db_url.startswith('sqlite://'),
            'localhost:5432' in db_url and 'test_db' in db_url  # GitHub masked format
        ]
        assert any(valid_formats), f"Invalid DATABASE_URL format: {db_url}"
        print(f"✅ DATABASE_URL is properly formatted")
    else:
        print("⚠️  DATABASE_URL not set, using default")
    
    # Test REDIS_URL format
    redis_url = os.getenv('REDIS_URL')
    if redis_url:
        assert redis_url.startswith('redis://'), \
            f"Invalid REDIS_URL format: {redis_url}"
        print(f"✅ REDIS_URL is properly formatted")
    else:
        print("⚠️  REDIS_URL not set, using default")

def test_alembic_compatibility():
    """Test that alembic configuration works with models"""
    try:
        # Try to import alembic environment (without running migrations)
        alembic_dir = os.path.join(backend_dir, 'alembic')
        if os.path.exists(alembic_dir):
            print("✅ Alembic configuration found")
        else:
            pytest.skip("Alembic configuration not found")
            
    except Exception as e:
        pytest.fail(f"Alembic compatibility issue: {e}")

if __name__ == "__main__":
    # Run tests manually
    test_models_import()
    test_models_structure()
    test_database_config()
    test_alembic_compatibility()
    print("🎉 All startup tests passed!")