from fastapi import FastAPI
from routers import properties

app = FastAPI()
app.include_router(properties.router)