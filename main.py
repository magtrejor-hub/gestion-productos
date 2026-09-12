import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from supabase import Client, create_client

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# ⚠️ Reemplaza con tus credenciales de Supabase
SUPABASE_URL = "TU_SUPABASE_URL"
SUPABASE_KEY = "TU_SUPABASE_ANON_KEY"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# --- RUTA PRINCIPAL: LEER (Visualizar en la Tablet) ---
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Consulta todos los productos ordenados por ID
    respuesta = (
        supabase.table("productos").select("*").order("id").execute()
    )
    productos = respuesta.data
    return templates.TemplateResponse(
        "index.html", {"request": request, "productos": productos}
    )


# --- ALTA: CREAR ---
@app.post("/alta")
async def alta(nombre: str = Form(...), precio: float = Form(...)):
    supabase.table("productos").insert(
        {"nombre": nombre, "precio": precio}
    ).execute()
    return RedirectResponse(url="/", status_code=303)


# --- CAMBIO: ACTUALIZAR ---
@app.post("/cambio/{id_producto}")
async def cambio(
    id_producto: int, nombre: str = Form(...), precio: float = Form(...)
):
    supabase.table("productos").update({"nombre": nombre, "precio": precio}).eq(
        "id", id_producto
    ).execute()
    return RedirectResponse(url="/", status_code=303)


# --- BAJA: ELIMINAR ---
@app.get("/baja/{id_producto}")
async def baja(id_producto: int):
    supabase.table("productos").delete().eq("id", id_producto).execute()
    return RedirectResponse(url="/", status_code=303)
