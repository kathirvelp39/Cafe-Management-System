from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from server.config.database import engine
from server.models import models
from server.routes import customers_routes, menu_routes, orders_routes, billing_routes, inventory_routes, employees_routes, reports_routes, reservations_routes, feedback_routes

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Monika G Cafe Management API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(customers_routes.router)
app.include_router(menu_routes.router)
app.include_router(orders_routes.router)
app.include_router(billing_routes.router)
app.include_router(inventory_routes.router)
app.include_router(employees_routes.router)
app.include_router(reports_routes.router)
app.include_router(reservations_routes.router)
app.include_router(feedback_routes.router)

app.mount("/", StaticFiles(directory="client", html=True), name="client")
