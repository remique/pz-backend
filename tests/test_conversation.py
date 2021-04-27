import json
import time
import unittest
import flask_restful
from flask import Flask

from tests.test_base import TestBase


class TestConversations(TestBase):

    def test_get_unauthorized_conversation_route(self):
        response = self.app.get('/conversation')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(data['msg'], "Missing Authorization Header")
        self.assertEqual(401, response.status_code)

    def test_get_conversation_route(self):
        response = self.app.get('/conversation', headers=self.header)

        self.assertEqual(200, response.status_code)

    def test_add_conversation(self):
        # Create second user
        user_data = {
            "email": "string",
            "password": "string",
            "firstname": "string",
            "surname": "string",
            "sex": 0,
            "active": 0,
            "institution_id": 1
        }
        post_user = self.app.post(
            '/user',
            data=json.dumps(user_data),
            content_type='application/json',
            headers=self.header
        )
        self.assertEqual(200, post_user.status_code)

        # Prepare conversation
        conversation_data = {
            "user_two": 2
        }

        conversation_result = self.app.post(
            '/conversation',
            data=json.dumps(conversation_data),
            content_type='application/json',
            headers=self.header
        )
        self.assertEqual(200, conversation_result.status_code)
