from pydantic import BaseModel, Field
from typing import Dict

class PredictionResponse(BaseModel):
    predicted_category: str = Field(..., description="The predicted insurance category for the user", examples=["low", "medium", "high"])
    confidence: float = Field(..., description="The confidence score of the prediction (between 0 and 1)", examples=[0.85])
    class_probabilities: Dict[str, float] = Field(..., description="A dictionary mapping each insurance category to its predicted probability", 
                                                  xamples={"low": 0.85, "medium": 0.10, "high": 0.05})