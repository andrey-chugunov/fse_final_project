from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import shutil


import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from model_inference import get_output

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/", response_class=HTMLResponse)
def form_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload", response_class=HTMLResponse)
async def upload_image(request: Request, file: UploadFile = File(...)):
    input_path = BASE_DIR / "static" / file.filename
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_dir = BASE_DIR / "static" / "results"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"output_{file.filename}"

    get_output(str(input_path), str(output_path))

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "input_image": f"/static/{file.filename}",
            "output_image": f"/static/results/output_{file.filename}",
        },
    )


@app.get("/health")
def health():
    return {"status": "ok"}
