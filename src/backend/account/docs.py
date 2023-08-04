from core.docs import SPEC


USER_PROPERTIES = {
    "pk": {
        "type": "integer",
        "example": 1,
    },
    "model": {
        "type": "string",
        "example": "account.user",
    },
    "fields": {
        "type": "object",
        "properties": {
            "username": {
                "type": "string",
                "example": "admin",
            },
            "email": {
                "type": "string",
                "example": "example@gmail.com",
            },
            "first_name": {
                "type": "string",
                "example": "admin",
            },
            "last_name": {
                "type": "string",
                "example": "admin",
            },
            "is_staff": {
                "type": "boolean",
                "example": True,
            },
            "is_active": {
                "type": "boolean",
                "example": True,
            },
            "date_joined": {
                "type": "string",
                "format": "date-time",
                "example": "2020-01-01T00:00:00Z",
            },
            "last_login": {
                "type": "string",
                "format": "date-time",
                "example": "2020-01-01T00:00:00Z",
            },
            "is_superuser": {
                "type": "boolean",
                "example": True,
            },
            "avatar": {
                "type": "string",
                "example": "avatar.png",
            }
        },
    },
}


SPEC.components.schema(
    "UserResponse",
    {
        "properties": USER_PROPERTIES,
    },
)


SPEC.components.schema(
    "UserLoginForm",
    {
        "properties": {
            "username": {
                "type": "string",
                "example": "admin",
            },
            "password": {
                "type": "string",
                "foramt": "password",
                "example": "admin",
            }
        },
        "required": ["username", "password"],
    },
)


SPEC.components.schema(
    "UserPasswordChangeForm",
    {
        "properties": {
            "old_password": {
                "type": "string",
                "foramt": "password",
                "example": "admin",
            },
            "new_password1": {
                "type": "string",
                "foramt": "password",
                "example": "admin",
            },
            "new_password2": {
                "type": "string",
                "foramt": "password",
                "example": "admin",
            },
        },
        "required": ["old_password", "new_password1", "new_password2"],
    }
)


SPEC.components.schema(
    "UserRegisterForm",
    {
        "properties": {
            "username": {
                "type": "string",
                "example": "admin",
            },
            "password1": {
                "type": "string",
                "foramt": "password",
                "example": "admin",
            },
            "password2": {
                "type": "string",
                "foramt": "password",
                "example": "admin",
            },
            "email": {
                "type": "string",
                "example": "example@gmail.com",
            },
            "first_name": {
                "type": "string",
                "example": "admin",
            },
            "last_name": {
                "type": "string",
                "example": "admin",
            },
        },
        "required": ["username", "password1", "password2"],
    }
)


SPEC.components.schema(
    "UserRegisterMultipartForm",
    {
        "properties": {
            "username": {
                "type": "string",
                "example": "admin",
            },
            "password1": {
                "type": "string",
                "foramt": "password",
                "example": "admin",
            },
            "password2": {
                "type": "string",
                "foramt": "password",
                "example": "admin",
            },
            "email": {
                "type": "string",
                "example": "example@gmail.com",
            },
            "first_name": {
                "type": "string",
                "example": "admin",
            },
            "last_name": {
                "type": "string",
                "example": "admin",
            },
            "avatar": {
                "type": "string",
                "format": "binary",
            },
        },
        "required": ["username", "password1", "password2"],
    }
)


SPEC.components.schema(
    "UserUpdateForm",
    {
        "properties": {
            "username": {
                "type": "string",
                "example": "admin",
            },
            "password1": {
                "type": "string",
                "foramt": "password",
                "example": "admin",
            },
            "password2": {
                "type": "string",
                "foramt": "password",
                "example": "admin",
            },
            "email": {
                "type": "string",
                "example": "example@gmail.com",
            },
            "first_name": {
                "type": "string",
                "example": "admin",
            },
            "last_name": {
                "type": "string",
                "example": "admin",
            },
        },
        "required": ["username"],
    }
)


SPEC.components.schema(
    "UserUpdateMultipartForm",
    {
        "properties": {
            "username": {
                "type": "string",
                "example": "admin",
            },
            "password1": {
                "type": "string",
                "foramt": "password",
                "example": "admin",
            },
            "password2": {
                "type": "string",
                "foramt": "password",
                "example": "admin",
            },
            "email": {
                "type": "string",
                "example": "example@gmail.com",
            },
            "first_name": {
                "type": "string",
                "example": "admin",
            },
            "last_name": {
                "type": "string",
                "example": "admin",
            },
            "avatar": {
                "type": "string",
                "format": "binary",
            },
        },
        "required": ["username"],
    }
)


