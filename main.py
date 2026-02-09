import json
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
import crud # Importujemy nasze zapytania SQL

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Logika startowa (migracja) została tutaj dla uproszczenia, 
    # ale też korzysta z połączenia z database.py
    yield

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")

# --- TRASY PUBLICZNE ---

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "items": []})

@app.post("/sort", response_class=HTMLResponse)
async def sort_list(request: Request, shopping_list: str = Form(...)):
    raw_items = [i.strip() for i in shopping_list.replace('\n', ',').split(',') if i.strip()]
    sorted_items = sorted(raw_items, key=lambda x: crud.get_item_priority(x))
    return templates.TemplateResponse("index.html", {"request": request, "items": sorted_items})

# --- TRASY ADMINA ---

@app.get("/admin/products", response_class=HTMLResponse)
async def admin_page(request: Request):
    products = crud.get_all_products()
    # Musisz dodać funkcję get_all_categories w crud.py!
    categories = crud.get_all_categories() 
    return templates.TemplateResponse("admin.html", {
        "request": request, 
        "products": products, 
        "categories": categories
    })

@app.post("/admin/add")
async def add_product(name: str = Form(...), category_id: int = Form(...)):
    crud.add_product_to_db(name, category_id)
    return RedirectResponse(url="/admin/products", status_code=303)

@app.post("/admin/delete/{product_id}")
async def delete_product(product_id: int):
    crud.delete_product_from_db(product_id)
    return RedirectResponse(url="/admin/products", status_code=303)