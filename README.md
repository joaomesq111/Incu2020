# Incu2020
This is my repository for the Automation Track.

ABOUT THE APPLICATION:

It was created a user called joao which has admin permissions to all databases and another user called svetlana with readWrite permissions for the Interfaces collection. The pass for this svetlana user is 'cisco123'.

This application has a validator upon the creation of the collection.
This is the jsonschema:

{
  "$jsonSchema": {
    "bsonType": "object",
    "required": [
      "interface",
      "switch",
      "description",
      "state"
    ],
    "additionalProperties": false,
    "properties": {
      "interface": {
        "bsonType": "string",
        "description": "must be a string and is required and needs to be separated with '-'"
      },
      "switch": {
        "bsonType": "string",
        "description": "the name of the switch this interface belongs and is required"
      },
      "description": {
        "bsonType": "string",
        "description": "description of the interface and is required"
      },
      "state": {
        "enum": [
          "up",
          "down"
        ],
        "description": "can only be one of those two values"
      }
    }
  }
}

Every post or update need to match this schema to be accepted.

This application counts with some extras to what was asked in first hand:

  -A post route to add new documents
  -A patch route but instead of using the id it uses the interface name
  -Some error handler routes to deal with the errors

There are no mongodb init script, so the servers need to be initialized by hand before trying to use any route of the application. 

Thank you!
