import pytest
import httpx

# TODO: Configure the base URL for the backend API (Issue #XX)
# For now, assume it's running locally on port 8000
BASE_URL = "http://localhost:8000"

@pytest.mark.asyncio
async def test_get_status():
    """
    Test the GET /status endpoint of the backend API.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/status")

    # Assert that the response status code is 200 OK
    assert response.status_code == 200

    # Assert that the response body contains the expected status message
    # TODO: Update this assertion based on the actual response structure (Issue #XX)
    assert "status" in response.json()
    assert response.json()["status"] == "Backend is running (POC)"

# TODO: Add more tests for other endpoints as they are implemented (Issue #XX)
# TODO: Implement test fixtures for database access, etc. (Issue #XX)
