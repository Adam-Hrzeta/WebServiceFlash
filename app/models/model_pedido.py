from pydantic import BaseModel
from typing import List
from datetime import datetime

class DetallePedido(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: float

class PedidoCreate(BaseModel):
    cliente_id: int
    total: float
    detalles: List[DetallePedido]
    fecha: datetime = datetime.utcnow()

class PedidoResponse(BaseModel):
    id: int
    cliente_id: int
    total: float
    fecha: datetime
    detalles: List[DetallePedido]

    class Config:
        from_attributes = True
