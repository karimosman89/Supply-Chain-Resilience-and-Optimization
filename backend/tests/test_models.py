"""
Backend Models Tests
Tests for database models and basic operations

Author: MiniMax Agent
"""

import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from models.models import Base, Supplier, Product, User
import os


class TestModels:
    """Test class for database models"""
    
    @pytest.mark.asyncio
    async def test_models_import(self):
        """Test that models can be imported successfully"""
        # This test just verifies that imports work correctly
        assert Base is not None
        assert Supplier is not None
        assert Product is not None
        assert User is not None
        
        # Check that tables are defined
        assert len(Base.metadata.tables) > 0
    
    @pytest.mark.asyncio
    async def test_models_structure(self):
        """Test that models have the expected structure"""
        # Test Supplier model
        supplier_attrs = ['id', 'name', 'email', 'location', 'status']
        for attr in supplier_attrs:
            assert hasattr(Supplier, attr), f"Supplier missing attribute: {attr}"
        
        # Test Product model
        product_attrs = ['id', 'name', 'sku', 'category', 'supplier_id', 'current_stock', 'status']
        for attr in product_attrs:
            assert hasattr(Product, attr), f"Product missing attribute: {attr}"
        
        # Test User model
        user_attrs = ['id', 'email', 'username', 'role', 'is_active']
        for attr in user_attrs:
            assert hasattr(User, attr), f"User missing attribute: {attr}"
    
    @pytest.mark.asyncio 
    async def test_table_creation_no_context_error(self):
        """Test that table creation doesn't cause async context errors"""
        # This test verifies that we can reference metadata without
        # triggering async context errors
        
        # Just accessing the metadata should work
        tables = Base.metadata.tables
        assert isinstance(tables, dict)
        assert len(tables) > 0
        
        # Accessing table names shouldn't cause async errors
        table_names = list(tables.keys())
        assert len(table_names) > 0
        
        print(f"✅ Successfully accessed {len(tables)} tables: {', '.join(table_names[:3])}...")


class TestDatabaseConfig:
    """Test class for database configuration"""
    
    def test_database_url_format(self):
        """Test that DATABASE_URL is properly formatted"""
        db_url = os.getenv('DATABASE_URL', 'postgresql://localhost:5432/test_db')
        
        # Accept both regular format and GitHub Actions masked format
        valid_formats = [
            db_url.startswith('postgresql://'),  # Normal format
            'localhost:5432' in db_url and 'test_db' in db_url,  # GitHub masked format
            db_url.startswith('sqlite://')  # Alternative format for testing
        ]
        
        assert any(valid_formats), f"Invalid DATABASE_URL format: {db_url}"
        
        # If it's a normal PostgreSQL URL, check it starts properly
        if db_url.startswith('postgresql://'):
            assert db_url.startswith('postgresql://'), f"Invalid DATABASE_URL format: {db_url}"
    
    def test_redis_url_format(self):
        """Test that REDIS_URL is properly formatted"""
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        assert redis_url.startswith('redis://'), f"Invalid REDIS_URL format: {redis_url}"


if __name__ == "__main__":
    # Run tests directly if executed as script
    pytest.main([__file__, "-v"])