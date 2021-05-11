import json
import time
import unittest
import flask_restful
from flask import Flask

from tests.test_base import TestBase


class TestDishes(TestBase):

    def test_get_unauthorized_dish_route(self):
        response = self.app.get('/dish')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(data['msg'], "Missing Authorization Header")
        self.assertEqual(401, response.status_code)

    def test_get_user_route(self):
        response = self.app.get('/dish', headers=self.header)

        self.assertEqual(200, response.status_code)

    def test_add_dish_unauthorized(self):
        data = {
            "name": "string",
            "description": "string",
            "type": "string",
            "is_alternative": 0
        }

        result = self.app.post(
            '/dish',
            data=json.dumps(data),
            content_type='application/json',
        )
        get_msg = json.loads(result.get_data(as_text=True))

        self.assertEqual(get_msg['msg'], "Missing Authorization Header")
        self.assertEqual(401, result.status_code)

    def test_add_dish_authorized(self):
        data = {
            "name": "string",
            "description": "string",
            "type": "string",
            "is_alternative": 0
        }

        result = self.app.post(
            '/dish',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.header
        )

        self.assertEqual(200, result.status_code)

    def test_add_dish_already_exists(self):
        data = {
            "name": "string",
            "description": "string",
            "type": "string",
            "is_alternative": 0
        }
        self.app.post(
            '/dish',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.header
        )

        result = self.app.post(
            '/dish',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.header
        )

        get_msg = json.loads(result.get_data(as_text=True))

        self.assertEqual(get_msg['msg'], "Dish with this name already exists")

    def test_delete_dish_unauthorized(self):
        response = self.app.delete('/dish/1')
        get_msg = json.loads(response.get_data(as_text=True))

        self.assertEqual(get_msg['msg'], "Missing Authorization Header")
        self.assertEqual(401, response.status_code)

    def test_delete_dish_authorized(self):
        # First POST
        data = {
            "name": "string",
            "description": "string",
            "type": "string",
            "is_alternative": 0
        }
        result = self.app.post(
            '/dish',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.header
        )
        self.assertEqual(200, result.status_code)

        # Then DELETE
        response = self.app.delete('/dish/1', headers=self.header)
        get_msg = json.loads(response.get_data(as_text=True))

        self.assertEqual(get_msg['msg'], "Successfully deleted dish")
        self.assertEqual(200, response.status_code)

    def test_put_dish_unauthorized(self):
        response = self.app.put('/dish/1')
        get_msg = json.loads(response.get_data(as_text=True))

        self.assertEqual(get_msg['msg'], "Missing Authorization Header")
        self.assertEqual(401, response.status_code)

    def test_put_no_dish_found(self):
        data = {
            "name": "string",
            "description": "string",
            "type": "string",
            "is_alternative": 0
        }
        result = self.app.put(
            '/dish/1',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.header
        )
        get_msg = json.loads(result.get_data(as_text=True))

        self.assertEqual(get_msg['msg'], "No dish found")
        self.assertEqual(200, result.status_code)

    def test_put_dish_authorized(self):
        # First POST
        data = {
            "name": "string",
            "description": "string",
            "type": "string",
            "is_alternative": 0
        }
        result = self.app.post(
            '/dish',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.header
        )
        self.assertEqual(200, result.status_code)

        # Then PUT
        second_data = {
            "name": "string_changed",
            "description": "string",
            "type": "string",
            "is_alternative": 0
        }
        second_result = self.app.put(
            '/dish/1',
            data=json.dumps(second_data),
            content_type='application/json',
            headers=self.header
        )
        get_msg = json.loads(second_result.get_data(as_text=True))

        self.assertEqual(200, second_result.status_code)
        self.assertEqual(get_msg['name'], "string_changed")
