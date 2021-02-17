from flask_restful_swagger_2 import Api, Schema


class User(Schema):
    type = 'object'
    description = 'Must provide these when creating new user'
    properties = {
        'email': {
            'type': 'string'
        },
        'password': {
            'type': 'string'
        },
        'firstname': {
            'type': 'string'
        },
        'surname': {
            'type': 'string'
        },
        'sex': {
            'type': 'integer',
        },
        'active': {
            'type': 'integer',
        },
    }
    required = ['email', 'password', 'firstname', 'surname', 'sex', 'active']
