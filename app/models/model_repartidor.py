from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

class RepartidorBase(BaseModel):
    nombre: str
    correo: EmailStr
    telefono: str
    fecha_nacimiento: Optional[datetime] = None
    disponibilidad: bool = True
    tipo_servicio: Optional[str] = None  # Puede ser "Cuenta Propia" o "Empresa"

class RepartidorCreate(RepartidorBase):
    contrasena: constr

class RepartidorLogin(BaseModel):
    correo: EmailStr
    contrasena: str

class RepartidorResponse(RepartidorBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True