from datetime import date
from fastapi import HTTPException


class BaseException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class AllRoomsAreBookedException(BaseException):
    detail = "Не осталось свободных номеров"


class UserAlreadyExistsException(BaseException):
    detail = "Пользователь уже существует"


class IncorrectTokenException(BaseException):
    detail = "Истек срок действия токена"


class IncorrectPasswordException(BaseException):
    detail = "Неверный пароль"


class ObjectAlreadyExistsException(BaseException):
    detail = "Похожий объект уже существует"


class ObjectNotFoundException(BaseException):
    detail = "Объект не найден"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Комната не найдена"


class EmailNotFoundException(ObjectAlreadyExistsException):
    detail = "Пользователь с таким email не зарегестрирован"


def check_dates(date_from: date, date_to: date) -> None:
    if date_from >= date_to:
        raise HTTPException(
            status_code=400, detail="Дата заезда должна быть раньше даты выезда"
        )


class BaseHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Комната не найдена"


class IncorrectTokenHTTPException(BaseHTTPException):
    status_code = 403
    detail = "Некорректный токен"


class UserEmailAlreadyExistsHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Пользователь с такой почтой уже существует"


class EmailNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Пользователь с таким email не зарегестрирован"


class IncorrectPasswordHTTPException(BaseHTTPException):
    status_code = 403
    detail = "Неверный пароль"


class AllRoomsAreBookedHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Не осталось свободных номеров"


class NoAccessTokenHTTPException(BaseHTTPException):
    status_code = 401
    detail = "Вы не предоставили токен доступа"
