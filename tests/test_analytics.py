"""Tests for analytics endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_dashboard_stats(client: AsyncClient, test_user_data: dict):
    """Test getting dashboard stats."""
    # Setup
    await client.post("/api/v1/auth/register", json=test_user_data)
    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )
    token = login_response.json()["access_token"]
    
    # Get dashboard
    response = await client.get(
        "/api/v1/analytics/dashboard",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "total_views" in data
    assert "total_revenue" in data


@pytest.mark.asyncio
async def test_get_analytics(client: AsyncClient, test_user_data: dict):
    """Test getting analytics."""
    # Setup
    await client.post("/api/v1/auth/register", json=test_user_data)
    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )
    token = login_response.json()["access_token"]
    
    # Get analytics
    response = await client.get(
        "/api/v1/analytics/?days=30",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
