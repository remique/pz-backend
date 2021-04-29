import json
import time
import unittest
import flask_restful
from flask import Flask

from tests.test_base import TestBase


class TestNews(TestBase):

    def test_get_unauthorized_news_route(self):
        response = self.app.get('/news')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(data['msg'], "Missing Authorization Header")
        self.assertEqual(401, response.status_code)

    def test_get_authorized_news_route(self):
        response = self.app.get('/news', headers=self.header)

        self.assertEqual(200, response.status_code)

    def test_add_authorized_news(self):
        post_data = {
            "title": "Jakiś post",
            "details": "Tutaj jest jakiś dłuuuugi opis.",
            "priority": 'true'
        }

        result = self.app.post(
            '/news',
            data=json.dumps(post_data),
            content_type='application/json'
        )
        data = json.loads(result.get_data(as_text=True))

        self.assertEqual(data['msg'], "Missing Authorization Header")
        self.assertEqual(401, result.status_code)

    def test_add_news_authorized(self):
        data = {
            "title": "Jakiś post",
            "details": "Tutaj jest jakiś dłuuuugi opis.",
            "priority": 'true'
        }

        result = self.app.post(
            '/news',
            data=json.dumps(data),
            content_type='application/json',
            headers=self.header
        )
        self.assertEqual(200, result.status_code)
