"""
Analytics API Endpoints
Real-time supply chain analytics and KPI tracking

Author: MiniMax Agent
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta, date
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc

# Local imports
from core.database import get_db
from models.schemas import (
    APIResponse, KPIMetrics, ExecutiveSummary, 
    RealTimeMetric, Alert, ReportRequest
)
from services.analytics_service import AnalyticsService
from services.alerting_service import AlertingService

router = APIRouter()

# Initialize services
analytics_service = AnalyticsService()
alerting_service = AlertingService()


@router.get("/dashboard", response_model=APIResponse)
async def get_dashboard_data(
    company_id: Optional[str] = Query(None, description="Company identifier for multi-tenant"),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive dashboard data with real-time metrics
    
    Returns:
    - Key performance indicators
    - Recent alerts
    - Trending metrics
    - Executive summary
    """
    try:
        dashboard_data = await analytics_service.get_dashboard_data(
            company_id=company_id,
            db=db
        )
        
        return APIResponse(
            success=True,
            message="Dashboard data retrieved successfully",
            data=dashboard_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve dashboard data: {str(e)}")


@router.get("/kpis", response_model=List[KPIMetrics])
async def get_kpi_metrics(
    period: Optional[str] = Query(None, description="Specific period (e.g., '2025-01', 'Q1-2025')"),
    start_date: Optional[date] = Query(None, description="Start date for custom range"),
    end_date: Optional[date] = Query(None, description="End date for custom range"),
    metrics: Optional[List[str]] = Query(None, description="Specific metrics to return"),
    db: Session = Depends(get_db)
):
    """
    Get Key Performance Indicators for supply chain operations
    
    Includes:
    - Financial metrics (cost reduction, savings)
    - Operational metrics (delivery rates, inventory turnover)
    - Quality metrics (defect rates, customer satisfaction)
    - Risk metrics (exposure, mitigation effectiveness)
    - Sustainability metrics (carbon footprint, waste reduction)
    """
    try:
        kpi_data = await analytics_service.get_kpi_metrics(
            period=period,
            start_date=start_date,
            end_date=end_date,
            metrics=metrics,
            db=db
        )
        
        return kpi_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve KPI metrics: {str(e)}")


@router.get("/trends", response_model=APIResponse)
async def get_trend_analysis(
    metric_name: str = Query(..., description="Metric to analyze trends for"),
    time_period: str = Query("30d", description="Time period: 7d, 30d, 90d, 1y"),
    granularity: str = Query("daily", description="Data granularity: hourly, daily, weekly, monthly"),
    include_forecasting: bool = Query(True, description="Include future predictions"),
    db: Session = Depends(get_db)
):
    """
    Get trend analysis for any supply chain metric
    
    Supports forecasting with confidence intervals and seasonal analysis.
    """
    try:
        trend_data = await analytics_service.analyze_trends(
            metric_name=metric_name,
            time_period=time_period,
            granularity=granularity,
            include_forecasting=include_forecasting,
            db=db
        )
        
        return APIResponse(
            success=True,
            message="Trend analysis completed successfully",
            data=trend_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze trends: {str(e)}")


@router.get("/supplier-performance", response_model=APIResponse)
async def get_supplier_performance_analytics(
    period: Optional[str] = Query(None, description="Performance period"),
    supplier_ids: Optional[List[int]] = Query(None, description="Specific suppliers to analyze"),
    metrics: Optional[List[str]] = Query(None, description="Performance metrics to include"),
    include_benchmarking: bool = Query(True, description="Include industry benchmarks"),
    db: Session = Depends(get_db)
):
    """
    Comprehensive supplier performance analytics
    
    Features:
    - Multi-dimensional performance scoring
    - Benchmark comparisons
    - Trend analysis and forecasting
    - Risk identification
    - Cost optimization opportunities
    """
    try:
        performance_data = await analytics_service.get_supplier_performance_analytics(
            period=period,
            supplier_ids=supplier_ids,
            metrics=metrics,
            include_benchmarking=include_benchmarking,
            db=db
        )
        
        return APIResponse(
            success=True,
            message="Supplier performance analytics retrieved",
            data=performance_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get supplier analytics: {str(e)}")


@router.get("/inventory-optimization", response_model=APIResponse)
async def get_inventory_optimization_analytics(
    product_categories: Optional[List[str]] = Query(None, description="Product categories to analyze"),
    analysis_type: str = Query("comprehensive", description="Analysis type: basic, advanced, comprehensive"),
    include_predictions: bool = Query(True, description="Include demand predictions"),
    db: Session = Depends(get_db)
):
    """
    Inventory optimization analytics and recommendations
    
    Provides:
    - Current stock optimization levels
    - Reorder point recommendations
    - Safety stock calculations
    - Dead stock identification
    - Cost optimization strategies
    """
    try:
        optimization_data = await analytics_service.get_inventory_optimization_analytics(
            product_categories=product_categories,
            analysis_type=analysis_type,
            include_predictions=include_predictions,
            db=db
        )
        
        return APIResponse(
            success=True,
            message="Inventory optimization analytics retrieved",
            data=optimization_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get inventory analytics: {str(e)}")


@router.get("/logistics-efficiency", response_model=APIResponse)
async def get_logistics_efficiency_metrics(
    period: Optional[str] = Query(None, description="Analysis period"),
    route_optimizations: bool = Query(True, include_optimizations=True),
    warehouse_performance: bool = Query(True, include_warehouse_metrics=True),
    include_cost_analysis: bool = Query(True, description="Include cost breakdown"),
    db: Session = Depends(get_db)
):
    """
    Logistics efficiency and optimization metrics
    
    Covers:
    - Route optimization effectiveness
    - Warehouse utilization and efficiency
    - Transportation cost analysis
    - Delivery performance metrics
    - Carbon footprint tracking
    """
    try:
        logistics_data = await analytics_service.get_logistics_efficiency_metrics(
            period=period,
            route_optimizations=route_optimizations,
            warehouse_performance=warehouse_performance,
            include_cost_analysis=include_cost_analysis,
            db=db
        )
        
        return APIResponse(
            success=True,
            message="Logistics efficiency metrics retrieved",
            data=logistics_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get logistics analytics: {str(e)}")


@router.get("/risk-heatmap", response_model=APIResponse)
async def get_risk_heatmap_data(
    risk_categories: Optional[List[str]] = Query(None, description="Risk categories to include"),
    include_predictive: bool = Query(True, description="Include predictive risk scores"),
    time_horizon: int = Query(30, description="Risk assessment horizon in days"),
    db: Session = Depends(get_db)
):
    """
    Get risk heatmap data for visual representation
    
    Displays:
    - Risk levels across different categories
    - Geographic risk distribution
    - Supplier risk assessments
    - Predictive risk indicators
    """
    try:
        risk_data = await analytics_service.get_risk_heatmap_data(
            risk_categories=risk_categories,
            include_predictive=include_predictive,
            time_horizon=time_horizon,
            db=db
        )
        
        return APIResponse(
            success=True,
            message="Risk heatmap data retrieved",
            data=risk_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get risk heatmap: {str(e)}")


@router.get("/executive-summary", response_model=ExecutiveSummary)
async def get_executive_summary(
    period: Optional[str] = Query(None, description="Summary period"),
    include_recommendations: bool = Query(True, description="Include strategic recommendations"),
    include_forecasting: bool = Query(True, description="Include forward-looking insights"),
    db: Session = Depends(get_db)
):
    """
    Generate executive summary report
    
    Provides C-level insights with:
    - Performance overview
    - Key achievements and challenges
    - Financial impact analysis
    - Strategic recommendations
    - Forward-looking goals
    """
    try:
        summary = await analytics_service.generate_executive_summary(
            period=period,
            include_recommendations=include_recommendations,
            include_forecasting=include_forecasting,
            db=db
        )
        
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate executive summary: {str(e)}")


@router.get("/real-time-metrics", response_model=List[RealTimeMetric])
async def get_real_time_metrics(
    metric_types: Optional[List[str]] = Query(None, description="Types of metrics to return"),
    include_alerts: bool = Query(True, description="Include current alerts"),
    db: Session = Depends(get_db)
):
    """
    Get real-time metrics for dashboard widgets
    
    Returns live data for:
    - Inventory levels
    - Order processing status
    - Delivery tracking
    - System performance
    - Financial indicators
    """
    try:
        metrics = await analytics_service.get_real_time_metrics(
            metric_types=metric_types,
            db=db
        )
        
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get real-time metrics: {str(e)}")


@router.get("/benchmarking", response_model=APIResponse)
async def get_industry_benchmarking(
    metric_name: str = Query(..., description="Metric to benchmark"),
    industry_sector: Optional[str] = Query(None, description="Industry sector for comparison"),
    company_size: Optional[str] = Query(None, description="Company size category"),
    include_recommendations: bool = Query(True, description="Include improvement recommendations"),
    db: Session = Depends(get_db)
):
    """
    Industry benchmarking analysis
    
    Compares performance against industry standards and provides
    actionable insights for improvement.
    """
    try:
        benchmark_data = await analytics_service.get_industry_benchmarking(
            metric_name=metric_name,
            industry_sector=industry_sector,
            company_size=company_size,
            include_recommendations=include_recommendations,
            db=db
        )
        
        return APIResponse(
            success=True,
            message="Industry benchmarking completed",
            data=benchmark_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get benchmarking data: {str(e)}")


@router.post("/generate-report", response_model=APIResponse)
async def generate_custom_report(
    report_request: ReportRequest,
    db: Session = Depends(get_db)
):
    """
    Generate custom analytics reports
    
    Supports multiple formats:
    - PDF reports with charts
    - Excel spreadsheets
    - JSON data exports
    - PowerBI compatible datasets
    """
    try:
        report_data = await analytics_service.generate_custom_report(
            report_request=report_request,
            db=db
        )
        
        return APIResponse(
            success=True,
            message="Custom report generated successfully",
            data={
                "report_id": report_data.get("report_id"),
                "download_url": report_data.get("download_url"),
                "format": report_request.format,
                "generated_at": datetime.utcnow().isoformat()
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")


@router.get("/cost-analysis", response_model=APIResponse)
async def get_cost_analysis(
    period: Optional[str] = Query(None, description="Analysis period"),
    cost_categories: Optional[List[str]] = Query(None, description="Cost categories to analyze"),
    include_projections: bool = Query(True, description="Include cost projections"),
    breakdown_level: str = Query("summary", description="Detail level: summary, detailed, itemized"),
    db: Session = Depends(get_db)
):
    """
    Comprehensive cost analysis and optimization
    
    Provides:
    - Cost breakdown by category
    - Trend analysis and projections
    - Optimization opportunities
    - Budget variance analysis
    - Cost reduction strategies
    """
    try:
        cost_data = await analytics_service.get_cost_analysis(
            period=period,
            cost_categories=cost_categories,
            include_projections=include_projections,
            breakdown_level=breakdown_level,
            db=db
        )
        
        return APIResponse(
            success=True,
            message="Cost analysis completed",
            data=cost_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get cost analysis: {str(e)}")


@router.get("/sustainability-metrics", response_model=APIResponse)
async def get_sustainability_metrics(
    period: Optional[str] = Query(None, description="Analysis period"),
    include_trends: bool = Query(True, description="Include historical trends"),
    include_projections: bool = Query(True, description="Include future projections"),
    include_benchmarks: bool = Query(True, description="Include industry benchmarks"),
    db: Session = Depends(get_db)
):
    """
    Sustainability and ESG metrics tracking
    
    Covers:
    - Carbon footprint measurement
    - Waste reduction tracking
    - Energy efficiency metrics
    - Supplier sustainability scores
    - ESG compliance reporting
    """
    try:
        sustainability_data = await analytics_service.get_sustainability_metrics(
            period=period,
            include_trends=include_trends,
            include_projections=include_projections,
            include_benchmarks=include_benchmarks,
            db=db
        )
        
        return APIResponse(
            success=True,
            message="Sustainability metrics retrieved",
            data=sustainability_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get sustainability metrics: {str(e)}")


print("✅ Analytics API endpoints loaded successfully")