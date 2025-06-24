from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class AdministradorBase(BaseModel):
    nombre: str
    correo: EmailStr
    telefono: str
    tipo_usuario: str

class AdministradorLogin(BaseModel):
    correo: EmailStr
    contrasena: str

class AdministradorResponse(AdministradorBase):
    id: int

    class Config:
        from_attributes = True
