"""
Tests for health check and status endpoints.
Verifies that the API is running and the model is loaded correctly.
"""

import pytest


class TestHealthEndpoints:
    """Test suite for health and status endpoints."""
    
    def test_home_endpoint(self, client):
        """Test root endpoint returns welcome message."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Health Insurance Premium Prediction API" in data["message"]

    def test_health_check_endpoint(self, client):
        """
        Test health check endpoint returns status and model info.
        Verifies:
        - Status is OK
        - Model is loaded
        - Model version is present
        """
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "OK"
        assert "model_loaded" in data
        assert isinstance(data["model_loaded"], bool)
        assert data["model_loaded"] is True, "Model should be loaded"
        assert "model_version" in data

    def test_health_check_response_structure(self, client):
        """Verify health check response has expected structure."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 3, "Health response should contain exactly 3 fields"
