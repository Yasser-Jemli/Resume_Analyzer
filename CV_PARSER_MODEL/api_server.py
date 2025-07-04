from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from main import CV_parsing_main  # Import your function

app = FastAPI()

# Mount the static directory
app.mount("/static", StaticFiles(directory="CV_PARSER_MODEL/static"), name="static")

@app.get("/favicon.ico")
def favicon():
    from fastapi.responses import FileResponse
    return FileResponse("CV_PARSER_MODEL/static/favicon.ico")

@app.get("/parse_cv")
def parse_cv(path: str = Query(..., description="Path to the resume PDF file")):
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    result = CV_parsing_main(path, save_results=False)
    print(type(result))
    print(result)
    if result is None:
        raise HTTPException(status_code=500, detail="Parsing failed")
    # Ensure result is JSON serializable
    return JSONResponse(content=jsonable_encoder(result))

if __name__ == "__main__":
    import sys
    port = int(os.environ.get("CV_API_PORT", 8000))
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    uvicorn.run(app, host="0.0.0.0", port=port)