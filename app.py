from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from routes import router

app = FastAPI(
    title="BroForms",
    description="""OpenSource Forms application"""
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.get('/ping')
async def ping():
    return {
        'message': 'ping'
    }

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

app.include_router(router)
