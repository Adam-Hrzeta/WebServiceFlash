from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductoBase(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    imagen_url: Optional[str] = None

class ProductoResponse(ProductoBase):
    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True 