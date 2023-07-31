from core.docs import SPEC

THREAD_PROPERTIES = {
    "pk": {
        "type": "integer",
        "example": 1,
    },
    "model": {
        "type": "string",
        "example": "forum.thread",
    },
    "fields": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "example": "How do I use the forum?",
            },
            "content": {
                "type": "string",
                "example": "I'm new to the forum and I don't know how to use it.",
            },
            "creator_type": {
                "type": "integer",
                "example": 1,
            },
            "creator_id": {
                "type": "integer",
                "example": 1,
            },
            "parent": {
                "type": "integer",
                "example": 1,
                "nullable": True,
            },
            "approved": {
                "type": "boolean",
                "example": False,
            },
            "approver_type": {
                "type": "integer",
                "example": 1,
                "nullable": True,
            },
            "approver_id": {
                "type": "integer",
                "example": 1,
                "nullable": True,
            },
            "approver_name": {
                "type": "string",
                "example": "John Doe",
            },
            "approver_email": {
                "type": "string",
                "example": "example@gmail.com",
            },
            "created": {
                "type": "string",
                "format": "date-time",
                "example": "2021-01-01T00:00:00Z",
            },
            "updated": {
                "type": "string",
                "format": "date-time",
                "example": "2021-01-01T00:00:00Z",
            },
        },
    }
}

THREAD_VOTE_PROPERTIES = {
    "pk": {
        "type": "integer",
        "example": 1,
    },
    "model": {
        "type": "string",
        "example": "forum.threadvote",
    },
    "fields": {
        "type": "object",
        "properties": {
            "thread": {
                "type": "integer",
                "example": 1,
            },
            "user_type": {
                "type": "integer",
                "example": 1,
            },
            "user_id": {
                "type": "integer",
                "example": 1,
            },
            "is_upvote": {
                "type": "boolean",
                "example": True,
            },
            "created": {
                "type": "string",
                "format": "date-time",
                "example": "2021-01-01T00:00:00Z",
            },
            "updated": {
                "type": "string",
                "format": "date-time",
            },
        },
    },
}

SPEC.components.schema(
    "ThreadResponse", 
    {
        "properties": THREAD_PROPERTIES,
    }
)


SPEC.components.schema(
    "ThreadVoteResponse",
    {
        "properties": THREAD_VOTE_PROPERTIES,
    },
)


SPEC.components.schema(
    "ThreadCreateForm",
    {
        "properties": {
            "title": {
                "type": "string",
                "example": "How do I use the forum?",
            },
            "content": {
                "type": "string",
                "example": "I'm new to the forum and I don't know how to use it.",
            },
            "parent": {
                "type": "integer",
                "example": 1,
                "nullable": True,
            },
            "tags": {
                "type": "array",
                "items": {
                    "type": "string",
                    "example": "tag",
                },
            },
        },
    },
)


SPEC.components.schema(
    "ThreadUpdateForm",
    {
        "properties": {
            "title": {
                "type": "string",
                "example": "How do I use the forum?",
            },
            "content": {
                "type": "string",
                "example": "I'm new to the forum and I don't know how to use it.",
            },
            "tags": {
                "type": "array",
                "items": {
                    "type": "string",
                    "example": "tag",
                },
            },
            "approved": {
                "type": "boolean",
                "example": False,
                "description": "Only admins can approve threads.",
            },
        },
    },
)


SPEC.components.schema(
    "ThreadVoteCreateForm",
    {
        "properties": {
            "thread": {
                "type": "integer",
                "example": 1,
            },
            "is_upvote": {
                "type": "boolean",
                "example": True,
            },
        },
    },
)


SPEC.components.schema(
    "ThreadVoteUpdateForm",
    {
        "properties": {
            "is_upvote": {
                "type": "boolean",
                "example": True,
            },
        },
    },
)

