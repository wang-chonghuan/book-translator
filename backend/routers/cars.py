# APIRouter 是用来创建 API 路由的类；Request 是代表 HTTP 请求的类；Body 是一个函数，用来标识一个请求体参数；status 是一个包含 HTTP 状态码常量的模块。
from typing import List, Optional
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Request, Body, status

# jsonable_encoder 函数，这个函数可以将 Python 对象转换为可以序列化为 JSON 的字典或者列表。
from fastapi.encoders import jsonable_encoder

# JSONResponse 类，这个类用来创建一个返回 JSON 数据的 HTTP 响应。
from fastapi.responses import JSONResponse
from models import CarBase, CarDB, CarUpdate

router = APIRouter()


@router.get("/test", response_description="List all cars")
async def test():
    return {"data": "All cars will go here."}


# min_price: int = 0, max_price: int = 100000, brand: Optional[str] = None, page: int = 1,：函数的其余参数定义了可选的查询条件，包括最低价格、最高价格、品牌和页码。它们都有默认值，所以在请求中可以省略。
@router.get("/", response_description="List all cars")
async def list_all_cars(
    request: Request,
    min_price: int = 0,
    max_price: int = 100000,
    brand: Optional[str] = None,
    page: int = 1,
) -> List[CarDB]:
    RESULTS_PER_PAGE = 25
    # 计算要跳过的结果数量。这用于实现分页功能。
    skip = (page - 1) * RESULTS_PER_PAGE
    # 定义查询条件，价格要小于 max_price 且大于 min_price。
    query = {"price": {"$lt": max_price, "$gt": min_price}}
    # 如果 brand 参数不为 None，则添加品牌查询条件。
    if brand:
        query["brand"] = brand
    # 定义一个完整的 MongoDB 查询，包括查询条件、排序、跳过和限制结果数量。
    # 这是一个 MongoDB 查询，首先在 "cars1" 集合中根据 query 查找文档，然后按 _id 倒序排序，跳过 skip 个结果，最后限制结果数量为 RESULTS_PER_PAGE。
    full_query = (
        request.app.mongodb["cars1"]
        .find(query)
        .sort("_id", -1)
        .skip(skip)
        .limit(RESULTS_PER_PAGE)
    )
    # 使用异步列表推导式（async list comprehension）从 full_query 中获取每一个原始的汽车数据 raw_car，并将其转换为 CarDB 对象。
    # 异步列表解析：这是 Python 中的一种语法，用于创建一个新的列表，列表中的元素是通过对另一个可迭代对象中的每个元素应用一个表达式得到的。如果这个可迭代对象是一个异步的，例如一个从数据库异步获取数据的查询，那么你需要使用异步列表解析，语法形式为 [expression async for item in async_iterable]。在你给出的代码中，[CarDB(**raw_car) async for raw_car in full_query] 是一个异步列表解析，它从 full_query 异步查询中获取每一个原始的汽车数据 raw_car，并将其转换为 CarDB 对象，最后得到一个 CarDB 对象的列表。
    results = [CarDB(**raw_car) async for raw_car in full_query]
    # this is also possible
    # results = await full_query.to_list(1000)
    return results


# 这行定义了一个异步函数 create_car。这个函数有两个参数：request 代表 HTTP 请求，它的类型是 Request；car 是请求体参数，它的类型是 CarBase，并使用 Body(...) 函数指定为请求体。
@router.post("/", response_description="Add new car")
async def create_car(request: Request, car: CarBase = Body(...)):
    # 将 car 参数转换为可以序列化为 JSON 的字典。
    car = jsonable_encoder(car)
    # 向 MongoDB 插入一条新的记录。request.app.mongodb["cars1"] 获取了 MongoDB 中名为 "cars1" 的集合（类似于 SQL 数据库中的表），insert_one(car) 插入一条记录，并返回一个插入结果。
    new_car = await request.app.mongodb["cars1"].insert_one(car)
    # 这行代码从 MongoDB 中查询刚刚插入的记录。find_one({"_id": new_car.inserted_id}) 查找 _id 等于新插入记录的 _id 的记录，并返回一个文档。
    created_car = await request.app.mongodb["cars1"].find_one(
        {"_id": ObjectId(new_car.inserted_id)}
    )
    # 这行代码创建了一个 JSONResponse 实例并将其返回。JSONResponse 的状态码是 201，表示创建了一条新的资源，内容是 created_car。
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_car)


# get car by ID
@router.get("/{id}", response_description="Get a single car")
async def show_car(id: str, request: Request):
    # 这行代码在 MongoDB 数据库的 "cars1" 集合中查询 _id 等于指定 ID 的文档。:= 是 Python 的 "海象运算符"（walrus operator），它在条件判断的同时赋值。如果找到了匹配的文档，car 变量将被赋值为该文档，然后检查 car 是否不为 None。
    if (car := await request.app.mongodb["cars1"].find_one({"_id": ObjectId(id)})) is not None:
        # 将 car 字典的键值对作为参数，创建一个 CarDB 对象，并返回该对象。在 FastAPI 中，返回的模型对象将被自动转换为 JSON 格式。 ** 是一个特殊的操作符，它被称为 "字典解包"（dictionary unpacking）操作符。
        return CarDB(**car)
    raise HTTPException(status_code=404, detail=f"Car with {id} not found")


@router.patch("/{id}", response_description="Update car")
async def update_task(id: str, request: Request, car: CarUpdate = Body(...)):
    await request.app.mongodb["cars1"].update_one(
        {"_id": ObjectId(id)}, {"$set": car.dict(exclude_unset=True)}
    )
    if (car := await request.app.mongodb["cars1"].find_one({"_id": ObjectId(id)})) is not None:
        return CarDB(**car)
    raise HTTPException(status_code=404, detail=f"Car with {id} not found")


@router.delete("/{id}", response_description="Delete car")
async def delete_task(id: str, request: Request):
    delete_result = await request.app.mongodb["cars1"].delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
    raise HTTPException(status_code=404, detail=f"Car with {id} not found")


# optional
@router.get("/brand/{brand}", response_description="Get brand overview")
async def brand_price(brand: str, request: Request):
    query = [
        {"$match": {"brand": brand}},
        {"$project": {"_id": 0, "price": 1, "year": 1, "make": 1}},
        {
            "$group": {"_id": {"model": "$make"}, "avgPrice": {"$avg": "$price"}},
        },
        {"$sort": {"avgPrice": 1}},
    ]
    full_query = request.app.mongodb["cars1"].aggregate(query)
    results = [el async for el in full_query]
    return results
