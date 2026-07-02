"""Tests for content endpoints."""

import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_create_content(client: AsyncClient, test_user_data: dict, test_content_data: dict):
    """Test creating content."""
    # Register and login
    await client.post("/api/v1/auth/register", json=test_user_data)
    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )
    token = login_response.json()["access_token"]
    
    # Create content
    response = await client.post(
        "/api/v1/content/",
        json=test_content_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_content_data["title"]
    assert data["script"] == test_content_data["script"]
    assert "id" in data


@pytest.mark.asyncio
async def test_list_content(client: AsyncClient, test_user_data: dict, test_content_data: dict):
    """Test listing user content."""
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
    
    # Create content
    await client.post(
        "/api/v1/content/",
        json=test_content_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # List content
    response = await client.get(
        "/api/v1/content/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["title"] == test_content_data["title"]


@pytest.mark.asyncio
async def test_get_content(client: AsyncClient, test_user_data: dict, test_content_data: dict):
    """Test getting specific content."""
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
    
    # Create content
    create_response = await client.post(
        "/api/v1/content/",
        json=test_content_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    content_id = create_response.json()["id"]
    
    # Get content
    response = await client.get(
        f"/api/v1/content/{content_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == content_id


@pytest.mark.asyncio
async def test_update_content(client: AsyncClient, test_user_data: dict, test_content_data: dict):
    """Test updating content."""
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
    
    # Create content
    create_response = await client.post(
        "/api/v1/content/",
        json=test_content_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    content_id = create_response.json()["id"]
    
    # Update content
    response = await client.patch(
        f"/api/v1/content/{content_id}",
        json={"title": "Updated Title"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"


@pytest.mark.asyncio
async def test_delete_content(client: AsyncClient, test_user_data: dict, test_content_data: dict):
    """Test deleting content."""
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
    
    # Create content
    create_response = await client.post(
        "/api/v1/content/",
        json=test_content_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    content_id = create_response.json()["id"]
    
    # Delete content
    response = await client.delete(
        f"/api/v1/content/{content_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
