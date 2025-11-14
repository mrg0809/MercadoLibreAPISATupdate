"""
MercadoLibre API Client
Handles all interactions with the MercadoLibre API
"""
import os
import requests
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from utils import logger

# Load environment variables
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
USER_ID = os.getenv("USER_ID")

# API Base URL
BASE_URL = "https://api.mercadolibre.com"


class MeliClient:
    """Client for MercadoLibre API operations"""
    
    def __init__(self):
        """Initialize the MercadoLibre client"""
        if not ACCESS_TOKEN or not USER_ID:
            raise ValueError("ACCESS_TOKEN and USER_ID must be set in .env file")
        
        self.access_token = ACCESS_TOKEN
        self.user_id = USER_ID
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def validate_token(self) -> bool:
        """
        Validate the access token by making a test request
        
        Returns:
            True if token is valid, False otherwise
        """
        try:
            url = f"{BASE_URL}/users/me"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Token validation failed: {e}")
            return False
    
    def get_user_items(self) -> List[str]:
        """
        Get all item IDs for the user
        
        Returns:
            List of item IDs
            
        Raises:
            PermissionError: If the access token is invalid or doesn't have required permissions
            requests.exceptions.RequestException: For other API errors
        """
        try:
            url = f"{BASE_URL}/users/{self.user_id}/items/search"
            all_items = []
            offset = 0
            limit = 50
            
            while True:
                params = {
                    "offset": offset,
                    "limit": limit
                }
                
                response = requests.get(url, headers=self.headers, params=params, timeout=30)
                
                # Handle specific error cases
                if response.status_code == 403:
                    error_msg = (
                        "Access forbidden (403). Please check:\n"
                        "1. Your ACCESS_TOKEN is valid and not expired\n"
                        "2. The token has the required scopes (read, write, offline_access)\n"
                        "3. The USER_ID matches the authenticated user\n"
                        "You can generate a new token at: https://developers.mercadolibre.com/"
                    )
                    logger.error(error_msg)
                    raise PermissionError(error_msg)
                elif response.status_code == 401:
                    error_msg = (
                        "Authentication failed (401). Your ACCESS_TOKEN may be invalid or expired.\n"
                        "Please generate a new token at: https://developers.mercadolibre.com/"
                    )
                    logger.error(error_msg)
                    raise PermissionError(error_msg)
                
                response.raise_for_status()
                
                data = response.json()
                results = data.get("results", [])
                
                if not results:
                    break
                
                all_items.extend(results)
                logger.info(f"Retrieved {len(results)} items (offset: {offset})")
                
                # Check if there are more items
                paging = data.get("paging", {})
                total = paging.get("total", 0)
                
                if offset + limit >= total:
                    break
                
                offset += limit
            
            logger.info(f"Total items retrieved: {len(all_items)}")
            return all_items
        
        except PermissionError:
            # Re-raise PermissionError as-is
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting user items: {e}")
            raise
    
    def get_item_details(self, item_id: str) -> Dict[str, Any]:
        """
        Get detailed information for a specific item
        
        Args:
            item_id: MercadoLibre item ID
        
        Returns:
            Dict with item details
        """
        try:
            url = f"{BASE_URL}/items/{item_id}"
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            return response.json()
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting item details for {item_id}: {e}")
            raise
    
    def update_item_sat_fields(self, item_id: str, sat_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Update SAT fields for a specific item
        
        Args:
            item_id: MercadoLibre item ID
            sat_data: Dictionary with SAT field values
                - ClaveProdServ
                - ClaveUnidad
                - Unidad_SAT
                - Descripción_SAT
        
        Returns:
            Dict with update response
        """
        try:
            url = f"{BASE_URL}/items/{item_id}"
            
            # Build the attributes array for the update
            attributes = []
            
            # Map SAT fields to attribute structure
            sat_field_mapping = {
                "ClaveProdServ": "GTIN",  # This might need adjustment based on actual API
                "ClaveUnidad": "UNIT_MEASURE",
                "Unidad_SAT": "SAT_UNIT",
                "Descripción_SAT": "SAT_DESCRIPTION"
            }
            
            for field_name, field_value in sat_data.items():
                if field_value and str(field_value).strip():  # Only add non-empty values
                    attributes.append({
                        "id": sat_field_mapping.get(field_name, field_name),
                        "value_name": str(field_value).strip()
                    })
            
            # Prepare the update payload
            payload = {
                "attributes": attributes
            }
            
            # If seller_custom_field is provided, add it
            if 'seller_custom_field' in sat_data:
                payload['seller_custom_field'] = sat_data['seller_custom_field']
            
            response = requests.put(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            
            logger.info(f"Successfully updated item {item_id}")
            return response.json()
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error updating item {item_id}: {e}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response: {e.response.text}")
            raise
    
    def get_all_items_details(self, item_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Get details for all items
        
        Args:
            item_ids: List of item IDs
        
        Returns:
            List of item details
        """
        items_details = []
        total = len(item_ids)
        
        for idx, item_id in enumerate(item_ids, 1):
            try:
                logger.info(f"Processing item {idx}/{total}: {item_id}")
                details = self.get_item_details(item_id)
                items_details.append(details)
            except Exception as e:
                logger.error(f"Failed to get details for item {item_id}: {e}")
                # Continue with next item
        
        return items_details
