from flask import Response, request, jsonify, make_response, json
from database.models import User, Activity, Role, Attendance, Image
from .schemas import UserGetSchema, UserTokenSchema, UserHomeSchema
from database.db import db
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, current_user, create_refresh_token, get_jwt
)
from flask_restful_swagger_2 import Api, swagger, Resource, Schema
from .swagger_models import User as UserSwaggerModel
from flask_sqlalchemy import SQLAlchemy
from .security import generate_salt, generate_hash
from datetime import datetime, timedelta

import math

user_home_schema = UserHomeSchema(many=True)


class HomeStatsApi(Resource):
    @swagger.doc({
        'tags': ['home'],
        'description': '''This endpoint is requested everytime user \
                loads the homepage. It returns: \
                \n * `teachers`: How many teachers are there in an institution \
                \n * `children`: How many children are \
                there in an institution \
                \n * `new_users`: Last 5 users created in an institution \
                \n * `images`: How many photos are there overall \
                in an institution \
                \n * `absence`: Returns the count of absent users in the \
                last seven days''',
        'responses': {
            '200': {
                'description': 'Successfully got all the users',
            }
        },
        'security': [
            {
                'api_key': []
            }
        ]
    })
    @ jwt_required()
    def get(self):
        """Return home stats"""
        claims = get_jwt()
        user_institution_id = claims['institution_id']

        teacher_role = Role.query.filter(Role.title == "Teacher").first()
        child_role = Role.query.filter(Role.title == "Child").first()

        num_of_teachers = User.query\
            .filter(User.roles.any(id=teacher_role.id))\
            .filter(User.institution_id == user_institution_id)\
            .count()

        num_of_children = User.query\
            .filter(User.roles.any(id=child_role.id))\
            .filter(User.institution_id == user_institution_id)\
            .count()

        new_users = User.query\
            .filter(User.institution_id == user_institution_id)\
            .order_by(User.id.desc())\
            .limit(5)\
            .all()

        last_seven_days = [datetime.today() - timedelta(days=i)
                           for i in range(1, 7)]

        attendances = []
        for day in last_seven_days:
            count = 0
            day_str = day.strftime("%Y-%m-%d")
            day_query = Attendance.query\
                .filter(Attendance.date == day_str)\
                .filter(Attendance.present == 0).all()

            # Check if user belongs to current institution_id
            for query in day_query:
                user = User.query\
                    .filter(User.id == query.user_id).first()

                if user is not None:
                    count += 1

            absent_json = {
                "day": day_str,
                "absent": count
            }

            attendances.append(absent_json)

        all_photos = Image.query\
            .filter(Image.institution_id == user_institution_id).count()

        new_users_result = user_home_schema.dump(new_users)

        result = {
            "teachers": num_of_teachers,
            "children": num_of_children,
            "new_users": new_users_result,
            "images": all_photos,
            "absence": attendances,
        }

        return jsonify(result)
