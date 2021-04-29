from flask import Response, request, jsonify, make_response, json
from database.models import News, Institution, Image, User
from .schemas import NewsSchema
from database.db import db
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt
)
from flask_restful_swagger_2 import Api, swagger, Resource, Schema
from .swagger_models import News as NewsSwaggerModel
from datetime import datetime
import math

news_schema = NewsSchema()
newsM_schema = NewsSchema(many=True)


class NewsMApi(Resource):
    @swagger.doc({
        'tags': ['news'],
        'description': 'Returns ALL the news',
        'responses': {
            '200': {
                'description': 'Successfully got all the news',
            }
        },
        'parameters': [
            {
                'name': 'page',
                'in': 'query',
                'type': 'integer',
                'description': '*Optional*: Which page to return'
            },
            {
                'name': 'per_page',
                'in': 'query',
                'type': 'integer',
                'description': '*Optional*: How many users to return per page'
            },
        ],
        'security': [
            {
                'api_key': []
            }
        ]
    })
    @jwt_required()
    def get(self):
        """Return ALL the news"""
        claims = get_jwt()
        user_institution_id = claims['institution_id']

        news_total = News.query.filter(
            News.institution_id == user_institution_id).count()

        MIN_PER_PAGE = 5
        MAX_PER_PAGE = 30

        page = request.args.get('page')
        per_page = request.args.get('per_page')

        if page is None or int(page) < 1:
            page = 1

        if per_page is None:
            per_page = 15

        if int(per_page) < MIN_PER_PAGE:
            per_page = MIN_PER_PAGE

        if int(per_page) > MAX_PER_PAGE:
            per_page = MAX_PER_PAGE

        last_page = math.ceil(int(news_total) / int(per_page))

        if int(page) >= last_page:
            page = int(last_page)

        page_offset = (int(page) - 1) * int(per_page)

        news_query = News.query.filter(News.institution_id == user_institution_id).order_by(News.created_at.desc()).offset(
            page_offset).limit(per_page).all()
        query_result = newsM_schema.dump(news_query)

        result = {
            "total": news_total,
            "per_page": int(per_page),
            "current_page": int(page),
            "last_page": last_page,
            "data": query_result
        }

        return jsonify(result)

    @swagger.doc({
        'tags': ['news'],
        'description': 'Adds a new news',
        'parameters': [
            {
                'name': 'Body',
                'in': 'body',
                'schema': NewsSwaggerModel,
                'type': 'object',
                'required': 'true'
            },
        ],
        'responses': {
            '200': {
                'description': 'Successfully added new news',
            }
        },
        'security': [
            {
                'api_key': []
            }
        ]
    })
    @jwt_required()
    def post(self):
        """Add a new news"""
        claims = get_jwt()
        user_institution_id = claims['institution_id']
        user_id = claims['id']

        title = request.json['title']
        details = request.json['details']
        priority = request.json['priority']
        institution_id = user_institution_id
        author_id = user_id

        created_at = db.func.current_timestamp()
        updated_at = db.func.current_timestamp()

        institution = Institution.query.get(institution_id)
        if not institution:
            return jsonify({'msg': 'Institution does not exist'})

        author = User.query.get(author_id)
        if not author:
            return jsonify({'msg': 'Author/User does not exist'})

        new_news = News(title, details, priority, created_at,
                        updated_at, institution_id, author_id)

        db.session.add(new_news)
        db.session.commit()

        return news_schema.jsonify(new_news)


class NewsApi(Resource):
    @swagger.doc({
        'tags': ['news'],
        'description': 'Updates an news',
        'parameters': [
            {
                'name': 'Body',
                'in': 'body',
                'schema': NewsSwaggerModel,
                'type': 'object',
                'required': 'true'
            },
            {
                'name': 'id',
                'in': 'path',
                'description': 'News identifier',
                'type': 'integer'
            }
        ],
        'responses': {
            '200': {
                'description': 'Successfully updated a news',
            }
        }
    })
    def put(self, id):
        """Update news"""
        news = News.query.get(id)

        if not news:
            return jsonify({'msg': 'No news found'})

        title = request.json['title']
        details = request.json['details']
        priority = request.json['priority']
        institution_id = request.json['institution_id']
        author_id = request.json['author_id']

        updated_at = db.func.current_timestamp()

        institution = Institution.query.get(institution_id)
        if not institution:
            return jsonify({'msg': 'Institution does not exist'})

        author = User.query.get(author_id)
        if not author:
            return jsonify({'msg': 'Author/User does not exist'})

        news.title = title
        news.details = details
        news.priority = priority
        news.institution_id = institution_id
        news.author_id = author_id
        news.updated_at = updated_at

        db.session.commit()
        return news_schema.jsonify(news)

    @swagger.doc({
        'tags': ['news'],
        'description': 'Deletes a news',
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
                'description': 'Successfully deleted news',
            }
        }
    })
    def delete(self, id):
        """Delete news"""
        news = db.session.query(News).filter(News.id == id).first()
        if not news:
            return jsonify({'msg': 'No news found'})
        db.session.delete(news)
        db.session.commit()

        return jsonify({"msg": "Successfully deleted news"})

