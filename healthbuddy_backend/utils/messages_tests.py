RESP_WITHOUT_TOKEN = {"detail": "Authentication credentials were not provided."}

RESP_WRONG_TOKEN = {
    "detail": "Given token not valid for any token type",
    "code": "token_not_valid",
    "messages": [{"token_class": "AccessToken", "token_type": "access", "message": "Token is invalid or expired"}],
}

RESP_DONT_HAVE_PERMISSION = {"detail": "You do not have permission to perform this action."}

USER_ALREADY_EXISTS = {"username": ["A user with that username already exists."]}

USER_CREATE_REQUIRED_FIELDS = {"username": ["This field is required."], "password": ["This field is required."]}

USER_CREATE_PASSWORD_LESS_THAN_8 = {"password": ["Ensure this field has at least 8 characters."]}
