"""Integration tests for end-to-end workflows."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_full_content_creation_workflow(
    client: AsyncClient,
    test_user_data: dict,
    test_content_data: dict
):
    """Test complete content creation workflow."""
    # 1. Register user
    register_response = await client.post("/api/v1/auth/register", json=test_user_data)
    assert register_response.status_code == 200
    user = register_response.json()
    
    # 2. Login
    login_response = await client.post(
        "/api/v1/auth/login",
        json={"email": test_user_data["email"], "password": test_user_data["password"]}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Create content
    content_response = await client.post(
        "/api/v1/content/",
        json=test_content_data,
        headers=headers
    )
    assert content_response.status_code == 200
    content = content_response.json()
    content_id = content["id"]
    
    # 4. Get analytics for content
    analytics_response = await client.get(
        "/api/v1/analytics/",
        headers=headers
    )
    assert analytics_response.status_code == 200
    
    # 5. Schedule content
    from datetime import datetime, timedelta
    schedule_response = await client.post(
        f"/api/v1/content/{content_id}/schedule",
        json={"scheduled_publish": (datetime.utcnow() + timedelta(days=1)).isoformat()},
        headers=headers
    )
    assert schedule_response.status_code == 200
    
    # 6. Get scheduled content
    scheduled_response = await client.get(
        "/api/v1/scheduling/scheduled",
        headers=headers
    )
    assert scheduled_response.status_code == 200
    
    # 7. Check dashboard stats
    dashboard_response = await client.get(
        "/api/v1/analytics/dashboard",
        headers=headers
    )
    assert dashboard_response.status_code == 200


@pytest.mark.asyncio
async def test_monetization_workflow(client: AsyncClient, test_user_data: dict):
    """Test monetization workflow."""
    # Register and login
    await client.post("/api/v1/auth/register", json=test_user_data)
    login_response = await client.post(
        "/api/v1/auth/login",
        json={"email": test_user_data["email"], "password": test_user_data["password"]}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get monetization info
    response = await client.get("/api/v1/monetization/", headers=headers)
    assert response.status_code == 200
    
    # Get earnings
    response = await client.get("/api/v1/monetization/earnings", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "total_earnings" in data
    assert "pending_payout" in data
    assert "paid_out" in data
