"""
Configuration Management for Supply Chain Platform
Centralized configuration with environment support

Author: MiniMax Agent
"""

from pydantic import BaseSettings, validator
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application settings with validation"""
    
    # Application
    APP_NAME: str = "Supply Chain Platform"
    VERSION: str = "2.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/supply_chain_db"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 30
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_DB: int = 0
    REDIS_TIMEOUT: int = 300
    
    # ML Model Configuration
    MODEL_CACHE_TTL: int = 3600  # 1 hour
    PREDICTION_BATCH_SIZE: int = 1000
    MAX_CONCURRENT_PREDICTIONS: int = 10
    
    # External APIs
    WEATHER_API_KEY: Optional[str] = None
    COMMODITY_API_KEY: Optional[str] = None
    GEOPOLITICAL_API_KEY: Optional[str] = None
    
    # Performance
    MAX_WORKERS: int = 4
    QUEUE_SIZE: int = 1000
    TIMEOUT_SECONDS: int = 30
    
    # Security
    SECURITY_HEADERS_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 100
    
    # Monitoring
    PROMETHEUS_ENABLED: bool = True
    HEALTH_CHECK_INTERVAL: int = 30
    
    # Business Metrics
    COST_SAVINGS_TARGET: float = 0.15  # 15% target
    EFFICIENCY_IMPROVEMENT_TARGET: float = 0.25  # 25% target
    RISK_REDUCTION_TARGET: float = 0.30  # 30% target
    
    @validator('ALLOWED_HOSTS', pre=True)
    def assemble_cors_origins(cls, v):
        """Parse CORS origins from string or list"""
        if isinstance(v, str) and v:
            return [i.strip() for i in v.split(',')]
        elif isinstance(v, list):
            return v
        else:
            return ["*"]
    
    @validator('DEBUG')
    def validate_debug_mode(cls, v):
        """Ensure debug is False in production"""
        if os.getenv('ENVIRONMENT') == 'production' and v:
            return False
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


# Environment-specific configurations
ENVIRONMENTS = {
    "development": {
        "DEBUG": True,
        "LOG_LEVEL": "DEBUG",
        "DATABASE_POOL_SIZE": 5
    },
    "staging": {
        "DEBUG": True,
        "LOG_LEVEL": "INFO",
        "DATABASE_POOL_SIZE": 10
    },
    "production": {
        "DEBUG": False,
        "LOG_LEVEL": "WARNING",
        "DATABASE_POOL_SIZE": 50,
        "PROMETHEUS_ENABLED": True
    }
}

# Feature flags for controlled rollouts
FEATURE_FLAGS = {
    "advanced_analytics": True,
    "real_time_processing": True,
    "ml_predictions": True,
    "blockchain_integration": False,
    "quantum_optimization": False,
    "iot_integration": True,
    "mobile_app": True,
    "multi_tenant": True,
    "audit_logging": True,
    "performance_monitoring": True
}

# Business KPIs and Targets
BUSINESS_METRICS = {
    "cost_reduction_target": 0.15,  # 15% cost reduction
    "efficiency_improvement": 0.25,  # 25% efficiency gain
    "risk_mitigation": 0.30,  # 30% risk reduction
    "forecast_accuracy": 0.95,  # 95% forecast accuracy
    "response_time_sla": 100,  # < 100ms response time
    "uptime_sla": 99.9,  # 99.9% uptime
    "customer_satisfaction": 4.8,  # 4.8/5.0 rating
    "roi_target": 3.5  # 3.5x ROI within 12 months
}

# API Rate Limits by Endpoint Type
RATE_LIMITS = {
    "analytics": "1000/hour",
    "forecasting": "500/hour", 
    "risk_assessment": "300/hour",
    "optimization": "100/hour",
    "reports": "50/hour",
    "bulk_operations": "10/hour"
}

# Data Retention Policies
DATA_RETENTION = {
    "operational_data": "2_years",
    "historical_analytics": "7_years", 
    "audit_logs": "7_years",
    "ml_training_data": "5_years",
    "user_sessions": "30_days",
    "temporary_files": "7_days"
}

print(f"✅ Configuration loaded for {settings.ENVIRONMENT} environment")