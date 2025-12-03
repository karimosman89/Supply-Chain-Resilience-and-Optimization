from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Date, Boolean, Text, 
    Enum, JSON, ForeignKey, Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from datetime import datetime

# Robust import for numeric types (SQLAlchemy 1.4+ and 2.0+)
try:
    from sqlalchemy import Numeric
except ImportError:
    from sqlalchemy.types import Numeric

Base = declarative_base()


class RiskLevel(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SupplierStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    UNDER_REVIEW = "under_review"
    SUSPENDED = "suspended"


class User(Base):
    """User management for multi-tenant access"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255))
    hashed_password = Column(String(255), nullable=False)
    company = Column(String(255))
    department = Column(String(100))
    role = Column(String(50), default="user")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    last_login = Column(DateTime)
    
    # Relationships
    audit_logs = relationship("AuditLog", back_populates="user")


class Supplier(Base):
    """Supplier master data with performance tracking"""
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    country = Column(String(2), nullable=False)  # ISO country code
    category = Column(String(100), nullable=False)
    contact_email = Column(String(255))
    contact_phone = Column(String(50))
    rating = Column(Float)  # 0-5 scale
    
    @property
    def email(self):
        """Backward compatibility property for email attribute"""
        return self.contact_email
    
    @property
    def location(self):
        """Backward compatibility property for location attribute"""
        return self.country
    
    # Performance metrics
    performance_score = Column(Float)  # 0-100 scale
    reliability_score = Column(Float)  # 0-100 scale
    cost_competitiveness = Column(Float)  # 0-100 scale
    on_time_delivery_rate = Column(Float)  # Percentage
    quality_score = Column(Float)  # 0-100 scale
    
    # Business information
    payment_terms = Column(String(100))
    delivery_terms = Column(String(100))
    risk_profile = Column(Enum(RiskLevel), default=RiskLevel.MEDIUM)
    status = Column(Enum(SupplierStatus), default=SupplierStatus.ACTIVE)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    products = relationship("Product", back_populates="supplier")
    performance_records = relationship("SupplierPerformance", back_populates="supplier")


class SupplierPerformance(Base):
    """Historical supplier performance data"""
    __tablename__ = "supplier_performance"
    
    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False, index=True)
    period = Column(String(20), nullable=False)  # e.g., "2025-01", "Q1-2025"
    
    # Performance metrics
    on_time_delivery_rate = Column(Float, nullable=False)  # Percentage
    quality_score = Column(Float, nullable=False)  # 0-100 scale
    cost_variance = Column(Float, nullable=False)  # Percentage
    response_time_hours = Column(Float, nullable=False)
    
    # Order statistics
    total_orders = Column(Integer, default=0)
    completed_orders = Column(Integer, default=0)
    cancelled_orders = Column(Integer, default=0)
    defects_rate = Column(Float, default=0.0)  # Percentage
    
    # Calculated metrics
    overall_score = Column(Float)  # Composite score 0-100
    
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    supplier = relationship("Supplier", back_populates="performance_records")
    
    # Indexes
    __table_args__ = (
        Index('idx_supplier_performance_supplier_period', 'supplier_id', 'period'),
    )


class Product(Base):
    """Product master data with inventory tracking"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text)
    unit_cost = Column(Numeric(10, 2))
    
    # Supply chain information
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    lead_time_days = Column(Integer, default=0)
    minimum_stock = Column(Integer, default=0)
    maximum_stock = Column(Integer, default=0)
    
    # Current inventory
    current_stock = Column(Integer, default=0)
    reserved_stock = Column(Integer, default=0)
    
    # Calculated fields
    available_stock = Column(Integer, default=0)
    stock_value = Column(Numeric(12, 2))
    turnover_rate = Column(Float)
    
    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    @property
    def status(self):
        """Backward compatibility property for status attribute"""
        return "active" if self.is_active else "inactive"
    # Relationships
    supplier = relationship("Supplier", back_populates="products")
    demand_history = relationship("HistoricalDemand", back_populates="product")
    
    # Indexes
    __table_args__ = (
        Index('idx_product_category', 'category'),
        Index('idx_product_supplier', 'supplier_id'),
    )


class HistoricalDemand(Base):
    """Historical demand data for ML training"""
    __tablename__ = "historical_demand"
    
    id = Column(Integer, primary_key=True, index=True)
    product_sku = Column(String(100), ForeignKey("products.sku"), nullable=False, index=True)
    date = Column(Date, nullable=False)
    
    # Demand data
    quantity_sold = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2))
    
    # Contextual factors
    promotion_applied = Column(Boolean, default=False)
    seasonality_factor = Column(Float, default=1.0)
    external_factors = Column(JSON)  # Weather, events, etc.
    
    # Quality metrics
    is_forecast_data = Column(Boolean, default=False)  # True if this is forecasted data
    
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    product = relationship("Product", back_populates="demand_history")
    
    # Indexes
    __table_args__ = (
        Index('idx_demand_product_date', 'product_sku', 'date'),
        Index('idx_demand_date', 'date'),
    )


