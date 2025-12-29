"""
Analytics Service - Foundation for Consulting Upsell
Provides data analysis and insights for business consulting
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.models.models import Sale, SaleItem, Product, Cost, Client
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, List, Any


class AnalyticsService:
    """Service for business analytics and insights"""
    
    def __init__(self, db: Session, client_id: str):
        self.db = db
        self.client_id = client_id
    
    def get_sales_summary(self, start_date: datetime = None, end_date: datetime = None) -> Dict[str, Any]:
        """Get sales summary for a period"""
        query = self.db.query(Sale).filter(Sale.client_id == self.client_id)
        
        if start_date:
            query = query.filter(Sale.sale_date >= start_date)
        if end_date:
            query = query.filter(Sale.sale_date <= end_date)
        
        sales = query.all()
        
        total_revenue = sum(sale.final_amount for sale in sales)
        total_sales = len(sales)
        avg_ticket = total_revenue / total_sales if total_sales > 0 else 0
        
        return {
            "total_revenue": total_revenue,
            "total_sales": total_sales,
            "average_ticket": avg_ticket,
            "period_start": start_date,
            "period_end": end_date
        }
    
    def get_top_products(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top-selling products"""
        results = self.db.query(
            Product.id,
            Product.name,
            func.sum(SaleItem.quantity).label('total_quantity'),
            func.sum(SaleItem.subtotal).label('total_revenue')
        ).join(
            SaleItem, Product.id == SaleItem.product_id
        ).filter(
            Product.client_id == self.client_id
        ).group_by(
            Product.id, Product.name
        ).order_by(
            func.sum(SaleItem.subtotal).desc()
        ).limit(limit).all()
        
        return [
            {
                "product_id": r.id,
                "product_name": r.name,
                "total_quantity": r.total_quantity,
                "total_revenue": float(r.total_revenue)
            }
            for r in results
        ]
    
    def get_profitability_analysis(self) -> Dict[str, Any]:
        """Analyze business profitability"""
        # Get total revenue from sales
        sales_query = self.db.query(
            func.sum(Sale.final_amount).label('total_revenue')
        ).filter(Sale.client_id == self.client_id).first()
        
        total_revenue = float(sales_query.total_revenue) if sales_query.total_revenue else 0
        
        # Get total costs
        costs_query = self.db.query(
            func.sum(Cost.amount).label('total_costs')
        ).filter(Cost.client_id == self.client_id).first()
        
        total_costs = float(costs_query.total_costs) if costs_query.total_costs else 0
        
        # Get product costs from sales
        product_costs_query = self.db.query(
            func.sum(SaleItem.quantity * Product.cost_price).label('cogs')
        ).join(
            Product, SaleItem.product_id == Product.id
        ).filter(
            Product.client_id == self.client_id
        ).first()
        
        cogs = float(product_costs_query.cogs) if product_costs_query.cogs else 0
        
        gross_profit = total_revenue - cogs
        net_profit = gross_profit - total_costs
        
        gross_margin = (gross_profit / total_revenue * 100) if total_revenue > 0 else 0
        net_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        return {
            "total_revenue": total_revenue,
            "cost_of_goods_sold": cogs,
            "gross_profit": gross_profit,
            "gross_margin_percent": gross_margin,
            "operational_costs": total_costs,
            "net_profit": net_profit,
            "net_margin_percent": net_margin
        }
    
    def get_monthly_trends(self, months: int = 12) -> List[Dict[str, Any]]:
        """Get monthly sales trends"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)
        
        results = self.db.query(
            extract('year', Sale.sale_date).label('year'),
            extract('month', Sale.sale_date).label('month'),
            func.count(Sale.id).label('total_sales'),
            func.sum(Sale.final_amount).label('total_revenue')
        ).filter(
            Sale.client_id == self.client_id,
            Sale.sale_date >= start_date,
            Sale.sale_date <= end_date
        ).group_by(
            'year', 'month'
        ).order_by(
            'year', 'month'
        ).all()
        
        return [
            {
                "year": int(r.year),
                "month": int(r.month),
                "total_sales": r.total_sales,
                "total_revenue": float(r.total_revenue)
            }
            for r in results
        ]
    
    def get_inventory_alerts(self) -> List[Dict[str, Any]]:
        """Get products with low stock"""
        products = self.db.query(Product).filter(
            Product.client_id == self.client_id,
            Product.stock_quantity <= Product.min_stock
        ).all()
        
        return [
            {
                "product_id": p.id,
                "product_name": p.name,
                "current_stock": p.stock_quantity,
                "min_stock": p.min_stock,
                "status": "critical" if p.stock_quantity == 0 else "low"
            }
            for p in products
        ]
    
    def get_customer_analysis(self) -> List[Dict[str, Any]]:
        """Analyze customer purchase behavior"""
        results = self.db.query(
            Client.id,
            Client.name,
            func.count(Sale.id).label('total_purchases'),
            func.sum(Sale.final_amount).label('total_spent'),
            func.avg(Sale.final_amount).label('avg_purchase')
        ).join(
            Sale, Client.id == Sale.customer_id
        ).filter(
            Client.client_id == self.client_id
        ).group_by(
            Client.id, Client.name
        ).order_by(
            func.sum(Sale.final_amount).desc()
        ).limit(20).all()
        
        return [
            {
                "customer_id": r.id,
                "customer_name": r.name,
                "total_purchases": r.total_purchases,
                "total_spent": float(r.total_spent),
                "average_purchase": float(r.avg_purchase)
            }
            for r in results
        ]
