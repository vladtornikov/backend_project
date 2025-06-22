from src.api.dependencies import DBDep
from src.services.auth import AuthService


def test_create_access_token(db: DBDep):
    data = {"user_id": 1}
    jwt_token = AuthService(db).create_access_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)

    payload = AuthService(db).decode_token(jwt_token)
    assert jwt_token
    assert payload["user_id"] == data["user_id"]
