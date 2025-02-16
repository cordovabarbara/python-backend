from fastapi import APIRouter

router = APIRouter(prefix="/products", 
                tags=["products"],
                responses={404: {"Message": "Not Found"}})

prodducts_list = ["producto 1", "producto 2", "producto 3", "producto 4", "producto 5"]

@router.get("/")
async def read_products():
    return prodducts_list

@router.get("/{id}")
async def read_products(id:int):
    return prodducts_list[id]