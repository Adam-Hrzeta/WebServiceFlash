from pydantic import BaseModel
from typing import List, Optional
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
    comentario: Optional[str] = None  # Nuevo campo para comentarios

class PedidoResponse(BaseModel):
    id: int
    cliente_id: int
    total: float
    fecha: datetime
    detalles: List[DetallePedido]
    comentario: Optional[str] = None  # Nuevo campo para comentarios

    class Config:
        from_attributes = True