class DemandForecast(Base):
    """ML-generated demand forecasts"""
    __tablename__ = "demand_forecasts"
    
    id = Column(Integer, primary_key=True, index=True)
    product_sku = Column(String(100), ForeignKey("products.sku"), nullable=False, index=True)
    forecast_date = Column(Date, nullable=False)
    horizon_days = Column(Integer, nullable=False)
    
    # Forecast data
    forecasted_demand = Column(Float, nullable=False)
    confidence_lower = Column(Float)
    confidence_upper = Column(Float)
    accuracy_score = Column(Float)  # Historical accuracy if available
    
    # Model information
    model_version = Column(String(50), nullable=False)
    factors_used = Column(JSON)  # Features used in prediction
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_forecast_product_date', 'product_sku', 'forecast_date'),
    )


class RiskAssessment(Base):
    """Risk assessments for various entities"""
    __tablename__ = "risk_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String(50), nullable=False)  # supplier, product, supply_chain
    entity_id = Column(Integer, nullable=False)
    
    # Risk metrics
    overall_risk_score = Column(Float, nullable=False)  # 0-100 scale
    risk_level = Column(Enum(RiskLevel), nullable=False)
    risk_factors = Column(JSON)  # Detailed breakdown by factor
    
    # Top risks and mitigation
    top_risks = Column(JSON)  # List of top risks with details
    mitigation_strategies = Column(JSON)  # Recommended strategies
    recommended_actions = Column(JSON)  # Immediate actions
    
    # Scenario analysis
    scenario_impacts = Column(JSON)  # What-if scenarios
    
    # Validity
    assessment_date = Column(DateTime, default=func.now())
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Indexes
    __table_args__ = (
        Index('idx_risk_entity_type', 'entity_type'),
        Index('idx_risk_assessment_date', 'assessment_date'),
    )


class SupplyChainDisruption(Base):
    """Supply chain disruption events"""
    __tablename__ = "supply_chain_disruptions"
    
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(100), nullable=False)
    severity = Column(Enum(RiskLevel), nullable=False)
    
    # Impact scope
    affected_suppliers = Column(JSON)  # List of supplier IDs
    affected_products = Column(JSON)  # List of product SKUs
    estimated_impact = Column(JSON)  # Financial, operational impact
    
    # Timeline
    detection_time = Column(DateTime, nullable=False)
    resolution_time = Column(DateTime)
    status = Column(String(50), default="active")  # active, resolved, escalated
    
    # Response
    response_actions = Column(JSON)
    escalation_level = Column(Integer, default=1)
    
    created_at = Column(DateTime, default=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_disruption_status', 'status'),
        Index('idx_disruption_severity', 'severity'),
    )


