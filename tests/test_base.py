import json
import time
import unittest
import flask_restful
from flask import Flask
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, current_user, get_jwt
)

from database.db import db, init_db
from resources.schemas import UserTokenSchema

from app import create_app
import config

user_token_schema = UserTokenSchema()


class TestBase(unittest.TestCase):

    def setUp(self):
        app = create_app('config.TestingConfig')
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

        # Hardcode testuser
        testuser = {
            "id": 1,
            "email": "testuser",
            "password": "015cbc70f1481cc3d30ed906e681f2e6f06cf060e4b09ba2adbffa75bddc8283",
            "salt": "jvP3wwmGV0fqfdh9o6XtkQ==",
            "firstname": "string",
            "surname": "string",
            "institution_id": 1,
            "sex": 0,
            "active": 0,
            "created_at": "2021-04-22T18:39:00",
            "updated_at": "2021-04-22T18:39:00",
            "roles": []
        }

        # Add testuser claims to the token
        testuser_claims = user_token_schema.dump(testuser)

        # Create access token
        access_token = create_access_token(
            identity=testuser, additional_claims=testuser_claims)

        # Add token to the header
        self.header = {
            'Authorization': 'Bearer {}'.format(access_token)
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()

        self.app_context.pop()
        pass
