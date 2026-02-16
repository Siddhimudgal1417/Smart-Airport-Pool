from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api.routes import router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(router)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/smart-matching")
async def smart_matching(request: Request):
    return templates.TemplateResponse("smart-matching.html", {"request": request})

@app.get("/real-time-updates")
async def real_time_updates(request: Request):
    return templates.TemplateResponse("real-time-updates.html", {"request": request})

@app.get("/safe-reliable")
async def safe_reliable(request: Request):
    return templates.TemplateResponse("safe-reliable.html", {"request": request})

@app.get("/health")
async def health():
    return {"status": "OK"}
