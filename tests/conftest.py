"""
Shared pytest configuration and fixtures for all tests.
This file is automatically discovered by pytest.
"""

import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


@pytest.fixture(scope="session")
def client():
    """
    Fixture that provides a FastAPI test client.
    Scope: session - this client is reused across all tests.
    """
    return TestClient(app)


@pytest.fixture
def valid_prediction_payload():
    """
    Standard valid payload for prediction tests.
    Contains realistic values for a healthy individual.
    """
    return {
        "age": 35,
        "weight": 70.0,
        "height": 1.75,
        "income_lpa": 10.0,
        "smoker": False,
        "city": "Delhi",
        "occupation": "private_job"
    }


@pytest.fixture
def valid_smoker_payload():
    """Valid payload for a smoker with high BMI (high-risk profile)."""
    return {
        "age": 45,
        "weight": 95.0,
        "height": 1.75,
        "income_lpa": 15.0,
        "smoker": True,
        "city": "Mumbai",
        "occupation": "business_owner"
    }


@pytest.fixture
def valid_high_risk_payload():
    """Valid payload for high-risk individual (older age, high smoker status, high BMI)."""
    return {
        "age": 55,
        "weight": 100.0,
        "height": 1.70,
        "income_lpa": 20.0,
        "smoker": True,
        "city": "Bangalore",
        "occupation": "government_job"
    }


@pytest.fixture
def valid_low_risk_payload():
    """Valid payload for low-risk individual (young, non-smoker, normal BMI)."""
    return {
        "age": 25,
        "weight": 60.0,
        "height": 1.75,
        "income_lpa": 5.0,
        "smoker": False,
        "city": "Pune",
        "occupation": "student"
    }


@pytest.fixture
def all_valid_occupations():
    """List of all valid occupation types."""
    return ["student", "freelancer", "private_job", "government_job", 
            "business_owner", "retired", "unemployed"]


# Pytest configuration hooks

def pytest_configure(config):
    """
    Called after command line options have been parsed
    and all plugins and initial conftest files been loaded.
    """
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "validation: mark test as a validation test"
    )
    config.addinivalue_line(
        "markers", "edge_case: mark test as an edge case test"
    )
