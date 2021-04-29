from flask import Response, request, jsonify, make_response, json
from database.models import Attendance, User
from .schemas import AttendanceSchema
from database.db import db
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_restful_swagger_2 import Api, swagger, Resource, Schema
from .swagger_models import Attendance as AttendanceSwaggerModel
from datetime import datetime

attendance_schema = AttendanceSchema()
attendanceM_schema = AttendanceSchema(many=True)


class AttendanceMApi(Resource):
    @swagger.doc({
        'tags': ['attendance'],
        'description': 'Returns ALL the attendances',
        'responses': {
            '200': {
                'description': 'Successfully got all the attendances',
            }
        }
    })
    def get(self):
        """Return ALL the attendances"""
        all_attendances = Attendance.query.all()
        result = attendanceM_schema.dump(all_attendances)
        return jsonify(result)

    @swagger.doc({
        'tags': ['attendance'],
        'description': 'Adds a new attendance',
        'parameters': [
            {
                'name': 'Body',
                'in': 'body',
                'schema': AttendanceSwaggerModel,
                'type': 'object',
                'required': 'true'
            },
        ],
        'responses': {
            '200': {
                'description': 'Successfully added new attendance',
            }
        }
    })
    def post(self):
        """Add a new attendance"""
        date_str = request.json['date']
        present = request.json['present']
        user_id = request.json['user_id']

        user = User.query.get(user_id)
        if not user:
            return jsonify({'msg': 'User does not exist'})

        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        new_attendance = Attendance(date, present, user_id)

        db.session.add(new_attendance)
        db.session.commit()

        return attendance_schema.jsonify(new_attendance)


class AttendanceApi(Resource):

    # GET single attendance with given id
    def get(self, id):
        single_attendance = Attendance.query.get(id)

        if not single_attendance:
            return jsonify({'msg': 'No attendance found'})

        return attendance_schema.jsonify(single_attendance)

    @swagger.doc({
        'tags': ['attendance'],
        'description': 'Updates an attendance',
        'parameters': [
            {
                'name': 'Body',
                'in': 'body',
                'schema': AttendanceSwaggerModel,
                'type': 'object',
                'required': 'true'
            },
            {
                'name': 'id',
                'in': 'path',
                'description': 'Attendance identifier',
                'type': 'integer'
            }
        ],
        'responses': {
            '200': {
                'description': 'Successfully updated an attendance',
            }
        }
    })
    def put(self, id):
        """Update attendance"""
        attendance = Attendance.query.get(id)

        date_str = request.json['date']
        present = request.json['present']
        user_id = request.json['user_id']

        user = User.query.get(user_id)
        if not user:
            return jsonify({'msg': 'User does not exist'})

        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        attendance.date = date
        attendance.present = present
        attendance.user_id = user_id

        db.session.commit()
        return attendance_schema.jsonify(attendance)

    @swagger.doc({
        'tags': ['attendance'],
        'description': 'Deletes an attendance',
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': 'true',
                'type': 'integer',
                'schema': {
                    'type': 'integer'
                }
            }
        ],
        'responses': {
            '200': {
                'description': 'Successfully deleted an attendance',
            }
        }
    })
    def delete(self, id):
        """Delete attendance"""
        attendance = db.session.query(Attendance).filter(
            Attendance.id == id).first()
        db.session.delete(attendance)
        db.session.commit()

        return jsonify({'msg': 'Successfully removed attendance'})
