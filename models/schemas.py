"""
Data Models and Schemas for Supply Chain Platform
Comprehensive data structures for enterprise operations

Author: MiniMax Agent
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from enum import Enum
from decimal import Decimal


# Enums for type safety
class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SupplierStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    UNDER_REVIEW = "under_review"
    SUSPENDED = "suspended"


class PredictionType(str, Enum):
    DEMAND = "demand"
    RISK = "risk"
    PRICE = "price"
    DELIVERY_TIME = "delivery_time"
    SUPPLIER_PERFORMANCE = "supplier_performance"


class ForecastHorizon(str, Enum):
    SHORT_TERM = "7_days"
    MEDIUM_TERM = "30_days"
    LONG_TERM = "90_days"
    STRATEGIC = "365_days"


# Base Response Schema
class APIResponse(BaseModel):
    """Standard API response format"""
    success: bool = True
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = None


# Health Check Schema
class HealthCheck(BaseModel):
    """Comprehensive health check response"""
    status: str
    timestamp: str
    version: str
    environment: str
    services: Dict[str, str]
    metrics: Dict[str, Any]
    uptime_percentage: Optional[float] = None


# User & Authentication Schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., regex=r'^[^@]+@[^@]+\.[^@]+$')
    full_name: Optional[str] = None
    role: str = Field(default="user")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    company: Optional[str] = None
    department: Optional[str] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Supply Chain Entity Schemas
class SupplierBase(BaseModel):
    """Supplier information schema"""
    name: str = Field(..., max_length=200)
    code: str = Field(..., max_length=50, description="Unique supplier code")
    country: str = Field(..., max_length=2, description="ISO country code")
    category: str = Field(..., max_length=100)
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0, le=5, description="Supplier rating 0-5")


class SupplierCreate(SupplierBase):
    """Create supplier with additional fields"""
    payment_terms: Optional[str] = None
    delivery_terms: Optional[str] = None
    risk_profile: Optional[RiskLevel] = RiskLevel.MEDIUM
    capabilities: Optional[List[str]] = None


class SupplierResponse(SupplierBase):
    """Supplier response with performance metrics"""
    id: int
    status: SupplierStatus
    performance_score: Optional[float] = Field(None, ge=0, le=100)
    reliability_score: Optional[float] = Field(None, ge=0, le=100)
    cost_competitiveness: Optional[float] = Field(None, ge=0, le=100)
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SupplierPerformance(BaseModel):
    """Supplier performance metrics"""
    supplier_id: int
    period: str
    on_time_delivery_rate: float = Field(..., ge=0, le=100)
    quality_score: float = Field(..., ge=0, le=100)
    cost_variance: float = Field(..., ge=0, le=100)
    response_time_hours: float = Field(..., ge=0)
    total_orders: int = Field(..., ge=0)
    completed_orders: int = Field(..., ge=0)
    cancelled_orders: int = Field(..., ge=0)
    defects_rate: float = Field(..., ge=0, le=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# Product & Inventory Schemas
class ProductBase(BaseModel):
    """Product information schema"""
    sku: str = Field(..., max_length=100, description="Stock Keeping Unit")
    name: str = Field(..., max_length=200)
    category: str = Field(..., max_length=100)
    description: Optional[str] = None
    unit_cost: Optional[Decimal] = Field(None, ge=0)
    supplier_id: Optional[int] = None
    lead_time_days: Optional[int] = Field(None, ge=0)
    minimum_stock: Optional[int] = Field(None, ge=0)
    maximum_stock: Optional[int] = Field(None, ge=0)


class ProductResponse(ProductBase):
    """Product response with inventory metrics"""
    id: int
    current_stock: int = Field(..., ge=0)
    reserved_stock: int = Field(..., ge=0)
    available_stock: int = Field(..., ge=0)
    stock_value: Optional[Decimal] = Field(None, ge=0)
    turnover_rate: Optional[float] = Field(None, ge=0)
    last_updated: datetime
    
    class Config:
        from_attributes = True


# Demand Forecasting Schemas
class DemandForecastRequest(BaseModel):
    """Demand forecasting request"""
    product_sku: str
    forecast_horizon: ForecastHorizon = ForecastHorizon.MEDIUM_TERM
    include_seasonality: bool = True
    include_promotions: bool = True
    include_external_factors: bool = True
    confidence_level: float = Field(0.95, ge=0.80, le=0.99)


class DemandForecastResponse(BaseModel):
    """Demand forecasting response with confidence intervals"""
    product_sku: str
    forecast_period: str
    horizon_days: int
    predictions: List[Dict[str, Any]] = Field(..., description="Daily predictions")
    total_forecasted_demand: float
    confidence_interval_lower: List[float]
    confidence_interval_upper: List[float]
    accuracy_score: Optional[float] = Field(None, ge=0, le=1)
    model_used: str
    factors_influencing_forecast: List[str]
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class HistoricalDemand(BaseModel):
    """Historical demand data for training"""
    product_sku: str
    date: date
    quantity_sold: int = Field(..., ge=0)
    unit_price: Optional[Decimal] = Field(None, ge=0)
    promotion_applied: bool = False
    seasonality_factor: Optional[float] = Field(None, ge=0, le=2)
    external_factors: Optional[Dict[str, Any]] = None


# Risk Management Schemas
class RiskAssessmentRequest(BaseModel):
    """Risk assessment request"""
    scope: str = Field(..., description="Assessment scope: 'supplier', 'product', 'supply_chain'")
    entity_id: Optional[int] = None
    risk_factors: List[str] = Field(default_factory=lambda: [
        "geopolitical", "financial", "operational", "environmental", "regulatory"
    ])
    scenario_analysis: bool = True
    time_horizon_days: int = Field(30, ge=1, le=365)


class RiskAssessmentResponse(BaseModel):
    """Risk assessment response"""
    entity_id: int
    overall_risk_score: float = Field(..., ge=0, le=100)
    risk_level: RiskLevel
    risk_factors: Dict[str, float]
    top_risks: List[Dict[str, Any]]
    mitigation_strategies: List[str]
    scenario_impacts: Optional[Dict[str, Any]] = None
    recommended_actions: List[str]
    assessment_date: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime


class SupplyChainDisruption(BaseModel):
    """Supply chain disruption event"""
    id: Optional[int]
    event_type: str = Field(..., max_length=100)
    severity: RiskLevel
    affected_suppliers: List[int]
    affected_products: List[str]
    estimated_impact: Dict[str, Any]
    detection_time: datetime
    resolution_time: Optional[datetime] = None
    status: str = Field(default="active", max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# Logistics & Optimization Schemas
class RouteOptimizationRequest(BaseModel):
    """Route optimization request"""
    origin: Dict[str, float] = Field(..., description="Latitude, longitude")
    destinations: List[Dict[str, Any]] = Field(..., min_items=1)
    vehicle_capacity: float = Field(..., gt=0)
    constraints: Optional[Dict[str, Any]] = None
    optimization_objective: str = Field(default="cost", max_length=50)


class RouteOptimizationResponse(BaseModel):
    """Route optimization response"""
    route_id: str
    total_distance: float
    total_cost: float
    estimated_duration: float
    optimized_route: List[Dict[str, Any]]
    fuel_savings: Optional[float] = None
    time_savings: Optional[float] = None
    carbon_reduction: Optional[float] = None
    optimization_score: float = Field(..., ge=0, le=100)
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class WarehouseOptimization(BaseModel):
    """Warehouse optimization metrics"""
    warehouse_id: int
    utilization_rate: float = Field(..., ge=0, le=100)
    picking_efficiency: float = Field(..., ge=0, le=100)
    storage_density: float = Field(..., ge=0, le=100)
    order_accuracy: float = Field(..., ge=0, le=100)
    throughput_per_hour: int = Field(..., ge=0)
    cost_per_unit: float = Field(..., ge=0)
    recommendations: List[str]
    optimization_potential: float = Field(..., ge=0, le=100)


# Analytics & Reporting Schemas
class KPIMetrics(BaseModel):
    """Key Performance Indicators"""
    period: str
    financial_metrics: Dict[str, float]
    operational_metrics: Dict[str, float]
    quality_metrics: Dict[str, float]
    sustainability_metrics: Dict[str, float]
    risk_metrics: Dict[str, float]
    benchmark_comparison: Optional[Dict[str, Any]] = None
    trend_analysis: Dict[str, str]
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class ExecutiveSummary(BaseModel):
    """Executive summary report"""
    period: str
    overview: Dict[str, Any]
    key_achievements: List[str]
    challenges: List[str]
    recommendations: List[str]
    financial_impact: Dict[str, Any]
    risk_overview: Dict[str, Any]
    next_period_goals: List[str]
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class ReportRequest(BaseModel):
    """Report generation request"""
    report_type: str = Field(..., max_length=100)
    parameters: Dict[str, Any]
    format: str = Field(default="pdf", max_length=20)
    include_charts: bool = True
    executive_summary: bool = True
    scheduled_delivery: Optional[datetime] = None


# Real-time Data Schemas
class RealTimeMetric(BaseModel):
    """Real-time metric for dashboard"""
    metric_name: str
    value: float
    unit: str
    timestamp: datetime
    trend: str = Field(..., max_length=20, description="up, down, stable")
    threshold_warning: Optional[float] = None
    threshold_critical: Optional[float] = None


class Alert(BaseModel):
    """System alert"""
    id: Optional[int]
    type: str = Field(..., max_length=50)
    severity: RiskLevel
    title: str = Field(..., max_length=200)
    description: str
    affected_systems: List[str]
    recommended_actions: List[str]
    acknowledged: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None


print("✅ Data schemas loaded successfully")