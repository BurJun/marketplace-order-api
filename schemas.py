from pydantic import BaseModel, conint

class AddItemRequest(BaseModel):
    order_id: int
    product_id: int
    quantity: conint(gt=0)

class OrderItemResponse(BaseModel):
    order_id: int
    product_id: int
    quantity: int 