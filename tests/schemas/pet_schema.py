from unicodedata import category

PET_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "name": {
            "type": "string"
        },
        "category": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer"
                },
                "name": {
                    "type": "string"
                },
            },
            "required": ["id", "name"],
            "additionalProperties": False
        },
        "photoUrls": {
            "type": "array",
            "items": {
                "type": "string"
            },
        },
        "tags": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "string"
                    }
                },
                "required": ["id", "name"],
                "additionalProperties": False
                },

        },
        "status": {
            "type": "string",
            "enum": ["available", "pending",
                     "sold"]
        },
    },
    "required": ["id", "name", "photoUrls", "status"],
    "additionalProperties": False
}

STORE_SCHEMA = {
    "type": "object",
    "properties":  {
        "id": {
            "type": "integer"
         },
        "petId": {
           "type": "integer"
        } ,
        "quantity": {
            "type": "integer"
        },
        "shipDate": {
            "type": "string"
        },
        "status": {
            "type": "string",
            "enum": ["placed", "approved", "delivered"]
        },
        "complete": {
            "type": "boolean"
        }
    },
    "required": ["id", "petId", "quantity", "status", "complete"],
    "additionalProperties": False
}

INVENTORY_SCHEMA = {
    "type": "object",
    "properties": {
        "approved": {
            "type": "integer"
        },
        "delivered": {
            "type": "integer"
        },
        "status": {
            "type": "string",
            "enum": ["placed", "approved", "delivered"]
        },
    },
    "required": ["approved", "delivered"],
    "additionalProperties": False
}