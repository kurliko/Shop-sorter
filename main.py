from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_items():
    return """
    <html>
        <head><title>Kaufland Sorter</title></head>
        <body>
            <h1>Witaj w Sorterze Zakupów!</h1>
            <p>Backend działa. Czas na logikę.</p>
        </body>
    </html>
    """