SPEC.path(
    path="/models/threads/records/",
    operations={
        "get": {
            "tags": ["Threads"],
            "summary": "List threads.",
            "description": "List threads.",
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
                {
                    "name": "search",
                    "in": "query",
                    "description": "Search",
                    "required": False,
                    "schema": {
                        "type": "string",
                        "example": "search",
                    },
                },
                {
                    "name": "creator",
                    "in": "query",
                    "description": "Creator",
                    "required": False,
                    "schema": {
                        "type": "integer",
                        "example": 1,
                    },
                },
                {
                    "name": "parent",
                    "in": "query",
                    "description": "Parent",
                    "required": False,
                    "schema": {
                        "type": "integer",
                        "example": 1,
                    },
                },
                {
                    "name": "approver",
                    "in": "query",
                    "description": "Approver",
                    "required": False,
                    "schema": {
                        "type": "integer",
                        "example": 1,
                    },
                },
                {
                    "name": "created_after",
                    "in": "query",
                    "description": "Created after",
                    "required": False,
                    "schema": {
                        "type": "string",
                        "format": "date-time",
                        "example": "2021-01-01T00:00:00Z",
                    },
                },
                {
                    "name": "created_before",
                    "in": "query",
                    "description": "Created before",
                    "required": False,
                    "schema": {
                        "type": "string",
                        "format": "date-time",
                        "example": "2021-01-01T00:00:00Z",
                    },
                },
                {
                    "name": "is_question",
                    "in": "query",
                    "description": "Is question",
                    "required": False,
                    "schema": {
                        "type": "boolean",
                        "example": True,
                    },
                },
                {
                    "name": "is_answer",
                    "in": "query",
                    "description": "Is answer",
                    "required": False,
                    "schema": {
                        "type": "boolean",
                        "example": True,
                    },
                },
                {
                    "name": "is_pending",
                    "in": "query",
                    "description": "Is pending",
                    "required": False,
                    "schema": {
                        "type": "boolean",
                        "example": True,
                    },
                },
                {
                    "name": "tag_names",
                    "in": "query",
                    "description": "Tag names",
                    "required": False,
                    "schema": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "example": "tag",
                        },
                    },
                },
                {
                    "name": "order",
                    "in": "query",
                    "description": "Order",
                    "required": False,
                    "schema": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": [
                                "count_votes",
                                "-count_votes",
                            ],
                        },
                    },
                },
            ],
            "responses": {
                "200": {
                    "description": "List threads.",
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
                                        "items": "ThreadResponse",
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        "post": {
            "tags": ["Threads"],
            "summary": "Create thread.",
            "description": "Create thread.",
            "security": [{"jwt": []}],
            "requestBody": {
                "description": "Thread create form.",
                "content": {
                    "application/json": {
                        "schema": "ThreadCreateForm",
                    },
                    "application/x-www-form-urlencoded": {
                        "schema": "ThreadCreateForm",
                    },
                    "multipart/form-data": {
                        "schema": "ThreadCreateForm",
                    },
                },
            },
            "responses": {
                "201": {
                    "description": "Thread created.",
                    "content": {
                        "application/json": {
                            "schema": "ThreadResponse",
                        },
                    },
                },
            },
        },
    }
)

SPEC.path(
    path="/models/threads/records/{pk}/",
    operations={
        "get": {
            "tags": ["Threads"],
            "summary": "Retrieve thread.",
            "description": "Retrieve thread.",
            "parameters": [
                {
                    "name": "pk",
                    "in": "path",
                    "description": "Thread primary key.",
                    "required": True,
                    "schema": {
                        "type": "integer",
                        "example": 1,
                    },
                },
            ],
            "responses": {
                "200": {
                    "description": "Thread retrieved.",
                    "content": {
                        "application/json": {
                            "schema": "ThreadResponse",
                        },
                    },
                },
            },
        },
        "put": {
            "tags": ["Threads"],
            "summary": "Update thread.",
            "description": "Update thread.",
            "security": [{"jwt": []}],
            "parameters": [
                {
                    "name": "pk",
                    "in": "path",
                    "description": "Thread primary key.",
                    "required": True,
                    "schema": {
                        "type": "integer",
                        "example": 1,
                    },
                },
            ],
            "requestBody": {
                "description": "Thread update form.",
                "content": {
                    "application/json": {
                        "schema": "ThreadUpdateForm",
                    },
                    "application/x-www-form-urlencoded": {
                        "schema": "ThreadUpdateForm",
                    },
                    "multipart/form-data": {
                        "schema": "ThreadUpdateForm",
                    },
                },
            },
            "responses": {
                "200": {
                    "description": "Thread updated.",
                    "content": {
                        "application/json": {
                            "schema": "ThreadResponse",
                        },
                    },
                }
            },
        },
        "delete": {
            "tags": ["Threads"],
            "summary": "Delete thread.",
            "description": "Delete thread.",
            "security": [{"jwt": []}],
            "parameters": [
                {
                    "name": "pk",
                    "in": "path",
                    "description": "Thread primary key.",
                    "required": True,
                    "schema": {
                        "type": "integer",
                        "example": 1,
                    },
                },
            ],
            "responses": {
                "204": {
                    "description": "Thread deleted.",
                },
            },
        },
    },
)

