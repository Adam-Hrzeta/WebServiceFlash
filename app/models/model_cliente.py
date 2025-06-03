from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

class ClienteBase(BaseModel):
    nombre: str
    correo: EmailStr
    telefono: str
    direccion: str
    fecha_nacimiento: Optional[datetime] = None

class ClienteCreate(ClienteBase):
    contrasena: constr

class ClienteLogin(BaseModel):
    correo: EmailStr
    contrasena: str

class ClienteResponse(ClienteBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True  # Permite que los atributos se carguen desde el modelo de Pydantic