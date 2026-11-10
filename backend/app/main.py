import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import config
from .routers import modulos, relatos, rpa, saude

logging.getLogger("citizentech").setLevel(logging.INFO)

app = FastAPI(title="CitizenTech API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,   # lista explícita, sem "*"
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["Content-Type"],
)
for r in (saude.router, relatos.router, rpa.router, modulos.router):
    app.include_router(r)
