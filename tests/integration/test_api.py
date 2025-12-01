"""
Integration tests for Supply Chain Platform API endpoints.
"""
import pytest
import asyncio
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint():
    """Test the health check endpoint."""
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_analytics_overview():
    """Test the analytics overview endpoint."""
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.get("/analytics/overview")
        assert response.status_code == 200
        data = response.json()
        assert "total_shipments" in data
        assert "on_time_delivery_rate" in data
        assert "avg_delivery_time" in data


@pytest.mark.asyncio
async def test_suppliers_endpoint():
    """Test the suppliers endpoint."""
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.get("/suppliers")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


@pytest.mark.asyncio
async def test_warehouses_endpoint():
    """Test the warehouses endpoint."""
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.get("/warehouses")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)