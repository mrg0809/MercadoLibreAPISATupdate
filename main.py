"""
Main FastAPI application for Meli SAT Manager
"""
import os
from pathlib import Path
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from services import MeliClient, FileManager
from utils import logger, log_update, format_error_response, format_success_response

# Initialize FastAPI app
app = FastAPI(
    title="Meli SAT Manager",
    description="Sistema para gestionar información SAT de publicaciones de Mercado Libre",
    version="1.0.0"
)

# Setup templates
templates = Jinja2Templates(directory="templates")

# Setup static files if needed
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize clients
try:
    meli_client = MeliClient()
    file_manager = FileManager()
    logger.info("Meli SAT Manager initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize: {e}")
    raise


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Render the main page
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/download")
async def download_publications(format: str = "xlsx"):
    """
    Download all publications with SAT fields
    
    Args:
        format: File format (xlsx or csv)
    
    Returns:
        File download response
    """
    try:
        logger.info(f"Starting download process in {format} format")
        
        # Validate format
        if format not in ["xlsx", "csv"]:
            raise HTTPException(status_code=400, detail="Invalid format. Use 'xlsx' or 'csv'")
        
        # Get all item IDs
        logger.info("Fetching item IDs...")
        item_ids = meli_client.get_user_items()
        
        if not item_ids:
            raise HTTPException(status_code=404, detail="No items found for this user")
        
        logger.info(f"Found {len(item_ids)} items. Fetching details...")
        
        # Get details for all items
        items_details = meli_client.get_all_items_details(item_ids)
        
        if not items_details:
            raise HTTPException(status_code=500, detail="Failed to fetch item details")
        
        # Convert to DataFrame
        df = file_manager.items_to_dataframe(items_details)
        
        # Save to file
        filename = f"publicaciones_meli.{format}"
        filepath = os.path.join("/tmp", filename)
        
        if format == "xlsx":
            file_manager.save_to_excel(df, filepath)
        else:
            file_manager.save_to_csv(df, filepath)
        
        logger.info(f"File created successfully: {filepath}")
        
        # Return file download
        return FileResponse(
            path=filepath,
            filename=filename,
            media_type="application/octet-stream"
        )
    
    except PermissionError as e:
        logger.error(f"Permission error in download endpoint: {e}")
        raise HTTPException(status_code=403, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in download endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload")
async def upload_sat_fields(file: UploadFile = File(...)):
    """
    Upload and update SAT fields from CSV or XLSX file
    
    Args:
        file: Uploaded file (CSV or XLSX)
    
    Returns:
        JSON response with update results
    """
    try:
        logger.info(f"Received file upload: {file.filename}")
        
        # Validate file extension
        if not file.filename.endswith(('.csv', '.xlsx')):
            raise HTTPException(
                status_code=400,
                detail="Invalid file format. Please upload a CSV or XLSX file."
            )
        
        # Save uploaded file temporarily
        temp_path = os.path.join("/tmp", file.filename)
        
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        logger.info(f"File saved to {temp_path}")
        
        # Read the file
        df = file_manager.read_upload_file(temp_path)
        
        # Extract SAT updates
        updates = file_manager.extract_sat_updates(df)
        
        if not updates:
            raise HTTPException(
                status_code=400,
                detail="No valid updates found in the file. Please check the file format."
            )
        
        logger.info(f"Found {len(updates)} items to update")
        
        # Process updates
        results = {
            'total_processed': len(updates),
            'successful': 0,
            'failed': 0,
            'logs': []
        }
        
        for update in updates:
            item_id = update['item_id']
            sat_data = update['sat_data']
            
            try:
                # Update the item
                meli_client.update_item_sat_fields(item_id, sat_data)
                results['successful'] += 1
                log_entry = log_update(item_id, 'success', 'SAT fields updated')
                results['logs'].append(log_entry)
                
            except Exception as e:
                results['failed'] += 1
                error_msg = str(e)
                log_entry = log_update(item_id, 'error', error_msg)
                results['logs'].append(log_entry)
        
        # Clean up temp file
        try:
            os.remove(temp_path)
        except:
            pass
        
        logger.info(f"Update process completed. Successful: {results['successful']}, Failed: {results['failed']}")
        
        return format_success_response(
            message=f"Process completed. {results['successful']} items updated successfully, {results['failed']} failed.",
            data=results
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in upload endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "service": "Meli SAT Manager"}


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
