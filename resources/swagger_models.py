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


class Login(Schema):
    type = 'object'
    description = 'Must provide these when loggin in'
    properties = {
        'email': {
            'type': 'string'
        },
        'password': {
            'type': 'string'
        },
    }
    required = ['email', 'password']


class Institution(Schema):
    type = 'object'
    description = 'Must provide these when creating new institution'
    properties = {
        'name': {
            'type': 'string'
        },
        'city': {
            'type': 'string'
        },
        'address': {
            'type': 'string'
        },
        'contact_number': {
            'type': 'string'
        },
    }
    required = ['name', 'city', 'address', 'contact_number']


class Role(Schema):
    type = 'object'
    description = 'Must provide these when creating new role'
    properties = {
        'title': {
            'type': 'string'
        },
    }
    required = ['title']


class UserRole(Schema):
    type = 'object'
    description = 'Must provide these when adding role to an user'
    properties = {
        'role_id': {
            'type': 'integer'
        },
        'user_id': {
            'type': 'integer'
        },
    }
    required = ['role_id', 'user_id']


class Group(Schema):
    type = 'object'
    description = 'Must provide these when creating new group'
    properties = {
        'name': {
            'type': 'string'
        },
    }
    required = ['name']


class UserGroup(Schema):
    type = 'object'
    description = 'Must provide these when adding group to an user'
    properties = {
        'group_id': {
            'type': 'integer'
        },
        'user_id': {
            'type': 'integer'
        },
    }
    required = ['group_id', 'user_id']


class Activity(Schema):
    type = 'object'
    description = 'Must provide these when editing user\'s activity'
    properties = {
        'sleep': {
            'type': 'integer'
        },
        'food_scale': {
            'type': 'integer'
        },
    }
    required = ['sleep', 'food_scale']


class DishMenu(Schema):
    type = 'object'
    description = 'Must provide these when creating dish menu'
    properties = {
        'date': {
            'type': 'string',
            'format': 'date'
        },
        'institution_id': {
            'type': 'integer'
        },
    }
    required = ['date']


class Dish(Schema):
    type = 'object'
    description = 'Must provide these when creating dish'
    properties = {
        'name': {
            'type': 'string'
        },
        'description': {
            'type': 'string'
        },
        'type': {
            'type': 'string'
        },
        'institution_id': {
            'type': 'integer'
        },
        'dishMenu_id': {
            'type': 'integer'
        },
        'is_alternative': {
            'type': 'integer'
        }
    }
    required = ['name', 'type', 'institution_id',
                'dishMenu_id', 'is_alternative']


class Conversation(Schema):
    type = 'object'
    description = 'Must provide these when creating new conversation'
    properties = {
        'user_one': {
            'type': 'integer'
        },
        'user_two': {
            'type': 'integer'
        },
    }
    required = ['user_one', 'user_two']


class ConversationReply(Schema):
    type = 'object'
    description = 'Must provide these when creating new reply'
    properties = {
        'reply': {
            'type': 'string'
        },
        'reply_user_id': {
            'type': 'integer'
        },
        'conv_id': {
            'type': 'integer'
        },
    }
    required = ['reply', 'reply_user_id', 'conv_id']
