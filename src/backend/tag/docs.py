from core.docs import SPEC

TAG_PROPERTIES = {
    "pk": {
        "type": "integer",
        "example": 1,
    },
    "model": {
        "type": "string",
        "example": "taggit.tag",
    },
    "fields": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "example": "testtag1",
            },
            "slug": {
                "type": "string",
                "example": "testtag1",
            },
        },
    },
}

SPEC.components.schema("TagResponse", {
    "properties": TAG_PROPERTIES,
})

SPEC.components.schema(
    "TagCreateForm", 
    {
        "properties": {
            "name": {
                "type": "string",
                "example": "testtag1",
            },
        },
    },
)


SPEC.path(
    path="/models/tags/records/",
    operations={
        "get": {
            "tags": ["Tag"],
            "summary": "List tags",
            "description": "List tags",
            "parameters": [
                {
                    "name": "search",
                    "in": "query",
                    "description": "Search tags",
                    "required": False,
                    "schema": {
                        "type": "string",
                        "example": "testtag1",
                    },
                },
            ],
            "responses": {
                "200": {
                    "description": "List tags",
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
                                        "items": "TagResponse",
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        "post": {
            "tags": ["Tag"],
            "summary": "Create tag",
            "description": "Create tag",
            "security": [{"jwt": []}],
            "requestBody": {
                "content": {
                    "application/json": {
                        "schema": "TagCreateForm",
                    },
                },
            },
            "responses": {
                "201": {
                    "description": "Create tag",
                    "content": {
                        "application/json": {
                            "schema": "TagResponse",
                        },
                    },
                },
            },
        },
    },
)

SPEC.path(
    path="/models/tags/records/{pk}/",
    operations={
        "get": {
            "tags": ["Tag"],
            "summary": "Retrieve tag",
            "description": "Retrieve tag",
            "parameters": [
                {
                    "name": "pk",
                    "in": "path",
                    "description": "Tag primary key",
                    "required": True,
                    "schema": {
                        "type": "integer",
                        "example": 1,
                    },
                },
            ],
            "responses": {
                "200": {
                    "description": "Retrieve tag",
                    "content": {
                        "application/json": {
                            "schema": "TagResponse",
                        },
                    },
                },
            },
        },
    },
)

