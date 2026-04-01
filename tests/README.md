# Testing Guide for FastAPI ML Project

## Overview

This directory contains comprehensive tests for the Health Insurance Premium Prediction API. The tests follow industry best practices and are organized into logical modules.

## Test Structure

```
tests/
├── conftest.py          # Shared fixtures and pytest configuration
├── test_health.py       # Health check endpoint tests
├── test_predict.py      # Prediction endpoint tests
├── __init__.py          # Package initialization
└── README.md            # This file
```

## Test Categories

### 1. **Health Checks** (`test_health.py`)
Tests for health and status endpoints:
- Root endpoint (`GET /`)
- Health check endpoint (`GET /health`)
- Response structure validation

### 2. **Prediction Success Tests** (`test_predict.py`)
Tests for valid prediction scenarios:
- Standard case (healthy individual)
- Smoker with high BMI
- High-risk individuals
- Low-risk individuals
- Different age groups
- All occupation types
- Smoker status variations
- Income level variations
- Response schema validation

### 3. **Validation Error Tests** (`test_predict.py`)
Tests for input validation and error handling:
- Missing required fields
- Invalid age values (must be 1-120)
- Invalid weight values (must be > 0)
- Invalid height values (must be 0 < h < 2.5)
- Invalid income values (must be > 0)
- Invalid occupation types
- Type mismatches
- Empty payloads

### 4. **Edge Cases** (`test_predict.py`)
Boundary condition and special case tests:
- Minimum valid values
- Maximum valid values
- BMI calculations (normal, overweight, obese)
- City name normalization
- Different city inputs

### 5. **Type Validation** (`test_predict.py`)
Tests for data type handling:
- String to int coercion
- String to float coercion
- Extra field handling

### 6. **Response Consistency** (`test_predict.py`)
Tests for output reliability:
- Deterministic outputs (same input → same output)
- Probability sum validation (should sum to ~1.0)
- Confidence score validation
- Category-probability consistency

## Running Tests

### Run All Tests
```bash
pytest tests/
```

### Run Tests with Verbose Output
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_predict.py -v
pytest tests/test_health.py -v
```

### Run Specific Test Class
```bash
pytest tests/test_predict.py::TestPredictionSuccess -v
```

### Run Specific Test Function
```bash
pytest tests/test_predict.py::TestPredictionSuccess::test_predict_success_standard_case -v
```

### Run Tests by Marker
```bash
# Run only integration tests
pytest tests/ -m integration -v

# Run only validation tests
pytest tests/ -m validation -v

# Run only edge case tests
pytest tests/ -m edge_case -v
```

### Run with Coverage Report
```bash
pytest tests/ --cov=. --cov-report=html
```

## Test Fixtures

All fixtures are defined in `conftest.py`:

### Session-scoped Fixtures
- `client`: FastAPI TestClient (reused across all tests)

### Function-scoped Fixtures
- `valid_prediction_payload`: Standard healthy individual
- `valid_smoker_payload`: High-risk smoker profile
- `valid_high_risk_payload`: Elderly smoker with high BMI
- `valid_low_risk_payload`: Young non-smoker with normal BMI
- `all_valid_occupations`: List of valid occupation types

## Expected Test Results

Running all tests should show:
- Total number of tests: 60+
- Success rate: 100%
- No warnings (except Pydantic deprecation warnings in the schema)

Example output:
```
collected 60+ items

test_health.py::TestHealthEndpoints::test_home_endpoint PASSED       [ 2%]
test_health.py::TestHealthEndpoints::test_health_check_endpoint PASSED [ 5%]
...
test_predict.py::TestResponseConsistency::test_predict_category_in_probabilities PASSED [100%]

======================== 60+ passed in X.XXs ========================
```

## Key Testing Principles

1. **Isolation**: Each test is independent and can run in any order
2. **Clarity**: Test names clearly describe what is being tested
3. **Coverage**: Tests cover happy paths, error cases, and edge cases
4. **Reusability**: Fixtures reduce code duplication
5. **Organization**: Tests are grouped by functionality and purpose
6. **Documentation**: Each test has a docstring explaining its purpose

## Pytest Markers

Tests are marked with custom markers for selective execution:

- `@pytest.mark.integration`: Integration tests (multiple components)
- `@pytest.mark.validation`: Input validation tests
- `@pytest.mark.edge_case`: Edge case and boundary tests

## Common Test Patterns

### Testing Success Cases
```python
def test_predict_success(client, valid_prediction_payload):
    response = client.post("/predict", json=valid_prediction_payload)
    assert response.status_code == 200
    assert "predicted_category" in response.json()
```

### Testing Validation Errors
```python
def test_predict_invalid_age(client, valid_prediction_payload):
    payload = valid_prediction_payload.copy()
    payload["age"] = -1  # Invalid
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # Unprocessable Entity
```

### Testing with Parametrization
```python
@pytest.mark.parametrize("age", [18, 25, 40, 60, 100])
def test_predict_different_ages(client, age, valid_prediction_payload):
    payload = valid_prediction_payload.copy()
    payload["age"] = age
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
```

## Dependencies

Tests require:
- `pytest>=7.0`
- `fastapi`
- `httpx` (required by TestClient)
- `pydantic`

These are typically included in your project dependencies. Install with:
```bash
pip install pytest
```

or if using conda:
```bash
conda install pytest
```

## Continuous Integration

To integrate tests with CI/CD (GitHub Actions, GitLab CI, etc.), use:
```bash
pytest tests/ -v --junitxml=junit.xml --cov=. --cov-report=xml
```

## Test Maintenance

- Update fixtures if API contract changes
- Add new tests for new features
- Keep test names descriptive and meaningful
- Use parametrization to avoid duplicate tests
- Review test coverage regularly

## Troubleshooting

### Import Errors
If you see `ModuleNotFoundError: No module named 'app'`, ensure:
1. conda environment is activated
2. pytest is running from the project root directory
3. conftest.py is correctly adding the parent directory to sys.path

### Test Failures
Common causes:
1. Environment not activated (check Python version is 3.11.15)
2. Missing dependencies (conda install pytest)
3. Model file path issues (check model/predict.py)
4. changes to API contract not reflected in tests

## Contributing

When adding new tests:
1. Follow the existing test structure
2. Use descriptive test names
3. Add docstrings to test functions
4. Use appropriate markers (@pytest.mark.*)
5. Use fixtures to avoid code duplication
6. Ensure tests are independent and can run in any order
