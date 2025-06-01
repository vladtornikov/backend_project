from fastapi import APIRouter, Body, Response

from src.exceptions import UserAlreadyExistsException, EmailNotFoundException, EmailNotFoundHTTPException, \
    IncorrectPasswordException, \
    IncorrectPasswordHTTPException, UserEmailAlreadyExistsHTTPException
from src.schemas_API.users import UserRequestAdd
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep, DBDep

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])

@router.post(
    '/register',
     summary='Регистрация пользователей',
     description='Тут можно зарегистрировать нового пользователя, введя эл. почту и пароль'
)
async def register_user(db: DBDep, data: UserRequestAdd = Body(openapi_examples={
    '1': {
        'summary': 'Тестовый вариант',
        'value': {
            'email': 'balesiy@mail.ru',
            'password': '123456789'
          }
        }
})
):
    try:
        await AuthService(db).add_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException
    return {'status': 'OK'}

@router.post(
    '/login',
     summary='Аутентификация пользователя',
     description='Тут можно аутентифицировать пользователя, введя эл. почту и пароль'
)
async def login_user(db: DBDep, response: Response, data: UserRequestAdd = Body(openapi_examples={
    '1': {
        'summary': 'Тестовый вариант',
        'value': {
            'email': 'balesiy@mail.ru',
            'password': '123456789'
          }
        }
})
):
    try:
        access_token = await AuthService(db).login_user(data)
    except EmailNotFoundException:
        raise EmailNotFoundHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException

    response.set_cookie('access_token', access_token)
    return {"access_token": access_token}

@router.get(
    '/me',
    summary='Получаем данные об аутентифицированном пользователе'
)
async def get_me(db: DBDep, user_id: UserIdDep):
    user_data = await AuthService(db).get_current_user(user_id)
    return user_data

@router.get(
    '/logout',
    summary='Удаляем JWT-токен после того, как пользователь разлогинился'
)
async def delete_jwt_token(response: Response):
    response.delete_cookie(key='access_token')
    return {'status': 'OK'}