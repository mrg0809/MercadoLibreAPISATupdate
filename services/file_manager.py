"""
File Manager
Handles reading and writing CSV/XLSX files
"""
import json
import pandas as pd
from typing import List, Dict, Any
from utils import logger


class FileManager:
    """Manager for handling CSV and XLSX files"""
    
    @staticmethod
    def items_to_dataframe(items: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Convert list of items to a pandas DataFrame with required columns
        
        Args:
            items: List of item details from MercadoLibre API
        
        Returns:
            DataFrame with structured data
        """
        rows = []
        
        for item in items:
            # Extract basic fields
            row = {
                'id': item.get('id', ''),
                'title': item.get('title', ''),
                'category_id': item.get('category_id', ''),
                'brand': '',
                'atributos_completos': '',
                'seller_custom_field': item.get('seller_custom_field', ''),
                'ClaveProdServ': '',
                'ClaveUnidad': '',
                'Unidad_SAT': '',
                'Descripción_SAT': ''
            }
            
            # Extract brand from attributes
            attributes = item.get('attributes', [])
            if attributes:
                row['atributos_completos'] = json.dumps(attributes, ensure_ascii=False)
                
                for attr in attributes:
                    if attr.get('id') == 'BRAND':
                        row['brand'] = attr.get('value_name', '')
                    # Check if SAT fields are already set
                    elif attr.get('id') == 'GTIN':
                        row['ClaveProdServ'] = attr.get('value_name', '')
                    elif attr.get('id') == 'UNIT_MEASURE':
                        row['ClaveUnidad'] = attr.get('value_name', '')
                    elif attr.get('id') == 'SAT_UNIT':
                        row['Unidad_SAT'] = attr.get('value_name', '')
                    elif attr.get('id') == 'SAT_DESCRIPTION':
                        row['Descripción_SAT'] = attr.get('value_name', '')
            
            rows.append(row)
        
        df = pd.DataFrame(rows)
        return df
    
    @staticmethod
    def save_to_excel(df: pd.DataFrame, filename: str) -> str:
        """
        Save DataFrame to Excel file
        
        Args:
            df: DataFrame to save
            filename: Output filename
        
        Returns:
            Path to saved file
        """
        try:
            df.to_excel(filename, index=False, engine='openpyxl')
            logger.info(f"Saved {len(df)} items to {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error saving to Excel: {e}")
            raise
    
    @staticmethod
    def save_to_csv(df: pd.DataFrame, filename: str) -> str:
        """
        Save DataFrame to CSV file
        
        Args:
            df: DataFrame to save
            filename: Output filename
        
        Returns:
            Path to saved file
        """
        try:
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            logger.info(f"Saved {len(df)} items to {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
            raise
    
    @staticmethod
    def read_upload_file(file_path: str) -> pd.DataFrame:
        """
        Read uploaded CSV or XLSX file
        
        Args:
            file_path: Path to the file
        
        Returns:
            DataFrame with file contents
        """
        try:
            if file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path, engine='openpyxl')
            elif file_path.endswith('.csv'):
                df = pd.read_csv(file_path, encoding='utf-8-sig')
            else:
                raise ValueError("Unsupported file format. Use CSV or XLSX.")
            
            logger.info(f"Read {len(df)} rows from {file_path}")
            return df
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            raise
    
    @staticmethod
    def extract_sat_updates(df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Extract SAT field updates from DataFrame
        
        Args:
            df: DataFrame with item data
        
        Returns:
            List of dicts with item_id and SAT fields to update
        """
        updates = []
        
        required_columns = ['id', 'ClaveProdServ', 'ClaveUnidad', 'Unidad_SAT', 'Descripción_SAT']
        
        # Check if required columns exist
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
        
        for idx, row in df.iterrows():
            item_id = str(row.get('id', '')).strip()
            
            if not item_id:
                logger.warning(f"Skipping row {idx}: missing item ID")
                continue
            
            # Extract SAT fields
            sat_data = {
                'ClaveProdServ': str(row.get('ClaveProdServ', '')).strip(),
                'ClaveUnidad': str(row.get('ClaveUnidad', '')).strip(),
                'Unidad_SAT': str(row.get('Unidad_SAT', '')).strip(),
                'Descripción_SAT': str(row.get('Descripción_SAT', '')).strip()
            }
            
            # Check if there's any data to update
            has_data = any(val for val in sat_data.values())
            
            if has_data:
                updates.append({
                    'item_id': item_id,
                    'sat_data': sat_data
                })
            else:
                logger.info(f"Skipping item {item_id}: no SAT data to update")
        
        logger.info(f"Extracted {len(updates)} items to update")
        return updates
