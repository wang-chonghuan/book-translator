from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class MongoBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    class Config:
            json_encoders = {ObjectId: str}
"""
#这个文件主要是定义了几个 Pydantic 数据模型，这些模型可以用于输入验证（如 HTTP 请求体）、序列化和反序列化（如从数据库读取数据和将数据写入数据库）。
#ObjectId 是 MongoDB 的一种数据类型，用于唯一标识数据库中的每一条记录（或称为文档）。每个 ObjectId 都是唯一的，它通常用作文档的主键。ObjectId 不在 JSON 支持的数据类型之内，因此我们需要将其转换为字符串才能将其转换为 JSON。
#当你从 MongoDB 读取数据时，你会得到 ObjectId 类型的主键。如果你需要将这个数据发送给前端或者存储为 JSON，你需要将 ObjectId 转换为字符串。
#当你从前端接收到数据，或者从 JSON 格式的文件中读取数据时，你可能会得到表示 ObjectId 的字符串。如果你需要将这个数据保存到 MongoDB，你需要将字符串转换为 ObjectId。
#在你的代码中，PyObjectId 类和 MongoBaseModel 类的配置就是用来处理这两种转换的。希望这个解释能帮到你。

"""