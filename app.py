from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="BroForms",
    description="""OpenSource Forms application"""
)

@app.get('/')
async def ping():
    return {
        'message': 'ping'
    }

app.include_router(router)
