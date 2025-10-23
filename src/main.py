from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
from pathlib import Path

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

    output_path = BASE_DIR / "static" / "output.png"

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "input_image": f"/static/{file.filename}", "output_image": "/static/output.png"},
    )

@app.get("/health")
def health():
    return {"status": "ok"}
