from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

class NegocioBase(BaseModel):
    nombre: str
    correo: EmailStr
    telefono: str
    direccion: str
    descripcion: Optional[str] = None
    disponibilidad: bool = True
    tipo_entrega: str
    categoria: str

class NegocioCreate(NegocioBase):
    contrasena: constr

class NegocioLogin(BaseModel):
    correo: EmailStr
    contrasena: str

class NegocioResponse(NegocioBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True 