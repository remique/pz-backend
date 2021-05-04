import json
import time
import unittest
import flask_restful
from flask import Flask

from tests.test_base import TestBase


class TestActivities(TestBase):

    def test_get_unauthorized_activity_route(self):
        response = self.app.get('/activity')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(data['msg'], "Missing Authorization Header")
        self.assertEqual(401, response.status_code)

    def test_get_authorized_activity_route(self):
        response = self.app.get('/activity', headers=self.header)
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(200, response.status_code)

    def test_get_activity_all_json(self):
        user_data = {
            "email": "string",
            "password": "string",
            "firstname": "string",
            "surname": "string",
            "sex": 0,
            "active": 0,
            "institution_id": 1
        }
        result = self.app.post(
            '/user',
            data=json.dumps(user_data),
            content_type='application/json',
            headers=self.header
        )

        response = self.app.get('/activity', headers=self.header)
        data = json.loads(response.get_data(as_text=True))

        expected = [
            {
                'id': 1,
                'sleep': 0,
                'food_scale': 0,
                'user_id': 2,
            }
        ]

        self.assertEqual(200, response.status_code)
        self.assertEqual(data, expected)

    def test_get_activity_only_institution(self):
        user_data = {
            "email": "another_one",
            "password": "string",
            "firstname": "string",
            "surname": "string",
            "sex": 0,
            "active": 0
        }
        result = self.app.post(
            '/user',
            data=json.dumps(user_data),
            content_type='application/json',
            headers=self.header
        )

        response = self.app.get(
            '/activity?only_institution=true', headers=self.header)
        data = json.loads(response.get_data(as_text=True))

        expected = [
            {
                'id': 1,
                'sleep': 0,
                'food_scale': 0,
                'user_id': 2,
            }
        ]

        self.assertEqual(200, response.status_code)
        self.assertEqual(data, expected)

    def test_update_activity(self):
        user_data = {
            "email": "another_one",
            "password": "string",
            "firstname": "string",
            "surname": "string",
            "sex": 0,
            "active": 0
        }
        user_create = self.app.post(
            '/user',
            data=json.dumps(user_data),
            content_type='application/json',
            headers=self.header
        )

        self.assertEqual(200, user_create.status_code)

        update_data = {
            "sleep": 1,
            "food_scale": 2
        }

        update_activity = self.app.put(
            '/activity/2',
            data=json.dumps(update_data),
            content_type='application/json',
            headers=self.header
        )

        self.assertEqual(200, update_activity.status_code)

        response = self.app.get(
            '/activity', headers=self.header)
        data = json.loads(response.get_data(as_text=True))

        expected = [{
            'id': 1,
            'sleep': 1,
            'food_scale': 2,
            'user_id': 2
        }]

        self.assertEqual(200, response.status_code)
        self.assertEqual(data, expected)
