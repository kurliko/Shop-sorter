import json
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# mapowanie kolejnosci alejek
KAUFLAND_LAYOUT = {
    "warzywa": 1, "owoce": 1, "pieczywo": 2, "nabiał": 3, 
    "mięso": 4, "napoje": 5, "mrożonki": 6, "chemia": 7, "inne": 99
}

def load_products():
    with open("products.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_category(item_name: str, categories_data: dict):
    item_name = item_name.lower().strip()

    # przeszukanie kategorii
    for category, keywords in categories_data.items():
        for key in keywords:
            if key in item_name or item_name in key:
                return category
    return "inne"



@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    # Ważne: przekazujemy 'request' i pustą listę 'items'
    return templates.TemplateResponse("index.html", {"request": request, "items": []})


@app.post("/sort", response_class=HTMLResponse)
async def sort_list(request: Request, shopping_list: str = Form(...)):
    product_data = load_products()

    # rozbicie tekstu na liste produktow
    raw_items = [i.strip() for i in shopping_list.replace('\n', ',').split(',') if i.strip()]

    # sortowanie
    sorted_items = sorted(
        raw_items,
        key=lambda x: KAUFLAND_LAYOUT.get(get_category(x, product_data), 99)
    )

    return templates.TemplateResponse("index.html", {
        "request": request,
        "items": sorted_items
        }) 
    
