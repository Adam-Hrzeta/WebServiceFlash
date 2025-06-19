from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductoBase(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    categoria: Optional[str] = None
    stock: int = 0
    # La imagen se maneja como blob en la base de datos, pero aquí solo se referencia
    imagen_url: Optional[str] = None

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(ProductoBase):
    pass

class ProductoResponse(ProductoBase):
    id: int
    negocio_id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True