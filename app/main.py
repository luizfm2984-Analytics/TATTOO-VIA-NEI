from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import clients, products, sales, inventory, sellers, costs

app = FastAPI(
    title="Management App API",
    description="Sistema de gestão para consultoria e análise de negócios",
    version="0.1.0",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(clients.router, prefix="/api/v1/clients", tags=["Clients"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(sales.router, prefix="/api/v1/sales", tags=["Sales"])
app.include_router(inventory.router, prefix="/api/v1/inventory", tags=["Inventory"])
app.include_router(sellers.router, prefix="/api/v1/sellers", tags=["Sellers"])
app.include_router(costs.router, prefix="/api/v1/costs", tags=["Costs"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Management App API",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
