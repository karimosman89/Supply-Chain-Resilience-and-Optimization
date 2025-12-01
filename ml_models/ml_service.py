"""
ML Models Service
FastAPI service for serving machine learning models

Author: MiniMax Agent
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
import asyncio
from typing import Dict, Any, Optional
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Supply Chain ML Models Service",
    description="Service for serving ML models for demand forecasting, risk prediction, and optimization",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API requests/responses
class PredictionRequest(BaseModel):
    """Request model for predictions"""
    features: Dict[str, Any]
    model_type: str
    return_probability: bool = False

class PredictionResponse(BaseModel):
    """Response model for predictions"""
    prediction: Any
    confidence: Optional[float] = None
    model_version: str
    prediction_time: str
    processing_time_ms: float

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: str
    services: Dict[str, str]

# Mock ML models registry
MODEL_REGISTRY = {
    "demand_forecasting": {
        "version": "1.0.0",
        "status": "ready",
        "description": "Demand forecasting model"
    },
    "risk_prediction": {
        "version": "1.0.0", 
        "status": "ready",
        "description": "Risk prediction model"
    },
    "route_optimization": {
        "version": "1.0.0",
        "status": "ready", 
        "description": "Route optimization model"
    }
}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Supply Chain ML Models Service",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.utcnow().isoformat(),
        services={
            "demand_forecasting": "ready",
            "risk_prediction": "ready",
            "route_optimization": "ready"
        }
    )

@app.get("/models", response_model=Dict[str, Dict[str, Any]])
async def list_models():
    """List available ML models"""
    return MODEL_REGISTRY

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Make a prediction using the specified model
    """
    start_time = asyncio.get_event_loop().time()
    
    try:
        # Validate model type
        if request.model_type not in MODEL_REGISTRY:
            raise HTTPException(
                status_code=400,
                detail=f"Model type '{request.model_type}' not supported. Available: {list(MODEL_REGISTRY.keys())}"
            )
        
        # Simulate model prediction (replace with actual ML model inference)
        await asyncio.sleep(0.1)  # Simulate processing time
        
        # Mock prediction logic based on model type
        prediction = None
        if request.model_type == "demand_forecasting":
            prediction = {
                "forecasted_demand": request.features.get("base_demand", 100) * 1.1,
                "confidence_interval": [90, 110],
                "seasonal_factor": 1.05
            }
        elif request.model_type == "risk_prediction":
            prediction = {
                "risk_score": min(100, max(0, request.features.get("supplier_risk", 50))),
                "risk_level": "medium" if request.features.get("supplier_risk", 50) < 70 else "high",
                "top_risks": ["delivery_delay", "quality_issues"]
            }
        elif request.model_type == "route_optimization":
            prediction = {
                "optimal_route": ["warehouse", "customer1", "customer2", "warehouse"],
                "total_distance": request.features.get("base_distance", 100) * 0.9,
                "cost_savings": 15.0
            }
        
        # Calculate processing time
        processing_time = (asyncio.get_event_loop().time() - start_time) * 1000
        
        return PredictionResponse(
            prediction=prediction,
            confidence=0.85,
            model_version=MODEL_REGISTRY[request.model_type]["version"],
            prediction_time=datetime.utcnow().isoformat(),
            processing_time_ms=round(processing_time, 2)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/metrics")
async def get_metrics():
    """Get service metrics"""
    return {
        "total_predictions": 1250,
        "average_response_time_ms": 45.2,
        "models_served": len(MODEL_REGISTRY),
        "uptime_seconds": 3600,
        "last_prediction": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    port = int(os.getenv("MODEL_SERVING_PORT", 8001))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting ML Models Service on {host}:{port}")
    
    uvicorn.run(
        "ml_service:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )
