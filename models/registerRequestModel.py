# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = register_request_model_from_dict(json.loads(json_string))

from typing import Any, TypeVar, Type, cast

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class RegisterRequestModel:
    first_name: str
    last_name: str
    phone: str
    age: int
    email: str
    password:str

    def __init__(self, first_name: str, last_name: str, phone: str, age: int, email: str,password:str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.age = age
        self.email = email
        self.password = password

    @staticmethod
    def from_dict(obj: Any) -> 'RegisterRequestModel':
        assert isinstance(obj, dict)
        first_name = from_str(obj.get("first_name"))
        last_name = from_str(obj.get("last_name"))
        phone = from_str(obj.get("phone"))
        age = int(from_str(obj.get("age")))
        email = from_str(obj.get("email"))
        password= from_str(obj.get("password"))
        return RegisterRequestModel(first_name, last_name, phone, age, email,password)

    def to_dict(self) -> dict:
        result: dict = {"first_name": from_str(self.first_name), "last_name": from_str(self.last_name),
                        "phone": from_str(self.phone), "age": from_str(str(self.age)), "password": from_str(self.password)
                        }
        return result


def register_request_model_from_dict(s: Any) -> RegisterRequestModel:
    return RegisterRequestModel.from_dict(s)


def register_request_model_to_dict(x: RegisterRequestModel) -> Any:
    return to_class(RegisterRequestModel, x)
