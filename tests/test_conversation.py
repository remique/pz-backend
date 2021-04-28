import json
import time
import unittest
import flask_restful
from flask import Flask

from tests.test_base import TestBase

# Tests for endpoints:
# - /conversation
# - /conversation_reply
# - /search_user


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

    def test_add_conversation_user_not_exists(self):
        conversation_data = {
            "user_two": 50
        }

        convo_query = self.app.post(
            '/conversation',
            data=json.dumps(conversation_data),
            content_type='application/json',
            headers=self.header
        )
        data = json.loads(convo_query.get_data(as_text=True))

        self.assertEqual(data['msg'], "User with given id does not exist")
        self.assertEqual(200, convo_query.status_code)

    def test_conversation_aleady_exists(self):
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

        conversation_data = {
            "user_two": 2
        }

        self.app.post(
            '/conversation',
            data=json.dumps(conversation_data),
            content_type='application/json',
            headers=self.header
        )

        second_query = self.app.post(
            '/conversation',
            data=json.dumps(conversation_data),
            content_type='application/json',
            headers=self.header
        )
        data = json.loads(second_query.get_data(as_text=True))

        self.assertEqual(data['msg'], "Conversation already exists")
        self.assertEqual(200, second_query.status_code)

    def test_add_conversation_with_yourself(self):
        conversation_data = {
            "user_two": 1
        }

        query = self.app.post(
            '/conversation',
            data=json.dumps(conversation_data),
            content_type='application/json',
            headers=self.header
        )
        data = json.loads(query.get_data(as_text=True))

        self.assertEqual(
            data['msg'], "Could not make conversation with the same user")
        self.assertEqual(200, query.status_code)

    def test_search_valid_user(self):
        search_data = {
            "name_like": "testuser"
        }

        query = self.app.post(
            '/search_user',
            data=json.dumps(search_data),
            content_type='application/json',
            headers=self.header
        )

        self.assertEqual(200, query.status_code)

    def test_search_not_existing_user(self):
        search_data = {
            "name_like": "asdfjhalkjdsghalkjshdg"
        }

        query = self.app.post(
            '/search_user',
            data=json.dumps(search_data),
            content_type='application/json',
            headers=self.header
        )
        data = json.loads(query.get_data(as_text=True))

        self.assertEqual(
            data['msg'], "No matching names")
        self.assertEqual(200, query.status_code)

    def test_get_unauthorized_conversation_reply_route(self):
        response = self.app.get('/conversation_reply/1')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(data['msg'], "Missing Authorization Header")
        self.assertEqual(401, response.status_code)

    def test_get_conversation_reply_route(self):
        response = self.app.get('/conversation_reply/1', headers=self.header)

        self.assertEqual(200, response.status_code)

    def test_add_conversation_reply(self):
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

        reply_data = {
            "reply": "string",
            "conv_id": 1
        }

        reply_result = self.app.post(
            '/conversation_reply',
            data=json.dumps(reply_data),
            content_type='application/json',
            headers=self.header
        )

        self.assertEqual(200, reply_result.status_code)
