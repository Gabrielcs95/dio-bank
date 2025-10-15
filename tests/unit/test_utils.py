from unittest.mock import patch
from http import HTTPStatus
from src.utils import requires_role 

def test_requires_roles_success(mocker):

    #given
    mock_user = mocker.Mock()
    mock_user.role.name = "admin"
    mocker.patch("src.utils.get_jwt_identity")
    mocker.patch("src.utils.db.get_or_404", return_value=mock_user)
    decorated_function = requires_role("admin") (lambda: "Success")
    
    #when
    result = decorated_function()

    #then
    assert result == "Success"

def test_requires_roles_fail(mocker):
    mock_user = mocker.Mock()
    mock_user.role.name = "normal"

    mocker.patch("src.utils.get_jwt_identity")
    mocker.patch("src.utils.db.get_or_404", return_value=mock_user)

    decorated_function = requires_role("admin") (lambda: "Success")
    result = decorated_function()

    assert result == ({"msg": "User dont have access!"}, HTTPStatus.FORBIDDEN)
    
