from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
import tempfile
import os
import logging

from processor import load_document
from vector_store import load_vector_db
from extractor import extract_prescription_data
from validator import validate


app = FastAPI(
    title="Prescription Validation API",
    version="1.0.0"
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


DB_PATH = r"D:\Prescription_validation\policy_db"

try:
    vector_db = load_vector_db(DB_PATH)
    logger.info("✅ Policy vector DB loaded successfully")
except Exception as e:
    logger.error(f"❌ Failed to load vector DB: {str(e)}")
    raise e



@app.get("/health")
def health_check():
    return {"status": "ok"}



@app.post("/validate")
async def validate_prescription(file: UploadFile = File(...)):
    """
    Upload a prescription PDF and get validation result
    """

    try:

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            temp_file_path = tmp.name

        pres_doc = load_document(temp_file_path)

        pres_json = extract_prescription_data(pres_doc.page_content)
        policy_chunks = vector_db.similarity_search(pres_json, k=5)
        result = validate(pres_json, policy_chunks)

        response = {
            "decision": result.get("decision", "INSUFFICIENT_INFORMATION"),
            "reasons": result.get("reasons", []),
            "missing_information": result.get("missing_information", []),
            "matched_policy_points": result.get("matched_policy_points", [])
        }

        return JSONResponse(content=response)

    except Exception as e:
        logger.error(f"❌ Error during validation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Cleanup temp file
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)