class RouteOptimization(Base):
    """Route optimization results"""
    __tablename__ = "route_optimizations"
    
    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(String(100), unique=True, nullable=False, index=True)
    
    # Route details
    origin_lat = Column(Float, nullable=False)
    origin_lng = Column(Float, nullable=False)
    destinations = Column(JSON, nullable=False)  # List of destinations
    
    # Optimization results
    total_distance = Column(Float, nullable=False)  # Kilometers
    total_cost = Column(Float, nullable=False)
    estimated_duration = Column(Float, nullable=False)  # Hours
    
    # Benefits
    fuel_savings = Column(Float)
    time_savings = Column(Float)
    carbon_reduction = Column(Float)
    optimization_score = Column(Float)  # 0-100 scale
    
    # Metadata
    optimization_objective = Column(String(50), default="cost")
    model_version = Column(String(50))
    created_at = Column(DateTime, default=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_route_created', 'created_at'),
    )


class Warehouse(Base):
    """Warehouse master data"""
    __tablename__ = "warehouses"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(50), unique=True, nullable=False, index=True)
    
    # Location
    country = Column(String(2), nullable=False)
    city = Column(String(100), nullable=False)
    address = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Capacity and performance
    total_capacity = Column(Float)  # Square meters
    current_utilization = Column(Float)  # Percentage
    
    # Performance metrics
    picking_efficiency = Column(Float)  # Orders per hour
    storage_density = Column(Float)  # Units per square meter
    order_accuracy = Column(Float)  # Percentage
    throughput_per_hour = Column(Integer)
    cost_per_unit = Column(Float)
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class KPIMetrics(Base):
    """Key Performance Indicators tracking"""
    __tablename__ = "kpi_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    period = Column(String(20), nullable=False)  # e.g., "2025-01", "Q1-2025"
    
    # Financial metrics
    total_cost = Column(Float)
    cost_reduction_percentage = Column(Float)
    savings_achieved = Column(Float)
    
    # Operational metrics
    on_time_delivery_rate = Column(Float)
    inventory_turnover = Column(Float)
    supplier_performance_score = Column(Float)
    order_fulfillment_rate = Column(Float)
    
    # Quality metrics
    defect_rate = Column(Float)
    customer_satisfaction = Column(Float)
    quality_score = Column(Float)
    
    # Risk metrics
    risk_exposure = Column(Float)
    disruption_incidents = Column(Integer)
    risk_mitigation_effectiveness = Column(Float)
    
    # Sustainability
    carbon_footprint = Column(Float)
    waste_reduction = Column(Float)
    sustainability_score = Column(Float)
    
    # Trends and benchmarks
    trend_analysis = Column(JSON)
    benchmark_comparison = Column(JSON)
    
    created_at = Column(DateTime, default=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_kpi_period', 'period'),
    )


class AuditLog(Base):
    """System audit logging for compliance"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Action details
    action = Column(String(100), nullable=False)
    resource = Column(String(100), nullable=False)
    resource_id = Column(Integer)
    details = Column(JSON)
    
    # Request context
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    session_id = Column(String(100))
    
    # Result
    success = Column(Boolean, nullable=False)
    error_message = Column(Text)
    
    timestamp = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
    
    # Indexes
    __table_args__ = (
        Index('idx_audit_user', 'user_id'),
        Index('idx_audit_timestamp', 'timestamp'),
        Index('idx_audit_action', 'action'),
    )


class SystemAlert(Base):
    """System alerts and notifications"""
    __tablename__ = "system_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)
    severity = Column(Enum(RiskLevel), nullable=False)
    
    # Alert details
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    affected_systems = Column(JSON)
    recommended_actions = Column(JSON)
    
    # Status
    acknowledged = Column(Boolean, default=False)
    acknowledged_by = Column(Integer, ForeignKey("users.id"))
    acknowledged_at = Column(DateTime)
    
    # Lifecycle
    created_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime)
    resolved_at = Column(DateTime)
    
    # Relationships
    acknowledged_by_user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_alert_severity', 'severity'),
        Index('idx_alert_status', 'acknowledged'),
    )


print("✅ Database models loaded successfully")
