import json
import time
import unittest
import flask_restful
from flask import Flask

from tests.test_base import TestBase


class TestImages(TestBase):

    def test_get_unauthorized_image_route(self):
        response = self.app.get('/image')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(data['msg'], "Missing Authorization Header")
        self.assertEqual(401, response.status_code)

    def test_get_authorized_image_route(self):
        response = self.app.get('/image', headers=self.header)

        self.assertEqual(200, response.status_code)
