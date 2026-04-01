"""
Tests for the /predict endpoint.
Covers success cases, validation errors, edge cases, and response consistency.
"""

import pytest


class TestPredictionSuccess:
    """Test suite for successful prediction scenarios."""
    
    def test_predict_success_standard_case(self, client, valid_prediction_payload):
        """Test prediction with standard valid input."""
        response = client.post("/predict", json=valid_prediction_payload)
        assert response.status_code == 200
        data = response.json()
        assert "predicted_category" in data
        assert "confidence" in data
        assert "class_probabilities" in data
        assert isinstance(data["class_probabilities"], dict)
        assert 0 <= data["confidence"] <= 1

    def test_predict_success_smoker(self, client, valid_smoker_payload):
        """Test prediction for smoker with high BMI."""
        response = client.post("/predict", json=valid_smoker_payload)
        assert response.status_code == 200
        data = response.json()
        assert "predicted_category" in data
        assert data["predicted_category"] in ["Low", "Medium", "High"]

    def test_predict_success_high_risk(self, client, valid_high_risk_payload):
        """Test prediction for high-risk individual."""
        response = client.post("/predict", json=valid_high_risk_payload)
        assert response.status_code == 200
        data = response.json()
        assert "predicted_category" in data

    def test_predict_success_low_risk(self, client, valid_low_risk_payload):
        """Test prediction for low-risk individual."""
        response = client.post("/predict", json=valid_low_risk_payload)
        assert response.status_code == 200
        data = response.json()
        assert "predicted_category" in data

    @pytest.mark.parametrize("age", [18, 25, 40, 60, 100])
    def test_predict_different_ages(self, client, age, valid_prediction_payload):
        """Test prediction with various age values."""
        payload = valid_prediction_payload.copy()
        payload["age"] = age
        response = client.post("/predict", json=payload)
        assert response.status_code == 200

    @pytest.mark.parametrize("occupation", 
                           ["student", "freelancer", "private_job", "government_job", 
                            "business_owner", "retired", "unemployed"])
    def test_predict_different_occupations(self, client, occupation, valid_prediction_payload):
        """Test prediction with all valid occupation types."""
        payload = valid_prediction_payload.copy()
        payload["occupation"] = occupation
        response = client.post("/predict", json=payload)
        assert response.status_code == 200

    @pytest.mark.parametrize("smoker", [True, False])
    def test_predict_smoker_status(self, client, smoker, valid_prediction_payload):
        """Test prediction for both smokers and non-smokers."""
        payload = valid_prediction_payload.copy()
        payload["smoker"] = smoker
        response = client.post("/predict", json=payload)
        assert response.status_code == 200

    @pytest.mark.parametrize("income", [1.0, 5.0, 10.0, 50.0, 100.0])
    def test_predict_different_income_levels(self, client, income, valid_prediction_payload):
        """Test prediction with various income levels."""
        payload = valid_prediction_payload.copy()
        payload["income_lpa"] = income
        response = client.post("/predict", json=payload)
        assert response.status_code == 200

    def test_predict_response_schema_validation(self, client, valid_prediction_payload):
        """
        Test that response matches expected schema.
        Validates all required fields and their types.
        """
        response = client.post("/predict", json=valid_prediction_payload)
        assert response.status_code == 200
        data = response.json()
        # Check all required fields exist
        required_fields = ["predicted_category", "confidence", "class_probabilities"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        # Validate class probabilities structure
        assert all(isinstance(k, str) and isinstance(v, (int, float)) 
                  for k, v in data["class_probabilities"].items())


class TestValidationErrors:
    """Test suite for validation errors with invalid inputs (422 responses)."""
    
    def test_predict_missing_required_field(self, client):
        """Test prediction with missing required field."""
        payload = {
            "age": 35,
            "weight": 70.0,
            # Missing height - required field
            "income_lpa": 10.0,
            "smoker": False,
            "city": "Delhi",
            "occupation": "private_job"
        }
        response = client.post("/predict", json=payload)
        assert response.status_code == 422

    def test_predict_missing_multiple_fields(self, client):
        """Test prediction with multiple missing fields."""
        payload = {"age": 35}
        response = client.post("/predict", json=payload)
        assert response.status_code == 422

    def test_predict_empty_payload(self, client):
        """Test prediction with empty payload."""
        response = client.post("/predict", json={})
        assert response.status_code == 422

    @pytest.mark.validation
    @pytest.mark.parametrize("invalid_age", [-1, 0, 121, 200])
    def test_predict_invalid_age(self, client, invalid_age, valid_prediction_payload):
        """Test prediction with invalid age values (age must be 1-120)."""
        payload = valid_prediction_payload.copy()
        payload["age"] = invalid_age
        response = client.post("/predict", json=payload)
        assert response.status_code == 422

    @pytest.mark.validation
    @pytest.mark.parametrize("invalid_weight", [-1, 0])
    def test_predict_invalid_weight(self, client, invalid_weight, valid_prediction_payload):
        """Test prediction with invalid weight values (weight must be > 0)."""
        payload = valid_prediction_payload.copy()
        payload["weight"] = invalid_weight
        response = client.post("/predict", json=payload)
        assert response.status_code == 422

    @pytest.mark.validation
    @pytest.mark.parametrize("invalid_height", [-1, 0, 2.5, 3.0])
    def test_predict_invalid_height(self, client, invalid_height, valid_prediction_payload):
        """Test prediction with invalid height values (height must be 0 < h < 2.5)."""
        payload = valid_prediction_payload.copy()
        payload["height"] = invalid_height
        response = client.post("/predict", json=payload)
        assert response.status_code == 422

    @pytest.mark.validation
    @pytest.mark.parametrize("invalid_income", [-5, 0])
    def test_predict_invalid_income(self, client, invalid_income, valid_prediction_payload):
        """Test prediction with invalid income values (income must be > 0)."""
        payload = valid_prediction_payload.copy()
        payload["income_lpa"] = invalid_income
        response = client.post("/predict", json=payload)
        assert response.status_code == 422

    @pytest.mark.validation
    def test_predict_invalid_occupation(self, client, valid_prediction_payload):
        """Test prediction with invalid occupation type."""
        payload = valid_prediction_payload.copy()
        payload["occupation"] = "invalid_occupation"
        response = client.post("/predict", json=payload)
        assert response.status_code == 422

    @pytest.mark.validation
    def test_predict_invalid_smoker_type(self, client, valid_prediction_payload):
        """Test prediction with non-boolean smoker value."""
        payload = valid_prediction_payload.copy()
        payload["smoker"] = "yes"
        response = client.post("/predict", json=payload)
        assert response.status_code == 422

    @pytest.mark.validation
    def test_predict_invalid_city_type(self, client, valid_prediction_payload):
        """Test prediction with non-string city value."""
        payload = valid_prediction_payload.copy()
        payload["city"] = 123
        response = client.post("/predict", json=payload)
        assert response.status_code == 422


class TestEdgeCases:
    """Test suite for edge cases and boundary conditions."""
    
    @pytest.mark.edge_case
    def test_predict_minimum_valid_values(self, client):
        """Test prediction with minimum valid values."""
        payload = {
            "age": 1,
            "weight": 0.1,
            "height": 0.5,
            "income_lpa": 0.01,
            "smoker": False,
            "city": "Delhi",
            "occupation": "student"
        }
        response = client.post("/predict", json=payload)
        assert response.status_code == 200

    @pytest.mark.edge_case
    def test_predict_maximum_valid_values(self, client, valid_prediction_payload):
        """Test prediction with maximum valid values."""
        payload = valid_prediction_payload.copy()
        payload["age"] = 120
        payload["weight"] = 200.0
        payload["height"] = 2.4
        payload["income_lpa"] = 1000.0
        response = client.post("/predict", json=payload)
        assert response.status_code == 200

    @pytest.mark.edge_case
    def test_predict_bmi_normal_range(self, client):
        """Test prediction with normal BMI (18.5-24.9)."""
        payload = {
            "age": 30,
            "weight": 70.0,
            "height": 1.75,
            "income_lpa": 10.0,
            "smoker": False,
            "city": "Delhi",
            "occupation": "private_job"
        }
        response = client.post("/predict", json=payload)
        assert response.status_code == 200
        # BMI = 70 / (1.75^2) = 22.86 (normal)

    @pytest.mark.edge_case
    def test_predict_bmi_overweight_range(self, client):
        """Test prediction with overweight BMI (25-29.9)."""
        payload = {
            "age": 30,
            "weight": 90.0,
            "height": 1.75,
            "income_lpa": 10.0,
            "smoker": False,
            "city": "Delhi",
            "occupation": "private_job"
        }
        response = client.post("/predict", json=payload)
        assert response.status_code == 200
        # BMI = 90 / (1.75^2) = 29.39 (overweight)

    @pytest.mark.edge_case
    def test_predict_bmi_obese_range(self, client):
        """Test prediction with obese BMI (>= 30)."""
        payload = {
            "age": 30,
            "weight": 110.0,
            "height": 1.75,
            "income_lpa": 10.0,
            "smoker": False,
            "city": "Delhi",
            "occupation": "private_job"
        }
        response = client.post("/predict", json=payload)
        assert response.status_code == 200
        # BMI = 110 / (1.75^2) = 35.92 (obese)

    @pytest.mark.edge_case
    def test_predict_city_normalization(self, client, valid_prediction_payload):
        """Test that city names are normalized (title case)."""
        payload = valid_prediction_payload.copy()
        payload["city"] = "newdelhi"  # lowercase input
        response = client.post("/predict", json=payload)
        assert response.status_code == 200

    @pytest.mark.edge_case
    @pytest.mark.parametrize("city", ["Delhi", "MUMBAI", "bangalore", "Kolkata"])
    def test_predict_different_cities(self, client, city, valid_prediction_payload):
        """Test prediction with various city names in different cases."""
        payload = valid_prediction_payload.copy()
        payload["city"] = city
        response = client.post("/predict", json=payload)
        # Should succeed since city normalization is applied
        assert response.status_code == 200


class TestTypeValidation:
    """Test suite for type validation and type coercion."""
    
    def test_predict_age_as_string(self, client, valid_prediction_payload):
        """Test prediction with age as string instead of int."""
        payload = valid_prediction_payload.copy()
        payload["age"] = "35"
        # FastAPI may coerce this or reject it
        response = client.post("/predict", json=payload)
        assert response.status_code in [200, 422]

    def test_predict_weight_as_string(self, client, valid_prediction_payload):
        """Test prediction with weight as string instead of float."""
        payload = valid_prediction_payload.copy()
        payload["weight"] = "70.0"
        response = client.post("/predict", json=payload)
        assert response.status_code in [200, 422]

    def test_predict_extra_fields_ignored(self, client, valid_prediction_payload):
        """Test prediction with extra unexpected fields (should be ignored by Pydantic)."""
        payload = valid_prediction_payload.copy()
        payload["extra_field"] = "should be ignored"
        payload["another_field"] = 123
        response = client.post("/predict", json=payload)
        # Should still work, extra fields are ignored by Pydantic
        assert response.status_code == 200


class TestResponseConsistency:
    """Test suite to verify response consistency and data integrity."""
    
    @pytest.mark.integration
    def test_predict_deterministic_output(self, client, valid_prediction_payload):
        """Test that same input produces same output (deterministic)."""
        response1 = client.post("/predict", json=valid_prediction_payload)
        response2 = client.post("/predict", json=valid_prediction_payload)
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response1.json() == response2.json()

    @pytest.mark.integration
    def test_predict_probabilities_sum_to_one(self, client, valid_prediction_payload):
        """Test that predicted probabilities sum to approximately 1.0."""
        response = client.post("/predict", json=valid_prediction_payload)
        assert response.status_code == 200
        data = response.json()
        probabilities = data["class_probabilities"]
        total = sum(probabilities.values())
        assert 0.99 <= total <= 1.01, f"Probabilities should sum to ~1.0, got {total}"

    @pytest.mark.integration
    def test_predict_confidence_matches_max_probability(self, client, valid_prediction_payload):
        """Test that confidence matches the highest probability."""
        response = client.post("/predict", json=valid_prediction_payload)
        assert response.status_code == 200
        data = response.json()
        max_probability = max(data["class_probabilities"].values())
        assert abs(data["confidence"] - max_probability) < 0.001, \
            "Confidence should match max probability"

    @pytest.mark.integration
    def test_predict_category_in_probabilities(self, client, valid_prediction_payload):
        """Test that predicted category exists in class probabilities."""
        response = client.post("/predict", json=valid_prediction_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["predicted_category"] in data["class_probabilities"], \
            "Predicted category should exist in class_probabilities"
