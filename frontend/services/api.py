"""
API Service - Handles all HTTP requests to the FastAPI backend
"""
import os
import requests
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API base URL from environment
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


class APIClient:
    """Client for making requests to the FastAPI backend"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.token = None
    
    def set_token(self, token: str):
        """Set the JWT token for authenticated requests"""
        self.token = token
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers with authorization if token is set"""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    def _handle_response(self, response: requests.Response) -> Any:
        """Handle API response and raise exceptions for errors"""
        if response.status_code == 401:
            raise Exception("Não autorizado. Faça login novamente.")
        elif response.status_code == 404:
            raise Exception("Recurso não encontrado.")
        elif response.status_code == 400:
            error_detail = response.json().get("detail", "Erro na requisição")
            raise Exception(f"Erro: {error_detail}")
        elif response.status_code >= 500:
            raise Exception("Erro no servidor. Tente novamente mais tarde.")
        elif response.status_code >= 400:
            raise Exception(f"Erro: {response.status_code}")
        
        try:
            return response.json()
        except:
            return response.text
    
    # Health check
    def health_check(self) -> Dict:
        """Check if API is accessible"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return self._handle_response(response)
        except requests.exceptions.ConnectionError:
            raise Exception("Não foi possível conectar à API. Verifique se ela está rodando.")
        except requests.exceptions.Timeout:
            raise Exception("Timeout ao conectar à API.")
    
    # ===== CLIENTS =====
    
    def list_clients(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """List all clients"""
        response = requests.get(
            f"{self.base_url}/api/v1/clients",
            params={"skip": skip, "limit": limit},
            headers=self._get_headers()
        )
        return self._handle_response(response)
    
    def get_client(self, client_id: int) -> Dict:
        """Get a specific client by ID"""
        response = requests.get(
            f"{self.base_url}/api/v1/clients/{client_id}",
            headers=self._get_headers()
        )
        return self._handle_response(response)
    
    def create_client(self, client_data: Dict) -> Dict:
        """Create a new client"""
        response = requests.post(
            f"{self.base_url}/api/v1/clients",
            json=client_data,
            headers=self._get_headers()
        )
        return self._handle_response(response)
    
    def update_client(self, client_id: int, client_data: Dict) -> Dict:
        """Update a client"""
        response = requests.put(
            f"{self.base_url}/api/v1/clients/{client_id}",
            json=client_data,
            headers=self._get_headers()
        )
        return self._handle_response(response)
    
    def delete_client(self, client_id: int) -> Dict:
        """Delete a client"""
        response = requests.delete(
            f"{self.base_url}/api/v1/clients/{client_id}",
            headers=self._get_headers()
        )
        return self._handle_response(response)
    
    # ===== PRODUCTS =====
    
    def list_products(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """List all products"""
        response = requests.get(
            f"{self.base_url}/api/v1/products",
            params={"skip": skip, "limit": limit},
            headers=self._get_headers()
        )
        return self._handle_response(response)
    
    def get_product(self, product_id: int) -> Dict:
        """Get a specific product by ID"""
        response = requests.get(
            f"{self.base_url}/api/v1/products/{product_id}",
            headers=self._get_headers()
        )
        return self._handle_response(response)
    
    def create_product(self, product_data: Dict) -> Dict:
        """Create a new product"""
        response = requests.post(
            f"{self.base_url}/api/v1/products",
            json=product_data,
            headers=self._get_headers()
        )
        return self._handle_response(response)
    
    def update_product(self, product_id: int, product_data: Dict) -> Dict:
        """Update a product"""
        response = requests.put(
            f"{self.base_url}/api/v1/products/{product_id}",
            json=product_data,
            headers=self._get_headers()
        )
        return self._handle_response(response)
    
    def delete_product(self, product_id: int) -> Dict:
        """Delete a product"""
        response = requests.delete(
            f"{self.base_url}/api/v1/products/{product_id}",
            headers=self._get_headers()
        )
        return self._handle_response(response)
    
    # ===== SALES =====
    
    def list_sales(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """List all sales"""
        response = requests.get(
            f"{self.base_url}/api/v1/sales",
            params={"skip": skip, "limit": limit},
            headers=self._get_headers()
        )
        return self._handle_response(response)
    
    def get_sale(self, sale_id: int) -> Dict:
        """Get a specific sale by ID"""
        response = requests.get(
            f"{self.base_url}/api/v1/sales/{sale_id}",
            headers=self._get_headers()
        )
        return self._handle_response(response)
    
    def create_sale(self, sale_data: Dict) -> Dict:
        """Create a new sale"""
        response = requests.post(
            f"{self.base_url}/api/v1/sales",
            json=sale_data,
            headers=self._get_headers()
        )
        return self._handle_response(response)
    
    def cancel_sale(self, sale_id: int) -> Dict:
        """Cancel a sale"""
        response = requests.delete(
            f"{self.base_url}/api/v1/sales/{sale_id}",
            headers=self._get_headers()
        )
        return self._handle_response(response)
    
    # ===== SELLERS =====
    
    def list_sellers(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """List all sellers"""
        response = requests.get(
            f"{self.base_url}/api/v1/sellers",
            params={"skip": skip, "limit": limit},
            headers=self._get_headers()
        )
        return self._handle_response(response)


# Global API client instance
api_client = APIClient()
