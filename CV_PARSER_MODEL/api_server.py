from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
import uvicorn
import logging
from datetime import datetime
from pathlib import Path
import shutil
import os

from main import CV_parsing_main  # Import your function

app = FastAPI()

# CORS for Angular or other frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static for favicon
app.mount("/static", StaticFiles(directory="CV_PARSER_MODEL/static"), name="static")

@app.get("/favicon.ico")
def favicon():
    from fastapi.responses import FileResponse
    return FileResponse("CV_PARSER_MODEL/static/favicon.ico")

# Directory to save uploads
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/parse")
async def parse_file(file: UploadFile = File(...)):
    # Save the uploaded file
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    saved_filename = f"{timestamp}_{file.filename}"
    saved_path = UPLOAD_DIR / saved_filename

    with saved_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Call your parser
    result = CV_parsing_main(str(saved_path), save_results=False)
    if result is None:
        raise HTTPException(status_code=500, detail="Parsing failed")

    # Optionally, delete the file after parsing
    # saved_path.unlink()

    return JSONResponse(content=jsonable_encoder(result))

@app.post("/CV/upload")
async def upload_and_parse(file: UploadFile = File(...)):
    # Save the uploaded file
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    saved_filename = f"{timestamp}_{file.filename}"
    saved_path = UPLOAD_DIR / saved_filename

    with saved_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Call your parser
    result = CV_parsing_main(str(saved_path), save_results=False)
    if result is None:
        raise HTTPException(status_code=500, detail="Parsing failed")

    # Optionally, delete the file after parsing
    # saved_path.unlink()

    return JSONResponse(content=jsonable_encoder(result))

if __name__ == "__main__":
    import sys
    port = int(os.environ.get("CV_API_PORT", 8000))
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    uvicorn.run(app, host="0.0.0.0", port=port)