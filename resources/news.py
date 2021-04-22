from flask import Response, request, jsonify, make_response, json
from database.models import News, NewsCategory, Institution, Image, User
from .schemas import NewsSchema, NewsCategorySchema
from database.db import db
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_restful_swagger_2 import Api, swagger, Resource, Schema
from .swagger_models import News as NewsSwaggerModel
from .swagger_models import NewsCategory as NewsCategorySwaggerModel
from datetime import datetime

news_schema = NewsSchema()
newsM_schema = NewsSchema(many=True)
newsCategory_schema = NewsCategorySchema()
newsCategories_schema = NewsCategorySchema(many=True)

class NewsMApi(Resource):
    @swagger.doc({
        'tags': ['news'],
        'description': 'Returns ALL the news',
        'responses': {
            '200': {
                'description': 'Successfully got all the news',
            }
        }
    })
    def get(self):
        """Return ALL the news"""
        all_news = News.query.all()
        result = news_schema.dump(all_news)
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
        }
    })
    def post(self):
        """Add a new news"""
        title = request.json['title']
        details = request.json['details']
        status = request.json['status']
        view_count = request.json['view_count']
        category_id = request.json['category_id']
        institution_id = request.json['institution_id']
        author_id = request.json['author_id']
        image_id = request.json['image_id']

        created_at = db.func.current_timestamp()
        updated_at = db.func.current_timestamp()

        category = NewsCategory.query.get(category_id)
        if not category:
            return jsonify({'msg': 'News category does not exist'})

        institution = Institution.query.get(institution_id)
        if not institution:
            return jsonify({'msg': 'Institution does not exist'})

        author = User.query.get(author_id)
        if not author:
            return jsonify({'msg': 'Author/User does not exist'})

        image = Image.query.get(image_id)
        if not image:
            return jsonify({'msg': 'Image does not exist'})

        new_news = News(title, details, status, view_count, created_at, updated_at, category_id, institution_id, author_id, image_id)

        db.session.add(new_news)
        db.session.commit()

        return news_schema.jsonify(new_news)


class NewsApi(Resource):

    # GET single news with given id
    def get(self, id):
        single_news = News.query.get(id)

        if not single_news:
            return jsonify({'msg': 'No news found'})

        return news_schema.jsonify(single_news)

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
        news = news.query.get(id)

        if not news:
            return jsonify({'msg': 'No news found'})

        title = request.json['title']
        details = request.json['details']
        status = request.json['status']
        view_count = request.json['view_count']
        category_id = request.json['category_id']
        institution_id = request.json['institution_id']
        author_id = request.json['author_id']
        image_id = request.json['image_id']

        updated_at = db.func.current_timestamp()

        category = NewsCategory.query.get(category_id)
        if not category:
            return jsonify({'msg': 'News category does not exist'})

        institution = Institution.query.get(institution_id)
        if not institution:
            return jsonify({'msg': 'Institution does not exist'})

        author = User.query.get(author_id)
        if not author:
            return jsonify({'msg': 'Author/User does not exist'})

        image = Image.query.get(image_id)
        if not image:
            return jsonify({'msg': 'Image does not exist'})

        news.title = title
        news.details = details
        news.status = status
        news.view_count = view_count
        news.category_id = category_id
        news.institution_id = institution_id
        news.author_id = author_id
        news.image_id = image_id
        news.updated_at =updated_at

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
        news = db.session.query(news).filter(News.id == id).first()
        if not news:
            return jsonify({'msg': 'No news found'})
        db.session.delete(news)
        db.session.commit()

        return jsonify({"msg": "Successfully deleted news"})

class NewsCategoriesApi(Resource):
    @swagger.doc({
        'tags': ['newsCategory'],
        'description': 'Returns ALL the news categories',
        'responses': {
            '200': {
                'description': 'Successfully got all the news categories',
            }
        }
    })
    def get(self):
        """Return ALL the news categories"""
        all_newsCategories = NewsCategory.query.all()
        result = newsCategories_schema.dump(all_newsCategories)
        return jsonify(result)

    @swagger.doc({
        'tags': ['newsCategory'],
        'description': 'Adds a new newsCategory',
        'parameters': [
            {
                'name': 'Body',
                'in': 'body',
                'schema': NewsCategorySwaggerModel,
                'type': 'object',
                'required': 'true'
            },
        ],
        'responses': {
            '200': {
                'description': 'Successfully added new news category',
            }
        }
    })
    def post(self):
        """Add a new news category"""
        name = request.json['name']
        created_at = db.func.current_timestamp()
        updated_at = db.func.current_timestamp()

        new_newsCategory = NewsCategory(name, created_at, updated_at)

        db.session.add(new_newsCategory)
        db.session.commit()

        return newsCategory_schema.jsonify(new_newsCategory)

class NewsCategoryApi(Resource):
    # GET single news category with given id
    def get(self, id):
        single_newsCategory = NewsCategory.query.get(id)

        if not single_newsCategory:
            return jsonify({'msg': 'No news category found'})

        return newsCategory_schema.jsonify(single_newsCategory)

    @swagger.doc({
        'tags': ['newsCategory'],
        'description': 'Updates a news category',
        'parameters': [
            {
                'name': 'Body',
                'in': 'body',
                'schema': NewsCategorySwaggerModel,
                'type': 'object',
                'required': 'true'
            },
            {
                'name': 'id',
                'in': 'path',
                'description': 'News category identifier',
                'type': 'integer'
            }
        ],
        'responses': {
            '200': {
                'description': 'Successfully updated a news category',
            }
        }
    })
    def put(self, id):
        """Update news category"""
        newsCategory = NewsCategory.query.get(id)

        if not newsCategory:
            return jsonify({'msg': 'No news category found'})

        name = request.json['name']
        updated_at = db.func.current_timestamp()

        newsCategory.name = name
        newsCategory.updated_at = updated_at

        db.session.commit()
        return newsCategory_schema.jsonify(newsCategory)

    @swagger.doc({
        'tags': ['newsCategory'],
        'description': 'Deletes a news category',
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
                'description': 'Successfully deleted news category',
            }
        }
    })
    def delete(self, id):
        """Delete news category"""
        newsCategory = db.session.query(NewsCategory).filter(NewsCategory.id == id).first()
        if not newsCategory:
            return jsonify({'msg': 'No news category found'})
        db.session.delete(newsCategory)
        db.session.commit()

        return jsonify({"msg": "Successfully deleted news category"})