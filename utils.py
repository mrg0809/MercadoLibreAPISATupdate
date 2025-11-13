"""
Utility functions for the Meli SAT Manager
"""
import logging
from datetime import datetime
from typing import Any, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('meli_sat_manager.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def log_update(item_id: str, status: str, message: str = "") -> Dict[str, Any]:
    """
    Log an update operation
    
    Args:
        item_id: MercadoLibre item ID
        status: Status of the update (success, error, skipped)
        message: Additional message
    
    Returns:
        Dict with log information
    """
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'item_id': item_id,
        'status': status,
        'message': message
    }
    
    if status == 'success':
        logger.info(f"Item {item_id}: {status} - {message}")
    elif status == 'error':
        logger.error(f"Item {item_id}: {status} - {message}")
    else:
        logger.warning(f"Item {item_id}: {status} - {message}")
    
    return log_entry


def validate_sat_fields(row: Dict[str, Any]) -> bool:
    """
    Validate that required SAT fields exist in the row
    
    Args:
        row: Dictionary with item data
    
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['id', 'ClaveProdServ', 'ClaveUnidad', 'Unidad_SAT', 'Descripción_SAT']
    return all(field in row for field in required_fields)


def format_error_response(error: Exception) -> Dict[str, Any]:
    """
    Format error response
    
    Args:
        error: Exception object
    
    Returns:
        Dict with error information
    """
    return {
        'success': False,
        'error': str(error),
        'type': type(error).__name__
    }


def format_success_response(message: str, data: Any = None) -> Dict[str, Any]:
    """
    Format success response
    
    Args:
        message: Success message
        data: Optional data to include
    
    Returns:
        Dict with success information
    """
    response = {
        'success': True,
        'message': message
    }
    
    if data is not None:
        response['data'] = data
    
    return response
