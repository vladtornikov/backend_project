from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
import jwt

from src.config import settings
from src.exceptions import IncorrectTokenException, UserAlreadyExistsException, \
    EmailNotFoundException, IncorrectPasswordException, ObjectAlreadyExistsException
from src.schemas_API.users import UserAdd, User, UserRequestAdd
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_token(self, access_token: str) -> dict:
        try:
            return jwt.decode(access_token, settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
        except jwt.exceptions.DecodeError:
            raise IncorrectTokenException

    async def add_user(self, data: UserRequestAdd):
        hashed_password = self.hash_password(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
        try:
            await self.db.users.add(new_user_data)
        except ObjectAlreadyExistsException as ex:
            raise UserAlreadyExistsException from ex
        await self.db.commit()

    async def login_user(self, data: UserRequestAdd) -> str:
        user = await self.db.users.get_user_with_hashed_password(data.email)
        if not user:
            raise EmailNotFoundException
        if not self.verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException
        access_token = self.create_access_token({'user_id': user.id})
        return access_token

    async def get_current_user(self, user_id: int) -> User:
        return await self.db.users.get_one_or_none(id=user_id)
