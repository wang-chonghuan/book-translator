#这个文件主要是定义了几个 Pydantic 数据模型，这些模型可以用于输入验证（如 HTTP 请求体）、序列化和反序列化（如从数据库读取数据和将数据写入数据库）。
#ObjectId 是 MongoDB 的一种数据类型，用于唯一标识数据库中的每一条记录（或称为文档）。每个 ObjectId 都是唯一的，它通常用作文档的主键。ObjectId 不在 JSON 支持的数据类型之内，因此我们需要将其转换为字符串才能将其转换为 JSON。
#当你从 MongoDB 读取数据时，你会得到 ObjectId 类型的主键。如果你需要将这个数据发送给前端或者存储为 JSON，你需要将 ObjectId 转换为字符串。
#当你从前端接收到数据，或者从 JSON 格式的文件中读取数据时，你可能会得到表示 ObjectId 的字符串。如果你需要将这个数据保存到 MongoDB，你需要将字符串转换为 ObjectId。
#在你的代码中，PyObjectId 类和 MongoBaseModel 类的配置就是用来处理这两种转换的。希望这个解释能帮到你。

#这行从 bson 库中导入 ObjectId 类。ObjectId 是 MongoDB 数据库中用于唯一标识文档的一个特殊类型。
from bson import ObjectId
#这行从 pydantic 库中导入 Field 和 BaseModel。BaseModel 是所有 Pydantic 模型的基类，Field 是用来描述模型字段的额外信息。
from pydantic import Field, BaseModel
#从 typing 模块导入 Optional 类型提示，表示一个变量可以是其类型，也可以是 None。
from typing import Optional

#这是一个 ObjectId 的子类，其中有三个类方法。这个类用来进行 MongoDB 中的 ObjectId 与 Python 中的 str 类型之间的转换和验证。
class PyObjectId(ObjectId):
    #这个类方法告诉 Pydantic 如何对此字段进行验证。
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    #这个类方法对给定值进行验证。如果值不是有效的 ObjectId，则抛出 ValueError，否则，返回 ObjectId 对象。
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    #这个类方法修改了 Pydantic 自动生成的 JSON Schema，表示此字段的类型应该是 "string"。
    #这是一个 Pydantic 模型的特殊方法，它允许你修改模型的 JSON schema，可以改变模型在 API 文档（例如使用 FastAPI 生成的 Swagger UI）中如何呈现。field_schema.update(type="string") 这一行将字段的类型更改为 "string"，这意味着在 JSON schema 中，该字段将被表示为字符串类型。
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

#这个类是所有其它模型的基类，它有一个名为 "id" 的字段，该字段的别名是 "_id"，其默认工厂函数是 PyObjectId，这样就可以自动处理 MongoDB 的 ObjectId。
class MongoBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    #在模型的配置中，设置了 JSON 编码器，让 ObjectId 在转为 JSON 时转换为字符串。
    # 在 Pydantic 模型的配置中，你可以指定一些自定义的 JSON 编码器。这里 {ObjectId: str} 是一个 Python 字典，它表示当 Pydantic 需要将 ObjectId 类型的字段转换为 JSON 时，应该使用 str 函数将其转换为字符串。否则，由于 JSON 标准不支持 ObjectId，如果不进行转换，将无法将 ObjectId 转换为 JSON。
    class Config:
        json_encoders = {ObjectId: str}

#这个类继承了 MongoBaseModel，它描述了车辆的基础数据模型，包括品牌、制造商、年份、价格、公里数和立方厘米数。
class CarBase(MongoBaseModel):
    brand: str = Field(..., min_length=1)
    make: str = Field(..., min_length=1)
    year: int = Field(..., gt=1975, lt=2023)
    price: int = Field(...)
    km: int = Field(...)
    cm3: int = Field(...)

#这个类也继承了 MongoBaseModel，它只有一个字段，用于表示车辆的价格，这个字段是可选的，可能会是 None，用于描述车辆的更新数据模型。
class CarUpdate(MongoBaseModel):
    price: Optional[int] = None

# 这个类继承了 CarBase，它表示存储在数据库中的车辆数据模型。在这个例子中，它与 CarBase 没有区别，但在实际的应用中，它可能会包含一些不应该由用户直接修改的字段，如创建和修改的时间戳等。
class CarDB(CarBase):
    pass