SPEC.path(
    path="/models/thread-votes/records/",
    operations={
        "get": {
            "tags": ["Thread Votes"],
            "summary": "List thread votes.",
            "description": "List thread votes.",
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
                {
                    "name": "thread",
                    "in": "query",
                    "description": "Thread",
                    "required": False,
                    "schema": {
                        "type": "integer",
                        "example": 1,
                    },
                },
                {
                    "name": "user",
                    "in": "query",
                    "description": "User",
                    "required": False,
                    "schema": {
                        "type": "integer",
                        "example": 1,
                    },
                },
                {
                    "name": "is_upvote",
                    "in": "query",
                    "description": "Is upvote",
                    "required": False,
                    "schema": {
                        "type": "boolean",
                        "example": True,
                    },
                },
            ],
            "responses": {
                "200": {
                    "description": "List thread votes.",
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
                                        "items": "ThreadVoteResponse",
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        "post": {
            "tags": ["Thread Votes"],
            "summary": "Create thread vote.",
            "description": "Create thread vote.",
            "security": [{"jwt": []}],
            "requestBody": {
                "description": "Thread vote create form.",
                "content": {
                    "application/json": {
                        "schema": "ThreadVoteCreateForm",
                    },
                    "application/x-www-form-urlencoded": {
                        "schema": "ThreadVoteCreateForm",
                    },
                    "multipart/form-data": {
                        "schema": "ThreadVoteCreateForm",
                    },
                },
            },
            "responses": {
                "201": {
                    "description": "Thread vote created.",
                    "content": {
                        "application/json": {
                            "schema": "ThreadVoteResponse",
                        },
                    },
                },
            },
        },
    }
)

SPEC.path(
    path="/models/thread-votes/records/{pk}/",
    operations={
        "get": {
            "tags": ["Thread Votes"],
            "summary": "Retrieve thread vote.",
            "description": "Retrieve thread vote.",
            "parameters": [
                {
                    "name": "pk",
                    "in": "path",
                    "description": "Thread vote primary key.",
                    "required": True,
                    "schema": {
                        "type": "integer",
                        "example": 1,
                    },
                },
            ],
            "responses": {
                "200": {
                    "description": "Thread vote retrieved.",
                    "content": {
                        "application/json": {
                            "schema": "ThreadVoteResponse",
                        },
                    },
                },
            },
        },
        "put": {
            "tags": ["Thread Votes"],
            "summary": "Update thread vote.",
            "description": "Update thread vote.",
            "security": [{"jwt": []}],
            "parameters": [
                {
                    "name": "pk",
                    "in": "path",
                    "description": "Thread vote primary key.",
                    "required": True,
                    "schema": {
                        "type": "integer",
                        "example": 1,
                    },
                },
            ],
            "requestBody": {
                "description": "Thread vote update form.",
                "content": {
                    "application/json": {
                        "schema": "ThreadVoteUpdateForm",
                    },
                    "application/x-www-form-urlencoded": {
                        "schema": "ThreadVoteUpdateForm",
                    },
                    "multipart/form-data": {
                        "schema": "ThreadVoteUpdateForm",
                    },
                },
            },
            "responses": {
                "200": {
                    "description": "Thread vote updated.",
                    "content": {
                        "application/json": {
                            "schema": "ThreadVoteResponse",
                        },
                    },
                }
            },
        },
        "delete": {
            "tags": ["Thread Votes"],
            "summary": "Delete thread vote.",
            "description": "Delete thread vote.",
            "security": [{"jwt": []}],
            "parameters": [
                {
                    "name": "pk",
                    "in": "path",
                    "description": "Thread vote primary key.",
                    "required": True,
                    "schema": {
                        "type": "integer",
                        "example": 1,
                    },
                },
            ],
            "responses": {
                "204": {
                    "description": "Thread vote deleted.",
                },
            },
        },
    },
)