SPEC.components.schema(
    "LoginResponse",
    {
        "properties": {
            "token": {
                "type": "string",
                "example": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9",
            },
            "user": {
                "type": "object",
                "properties": USER_PROPERTIES,
            },
        }
    },
)


SPEC.path(
    path="/models/users/login/",
    operations={
        "post": {
            "tags": ["account"],
            "summary": "Login",
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": "UserLoginForm",
                    },
                    "application/x-www-form-urlencoded": {
                        "schema": "UserLoginForm",
                    },
                    "multipart/form-data": {
                        "schema": "UserLoginForm",
                    },
                },
            },
            "responses": {
                "201": {
                    "content": {
                        "application/json": {
                            "schema": "LoginResponse",
                        }
                    }
                }
            }
        },
    }
)


SPEC.path(
    path="/models/users/auth-refresh/",
    operations={
        "post": {
            "tags": ["account"],
            "summary": "Auth refresh",
            "security": [{"jwt": []}],
            "responses": {
                "200": {
                    "content": {
                        "application/json": {
                            "schema": "LoginResponse",
                        }
                    }
                }
            }
        },
    }
)


SPEC.path(
    path="/models/users/change-password/",
    operations={
        "post": {
            "tags": ["account"],
            "summary": "Change password",
            "security": [{"jwt": []}],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": "UserPasswordChangeForm",
                    },
                    "application/x-www-form-urlencoded": {
                        "schema": "UserPasswordChangeForm",
                    },
                    "multipart/form-data": {
                        "schema": "UserPasswordChangeForm",
                    },
                },
            },
            "responses": {
                "200": {
                    "content": {
                        "application/json": {
                            "schema": "UserResponse",
                        }
                    }
                }
            }
        },
    }
)


SPEC.path(
    path="/models/users/records/",
    operations={
        "get": {
            "tags": ["account"],
            "summary": "List users",
            "security": [{"jwt": []}],
            "parameters": [
                {
                    "name": "limit",
                    "in": "query",
                    "description": "Limit",
                    "required": False,
                    "schema": {
                        "type": "integer",
                        "example": 10,
                    },
                },
                {
                    "name": "offset",
                    "in": "query",
                    "description": "Offset",
                    "required": False,
                    "schema": {
                        "type": "integer",
                        "example": 0,
                    },
                },
            ],
            "responses": {
                "200": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "count": {
                                        "type": "integer",
                                        "example": 1,
                                    },
                                    "results": {
                                        "type": "array",
                                        "items": "UserResponse",
                                    },
                                }
                            }
                        }
                    }
                }
            }
        },
        "post": {
            "tags": ["account"],
            "summary": "Create users",
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": "UserRegisterForm",
                    },
                    "application/x-www-form-urlencoded": {
                        "schema": "UserRegisterForm",
                    },
                    "multipart/form-data": {
                        "schema": "UserRegisterMultipartForm",
                    },
                }
            },
            "responses": {
                "200": {
                    "content": {
                        "application/json": {
                            "schema": "UserResponse",
                        }
                    }
                }
            }
        },
    }
)


SPEC.path(
    path="/models/users/records/{pk}/",
    operations={
        "get": {
            "tags": ["account"],
            "summary": "Detail user",
            "security": [{"jwt": []}],
            "parameters": [
                {
                    "name": "pk",
                    "in": "path",
                    "description": "User primary key.",
                    "required": True,
                    "schema": {
                        "type": "integer",
                        "example": 1,
                    },
                },
            ],
            "responses": {
                "200": {
                    "content": {
                        "application/json": {
                            "schema": "UserResponse",
                        }
                    }
                }
            }
        },
        "put": {
            "tags": ["account"],
            "summary": "Update users",
            "security": [{"jwt": []}],
            "parameters": [
                {
                    "name": "pk",
                    "in": "path",
                    "description": "User primary key.",
                    "required": True,
                    "schema": {
                        "type": "integer",
                        "example": 1,
                    },
                },
            ],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": "UserUpdateForm",
                    },
                    "application/x-www-form-urlencoded": {
                        "schema": "UserUpdateForm",
                    },
                    "multipart/form-data": {
                        "schema": "UserUpdateMultipartForm",
                    },
                }
            },
            "responses": {
                "200": {
                    "content": {
                        "application/json": {
                            "schema": "UserResponse",
                        }
                    }
                }
            }
        },
        "delete": {
            "tags": ["account"],
            "summary": "Delete users",
            "security": [{"jwt": []}],
            "parameters": [
                {
                    "name": "pk",
                    "in": "path",
                    "description": "User primary key.",
                    "required": True,
                    "schema": {
                        "type": "integer",
                        "example": 1,
                    },
                },
            ],
            "responses": {
                "204": {}
            }
        },
    }
)
