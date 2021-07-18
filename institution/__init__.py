from flask import Flask, Blueprint, request, make_response, send_file
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import config
from flask import jsonify
import json
from datetime import datetime
import random
import string
from gridfs import GridFS

jwt = config.jwt
mongo = config.mongo


institution = Blueprint('institution', __name__, url_prefix='/institution')


@institution.route('/create', methods=['POST'])
@jwt_required()
def create():
    name = request.json.get('name')
    country = request.json.get('country')
    region = request.json.get('region')
    city = request.json.get('city')
    street = request.json.get('street')
    number = request.json.get('number')
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    institutions = mongo.db.institutions
    institutions.insert({'name': name, 'country': country, 'region': region, 'city': city, 'street': street, 'number': number, 'owner': user['_id'], 'users': [], 'roles': []})

    return {
        'create': '0'
    }


@institution.route('/delete', methods=['DELETE'])
@jwt_required()
def delete():
    id_institution = request.json.get('institution')
    
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    institutions = mongo.db.institutions
    obj_institution = ObjectId(id_institution)
    current_institution = institutions.find_one({'_id': obj_institution})
    if current_institution is not None:
        if user['_id'] == current_institution['owner']:
            subjects = mongo.db.subjects
            institutions = mongo.db.institutions

            allSubjects = subjects.find({'institution': current_institution['_id']})
            for subject in allSubjects:
                # delete subject data
                deleteSubjectData(str(subject['_id']))
            
            # subjects from institution are deleted
            subjects.delete_many({'institution': obj_institution})

             # institution is deleted
            institutions.delete_one({'_id': obj_institution})  
            return {
                'delete': '0'
            }
        else:
            # user is not the owner of the institution
            return {
            'delete': '1'
        }
    else:
        # institution id is invalid
        return {
            'delete': '1'
        }


@institution.route('/getInstitutionInfo', methods=['POST'])
@jwt_required()
def getInstitutionInfo():
    id_institution = request.json.get('institution')
    
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    institutions = mongo.db.institutions
    obj_institution = ObjectId(id_institution)
    current_institution = institutions.find_one({'_id': obj_institution})

    if(current_institution['owner'] == user['_id']):
        role = "owner"
    else:
        role = "user"

    isIn = isInInstitution(id_institution, str(user['_id']))

    if current_institution is not None:
        return {
            'ok': '0',
            'name': current_institution['name'], 
            'country': current_institution['country'], 
            'region': current_institution['region'], 
            'city': current_institution['city'], 
            'street': current_institution['street'], 
            'number': current_institution['number'],
            'role': role,
            'isIn': isIn
        }
    else:
        return {
            'ok': '1'
        }


@institution.route('/editInstitutionInfo', methods=['POST'])
@jwt_required()
def editInstitutionInfo():
    id_institution = request.json.get('id')
    name = request.json.get('name')
    country = request.json.get('country')
    region = request.json.get('region')
    city = request.json.get('city')
    street = request.json.get('street')
    number = request.json.get('number')
    
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    institutions = mongo.db.institutions
    mycol = mongo.db["institutions"]
    obj_institution = ObjectId(id_institution)
    current_institution = institutions.find_one({'_id': obj_institution})

    if current_institution is not None:
        if(current_institution['owner'] != user['_id']):
            return {
                'ok': '1',
            }
        edited_institution = { "$set": { "name": name, "country": country, "region": region, "city": city, "street": street, "number": number } }
        mycol.update_one(current_institution, edited_institution)
        return {
            'ok': '0',
        }
    else:
        return {
            'ok': '1'
        }


@institution.route('/getSubjectInfo', methods=['POST'])
@jwt_required()
def getSubjectInfo():
    id_subject = request.json.get('subject')
    
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    subjects = mongo.db.subjects
    obj_subject = ObjectId(id_subject)
    current_subject = subjects.find_one({'_id': obj_subject})

    if current_subject is not None:
        isTeacher = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'teachers': user['_id']}]}).count()
        if isTeacher > 0:
            role = "teacher"
        else:
            role = "user"

        isIn = isInSubject(id_subject, str(user['_id']))

        return {
            'ok': '0',
            'name': current_subject['name'], 
            'public': current_subject['public'], 
            'message': current_subject['message'],
            'image': current_subject['image'],
            'role': role,
            'isIn': isIn
        }
    else:
        return {
            'ok': '1'
        }


@institution.route('/editSubjectInfo', methods=['POST'])
@jwt_required()
def editSubjectInfo():
    id_subject = request.json.get('id')
    name = request.json.get('name')
    public = request.json.get('public')
    message = request.json.get('message')
    
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    subjects = mongo.db.subjects
    mycol = mongo.db["subjects"]
    obj_subject = ObjectId(id_subject)
    current_subject = subjects.find_one({'_id': obj_subject})

    if current_subject is not None:
        isTeacher = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'teachers': user['_id']}]}).count()
        if isTeacher == 0:
            return {
                'ok': 'You are not a teacher!'
                } 
        edited_subject = { "$set": { "name": name, "public": public, "message": message } }
        mycol.update_one(current_subject, edited_subject)
        return {
            'ok': '0',
        }
    else:
        return {
            'ok': '1'
        }


@institution.route('/editSubjectImage', methods=['POST'])
@jwt_required()
def editSubjectImage():
    id_subject = request.json.get('id')
    image = request.json.get('image')
    
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    subjects = mongo.db.subjects
    mycol = mongo.db["subjects"]
    obj_subject = ObjectId(id_subject)
    current_subject = subjects.find_one({'_id': obj_subject})

    if current_subject is not None:   
        isTeacher = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'teachers': user['_id']}]}).count()
        if isTeacher == 0:
            return {
                'ok': 'You are not a teacher!'
                } 
        edited_subject = { "$set": { "image": image } }
        mycol.update_one(current_subject, edited_subject)
        return {
            'ok': '0',
        }
    else:
        return {
            'ok': '1'
        }
        

@institution.route('/allInstitutions', methods=['POST'])
@jwt_required()
def allInstitutions():
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    pageNumber = request.json.get('pageNumber')
    pageNr = int(pageNumber)
    nPerPage = 12

    institutions = mongo.db.institutions

    institutionsNr = institutions.find({ "$or": [ { 'owner': user['_id'] }, {'users': user['_id']} ] }).count()
    nr = institutionsNr / nPerPage
    if(int(nr) < nr):
        nrPages = int(nr) + 1
    else:
        nrPages = int(nr)

    page = institutions.find({ "$or": [ { 'owner': user['_id'] }, {'users': user['_id']} ] }).sort('name').skip(nPerPage *(pageNumber-1)).limit(nPerPage)

    institutionsList = []
    for institution in page:
        idInstitution = str(institution['_id'])
        institutionsList.append({ "id": idInstitution, "name": institution['name'] , "city": institution['city'] })

    return {
        'ok': '0',
        'pages': nrPages,
        'institutions': institutionsList
    }

@institution.route('/allSubjects', methods=['POST'])
@jwt_required()
def allSubjects():
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    pageNumber = request.json.get('pageNumber')
    pageNr = int(pageNumber)
    nPerPage = 12

    subjects = mongo.db.subjects

    subjectsNr = subjects.find({ "$or": [ {'teachers': user['_id']}, {'users': user['_id']} ] }).count()
    nr = subjectsNr / nPerPage
    if(int(nr) < nr):
        nrPages = int(nr) + 1
    else:
        nrPages = int(nr)

    page = subjects.find({ "$or": [ {'teachers': user['_id']}, {'users': user['_id']} ] }).sort('name').skip(nPerPage *(pageNumber-1)).limit(nPerPage)
    institutions = mongo.db.institutions
    subjectList = []
    for subject in page:
        idSubject = str(subject['_id'])
        institution = institutions.find_one({'_id': subject['institution']})
        subjectList.append({ "id": idSubject, "name": subject['name'] , "image": subject['image'], "institution": institution['name'] })

    return {
        'ok': '0',
        'pages': nrPages,
        'subjects': subjectList
    }

@institution.route('/allInstitutionSubjects', methods=['POST'])
@jwt_required()
def allInstitutionSubjects():
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    pageNumber = request.json.get('pageNumber')
    id_institution = request.json.get('institution')
    pageNr = int(pageNumber)
    nPerPage = 12

    subjects = mongo.db.subjects

    institutions = mongo.db.institutions
    obj_institution = ObjectId(id_institution)
    institution = institutions.find_one({'_id': obj_institution})
    subjectsNr = subjects.find({"$and":[ { "$or": [ {'teachers': user['_id']}, {'users': user['_id']}]}, {'institution': institution['_id']} ]} ).count()
    nr = subjectsNr / nPerPage
    if(int(nr) < nr):
        nrPages = int(nr) + 1
    else:
        nrPages = int(nr)

    page = subjects.find({"$and":[ { "$or": [ {'teachers': user['_id']}, {'users': user['_id']}]}, {'institution': institution['_id']} ]} ).sort('name').skip(nPerPage *(pageNumber-1)).limit(nPerPage)
    subjectList = []
    for subject in page:
        idSubject = str(subject['_id'])
        subjectList.append({ "id": idSubject, "name": subject['name'] , "image": subject['image'], "institution": institution['name'] })

    if(institution['owner'] == user['_id']):
        role = "owner"
    else:
        role = "user"
    
    isIn = isInInstitution(id_institution, str(user['_id']))

    return {
        'ok': '0',
        'pages': nrPages,
        'subjects': subjectList,
        'institutionName': institution['name'],
        'role': role,
        'isIn': isIn
    }

@institution.route('/pageNumbers', methods=['GET'])
def pageNumbers():
    current_user = 'test'
    users = mongo.db.users
    user = users.find_one({'username': current_user})
    nPerPage = 3

    institutions = mongo.db.institutions
    institutionsNr = institutions.find({ "$or": [ { 'owner': user['_id'] }, {'users': user['_id']} ] }).count()
    nr = institutionsNr / nPerPage
    
    if(int(nr) < nr):
        nrPages = int(nr) + 1
    else:
        nrPages = int(nr)
    
    return{
        'pages': nrPages
    }

@institution.route('/createSubject', methods=['POST'])
@jwt_required()
def createSubject():
    id_institution = request.json.get('institution')
    name = request.json.get('name')
    public = request.json.get('public')
    message = request.json.get('message')

    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    institutions = mongo.db.institutions
    obj_institution = ObjectId(id_institution)
    current_institution = institutions.find_one({'_id': obj_institution})

    if current_institution is not None:
        if user['_id'] == current_institution['owner']:
            subjects = mongo.db.subjects
            teachers = []
            teachers.append(user['_id'])
            image = "data:image/svg+xml;base64,PHN2ZyBpZD0iYjZjNmU2YTEtNzk3Mi00N2U3LWJlOGQtNzQzZTg4YTgzMmQ4IiBkYXRhLW5hbWU9IkxheWVyIDEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgd2lkdGg9Ijk0OC4zNyIgaGVpZ2h0PSI3NTgiIHZpZXdCb3g9IjAgMCA5NDguMzcgNzU4Ij48dGl0bGU+dGVhY2hpbmc8L3RpdGxlPjxyZWN0IHg9IjE5My44NyIgeT0iMTMwIiB3aWR0aD0iODYiIGhlaWdodD0iMjYiIHJ4PSI3LjQzIiBmaWxsPSIjNGQ5NmI4IiBvcGFjaXR5PSIwLjEiLz48cmVjdCB4PSIyODMuODciIHk9IjE1NiIgd2lkdGg9Ijg2IiBoZWlnaHQ9IjI2IiByeD0iNy40MyIgZmlsbD0iIzRkOTZiOCIgb3BhY2l0eT0iMC4xIi8+PHJlY3QgeD0iMzczLjg3IiB5PSIxODIiIHdpZHRoPSI4NiIgaGVpZ2h0PSIyNiIgcng9IjcuNDMiIGZpbGw9IiM0ZDk2YjgiIG9wYWNpdHk9IjAuMSIvPjxyZWN0IHg9IjE5My44NyIgeT0iOTEiIHdpZHRoPSI4NiIgaGVpZ2h0PSIyNiIgcng9IjcuNDMiIGZpbGw9IiM0ZDk2YjgiIG9wYWNpdHk9IjAuMSIvPjxyZWN0IHg9IjI4My44NyIgeT0iMTE3IiB3aWR0aD0iODYiIGhlaWdodD0iMjYiIHJ4PSI3LjQzIiBmaWxsPSIjNGQ5NmI4IiBvcGFjaXR5PSIwLjEiLz48cmVjdCB4PSIzNzMuODciIHk9IjE0MyIgd2lkdGg9Ijg2IiBoZWlnaHQ9IjI2IiByeD0iNy40MyIgZmlsbD0iIzRkOTZiOCIgb3BhY2l0eT0iMC4xIi8+PHJlY3QgeD0iNDczLjg3IiB5PSIxMzAiIHdpZHRoPSI4NiIgaGVpZ2h0PSIyNiIgcng9IjcuNDMiIGZpbGw9IiM0ZDk2YjgiIG9wYWNpdHk9IjAuMSIvPjxyZWN0IHg9IjU2My44NyIgeT0iMTU2IiB3aWR0aD0iODYiIGhlaWdodD0iMjYiIHJ4PSI3LjQzIiBmaWxsPSIjNGQ5NmI4IiBvcGFjaXR5PSIwLjEiLz48cmVjdCB4PSI2NTMuODciIHk9IjE4MiIgd2lkdGg9Ijg2IiBoZWlnaHQ9IjI2IiByeD0iNy40MyIgZmlsbD0iIzRkOTZiOCIgb3BhY2l0eT0iMC4xIi8+PHJlY3QgeD0iNDczLjg3IiB5PSI5MSIgd2lkdGg9Ijg2IiBoZWlnaHQ9IjI2IiByeD0iNy40MyIgZmlsbD0iIzRkOTZiOCIgb3BhY2l0eT0iMC4xIi8+PHJlY3QgeD0iNTYzLjg3IiB5PSIxMTciIHdpZHRoPSI4NiIgaGVpZ2h0PSIyNiIgcng9IjcuNDMiIGZpbGw9IiM0ZDk2YjgiIG9wYWNpdHk9IjAuMSIvPjxyZWN0IHg9IjY1My44NyIgeT0iMTQzIiB3aWR0aD0iODYiIGhlaWdodD0iMjYiIHJ4PSI3LjQzIiBmaWxsPSIjNGQ5NmI4IiBvcGFjaXR5PSIwLjEiLz48cmVjdCB4PSIxOTMuODciIHk9IjM5IiB3aWR0aD0iODYiIGhlaWdodD0iMjYiIHJ4PSI3LjQzIiBmaWxsPSIjNGQ5NmI4IiBvcGFjaXR5PSIwLjEiLz48cmVjdCB4PSIyODMuODciIHk9IjY1IiB3aWR0aD0iODYiIGhlaWdodD0iMjYiIHJ4PSI3LjQzIiBmaWxsPSIjNGQ5NmI4IiBvcGFjaXR5PSIwLjEiLz48cmVjdCB4PSIzNzMuODciIHk9IjkxIiB3aWR0aD0iODYiIGhlaWdodD0iMjYiIHJ4PSI3LjQzIiBmaWxsPSIjNGQ5NmI4IiBvcGFjaXR5PSIwLjEiLz48cmVjdCB4PSIxOTMuODciIHdpZHRoPSI4NiIgaGVpZ2h0PSIyNiIgcng9IjcuNDMiIGZpbGw9IiM0ZDk2YjgiIG9wYWNpdHk9IjAuMSIvPjxyZWN0IHg9IjI4My44NyIgeT0iMjYiIHdpZHRoPSI4NiIgaGVpZ2h0PSIyNiIgcng9IjcuNDMiIGZpbGw9IiM0ZDk2YjgiIG9wYWNpdHk9IjAuMSIvPjxyZWN0IHg9IjM3My44NyIgeT0iNTIiIHdpZHRoPSI4NiIgaGVpZ2h0PSIyNiIgcng9IjcuNDMiIGZpbGw9IiM0ZDk2YjgiIG9wYWNpdHk9IjAuMSIvPjxyZWN0IHg9IjQ3My44NyIgeT0iMzkiIHdpZHRoPSI4NiIgaGVpZ2h0PSIyNiIgcng9IjcuNDMiIGZpbGw9IiM0ZDk2YjgiIG9wYWNpdHk9IjAuMSIvPjxyZWN0IHg9IjU2My44NyIgeT0iNjUiIHdpZHRoPSI4NiIgaGVpZ2h0PSIyNiIgcng9IjcuNDMiIGZpbGw9IiM0ZDk2YjgiIG9wYWNpdHk9IjAuMSIvPjxyZWN0IHg9IjY1My44NyIgeT0iOTEiIHdpZHRoPSI4NiIgaGVpZ2h0PSIyNiIgcng9IjcuNDMiIGZpbGw9IiM0ZDk2YjgiIG9wYWNpdHk9IjAuMSIvPjxyZWN0IHg9IjQ3My44NyIgd2lkdGg9Ijg2IiBoZWlnaHQ9IjI2IiByeD0iNy40MyIgZmlsbD0iIzRkOTZiOCIgb3BhY2l0eT0iMC4xIi8+PHJlY3QgeD0iNTYzLjg3IiB5PSIyNiIgd2lkdGg9Ijg2IiBoZWlnaHQ9IjI2IiByeD0iNy40MyIgZmlsbD0iIzRkOTZiOCIgb3BhY2l0eT0iMC4xIi8+PHJlY3QgeD0iNjUzLjg3IiB5PSI1MiIgd2lkdGg9Ijg2IiBoZWlnaHQ9IjI2IiByeD0iNy40MyIgZmlsbD0iIzRkOTZiOCIgb3BhY2l0eT0iMC4xIi8+PHJlY3QgeD0iMTkzLjg3IiB5PSI1OTMiIHdpZHRoPSI4NiIgaGVpZ2h0PSIyNiIgcng9IjcuNDMiIGZpbGw9IiM0ZDk2YjgiIG9wYWNpdHk9IjAuMSIvPjxyZWN0IHg9IjI4My44NyIgeT0iNjE5IiB3aWR0aD0iODYiIGhlaWdodD0iMjYiIHJ4PSI3LjQzIiBmaWxsPSIjNGQ5NmI4IiBvcGFjaXR5PSIwLjEiLz48cmVjdCB4PSIzNzMuODciIHk9IjY0NSIgd2lkdGg9Ijg2IiBoZWlnaHQ9IjI2IiByeD0iNy40MyIgZmlsbD0iIzRkOTZiOCIgb3BhY2l0eT0iMC4xIi8+PHJlY3QgeD0iMTkzLjg3IiB5PSI1NTQiIHdpZHRoPSI4NiIgaGVpZ2h0PSIyNiIgcng9IjcuNDMiIGZpbGw9IiM0ZDk2YjgiIG9wYWNpdHk9IjAuMSIvPjxyZWN0IHg9IjI4My44NyIgeT0iNTgwIiB3aWR0aD0iODYiIGhlaWdodD0iMjYiIHJ4PSI3LjQzIiBmaWxsPSIjNGQ5NmI4IiBvcGFjaXR5PSIwLjEiLz48cmVjdCB4PSIzNzMuODciIHk9IjYwNiIgd2lkdGg9Ijg2IiBoZWlnaHQ9IjI2IiByeD0iNy40MyIgZmlsbD0iIzRkOTZiOCIgb3BhY2l0eT0iMC4xIi8+PHJlY3QgeD0iNDczLjg3IiB5PSI1OTMiIHdpZHRoPSI4NiIgaGVpZ2h0PSIyNiIgcng9IjcuNDMiIGZpbGw9IiM0ZDk2YjgiIG9wYWNpdHk9IjAuMSIvPjxyZWN0IHg9IjU2My44NyIgeT0iNjE5IiB3aWR0aD0iODYiIGhlaWdodD0iMjYiIHJ4PSI3LjQzIiBmaWxsPSIjNGQ5NmI4IiBvcGFjaXR5PSIwLjEiLz48cmVjdCB4PSI2NTMuODciIHk9IjY0NSIgd2lkdGg9Ijg2IiBoZWlnaHQ9IjI2IiByeD0iNy40MyIgZmlsbD0iIzRkOTZiOCIgb3BhY2l0eT0iMC4xIi8+PHJlY3QgeD0iNDczLjg3IiB5PSI1NTQiIHdpZHRoPSI4NiIgaGVpZ2h0PSIyNiIgcng9IjcuNDMiIGZpbGw9IiM0ZDk2YjgiIG9wYWNpdHk9IjAuMSIvPjxyZWN0IHg9IjU2My44NyIgeT0iNTgwIiB3aWR0aD0iODYiIGhlaWdodD0iMjYiIHJ4PSI3LjQzIiBmaWxsPSIjNGQ5NmI4IiBvcGFjaXR5PSIwLjEiLz48cmVjdCB4PSI2NTMuODciIHk9IjYwNiIgd2lkdGg9Ijg2IiBoZWlnaHQ9IjI2IiByeD0iNy40MyIgZmlsbD0iIzRkOTZiOCIgb3BhY2l0eT0iMC4xIi8+PHJlY3QgeD0iMTkzLjg3IiB5PSI1MDIiIHdpZHRoPSI4NiIgaGVpZ2h0PSIyNiIgcng9IjcuNDMiIGZpbGw9IiM0ZDk2YjgiIG9wYWNpdHk9IjAuMSIvPjxyZWN0IHg9IjI4My44NyIgeT0iNTI4IiB3aWR0aD0iODYiIGhlaWdodD0iMjYiIHJ4PSI3LjQzIiBmaWxsPSIjNGQ5NmI4IiBvcGFjaXR5PSIwLjEiLz48cmVjdCB4PSIzNzMuODciIHk9IjU1NCIgd2lkdGg9Ijg2IiBoZWlnaHQ9IjI2IiByeD0iNy40MyIgZmlsbD0iIzRkOTZiOCIgb3BhY2l0eT0iMC4xIi8+PHJlY3QgeD0iMTkzLjg3IiB5PSI0NjMiIHdpZHRoPSI4NiIgaGVpZ2h0PSIyNiIgcng9IjcuNDMiIGZpbGw9IiM0ZDk2YjgiIG9wYWNpdHk9IjAuMSIvPjxyZWN0IHg9IjI4My44NyIgeT0iNDg5IiB3aWR0aD0iODYiIGhlaWdodD0iMjYiIHJ4PSI3LjQzIiBmaWxsPSIjNGQ5NmI4IiBvcGFjaXR5PSIwLjEiLz48cmVjdCB4PSIzNzMuODciIHk9IjUxNSIgd2lkdGg9Ijg2IiBoZWlnaHQ9IjI2IiByeD0iNy40MyIgZmlsbD0iIzRkOTZiOCIgb3BhY2l0eT0iMC4xIi8+PHJlY3QgeD0iNDczLjg3IiB5PSI1MDIiIHdpZHRoPSI4NiIgaGVpZ2h0PSIyNiIgcng9IjcuNDMiIGZpbGw9IiM0ZDk2YjgiIG9wYWNpdHk9IjAuMSIvPjxyZWN0IHg9IjU2My44NyIgeT0iNTI4IiB3aWR0aD0iODYiIGhlaWdodD0iMjYiIHJ4PSI3LjQzIiBmaWxsPSIjNGQ5NmI4IiBvcGFjaXR5PSIwLjEiLz48cmVjdCB4PSI2NTMuODciIHk9IjU1NCIgd2lkdGg9Ijg2IiBoZWlnaHQ9IjI2IiByeD0iNy40MyIgZmlsbD0iIzRkOTZiOCIgb3BhY2l0eT0iMC4xIi8+PHJlY3QgeD0iNDczLjg3IiB5PSI0NjMiIHdpZHRoPSI4NiIgaGVpZ2h0PSIyNiIgcng9IjcuNDMiIGZpbGw9IiM0ZDk2YjgiIG9wYWNpdHk9IjAuMSIvPjxyZWN0IHg9IjU2My44NyIgeT0iNDg5IiB3aWR0aD0iODYiIGhlaWdodD0iMjYiIHJ4PSI3LjQzIiBmaWxsPSIjNGQ5NmI4IiBvcGFjaXR5PSIwLjEiLz48cmVjdCB4PSI2NTMuODciIHk9IjUxNSIgd2lkdGg9Ijg2IiBoZWlnaHQ9IjI2IiByeD0iNy40MyIgZmlsbD0iIzRkOTZiOCIgb3BhY2l0eT0iMC4xIi8+PGVsbGlwc2UgY3g9IjQ4Mi4zNyIgY3k9IjcyMiIgcng9IjQzOC41IiByeT0iMzYiIGZpbGw9IiM0ZDk2YjgiIG9wYWNpdHk9IjAuMSIvPjxwYXRoIGQ9Ik0yMTAuNDcsMjU3LjhjNDEuMzUsMTcuOTIsNjUuMTEsNTUsNjUuMTEsNTVzLTQzLjI5LDgtODQuNjUtOS45MS02NS4xMS01NS02NS4xMS01NVMxNjkuMTEsMjM5Ljg4LDIxMC40NywyNTcuOFoiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMjUuODIgLTcxKSIgZmlsbD0iIzRkOTZiOCIvPjxwYXRoIGQ9Ik0zMzcuMzcsMTg5QzM1MC4xNiwxNjgsMzcxLjk0LDE1OCwzNzEuOTQsMTU4czEsMjMuOTQtMTEuNzUsNDQuODgtMzQuNTgsMzAuOTMtMzQuNTgsMzAuOTNTMzI0LjU3LDIwOS44OCwzMzcuMzcsMTg5WiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyNS44MiAtNzEpIiBmaWxsPSIjNGQ5NmI4Ii8+PHBhdGggZD0iTTI0My4zNSwyMTEuNDdjOS4xNSwzMi42NiwzNC4zNyw1NC4xNiwzNC4zNyw1NC4xNnMxMC4zOS0zMS40NywxLjI0LTY0LjE0LTM0LjM4LTU0LjE2LTM0LjM4LTU0LjE2UzIzNC4xOSwxNzguOCwyNDMuMzUsMjExLjQ3WiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyNS44MiAtNzEpIiBmaWxsPSIjNDY0NTViIi8+PHJlY3QgeD0iMTE4Ljg3IiB5PSIxMzkiIHdpZHRoPSI3MjkiIGhlaWdodD0iMzY1IiByeD0iNy4yMSIgZmlsbD0iIzNmM2Q1NiIvPjxwYXRoIGQ9Ik0xMTguODcsNDgyaDcyOWEwLDAsMCwwLDEsMCwwdjE0Ljc5YTcuMjEsNy4yMSwwLDAsMS03LjIxLDcuMjFIMTI2LjA4YTcuMjEsNy4yMSwwLDAsMS03LjIxLTcuMjFWNDgyYTAsMCwwLDAsMSwwLDBaIiBvcGFjaXR5PSIwLjEiLz48cmVjdCB4PSIxODkuODciIHk9IjQ1NSIgd2lkdGg9IjU0IiBoZWlnaHQ9IjI3IiByeD0iMi41IiBmaWxsPSIjNGQ5NmI4Ii8+PHJlY3QgeD0iMjU4Ljg3IiB5PSI0NzgiIHdpZHRoPSIzNyIgaGVpZ2h0PSI0IiByeD0iMiIgZmlsbD0iIzRkOTZiOCIvPjxwYXRoIGQ9Ik0zNTEuODQsMjgxLjM4YzI2LjM5LDQuODcsNTMuMzEsMCw3OS41OS0zLjNsNzkuODctMTBjMy4yMy0uNDEsNy45My0yLjM0LDkuODMsMS42MSwxLjA3LDIuMjEuMzUsNywuNDMsOS41NC4yMSw3LC4xOSwxNCwwLDIxLS4zNiwxMy4zOC0xLjM0LDI2LjczLTIuNTksNDAuMDUtMi40MywyNi4wNy01Ljg3LDUyLTcuNTksNzguMTctLjg4LDEzLjMyLTEuMzIsMjYuNjgtLjkzLDQwLC4wOSwzLjE4LjIyLDYuMzYuNDEsOS41My4yMSwzLjU1LDEuOCw4LjgyLTIuMDcsMTEuMTktMi4yMSwxLjM2LTYuNTYsMS4yOS05LjA5LDEuNjktNCwuNjMtOCwxLjEzLTEyLjA4LDEuNTQtMjYuODksMi42OS01NC4xMywxLjU3LTgxLjEyLDEuNDFMMzI1LDQ4My4zOWwtMTkuODgtLjExYy0xLjgsMC04LjI5LDEuMDgtOS40LTEuMDYtLjQ3LS45MS43OC01LjE3LDEtNi4zMXEuNDYtMi44MiwxLTUuNjNjMi4zMi0xMy4xNSw1LjA2LTI2LjIyLDcuODItMzkuMjgsNS45My0yOCwxMi01Ni4xNCwxNC40NC04NC43NCwxLjIxLTE0LjM1LjQxLTI4LjgzLDEuODktNDMuMTUuNjktNi42NSwxLjUxLTIxLjQ5LDEwLjM2LTIyLjA4LDcuNS0uNSwxNS4yMiwwLDIyLjc0LDBhMS41LDEuNSwwLDAsMCwwLTNjLTcuMSwwLTE0LjIxLS4xOS0yMS4zMS0uMDUtNC43Mi4wOS04LDEuMjEtMTAuMjUsNS41NS01Ljc1LDExLjE0LTUuMTYsMjYtNS4zNCwzOC4xNi0uNDMsMjkuMTEtNC45LDU3LjYtMTAuNzIsODYuMDctMi45MywxNC4zMy02LjA5LDI4LjYxLTksNDIuOTUtMS4zNyw2Ljg1LTIuNjgsMTMuNzItMy44OCwyMC42MS0uNTYsMy4yOC0zLjM5LDEwLjUxLS45LDEzLjUyczEwLjE1LDEuMzksMTMuNTgsMS40MWwyMy44Ni4xNCw0NS43Mi4yNmMyOS41NC4xNyw1OS4xOCwxLDg4LjcxLjEzLDE0LjEtLjQyLDI5LTEsNDIuNzMtNC4zNyw0LjA5LTEsNi4wNi0yLjg4LDYuMjItNy4yNC4yNC02Ljc2LS44Ni0xMy43My0xLTIwLjUyLTEtNTguMSwxMi42NS0xMTUuMzksMTEuMjUtMTczLjUxLS4wOS0zLjk1LDEuNC0xMy45MS0yLjkyLTE2LjMtMS45NC0xLjA4LTQuNDYtLjQ5LTYuNS0uMjUtMy45LjQ1LTcuNzksMS0xMS42OSwxLjQ2bC01MC42NSw2LjMyYy0xNi4xOSwyLTMyLjM3LDQuMTYtNDguNTksNi0xNy4xNywyLTM0LjUxLDMuMTktNTEuNjIsMC0xLjg5LS4zNS0yLjcsMi41NC0uOCwyLjg5WiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyNS44MiAtNzEpIiBmaWxsPSIjNGQ5NmI4Ii8+PHBhdGggZD0iTTMyMCwzMTYuNzNsMTk5LjgyLTkuOGMxLjkzLS4xLDEuOTQtMy4xLDAtM0wzMjAsMzEzLjczYy0xLjkyLjA5LTEuOTMsMy4wOSwwLDNaIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMTI1LjgyIC03MSkiIGZpbGw9IiM0ZDk2YjgiLz48cGF0aCBkPSJNMzgxLjU2LDI5MmE1LDUsMCwwLDAsMS43Nyw4LjA3YzIuNjksMS4yMyw1Ljg1LjIsOC41Mi0uNDcsNC0xLDgtMS44OSwxMi4xMS0yLjYyYTE2NS4xNSwxNjUuMTUsMCwwLDEsMjcuMDktMi41MmM0LjE0LS4wNSw4LjI1LjE0LDEyLjM5LjMyLDMsLjEyLDYuMjMuMzYsOC43Ny0xLjUsMi45LTIuMTIsMy44NC02LjI2LDEtOC44NC00LTMuNjUtMTIuNjItMS41My0xNy4yNC0xLjE1YTM4Ni42MiwzODYuNjIsMCwwLDAtNDkuODYsNy40NGMtMS44OC40LTEuMDksMy4zLjgsMi44OXExNi4yNy0zLjUxLDMyLjc5LTUuNjQsOC4xMi0xLDE2LjI3LTEuNjljMi41Ni0uMjEsNS4xMi0uNCw3LjY4LS41NSwxLS4wNiwyLjA2LS4xNywzLjA4LS4xNCwzLjE3LjA3LDMuNTQtLjUsMS42NCwzLjMzLTEuNjksMy4zOS0xLjE1LDMtNC4wOCwyLjg5LTEuMjQsMC0yLjQ4LS4xNC0zLjcyLS4ycS0zLjgxLS4xNi03LjYyLS4xNy04LjExLDAtMTYuMTguNzhjLTQuNTYuNDQtOS4xMSwxLjA2LTEzLjYyLDEuODYtMi44Mi41LTUuNjIsMS4wOC04LjQxLDEuNzItMS4yMy4yOS0yLjQ3LjU5LTMuNy45LS41OS4xNi0xLjE5LjMtMS43OC40NXEtMy4yOCwxLjE0LTUuNTktM2MxLjM0LTEuMzktLjc3LTMuNTItMi4xMi0yLjEyWiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyNS44MiAtNzEpIiBmaWxsPSIjNGQ5NmI4Ii8+PHBhdGggZD0iTTQxNy43OCwzMzQuNjhjLTE0LjQ3LS41Ni0zMC4xLDMuMzUtMzkuNjMsMTUtNy40Niw5LjExLTExLjcxLDI0Ljc0LTMuODEsMzUsOC40OSwxMSwyNy4xMSw5LjA2LDM4LjM0LDQuMzcsMTEuODgtNSwyNC44OC0xNS4zMSwyOC40NS0yOC4yMSw0LjQ1LTE2LjExLTEwLTI4LjI5LTI1LjA1LTI4LjQ3LTEuOTMsMC0xLjkzLDMsMCwzLDguNTguMSwxNywzLjc4LDIxLDExLjc3LDQuMTksOC40Mi41OCwxNy4yNi01LDI0LTguOTQsMTAuNzMtMjIuOTIsMTguODItMzcuMTYsMTguNTktOC41NS0uMTMtMTgtMy4wNi0yMC42NS0xMi4wOC0yLjE4LTcuMzEtLjUyLTE1LjMsMy4yOC0yMS43OCw4LjIyLTE0LDI0Ljk1LTE4Ljc0LDQwLjI5LTE4LjE0LDEuOTMuMDcsMS45My0yLjkzLDAtM1oiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMjUuODIgLTcxKSIgZmlsbD0iIzRkOTZiOCIvPjxwYXRoIGQ9Ik00MDMuNDEsMzU2LjlhMy45LDMuOSwwLDAsMC01LjI0LDRjLjMsMy45LDQuNiw1LDcuODMsNC43NywyLjc5LS4yNCw2LjA1LTEuMjcsNS4wNy00Ljc2YTQuNDgsNC40OCwwLDAsMC0yLjQ0LTIuODIsNS42NSw1LjY1LDAsMCwwLTIuODItLjM1Yy0uMzcsMC0zLjc2LDEuMjQtMi4zMi0uMjVsLTIuMzYtLjMxYTIuNDYsMi40NiwwLDAsMSwuNzIsMiwxLjUxLDEuNTEsMCwwLDAsMi4yNSwxLjI5LDIsMiwwLDAsMSwyLjcxLDIuMzQsMS41MSwxLjUxLDAsMCwwLDIuNzQsMS4xNmMxLTEuOCwyLjIxLTUuMzguNzEtNy4yNi0xLTEuMjctMi45My0uODktNC4xMy0uMTVhMTQuNDcsMTQuNDcsMCwwLDAtMi4wNiwxLjc3Yy0xLjIxLDEuMDctMiwxLjU3LTEuNTUtLjQ4Ljc1LTMuNzMsNC4zMS02LjcsNy41Ni04LjE5bC0yLjItMS42OWEzMS42MiwzMS42MiwwLDAsMS02LjA1LDExLjg1bDIuNTYsMS4wNmE2LjY4LDYuNjgsMCwwLDEsNC4wOC02LjUxSDQwN2wuNzgsMS4yOGMtLjI5LDEuODksMi42LDIuNywyLjg5Ljc5LjM4LTIuNDctMS4xOC01LjY4LTQuMDctNC40Ny0zLjQ1LDEuNDQtNS4yNCw1LjM5LTUuMTcsOC45MSwwLDEuMiwxLjcsMi4xMywyLjU3LDEuMDdhMzUuMjYsMzUuMjYsMCwwLDAsNi44MS0xMy4xOSwxLjUyLDEuNTIsMCwwLDAtMi4yMS0xLjY5LDE2Ljc3LDE2Ljc3LDAsMCwwLTcuMjgsNi4zNGMtMS4yMiwyLTIuNzUsNS4xMi0xLjUxLDcuNDJhMy4xOCwzLjE4LDAsMCwwLDQuMzUsMS4yMywxMS43LDExLjcsMCwwLDAsMi41MS0yYy4zNy0uMzMuNzgtLjksMS4yNy0xLC40NC0uMy40Mi0uMTMtLjA3LjUzYTUuNDUsNS40NSwwLDAsMS0uODcsMi45MmwyLjc0LDEuMTVhNSw1LDAsMCwwLTcuMTEtNS43M2wyLjI2LDEuM2E1LjQ1LDUuNDUsMCwwLDAtMS4xMy0zLjUzLDEuNTIsMS41MiwwLDAsMC0yLjM1LS4zMWMtMS41MiwxLjU5LTEuODEsNC4zNC4xLDUuODEsMS40MywxLjA5LDIuMTMsMCwzLjctLjI1LDUuMzMtLjY5LDIuMjIsMS43MS4zNCwxLjc5YTcuMDksNy4wOSwwLDAsMS0yLjUxLS4xOHEtMy4xMy0xLjA2LS4zOS0yLjczYzEuNzkuNzMsMi41Ni0yLjE3LjgtMi44OVoiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMjUuODIgLTcxKSIgZmlsbD0iIzRkOTZiOCIvPjxwYXRoIGQ9Ik00MDEsMzYyLjM4YzEuMjMsNC0zLjg1LDUuMzItNi4yNiw2LjdhMTMuOTQsMTMuOTQsMCwwLDAtNC4zMywzLjc5Yy0yLjUyLDMuMzgtMy40Niw3LjY4LTQuMjksMTEuNzMtLjM4LDEuODksMi41MSwyLjY5LDIuOS44YTM0LDM0LDAsMCwxLDIuNTMtOC42M2MxLjgtMy41OCw0LjM4LTQuNzgsNy43NC02LjYyczUuNzktNC42OSw0LjYtOC41N2MtLjU2LTEuODQtMy40Ni0xLjA1LTIuODkuOFoiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMjUuODIgLTcxKSIgZmlsbD0iIzRkOTZiOCIvPjxwYXRoIGQ9Ik00MDYsMzYwLjM3YTIuOSwyLjksMCwwLDAtMi41LDNjMCwxLjE5Ljc5LDEuOTUsMS4zMywyLjlhMjIuOSwyMi45LDAsMCwxLDIuOSw2LjMxYy40OCwyLjE1Ljk1LDYtLjE3LDgtMi4wNywzLjcxLTUuODEsMy05LDMtMywwLTUuMzIsMS01LjIyLTMuMTguMDYtMi4zNSwxLjctNC43MywzLTYuNThsLTIuNzQtLjM2YTUyLjI3LDUyLjI3LDAsMCwxLC45MSw5LjI2YzAsMS4zOSwyLjEzLDIuMTYsMi43OS43NWE1Ny45Myw1Ny45MywwLDAsMCwzLjgxLTEwLjU0bC0yLjk1LS40LjUyLDcuNmExLjUxLDEuNTEsMCwwLDAsMi43OS43NiwzLjQsMy40LDAsMCwwLC43NS0xLjM1Yy4xLS40Ny0uODItMy42NC0xLjE5LTIuNTFsMi45NC40LjIxLTcuMjItMywuNGExNC45NCwxNC45NCwwLDAsMSwuNTYsNi4zYy0uMTksMS42NywyLjYyLDIuMDUsMywuNGwxLjg4LTkuNy0yLjc0LjM1YTYuNjMsNi42MywwLDAsMSwuNTEsNC4zMmMtLjIyLDEuOTIsMi43OCwxLjksMywwYTEwLjU0LDEwLjU0LDAsMCwwLS45Mi01LjgzLDEuNTEsMS41MSwwLDAsMC0yLjc0LjM2bC0xLjg5LDkuNywyLjk1LjRhMTYuMzYsMTYuMzYsMCwwLDAtLjY3LTcuMDksMS41LDEuNSwwLDAsMC0yLjk0LjM5bC0uMjEsNy4yMmMwLDEuNzUsMi40MywyLDIuOTUuNGwuMTYtLjQ5YTEuNTIsMS41MiwwLDAsMC0uMzgtMS40NmMtMy4xMS0zLjM4LTMuNzQsMi00LjgyLDMuNDlsMi44Ljc2LS41Mi03LjZjLS4xMS0xLjYyLTIuNTEtMi4xMi0yLjk1LS40YTUzLjc2LDUzLjc2LDAsMCwxLTMuNSw5LjgzbDIuOC43NmE1Ni41NCw1Ni41NCwwLDAsMC0xLTEwLjA2Yy0uMjYtMS4zOC0yLjA3LTEuMzItMi43NC0uMzYtMiwyLjg4LTUuNDYsOS4xNy0yLjc5LDEyLjYyLDIuMzMsMyw5LjY2LDEuODQsMTIuNzksMS42NSw0Ljk0LS4yOCw2LjczLTMuNDEsNy4yNy04LjA3YTE5Ljc2LDE5Ljc2LDAsMCwwLS4zNy02LjY4Yy0uMjctMS4xOC0zLTguNjYtMy44Mi04LjUxLDEuOS0uMzUsMS4wOS0zLjI1LS44LTIuOVoiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMjUuODIgLTcxKSIgZmlsbD0iIzRkOTZiOCIvPjxwYXRoIGQ9Ik00MDAuMTksMzY3LjExLDM5MiwzNzcuOTJsMi41OSwxLjUxLDYtOC42OC0yLjc0LTEuMTZMMzk0Ljg2LDM4MWExLjUxLDEuNTEsMCwwLDAsMi43NCwxLjE2LDUyLjcxLDUyLjcxLDAsMCwxLDQuNTctNi40M2wtMi41LTEuNDZhMTYuMzMsMTYuMzMsMCwwLDEtMy43Nyw2LjkzbDIuNTEsMS40NmExMy40LDEzLjQsMCwwLDEsMS4wOS00Yy43Ny0xLjczLTEuNjctMy4yNi0yLjU5LTEuNTJhMzUuMjEsMzUuMjEsMCwwLDEtMi44OSw0LjU0bDIuNzQuMzYuNjEtMi44NS0yLjc0LS4zNi40NCwyLjVhMS41MSwxLjUxLDAsMCwwLDIuNTEuNjYsMjkuODYsMjkuODYsMCwwLDAsNi05LjA1SDQwMWExMy40NywxMy40NywwLDAsMSwxLjQxLDRjLjM2LDEuOCwyLjc1LDEuMTMsMi45NC0uNGE4MS4zMSw4MS4zMSwwLDAsMCwuNjYtMTAuMWgtM2wwLDYuMjljMCwxLjYzLDIuNjcsMi4xMSwyLjk1LjRhMTEuNDYsMTEuNDYsMCwwLDEsMS40Ny00LjNINDA0LjhhNi42Nyw2LjY3LDAsMCwxLDEsMy40LDEuNSwxLjUsMCwwLDAsMywwbC4zOC0yaC0yLjg5Yy4yOSwxLjc3LDEuMzksMTEuNzQtMi41MiwxMC41Ny0uNjYtLjE2LS44NS0uMTItLjU3LjExbC44OS0xLjksMi4wOS00LjQzLTIuOC0uNzZjLjE4LDIuMDYuMzcsNS0uODcsNi43Ni0xLDEuNDMtNC4wOCwyLTUuNjUsMS4xNmExMCwxMCwwLDAsMS0yLjYxLTIuNzRsLTIuMDUsMmMxLjY2LDEuMjEsNC4zNSw0LjE4LDYuNDksNC4zNSwxLjYzLjEzLDMtMS4yMiw0LjA3LTIuM2ExNy40MywxNy40MywwLDAsMCw0Ljg5LTEyLjgzLDEuNSwxLjUsMCwwLDAtMywwbDAsMy40MmExLjUsMS41LDAsMCwwLDMsMHYtOC4zOWExLjUsMS41LDAsMCwwLTMsMCwzNiwzNiwwLDAsMS0uNTIsNmwyLjk1LjRhNjkuMDcsNjkuMDcsMCwwLDEtLjMzLTcuMTksMS41LDEuNSwwLDAsMC0yLjk0LS40Yy0uNDUsMS45MS0xLDMuNzktMS41Myw1LjY2bDIuNzQtLjM2LS4yMS0uOGMtLjE0LTEuOTEtMy4xNC0xLjkyLTMsMGE1LjQ5LDUuNDksMCwwLDAsLjYyLDIuMzJjLjU4LDEuMjIsMi4zOS43OSwyLjc0LS4zNi41Ny0xLjg4LDEuMDgtMy43NiwxLjUzLTUuNjZsLTIuOTUtLjRhNjkuMDcsNjkuMDcsMCwwLDAsLjMzLDcuMTljLjE1LDEuNTQsMi42MywyLjIsMi45NC40YTQxLjMzLDQxLjMzLDAsMCwwLC42My02Ljg0aC0zdjguMzloM2wwLTMuNDJoLTNBMTQuNDIsMTQuNDIsMCwwLDEsNDAxLDM4MC40NmExMi4yOSwxMi4yOSwwLDAsMS0xLjI2LDEuMjRjLS43MS42OC0xLjM2LjU4LTEuOTMtLjMxLTEuNDItLjU5LTIuODktMi4xMS00LjEzLTNzLTIuOTQuODctMi4wNiwyLjA1YzIuMywzLjA2LDUuNzMsNi40NywxMCw1LDQuNDktMS41OSw1LjEtNy42Nyw0Ljc2LTExLjY3LS4xMS0xLjMzLTIuMS0yLjIzLTIuNzktLjc1LTEsMi4xMS0yLDQuMjEtMyw2LjMzLS4zNS43NC0xLDEuNzYtLjksMi42NC4zMywyLjI1LDMuMDYsMS44OCw0Ljc0LDEuNzUsNi41MS0uNDksNS40OC05LjcyLDQuNzMtMTQuMzYtLjI1LTEuNTQtMi40OS0xLjMtMi44OSwwYTguODMsOC44MywwLDAsMC0uNDksMi44NGgzYTExLjg5LDExLjg5LDAsMCwwLTEuNDEtNC45MSwxLjUxLDEuNTEsMCwwLDAtMi41OSwwLDE0LjU4LDE0LjU4LDAsMCwwLTEuNzgsNWwzLC40LDAtNi4yOWExLjUsMS41LDAsMCwwLTMsMCw4MS4zMSw4MS4zMSwwLDAsMS0uNjYsMTAuMWwyLjk1LS40YTE3LjE3LDE3LjE3LDAsMCwwLTEuNzEtNC42OCwxLjUxLDEuNTEsMCwwLDAtMi41OSwwLDI3LjM2LDI3LjM2LDAsMCwxLTUuNTMsOC40NGwyLjUxLjY2LS40NC0yLjVjLS4yMy0xLjMzLTIuMTEtMS4zNy0yLjc0LS4zNmE2LjU4LDYuNTgsMCwwLDAtLjkxLDUuMTZjLjI1LDEuNDIsMi4wNSwxLjI3LDIuNzQuMzZhMzUuMSwzNS4xLDAsMCwwLDIuODktNC41M2wtMi41OS0xLjUyYTE3LjA2LDE3LjA2LDAsMCwwLTEuNCw0LjcxYy0uMTgsMS4zMiwxLjM5LDIuNywyLjUxLDEuNDZhMjAsMjAsMCwwLDAsNC41NC04LjI2Yy4zNy0xLjM2LTEuNTEtMi42NS0yLjUxLTEuNDZhNTcuMjksNTcuMjksMCwwLDAtNSw3bDIuNzQsMS4xNiwzLjA1LTExLjM3YTEuNTEsMS41MSwwLDAsMC0yLjc0LTEuMTZsLTYsOC42OWMtMS4xMiwxLjYxLDEuNDUsMywyLjU5LDEuNTFsOC4xNi0xMC44YzEuMTYtMS41NC0xLjQ0LTMtMi41OS0xLjUyWiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyNS44MiAtNzEpIiBmaWxsPSIjNGQ5NmI4Ii8+PHBhdGggZD0iTTUyNy43Nyw0MDMuMmMxMi03LjM0LDIxLjU0LTE4LjI5LDMyLjE0LTI3LjQ1LDExLjUtOS45MywyMy41Ny0xOS4xOCwzNi0yNy45NCwyNC4xNC0xNyw0OS40OS0zMi4yMSw3NC44Mi00Ny4zOGExLjUsMS41LDAsMCwwLTEuNTEtMi41OWMtMjUuMzMsMTUuMTctNTAuNjksMzAuMzUtNzQuODMsNDcuMzgtMTEuMzksOC0yMi41MSwxNi40OC0zMy4xNywyNS40OC0xMS42LDkuOC0yMS45MywyMi0zNSwyOS45MS0xLjY1LDEtLjE0LDMuNiwxLjUxLDIuNTlaIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMTI1LjgyIC03MSkiIGZpbGw9IiM0ZDk2YjgiLz48cGF0aCBkPSJNNzA5LjQ2LDI1My44NWMtMTMsMS4zMi0yNyw0LjYzLTM1LDE2LTYuOTEsOS43OC02Ljc2LDI2Ljg0LS4yNywzNi44OCw3LjM3LDExLjQxLDIyLjQzLDExLjgyLDM0LjEzLDguMTNzMjMuODEtMTAuMTYsMjMuNy0yNC4xNGMtLjA2LTcuNS0yLjc3LTE1LjMxLTUuNzYtMjIuMTEtMi41OC01Ljg3LTcuMTUtMTEtMTQuMDctMTAuMzUtMS45MS4xOC0xLjkzLDMuMTgsMCwzLDkuMjctLjg2LDEyLjI1LDEwLjE1LDE0LjQ1LDE3LjEsMiw2LjQ5LDMuODUsMTQuMTcuNzEsMjAuNjJzLTEwLjcxLDkuNzQtMTcuMTgsMTIuMWMtNywyLjU0LTE0LjY5LDQuMDktMjIsMi0xNC40OC00LjA1LTE4LjQ4LTIyLjQtMTQuMzEtMzUuNDIsNC44LTE1LDIxLjgtMTkuNDEsMzUuNjUtMjAuODEsMS45LS4xOSwxLjkyLTMuMTksMC0zWiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyNS44MiAtNzEpIiBmaWxsPSIjNGQ5NmI4Ii8+PHBhdGggZD0iTTcyOS40NiwzNjkuODVjLTEzLDEuMzItMjcsNC42My0zNSwxNi02LjkxLDkuNzgtNi43NiwyNi44NC0uMjcsMzYuODgsNy4zNywxMS40MSwyMi40MywxMS44MiwzNC4xMyw4LjEzczIzLjgxLTEwLjE2LDIzLjctMjQuMTRjLS4wNi03LjUtMi43Ny0xNS4zMS01Ljc2LTIyLjExLTIuNTgtNS44Ny03LjE1LTExLTE0LjA3LTEwLjM1LTEuOTEuMTgtMS45MywzLjE4LDAsMyw5LjI3LS44NiwxMi4yNSwxMC4xNSwxNC40NSwxNy4xLDIsNi40OSwzLjg1LDE0LjE3LjcxLDIwLjYycy0xMC43MSw5Ljc0LTE3LjE4LDEyLjFjLTcsMi41NC0xNC42OSw0LjA5LTIyLDItMTQuNDgtNC4wNS0xOC40OC0yMi40LTE0LjMxLTM1LjQyLDQuOC0xNSwyMS44LTE5LjQxLDM1LjY1LTIwLjgxLDEuOS0uMTksMS45Mi0zLjE5LDAtM1oiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMjUuODIgLTcxKSIgZmlsbD0iIzRkOTZiOCIvPjxwYXRoIGQ9Ik02ODkuODUsMjgzLjA2bDkuNDcsMTAuOGExLjUxLDEuNTEsMCwwLDAsMi41LS42N2MyLTUuMjYsMS42Mi0xMC43MSwyLjA5LTE2LjI0YTUzLjQ3LDUzLjQ3LDAsMCwxLDQuMjUtMTYuNTcsNTUuOTMsNTUuOTMsMCwwLDEsMjIuMzgtMjUuNjVjMS42NS0xLC4xNC0zLjYtMS41MS0yLjU5QTU4LjcyLDU4LjcyLDAsMCwwLDcwNi40LDI1N2E1Ny40Nyw1Ny40NywwLDAsMC01LDE1Ljg3Yy0xLDYuNDktLjA5LDEzLjI5LTIuNDksMTkuNTJsMi41MS0uNjdMNjkyLDI4MC45NGMtMS4yOC0xLjQ1LTMuMzkuNjgtMi4xMiwyLjEyWiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyNS44MiAtNzEpIiBmaWxsPSIjNGQ5NmI4Ii8+PHBhdGggZD0iTTUzMi42LDQxNC44OXE3Ny4zNy0yLjM2LDE1NC43OC0xYzEuOTMsMCwxLjkzLTMsMC0zcS03Ny4zOS0xLjM4LTE1NC43OCwxYy0xLjkzLjA2LTEuOTQsMy4wNiwwLDNaIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMTI1LjgyIC03MSkiIGZpbGw9IiM0ZDk2YjgiLz48cGF0aCBkPSJNNjk4LjE2LDM4NS4zMWEzMDkuOTIsMzA5LjkyLDAsMCwxLDUwLjY3LDI1LjQ2YzEuNjQsMSwzLjE1LTEuNTcsMS41MS0yLjU5QTMxMy4yMywzMTMuMjMsMCwwLDAsNjk5LDM4Mi40MmMtMS43OS0uNzEtMi41NywyLjE5LS43OSwyLjg5WiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyNS44MiAtNzEpIiBmaWxsPSIjNGQ5NmI4Ii8+PHBhdGggZD0iTTczMC4xOCwzNzEuNzJhMTIyLjUsMTIyLjUsMCwwLDAtMjkuNDEsNzQuNTNjLS4wOCwxLjkzLDIuOTIsMS45MywzLDBhMTE5LjE0LDExOS4xNCwwLDAsMSwyOC41My03Mi40MWMxLjI1LTEuNDYtLjg2LTMuNTktMi4xMi0yLjEyWiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyNS44MiAtNzEpIiBmaWxsPSIjNGQ5NmI4Ii8+PHBhdGggZD0iTTMzMC4yMyw0MDQsNDQyLDQwMi41NGwxMi44NS0uMTdjMi4zMSwwLDQuNjItLjA4LDYuOTMtLjA5LDMuMjUsMCw1LjQ0LDIuNyw1LjM4LDYtLjE1LDctNC41NSw2Ljc1LTEwLjMxLDdsLTEzLjg5LjYzTDM4Ni40LDQxOC40Yy0xMC4xMy40NS0yMC4yNywxLTMwLjQsMS4zNS05LjE0LjI4LTI2LjUyLTIuNy0yMi40Ni0xNiwuNTYtMS44NS0yLjMzLTIuNjQtMi45LS44LTIsNi41NCwxLjU0LDEzLjE4LDcuMjQsMTYuNjEsOC4wOSw0Ljg2LDE4Ljc1LDMuMjEsMjcuNjgsMi44MUw0MzUsNDE5LjIybDE2Ljg2LS43NWM0LjMyLS4yLDEwLjMzLjY4LDE0LjMtMS4zMyw0LjY2LTIuMzUsNS40OC0xMS42OCwyLjU0LTE1LjYxLTEuNTEtMi0zLjYzLTIuMTgtNi0yLjI3LTYuMjItLjI0LTEyLjU1LjE3LTE4Ljc4LjI1bC0zNC42Mi40Ni03OS4xMSwxYy0xLjkzLDAtMS45MywzLDAsM1oiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMjUuODIgLTcxKSIgZmlsbD0iIzRkOTZiOCIvPjxnIGlkPSJiMzBlY2NmNi03Y2ZlLTQ4ZGYtOWNhYS00MTVhMTI4YmQ1NjgiIGRhdGEtbmFtZT0iTWljaGVsIj48cGF0aCBkPSJNNzgxLjgxLDc3MS41Yy0yLjUyLDEuNTgtNS40LDIuNDctOCwzLjg2cy01LjEzLDMuNDgtNS44Nyw2LjM2YTQsNCwwLDAsMCwuMTMsMi43Miw1LjI4LDUuMjgsMCwwLDAsMi44LDIuMjIsNDIuNDksNDIuNDksMCwwLDAsMzMuNjEuMzgsNDQuMjcsNDQuMjcsMCwwLDEsNS44LTIuMywzNy42OSwzNy42OSwwLDAsMSw3LjQzLS43Niw1Ny4xMSw1Ny4xMSwwLDAsMCw3LjgxLTEsNi44Nyw2Ljg3LDAsMCwwLDMuNTQtMS40Nyw2LjU3LDYuNTcsMCwwLDAsMS41OS0zLjgyLDMxLjQ1LDMxLjQ1LDAsMCwwLTUtMjIuMjgsNy41Myw3LjUzLDAsMCwwLTIuMTgtMi4zMSw4LjQxLDguNDEsMCwwLDAtMy40Ny0uOTNjLTUtLjYxLTEwLjI0LTEuNzMtMTUuMjktMS44NS0zLjYyLS4wOC01LjQ0LDEuNjQtOCw0LjEzQzc5MS40Miw3NTkuNzQsNzg4LjMzLDc2Ny40Myw3ODEuODEsNzcxLjVaIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMTI1LjgyIC03MSkiIGZpbGw9IiMzMjM0NDQiLz48cGF0aCBkPSJNODU1LjUsNzcwLjc2YzAsNC45LjU5LDEwLjA5LDMuNTYsMTRhMTguNDksMTguNDksMCwwLDAsNC44Niw0LjI1YzYuMjgsNCwxNC42LDUuNDcsMjEuMjIsMi4wOGE2LjMsNi4zLDAsMCwwLDIuNjQtMi4yMmMxLTEuNzQuNDctMy45MS0uMDktNS44M2wtOS41OC0zMy4yYy02LjE5Ljk1LTE1LjI5LDEuNjItMjAuNzksNC43NkM4NTMuMzMsNzU2Ljg3LDg1NS41LDc2Ni4zOCw4NTUuNSw3NzAuNzZaIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMTI1LjgyIC03MSkiIGZpbGw9IiMzMjM0NDQiLz48cGF0aCBkPSJNNzc2LjE5LDU2Ni4zM2MtLjU4LDEuODMtMi42OCwyLjY4LTMuODMsNC4yMi0xLjM1LDEuODEtMS4yMSw0LjMyLS43Miw2LjUyYTE3LjI0LDE3LjI0LDAsMCwwLDQuMzksOC42NSwxMC4zNywxMC4zNywwLDAsMCw5LDMuMDZjMy4yMi0uNjEsNi0zLjQ2LDYuMTEtNi43M2ExMi43NCwxMi43NCwwLDAsMC0uOTQtNC4zM0w3ODMuMzgsNTU4YTEsMSwwLDAsMC0uNDgtLjY3LDEsMSwwLDAsMC0uNzUuMTNjLTEuNjEuNzYtNC44NCwxLjU2LTUuNzgsMy4yM1M3NzYuODcsNTY0LjUyLDc3Ni4xOSw1NjYuMzNaIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMTI1LjgyIC03MSkiIGZpbGw9IiNmYmIzYjIiLz48cGF0aCBkPSJNNzczLDU2NS4zNGMyLjQ5LS4zOSw0LjY3LTEuODUsNy0yLjgxczUuMjUtMS4zMyw3LjIxLjI3Yy41Ni40NiwxLjEsMS4wOSwxLjgzLDEuMDhhNzEuNTksNzEuNTksMCwwLDAtNC40OC0xNC4yNCwxLjExLDEuMTEsMCwwLDAtLjM5LS41NSwxLjEzLDEuMTMsMCwwLDAtLjg1LDBsLTYuNzMsMS43NmMtMi40OS42NS0yLjc4LjQ1LTIuNTksMi45Qzc3NC4wNSw1NTQuODQsNzc0LjYxLDU2NS4zNCw3NzMsNTY1LjM0WiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyNS44MiAtNzEpIiBmaWxsPSIjMzIzNDQ0Ii8+PHBhdGggZD0iTTc3Mi4yNiw0MjIuOTRjLTEsMS41NC0xLDMuNDYtMSw1LjI3LDAsOC44NS4wOSwxNy43NSwxLjQsMjYuNTEuMzEsMi4xLjcsNC4yLjksNi4zMmE3Mi45MSw3Mi45MSwwLDAsMSwuMTQsOC44N2wtMSwzOC41Yy0uMTIsNC43MS0uMzYsOS43Ny0zLjI3LDEzLjQ3YTYuNDQsNi40NCwwLDAsMC0xLjE3LDQuMjdjLjc2LDkuNjYsMi4zNiwxOS4yNCwzLjk1LDI4Ljc5YTE3Ljc5LDE3Ljc5LDAsMCwxLDE2LjE0Ljc3LDE3Ny42NiwxNzcuNjYsMCwwLDAsOC4yOS00OWMuMjMtOC4xOS0uMTItMTYuNDMsMS4xNC0yNC41MiwyLjExLTEzLjYyLDEuMjUtMjcuNTktLjMtNDEuMjktLjQ5LTQuMzQtMS41My04LjgxLTQuMzEtMTIuMTdhMTguNDUsMTguNDUsMCwwLDAtMTAtNS43NkM3NzkuNDcsNDIyLDc3Ni4xNiw0MjMsNzcyLjI2LDQyMi45NFoiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMjUuODIgLTcxKSIgZmlsbD0iIzViNTU4MyIvPjxwYXRoIGQ9Ik03NzIuMjYsNDIyLjk0Yy0xLDEuNTQtMSwzLjQ2LTEsNS4yNywwLDguODUuMDksMTcuNzUsMS40LDI2LjUxLjMxLDIuMS43LDQuMi45LDYuMzJhNzIuOTEsNzIuOTEsMCwwLDEsLjE0LDguODdsLTEsMzguNWMtLjEyLDQuNzEtLjM2LDkuNzctMy4yNywxMy40N2E2LjQ0LDYuNDQsMCwwLDAtMS4xNyw0LjI3Yy43Niw5LjY2LDIuMzYsMTkuMjQsMy45NSwyOC43OWExNy43OSwxNy43OSwwLDAsMSwxNi4xNC43NywxNzcuNjYsMTc3LjY2LDAsMCwwLDguMjktNDljLjIzLTguMTktLjEyLTE2LjQzLDEuMTQtMjQuNTIsMi4xMS0xMy42MiwxLjI1LTI3LjU5LS4zLTQxLjI5LS40OS00LjM0LTEuNTMtOC44MS00LjMxLTEyLjE3YTE4LjQ1LDE4LjQ1LDAsMCwwLTEwLTUuNzZDNzc5LjQ3LDQyMiw3NzYuMTYsNDIzLDc3Mi4yNiw0MjIuOTRaIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMTI1LjgyIC03MSkiIG9wYWNpdHk9IjAuMSIvPjxwYXRoIGQ9Ik03ODQuNDgsNTM0LjU5QTE3Ni42MSwxNzYuNjEsMCwwLDAsNzk1LDYzNi44M2EyNy43MywyNy43MywwLDAsMSwyLjQ0LDcuNTZjLjU1LDQuOS0xLjcxLDkuNjEtMywxNC4zNS0zLDEwLjc4LTEuMjcsMjIuMjYuNjUsMzMuMjlxMS4yLDYuOSwyLjQ3LDEzLjc5Yy44Myw0LjQ4LDEuNjMsOS4zNS0uNDUsMTMuNDEsMS43OSw3LjQ2LDIuODUsMTQuODUsNC42NCwyMi4zMWE0LjI0LDQuMjQsMCwwLDEsLjE3LDEuODMsNS4zOSw1LjM5LDAsMCwxLTEuODMsMi40NSwxMC45NCwxMC45NCwwLDAsMC0yLjc5LDEwLjQ3YzQuNTctMy4yOCwxMC45NC0yLjEzLDE2LjE2LDBzMTAuMzYsNSwxNiw1Yy0uODItNi42Mi0xLjYxLTEzLjU3LjgzLTE5Ljc4LDEuNDItMy42LDMuOTItNywzLjg1LTEwLjg1LS4wNy0zLjQ1LTIuMTgtNi41My0yLjY5LTkuOTRhMjUuMTYsMjUuMTYsMCwwLDEsLjI0LTYuMzZjMS4zNC0xMi4yNC0uMTgtMjQuNi0xLjctMzYuODJhMjIsMjIsMCwwLDAtMS42OC03Yy0uNzEtMS40NC0xLjc3LTIuODItMS43NS00LjQzLDAtMS44NywxLjUxLTMuMzksMi4wNy01LjE3LDEtMy4yOC0uODQtNy43NCwxLjkzLTkuNzcsNy4zLTUuMzYsNC41LTE4LjE2LDQuMzQtMjcuMjFxLS4xOS0xMS43MS0xLTIzLjRhOTkuNjcsOTkuNjcsMCwwLDEsNS41Miw0MC4zNGMtLjMyLDQuNDgtLjkxLDkuMTkuODQsMTMuMzMsMS4zNCwzLjE4LDQsNS44LDQuNzIsOS4xNy40NSwyLjA4LjEzLDQuMjMuMjMsNi4zNXMuODIsNC40MywyLjY1LDUuNWMuMTQsOS42NCwxLDE5Ljk1LDEuMTUsMjkuNTlhNzMsNzMsMCwwLDAsMS4yLDE0LjcsMTguNzMsMTguNzMsMCwwLDEsLjc0LDQuNzQsMTkuODEsMTkuODEsMCwwLDEtMS41OCw1LjgzLDMzLjQzLDMzLjQzLDAsMCwwLDUsMzAuODVjMi4zNi00LjE5LDcuMjgtNi40MSwxMi4wOC02Ljc2czkuNTQuODYsMTQuMTksMi4wOGEyNy43OSwyNy43OSwwLDAsMSwzLjMyLTE2LjksMTMuODMsMTMuODMsMCwwLDAsMS43NS0zLjc2Yy41NC0yLjU0LS43Mi01LjA3LTEuNC03LjU4LTEuMTEtNC0uNzItOC4zMS0uNDYtMTIuNDlBMTk3LjY0LDE5Ny42NCwwLDAsMCw4ODIsNjczLjYzYTM1LjUxLDM1LjUxLDAsMCwwLTEuOTEtOGMtLjM2LS45Mi0uOC0xLjgtMS4xLTIuNzNhMjEuNTIsMjEuNTIsMCwwLDEtLjgtNS4xMmwtMS4xNS0xNmMtLjgxLTExLjIxLDIuODctMjIuMjgsNS40NC0zMy4yMiwxLjE1LTQuOSwyLjQtOS43OSwzLjE3LTE0Ljc3LDEuMDUtNi43OCwxLjIyLTEzLjcxLDIuNzYtMjAuNCwxLjM4LTYsMy44Ny0xMS44NSw0LjM5LTE4LC44LTkuNTMtMy4xNi0xOC43NC03LTI3LjQ4LTEuNi0zLjYtNy42NS0zLjI0LTExLjU0LTMuODgtMjcuNTktNC41My01Ni42NS00LjU2LTgyLjY3LDUuNjVBMjAuNTcsMjAuNTcsMCwwLDAsNzg0LjQ4LDUzNC41OVoiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMjUuODIgLTcxKSIgZmlsbD0iIzNjMzU0YyIvPjxwYXRoIGQ9Ik04MDQuMzcsMzU3LjEsODA3LjQzLDM2OWEzMS44LDMxLjgsMCwwLDEsMS4zNyw4LjQxLDYuMjEsNi4yMSwwLDAsMS0uNjcsMyw3LjE1LDcuMTUsMCwwLDEtMS45LDEuOTRjLTIuMDksMS41OS0zLjU0LDUuMy01LjkzLDYuNCwxLjIzLDIuMTQsMi45My43NSw1LjE1LDEuODIsMy45MSwxLjksNy40OSw0LjYzLDExLjczLDUuNTcsNCwuODgsOC4yLjA1LDEyLjE3LTEsNS42My0xLjUzLDExLjIzLTMuNjQsMTUuNzYtNy4zM3M3LjExLTYuOTUsNy4wOS0xMi43OGMtNSwuNTktOS40NS00LjQ2LTExLjY2LTlhMjQuNDUsMjQuNDUsMCwwLDEtMS42OC01LjM5bC0yLjY4LTExLjc5Yy0yLjkyLjY0LTUuMywyLjczLTguMDksMy44MlM4MjIsMzUzLjg2LDgxOC45LDM1NGE5OSw5OSwwLDAsMC0xNi4zNiwyLjEyYy0uNzQuMTUtMS42Ny42Mi0xLjQ5LDEuMzQiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMjUuODIgLTcxKSIgZmlsbD0iI2ZiYjNiMiIvPjxwYXRoIGQ9Ik04MDQuMzcsMzU3LjEsODA3LjQzLDM2OWEzMS44LDMxLjgsMCwwLDEsMS4zNyw4LjQxLDYuMjEsNi4yMSwwLDAsMS0uNjcsMyw3LjE1LDcuMTUsMCwwLDEtMS45LDEuOTRjLTIuMDksMS41OS0zLjU0LDUuMy01LjkzLDYuNCwxLjIzLDIuMTQsMi45My43NSw1LjE1LDEuODIsMy45MSwxLjksNy40OSw0LjYzLDExLjczLDUuNTcsNCwuODgsOC4yLjA1LDEyLjE3LTEsNS42My0xLjUzLDExLjIzLTMuNjQsMTUuNzYtNy4zM3M3LjExLTYuOTUsNy4wOS0xMi43OGMtNSwuNTktOS40NS00LjQ2LTExLjY2LTlhMjQuNDUsMjQuNDUsMCwwLDEtMS42OC01LjM5bC0yLjY4LTExLjc5Yy0yLjkyLjY0LTUuMywyLjczLTguMDksMy44MlM4MjIsMzUzLjg2LDgxOC45LDM1NGE5OSw5OSwwLDAsMC0xNi4zNiwyLjEyYy0uNzQuMTUtMS42Ny42Mi0xLjQ5LDEuMzQiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMjUuODIgLTcxKSIgb3BhY2l0eT0iMC4xIi8+PGNpcmNsZSBjeD0iNjkxLjY5IiBjeT0iMjY2LjE4IiByPSIyNi40OCIgZmlsbD0iI2ZiYjNiMiIvPjxwYXRoIGQ9Ik04MjQuOCwzODAuODNhMjQsMjQsMCwwLDEsNi04YzMuNzMtMy4yNyw4LjgzLTUuOTIsOS43MS0xMC44bDguMDgsOS40MWE0LjM1LDQuMzUsMCwwLDEsMSwxLjU0LDMuODgsMy44OCwwLDAsMS0uNzYsMy4xMWMtMiwzLjE5LTUuMTUsNS40Ny04LjEzLDcuNzhhMjQ2LjkxLDI0Ni45MSwwLDAsMC0xOS41OSwxNy4yOCwyLDIsMCwwLDEtMS4wNS42NCwxLjg5LDEuODksMCwwLDEtMS4wOS0uMzFBNDUuNDksNDUuNDksMCwwLDEsODA1LDM5MC4xMmMtLjI5LS4zNS0uNjUtLjc1LTEuMTItLjcyYTEuNDQsMS40NCwwLDAsMC0uNzUuMzljLTIuNjksMi4yLTUuNjMsNC44My05LjA4LDQuNDksNC40Ny0zLjIxLDctOC41Nyw3Ljk0LTE0YTI2LjQ2LDI2LjQ2LDAsMCwxLDEuMTQtNS40Nyw1LjcxLDUuNzEsMCwwLDEsMy45LTMuN2MtMi4xOCwzLjMzLS42OSw4LjA1LDIuMjQsMTAuNzRhMjIuMDgsMjIuMDgsMCwwLDAsOS45Miw0LjgxQzgyMi41OSwzODcuMyw4MjMuNTksMzgzLjQ1LDgyNC44LDM4MC44M1oiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMjUuODIgLTcxKSIgZmlsbD0iIzMyMzQ0NCIvPjxwYXRoIGQ9Ik03OTAuMzUsNTM3LjMxYzMuNzcuOTMsNy4zNCwyLjUxLDExLDMuNjhBNTIuNTcsNTIuNTcsMCwwLDAsODIyLDU0My4xNmExMS4xNSwxMS4xNSwwLDAsMCw2LTEuOTFjLjQ3LS4zOC45LS44MywxLjQtMS4xOGE5Ljc5LDkuNzksMCwwLDEsMi42OS0xLjExYzkuMTctMi44NywxNi44NS05LjA2LDI0LjMtMTUuMTIuMjQtLjIuNTEtLjQ1LjQ5LS43N2ExLDEsMCwwLDAtLjMtLjU3bC0zLjkyLTQuNWMtMTAuMjgsMS43NS0yMC44MSwxLjA5LTMxLjI0LjgzQTQ1LjM2LDQ1LjM2LDAsMCwwLDgxNSw1MTljLTIuMDYuMjQtNC4wOS43Ni02LjEyLDEuMi03LjcxLDEuNjgtMTUuNTksMi4zMi0yMy40LDMuNDJhMy42MSwzLjYxLDAsMCwwLTEuNTUuNDgsMy40OSwzLjQ5LDAsMCwwLS44My45MmwtMi43NCwzLjg1YTEyLjExLDEyLjExLDAsMCwwLTIuMyw0LjQxYy0uNjQsMywuNyw0LDMuMjUsMy42MUEyMy43NCwyMy43NCwwLDAsMSw3OTAuMzUsNTM3LjMxWiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyNS44MiAtNzEpIiBmaWxsPSIjMzIzNDQ0Ii8+PHBhdGggZD0iTTgyMSwzOTYuNTdhNDguNzEsNDguNzEsMCwwLDAtMTAuMzEtOC4wNSwxNC42MSwxNC42MSwwLDAsMC01LTIsNi4yNCw2LjI0LDAsMCwwLTUuMTIsMS4yNmMtLjg5Ljc5LTEuNDUsMS44OS0yLjMxLDIuNzJhMTEuNDksMTEuNDksMCwwLDEtMy42NiwyLjA3LDY0LjkyLDY0LjkyLDAsMCwwLTEyLjg2LDcuMzMsMjkuNSwyOS41LDAsMCwwLTUuODMsNS4zOGMtNC41Myw1LjgtNS4yMSwxMy42OS01LjA5LDIxLjA1LjA5LDUuMTIsNSw4LjkyLDguMzgsMTIuNzVhOTMuOTQsOTMuOTQsMCwwLDEsOC41OCwxMmMxLjgyLDIuODgsMy43Miw2LDMuNDksOS40My0uMTksMi44MS0xLjgzLDUuNDUtMS41Nyw4LjI1LjA5LDEsLjQxLDEuOTIuNSwyLjg5LjE4LDItLjYxLDQtLjgxLDYtLjI3LDIuODMuNjUsNS42NC43LDguNDlhMjcsMjcsMCwwLDEtLjc0LDUuNzljLTEuOTIsOS4xNC00LjMzLDE4LjMzLTMuODQsMjcuNjZsLTUuNTQsMWE0LjY4LDQuNjgsMCwwLDEtMS4wNyw3LjQ3YzguNjUsMi44OSwxOCwxLjQzLDI3LjE3LDEuNDIsNy41OSwwLDE1LjE1LDEsMjIuNzMuODZzMTUuNC0xLjUxLDIxLjY1LTUuOGMxLjctMS4xNiwzLjI2LTIuNTIsNS4wNS0zLjUzYTI0LjkxLDI0LjkxLDAsMCwxLDcuNjUtMi41LDc1LjkxLDc1LjkxLDAsMCwxLDE1LTEuMzRjMi40NiwwLDUuMTQuMSw3LjEtMS4zOCwyLjE2LTEuNjQsMi43MS00LjYxLDMtNy4zLjI5LTIuODQuNDctNS42OS41Mi04LjU0YTM2LjgyLDM2LjgyLDAsMCwwLS4zNS02LjY0LDQzLjQ4LDQzLjQ4LDAsMCwwLTEuMTctNC43NmwtMy43Ny0xMy4yOGMtMS41Ni01LjQ4LjYxLTExLjQ5LDEuMDctMTcuMTcuMTEtMS4zNC4xMy0yLjktLjktMy43Ni0uMzctLjMxLS44OC0uNTItMS0xYTEuNzEsMS43MSwwLDAsMSwuMjQtMS4zNGMyLTQsNS03LjUzLDcuNzQtMTEuMTRhMjI3LjY0LDIyNy42NCwwLDAsMCwxMi44LTE5LjY3LDYzLjI5LDYzLjI5LDAsMCwwLTE2Ljk0LTM3Ljg4Yy0yLTIuMTctNC4yOS00LjI1LTcuMDktNS4yM2EyMSwyMSwwLDAsMC01LjY0LS45MWMtNy44NC0uNTMtMTYtMS0yMi44My00Ljk0YTQuMzQsNC4zNCwwLDAsMC0xLjYzLS42OWMtMS41MS0uMTctMi42MSwxLjMyLTMuNTksMi41LTIuNTIsMy02LjIzLDQuNzItOS40OSw2LjkzQzgzMC4xNCwzODUuMSw4MjUuMzksMzkwLjc4LDgyMSwzOTYuNTdaIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMTI1LjgyIC03MSkiIGZpbGw9IiM1YjU1ODMiLz48cGF0aCBkPSJNOTA0LjExLDQyNS4yOGMxLjU2LDQuOTQsMS40MSwxMC4yMiwxLjkyLDE1LjM3YTU5LjgsNTkuOCwwLDAsMCwxLjYzLDkuMjEsMTQuNywxNC43LDAsMCwwLDEuOSw0LjY5Yy45LDEuMzIsMi4xOSwyLjM5LDIuNzYsMy44OGE5LjM3LDkuMzcsMCwwLDEsLjQxLDMuMTJsLjEyLDYuOWEyNC44MSwyNC44MSwwLDAsMS0xLjYzLDEwLjc0bC00LjMxLDEzLjExYy0yLjMzLDcuMS00LjcyLDE0LjMxLTguOTIsMjAuNDlhNS45MSw1LjkxLDAsMCwxLTIuNTcsMi40MSwxMi40OCwxMi40OCwwLDAsMS0yLjU5LjQsNi42Niw2LjY2LDAsMCwwLTUuNDksNi40NywxNS4xOSwxNS4xOSwwLDAsMC0zLjY5LTMuNzdsLTguNzctN2MtMy0yLjQ0LTYuMTMtNC45Mi05Ljc3LTYuMzNhMjYuNDksMjYuNDksMCwwLDAsMTguNDItMjIuMjYsMTAsMTAsMCwwLDEsMS00LjM4Yy43My0xLjE4LDIuMDgtMi4wOCwyLjE4LTMuNDcuMTItMS43NS0xLjg2LTMuMDctMS44Ni00LjgyLDAtMS4xNi44Ni0yLjEyLDEuMjQtMy4yMWE4LjA2LDguMDYsMCwwLDAsMC00LjExTDg4NC44OCw0NTZhNS4xMyw1LjEzLDAsMCwwLS42LTEuOTIsMTIuNDIsMTIuNDIsMCwwLDAtMS41LTEuNThjLTIuMDgtMi4zMy0xLjE2LTYsMC04Ljg3QTg0Ljc4LDg0Ljc4LDAsMCwxLDg5Myw0MjUuN2E2MS4zMSw2MS4zMSwwLDAsMCw0LjA3LTUuODJjMS4wNi0xLjg0LDEuMy00LjM5LDIuNDItNkM5MDAuOTMsNDE3LjY2LDkwMi44OCw0MjEuMzksOTA0LjExLDQyNS4yOFoiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMjUuODIgLTcxKSIgZmlsbD0iIzViNTU4MyIvPjxwYXRoIGQ9Ik04NjQuOCw1MDUuMzhhNC44Miw0LjgyLDAsMCwwLTEuMTQsMS4yLDEwLjExLDEwLjExLDAsMCwxLTQuNTMsMy4yM2MxLC43MiwxLjkxLDEuNDMsMi44NSwyLjE2YTEyNC44OCwxMjQuODgsMCwwLDEsMTksMTguMTdjLjYzLTIuMjUsNC40LTIuMDksNS4zMi00LjI0YTQuMTUsNC4xNSwwLDAsMCwuMi0xLjkyLDU4LjU3LDU4LjU3LDAsMCwwLTEuNDQtMTAsMTEuMzIsMTEuMzIsMCwwLDAtMi00LjY4Yy0xLjQtMS42OS0zLjU4LTIuNS01LjY2LTMuMkM4NzQuMjUsNTA1LDg2OCw1MDMuNDUsODY0LjgsNTA1LjM4WiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyNS44MiAtNzEpIiBmaWxsPSIjMzIzNDQ0Ii8+PHBhdGggZD0iTTg1Mi4zLDUxMy4yNGMtMywyLjIyLTUuNjMsNS05LDYuNTItMi4zOCwxLjA4LTUuMDksMS41NS03LjE3LDMuMTYsMS4xMywyLjQ5LDQuMDcsMy43OCw2LjgsMy42OGExNi4xNiwxNi4xNiwwLDAsMCw3LjYxLTIuNzljMS43OS0xLjEsMy44OS0yLjM4LDUuODQtMS42MS4zLDEuNTItMSwyLjk1LTEsNC40OXMxLjI4LDIuNjYsMi41NCwzLjQ3YzYsMy44NywxMy43MiwzLjU1LDIwLjg3LDMuMWExLjg4LDEuODgsMCwwLDAsMS4xNS0uMzQsMS44MSwxLjgxLDAsMCwwLC40My0xLjMyYy4wOS0xLjU4LjEzLTMuMTUuMTQtNC43M2E2Ljc4LDYuNzgsMCwwLDAtMi45LTYuNjgsODEuNjEsODEuNjEsMCwwLDAtMTIuNS04Ljg1Qzg2MC43MSw1MDguNzksODU2LjI1LDUxMC4zLDg1Mi4zLDUxMy4yNFoiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMjUuODIgLTcxKSIgZmlsbD0iI2ZiYjNiMiIvPjxwYXRoIGQ9Ik04MjYuODEsMzI2LjExYy00LjQ0LjUzLTcuNjcsNC03LjIyLDcuNzdzNC40MSw2LjM3LDguODUsNS44Myw3LjY3LTQsNy4yMi03Ljc2UzgzMS4yNSwzMjUuNTgsODI2LjgxLDMyNi4xMVptMS41MSwxMi41NmMtMy43Ni40NS03LjExLTEuNzYtNy41LTQuOTRzMi4zNi02LjEyLDYuMTEtNi41Nyw3LjExLDEuNzYsNy41LDQuOTRTODMyLjA3LDMzOC4yMiw4MjguMzIsMzM4LjY3WiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyNS44MiAtNzEpIiBmaWxsPSIjM2MzNTRjIi8+PHBhdGggZD0iTTgwNS4xNywzMjguNzFjLTQuNDQuNTMtNy42Nyw0LTcuMjIsNy43NnM0LjQxLDYuMzcsOC44NSw1Ljg0LDcuNjctNCw3LjIyLTcuNzdTODA5LjYxLDMyOC4xOCw4MDUuMTcsMzI4LjcxWm0xLjUxLDEyLjU1Yy0zLjc2LjQ1LTcuMTEtMS43Ni03LjQ5LTQuOTNzMi4zNS02LjEyLDYuMTEtNi41OCw3LjExLDEuNzYsNy40OSw0Ljk0UzgxMC40MywzNDAuODEsODA2LjY4LDM0MS4yNloiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMjUuODIgLTcxKSIgZmlsbD0iIzNjMzU0YyIvPjxwb2x5Z29uIHBvaW50cz0iNjYzLjI4IDI1OS42NCA2NzIuOTMgMjYxLjcgNjcxLjk4IDI2NC4yNCA2NjIuODggMjYxLjU3IDY2My4yOCAyNTkuNjQiIGZpbGw9IiMzYzM1NGMiLz48cG9seWdvbiBwb2ludHM9IjcxNy4wNyAyNTMuMTggNzA4LjE3IDI1Ny40NyA3MDkuNyAyNTkuNzEgNzE3LjkxIDI1NC45NiA3MTcuMDcgMjUzLjE4IiBmaWxsPSIjM2MzNTRjIi8+PHBvbHlnb24gcG9pbnRzPSI2ODcuMzEgMjYxLjA2IDY5NC4wOCAyNjAuMjUgNjkzLjczIDI2MS45MyA2ODcuOTIgMjYyLjMyIDY4Ny4zMSAyNjEuMDYiIGZpbGw9IiMzYzM1NGMiLz48cGF0aCBkPSJNODAwLDMyOS43OWExMC43NCwxMC43NCwwLDAsMCwxLTQuMzcsOS4zNCw5LjM0LDAsMCwxLC40Ni0yLjY2LDcuNDQsNy40NCwwLDAsMSwyLjE4LTIuNzljMy4xMi0yLjY0LDcuNTktNCwxMi00LjE5YTI3Ljc0LDI3Ljc0LDAsMCwxLDEzLjg4LDMsMTAuOCwxMC44LDAsMCwxLDMuNDUsMi41NmMxLjQsMS43MSwxLjcsMy45MiwzLjExLDUuNjFhOC4xNyw4LjE3LDAsMCwwLDcuNjYsMi40Yy40OS0xLjc0LS4xNS0zLjU4LjEtNS4zNmEyNS45MywyNS45MywwLDAsMSwxLjU5LTQuNDRjMS41NS00LjU3LS43MS05Ljg3LTUuMzctMTIuNi0xLjYzLTEtMy41Ni0xLjY1LTQuNzgtM3MtMS41MS0yLjc1LTIuMzUtNC4xYy0yLjIzLTMuNTctOC01LjI0LTEyLjM5LTMuNTktMS4zOC41Mi0yLjYsMS4zMS00LDEuODctMi42LDEuMDctNS41NiwxLjI2LTguNDIsMS42MmEyNS43OSwyNS43OSwwLDAsMC04LjE2LDIuMTRjLTIuNDcsMS4yMi00LjU0LDMuMTgtNS4xMSw1LjUyLS4yNywxLjA4LS4yMSwyLjItLjQ4LDMuMjctMS4zOCw1LjQzLTEwLjI5LDguMDctMTAuNzksMTMuNjEtLjE4LDIsLjkxLDMuOTIsMi4yNyw1LjU1Ljk0LDEuMTEsMy4xOSw0LjA4LDQuNzgsNC41MXMyLjgtMS4wOCw0LjMyLTEuNkM3OTcuMzUsMzMyLDc5OC44LDMzMS44NCw4MDAsMzI5Ljc5WiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyNS44MiAtNzEpIiBmaWxsPSIjY2JjZWRhIi8+PC9nPjxwYXRoIGQ9Ik05MTIuODEsNjgyYzAsNTAuMjQsMzEuNTIsOTAuOSw3MC40Nyw5MC45IiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMTI1LjgyIC03MSkiIGZpbGw9IiM0NjQ1NWIiLz48cGF0aCBkPSJNOTgzLjI4LDc3Mi45MWMwLTUwLjgxLDM1LjE4LTkxLjkyLDc4LjY1LTkxLjkyIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMTI1LjgyIC03MSkiIGZpbGw9IiM0ZDk2YjgiLz48cGF0aCBkPSJNOTM4LjM1LDY4Ni41NmMwLDQ3LjczLDIwLjEsODYuMzUsNDQuOTMsODYuMzUiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMjUuODIgLTcxKSIgZmlsbD0iIzRkOTZiOCIvPjxwYXRoIGQ9Ik05ODMuMjgsNzcyLjkxYzAtNjQuOTIsNDAuNjYtMTE3LjQ2LDkwLjktMTE3LjQ2IiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMTI1LjgyIC03MSkiIGZpbGw9IiM0NjQ1NWIiLz48ZWxsaXBzZSBjeD0iODU0LjQxIiBjeT0iNzE2LjMxIiByeD0iMTcuNTIiIHJ5PSIyLjk2IiBmaWxsPSIjNGQ5NmI4IiBvcGFjaXR5PSIwLjEiLz48cGF0aCBkPSJNOTY4LjQ2LDc3My41NXMxMC0uMzEsMTMtMi40NSwxNS4zNy00LjcxLDE2LjEyLTEuMjcsMTUsMTcuMTEsMy43MywxNy4yLTI2LjIyLTEuNzYtMjkuMjItMy41OVM5NjguNDYsNzczLjU1LDk2OC40Niw3NzMuNTVaIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMTI1LjgyIC03MSkiIGZpbGw9IiNhOGE4YTgiLz48cGF0aCBkPSJNMTAwMS41Miw3ODUuODNjLTExLjI4LjA5LTI2LjIxLTEuNzYtMjkuMjItMy41OS0yLjI5LTEuMzktMy4yLTYuNC0zLjUxLTguN2gtLjMzcy42Myw4LjA2LDMuNjQsOS44OSwxNy45NCwzLjY4LDI5LjIyLDMuNTljMy4yNiwwLDQuMzgtMS4xOSw0LjMyLTIuOUMxMDA1LjE5LDc4NS4xNiwxMDA0LDc4NS44MSwxMDAxLjUyLDc4NS44M1oiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMjUuODIgLTcxKSIgb3BhY2l0eT0iMC4yIi8+PHBhdGggZD0iTTE0OC4zMSw3MTEuMzZjMCw0MCwyNS4wNyw3Mi4zMiw1Ni4wNiw3Mi4zMiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyNS44MiAtNzEpIiBmaWxsPSIjNDY0NTViIi8+PHBhdGggZD0iTTIwNC4zNyw3ODMuNjhjMC00MC40MiwyOC03My4xMyw2Mi41Ny03My4xMyIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyNS44MiAtNzEpIiBmaWxsPSIjNGQ5NmI4Ii8+PHBhdGggZD0iTTE2OC42Miw3MTVjMCwzOCwxNiw2OC43LDM1Ljc1LDY4LjciIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMjUuODIgLTcxKSIgZmlsbD0iIzRkOTZiOCIvPjxwYXRoIGQ9Ik0yMDQuMzcsNzgzLjY4YzAtNTEuNjUsMzIuMzUtOTMuNDUsNzIuMzItOTMuNDUiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xMjUuODIgLTcxKSIgZmlsbD0iIzQ2NDU1YiIvPjxlbGxpcHNlIGN4PSI3Ni4xMiIgY3k9IjcyNC4xNCIgcng9IjEzLjk0IiByeT0iMi4zNiIgZmlsbD0iIzRkOTZiOCIgb3BhY2l0eT0iMC4xIi8+PHBhdGggZD0iTTE5Mi41OCw3ODQuMTlzNy45NS0uMjUsMTAuMzQtMiwxMi4yNC0zLjc1LDEyLjgzLTEsMTEuOTUsMTMuNjEsMywxMy42OC0yMC44Ni0xLjQtMjMuMjUtMi44NVMxOTIuNTgsNzg0LjE5LDE5Mi41OCw3ODQuMTlaIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMTI1LjgyIC03MSkiIGZpbGw9IiNhOGE4YTgiLz48cGF0aCBkPSJNMjE4Ljg4LDc5NGMtOSwuMDctMjAuODYtMS40LTIzLjI1LTIuODYtMS44Mi0xLjEtMi41NC01LjA5LTIuNzktNi45MmgtLjI2cy41LDYuNDEsMi44OSw3Ljg3LDE0LjI4LDIuOTIsMjMuMjUsMi44NWMyLjU5LDAsMy40OS0uOTQsMy40NC0yLjMxQzIyMS44LDc5My40MywyMjAuODEsNzkzLjk0LDIxOC44OCw3OTRaIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMTI1LjgyIC03MSkiIG9wYWNpdHk9IjAuMiIvPjwvc3ZnPg=="
            subjects.insert({'name': name, 'institution': current_institution['_id'], 'image': image, 'public': public, 'users': [], 'teachers': teachers, 'waitingUsers': [], 'message': message})
            # subject is created
            return {
                'createSubject': '0'
            }
        else:
            # user is not the owner of the institution
            return {
            'createSubject': '1'
        }
    else:
        # institution id is invalid
        return {
            'createSubject': '1'
        }


def deleteSubjectData(id):
    subjects = mongo.db.subjects
    obj_subject = ObjectId(id)
    current_subject = subjects.find_one({'_id': obj_subject})
    subjectFiles = mongo.db.subjectFiles

    allFiles = subjectFiles.find({'subject': current_subject['_id']}).sort('name')
    grid_fs = GridFS(mongo.db)
    for file in allFiles:  
        grid_fs.delete(file['file'])
    
    subjectFiles.delete_many({'subject': current_subject['_id']})
    subjectFolders = mongo.db.folders
    subjectFolders.delete_many({'subject': current_subject['_id']})

    posts = mongo.db.posts
    allPosts = posts.find({'subject': current_subject['_id']})
    for post in allPosts:
        deletePostAndMessages(str(post['_id']))


@institution.route('/deleteSubject', methods=['DELETE'])
@jwt_required()
def deleteSubject():
    id_subject = request.json.get('subject')

    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})
     
    subjects = mongo.db.subjects
    obj_subject = ObjectId(id_subject)
    current_subject = subjects.find_one({'_id': obj_subject})
    institutions = mongo.db.institutions
    obj_institution = current_subject['institution']
    current_institution = institutions.find_one({'_id': obj_institution})

    if current_subject is not None:
        if user['_id'] == current_institution['owner']:
            deleteSubjectData(id_subject)
            subjects.delete_one({'_id': obj_subject})  
            # subject is deleted
            return {
                'delete': '0'
            }
        else:
            # user is not the owner of the institution
            return {
            'delete': '1'
        }
    else:
        # subject id is invalid 
        return {
            'delete': '1'
        }

@institution.route('/participantsInfo', methods=['POST'])
@jwt_required()
def participantsInfo():
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    id = request.json.get('id')

    institutions = mongo.db.institutions
    obj_institution = ObjectId(id)
    current_institution = institutions.find_one({'_id': obj_institution})

    if current_institution is not None:
        obj_owner = ObjectId(current_institution['owner'])
        ownerInfo = users.find_one({'_id': obj_owner}) 
        owner = {"name": ownerInfo['username'], "image": ownerInfo['photo']}

        allusers = current_institution['users']
        usersIns = []
        for userid in allusers:
            obj_user = ObjectId(userid)
            userInfo = users.find_one({'_id': obj_user})
            usersIns.append({"name": userInfo['username'], "image": userInfo['photo']})

        if(current_institution['owner'] == user['_id']):
            role = "owner"
        else:
            role = "user"

        isIn = isInInstitution(id, str(user['_id']))

        return {
        'ok': '0',
        'institution': current_institution['name'],
        'users': usersIns,
        'owner': owner,
        'role': role,
        'isIn': isIn
        }

    return {
        'ok': '1'
    }   


@institution.route('/addUserToInstitution', methods=['POST'])
@jwt_required()
def addUserToInstitution():

    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    id = request.json.get('id')
    username = request.json.get('username')

    institutions = mongo.db.institutions
    obj_institution = ObjectId(id)
    current_institution = institutions.find_one({'_id': obj_institution})

    if current_institution is not None:
        if(user['_id'] != current_institution['owner']):
            return{
                'ok': 'You are not the owner!'
            }
        new_user = users.find_one({'username': username})
        if new_user is not None:
            if new_user['_id'] == current_institution['owner']:
                return {
                'ok': 'This user is already in this institution!'
                } 
            alreadyUser = institutions.find({"$and": [ {'_id': current_institution['_id']}, {'users': new_user['_id']}]}).count()
            if alreadyUser > 0:
                return {
                'ok': 'This user is already in this institution!'
                }  
            else:
                mycol = mongo.db["institutions"]
                edited_institution = { "$addToSet": { "users": new_user['_id'] } }
                mycol.update_one(current_institution, edited_institution)
                new_institution = institutions.find_one({'_id': obj_institution})
                allusers = new_institution['users']
                usersIns = []
                for userid in allusers:
                    obj_user = ObjectId(userid)
                    userInfo = users.find_one({'_id': obj_user})
                    usersIns.append({"name": userInfo['username'], "image": userInfo['photo']})
                return {
                'ok': '0',
                'users': usersIns
                }
        else:
            return {
                'ok': 'This username does not exists!'
            }  

    return {
        'ok': 'An unexpected error occured!'
    } 


@institution.route('/removeUserFromInstitution', methods=['POST'])
@jwt_required()
def removeUserFromInstitution():

    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    id = request.json.get('id')
    username = request.json.get('username')

    institutions = mongo.db.institutions
    obj_institution = ObjectId(id)
    current_institution = institutions.find_one({'_id': obj_institution})

    if current_institution is not None:
        if(user['_id'] != current_institution['owner']):
            return{
                'ok': 'You are not the owner!'
            }
        new_user = users.find_one({'username': username})
        if new_user is not None:
            if new_user['_id'] == current_institution['owner']:
                return {
                'ok': '1'
                } 
            alreadyUser = institutions.find({"$and": [ {'_id': current_institution['_id']}, {'users': new_user['_id']}]}).count()
            if alreadyUser == 0:
                return {
                'ok': '1'
                }  
            else:
                mycol = mongo.db["institutions"]
                edited_institution = { "$pull": { "users": new_user['_id'] } }
                mycol.update_one(current_institution, edited_institution)
                new_institution = institutions.find_one({'_id': obj_institution})
                allusers = new_institution['users']
                usersIns = []
                for userid in allusers:
                    obj_user = ObjectId(userid)
                    userInfo = users.find_one({'_id': obj_user})
                    usersIns.append({"name": userInfo['username'], "image": userInfo['photo']})
                return {
                'ok': '0',
                'users': usersIns
                }
    return {
        'ok': '1'
    }     


@institution.route('/participantsSubjectInfo', methods=['POST'])
@jwt_required()
def participantsSubjectInfo():
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    id = request.json.get('id')

    subjects = mongo.db.subjects
    obj_subject = ObjectId(id)
    current_subject = subjects.find_one({'_id': obj_subject})

    if current_subject is not None:
        isTeacher = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'teachers': user['_id']}]}).count()
        if isTeacher > 0:
            role = "teacher"
        else:
            role = "user"
        allusers = current_subject['users']
        usersIns = []
        for userid in allusers:
            obj_user = ObjectId(userid)
            userInfo = users.find_one({'_id': obj_user})
            usersIns.append({"name": userInfo['username'], "image": userInfo['photo']})
        allteachers = current_subject['teachers']
        teachersIns = []
        for teacherid in allteachers:
            obj_teacher = ObjectId(teacherid)
            teacherInfo = users.find_one({'_id': obj_teacher})
            teachersIns.append({"name": teacherInfo['username'], "image": teacherInfo['photo']})

        isIn = isInSubject(id, str(user['_id']))

        return {
        'ok': '0',
        'subject': current_subject['name'],
        'users': usersIns,
        'teachers': teachersIns,
        'role': role,
        'isIn': isIn
        }

    return {
        'ok': '1'
    }


@institution.route('/addUserToSubject', methods=['POST'])
@jwt_required()
def addUserToSubject():
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    id = request.json.get('id')
    username = request.json.get('username')

    subjects = mongo.db.subjects
    obj_subject = ObjectId(id)
    current_subject = subjects.find_one({'_id': obj_subject})

    institutions = mongo.db.institutions
    current_institution = institutions.find_one({'_id': current_subject['institution']})

    if current_institution is not None:
        new_user = users.find_one({'username': username})
        isTeacher = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'teachers': user['_id']}]}).count()
        if isTeacher == 0:
            return {
                'ok': 'You are not a teacher!'
                } 
        if new_user is not None:
            isUserIns = institutions.find({"$and": [ {'_id': current_institution['_id']}, {'users': new_user['_id']}]}).count()
            if isUserIns == 0 and new_user['_id'] != current_institution['owner']: 
                return {
                'ok': 'This user is not in the institution of the subject!'
                } 
            else:
                alreadyUser = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'users': new_user['_id']}]}).count()
                if alreadyUser > 0:
                    return {
                        'ok': 'Already a user!'
                    } 
                alreadyTeacher = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'teachers': new_user['_id']}]}).count()
                if alreadyTeacher > 0:
                    return {
                        'ok': 'Already a teacher!'
                    } 

                mycol = mongo.db["subjects"]
                edited_subject = { "$addToSet": { "users": new_user['_id'] } }
                mycol.update_one(current_subject, edited_subject)

                new_subject = subjects.find_one({'_id': obj_subject})
                allusers = new_subject['users']
                usersIns = []
                for userid in allusers:
                    obj_user = ObjectId(userid)
                    userInfo = users.find_one({'_id': obj_user})
                    usersIns.append({"name": userInfo['username'], "image": userInfo['photo']})
                allteachers = new_subject['teachers']
                teachersIns = []
                for teacherid in allteachers:
                    obj_teacher = ObjectId(teacherid)
                    teacherInfo = users.find_one({'_id': obj_teacher})
                    teachersIns.append({"name": teacherInfo['username'], "image": teacherInfo['photo']})
                return {
                'ok': '0',
                'users': usersIns,
                'teachers': teachersIns
                }
        else:
            return {
                'ok': 'This username does not exists!'
            }  

    return {
        'ok': 'An unexpected error occured!'
    } 


@institution.route('/addTeacherToSubject', methods=['POST'])
@jwt_required()
def addTeacherToSubject():
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    id = request.json.get('id')
    username = request.json.get('username')

    subjects = mongo.db.subjects
    obj_subject = ObjectId(id)
    current_subject = subjects.find_one({'_id': obj_subject})

    institutions = mongo.db.institutions
    current_institution = institutions.find_one({'_id': current_subject['institution']})

    if current_institution is not None:
        new_user = users.find_one({'username': username})
        isTeacher = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'teachers': user['_id']}]}).count()
        if isTeacher == 0:
            return {
                'ok': 'You are not a teacher!'
                } 
        if new_user is not None:
            isUserIns = institutions.find({"$and": [ {'_id': current_institution['_id']}, {'users': new_user['_id']}]}).count()
            if isUserIns == 0 and new_user['_id'] != current_institution['owner']: 
                return {
                'ok': 'This user is not in the institution of the subject!'
                } 
            else:
                alreadyUser = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'users': new_user['_id']}]}).count()
                if alreadyUser > 0:
                    return {
                        'ok': 'Already a user!'
                    } 
                alreadyTeacher = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'teachers': new_user['_id']}]}).count()
                if alreadyTeacher > 0:
                    return {
                        'ok': 'Already a teacher!'
                    } 

                mycol = mongo.db["subjects"]
                edited_subject = { "$addToSet": { "teachers": new_user['_id'] } }
                mycol.update_one(current_subject, edited_subject)

                new_subject = subjects.find_one({'_id': obj_subject})
                allusers = new_subject['users']
                usersIns = []
                for userid in allusers:
                    obj_user = ObjectId(userid)
                    userInfo = users.find_one({'_id': obj_user})
                    usersIns.append({"name": userInfo['username'], "image": userInfo['photo']})
                allteachers = new_subject['teachers']
                teachersIns = []
                for teacherid in allteachers:
                    obj_teacher = ObjectId(teacherid)
                    teacherInfo = users.find_one({'_id': obj_teacher})
                    teachersIns.append({"name": teacherInfo['username'], "image": teacherInfo['photo']})
                return {
                'ok': '0',
                'users': usersIns,
                'teachers': teachersIns
                }
        else:
            return {
                'ok': 'This username does not exists!'
            }  

    return {
        'ok': 'An unexpected error occured!'
    } 


@institution.route('/removeUserFromSubject', methods=['POST'])
@jwt_required()
def removeUserFromSubject():
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    id = request.json.get('id')
    username = request.json.get('username')

    subjects = mongo.db.subjects
    obj_subject = ObjectId(id)
    current_subject = subjects.find_one({'_id': obj_subject})

    if current_subject is not None:
        new_user = users.find_one({'username': username})
        isTeacher = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'teachers': user['_id']}]}).count()
        if isTeacher == 0:
            return {
                'ok': 'You are not a teacher!'
                } 
        if new_user is not None:
            if new_user['_id'] == user['_id']:
                return {
                'ok': 'You can not delete yourself!'
                } 
            else:
                mycol = mongo.db["subjects"]
                edited_subject = { "$pull": { "users": new_user['_id'] } }
                edited_subject2 = { "$pull": { "teachers": new_user['_id'] } }
                mycol.update_one(current_subject, edited_subject)
                current_subject2 = subjects.find_one({'_id': obj_subject})
                mycol.update_one(current_subject2, edited_subject2)

                new_subject = subjects.find_one({'_id': obj_subject})
                allusers = new_subject['users']
                usersIns = []
                for userid in allusers:
                    obj_user = ObjectId(userid)
                    userInfo = users.find_one({'_id': obj_user})
                    usersIns.append({"name": userInfo['username'], "image": userInfo['photo']})
                allteachers = new_subject['teachers']
                teachersIns = []
                for teacherid in allteachers:
                    obj_teacher = ObjectId(teacherid)
                    teacherInfo = users.find_one({'_id': obj_teacher})
                    teachersIns.append({"name": teacherInfo['username'], "image": teacherInfo['photo']})
                return {
                'ok': '0',
                'users': usersIns,
                'teachers': teachersIns
                }
    return {
        'ok': 'An unexpected error occured!'
    }     


@institution.route('/makeTeacherSubject', methods=['POST'])
@jwt_required()
def makeTeacherSubject():
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    id = request.json.get('id')
    username = request.json.get('username')

    subjects = mongo.db.subjects
    obj_subject = ObjectId(id)
    current_subject = subjects.find_one({'_id': obj_subject})


    if current_subject is not None:
        isTeacher = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'teachers': user['_id']}]}).count()
        if isTeacher == 0:
            return {
                'ok': 'You are not a teacher!'
                } 
        new_user = users.find_one({'username': username})
        if new_user is not None:
            if new_user['_id'] == user['_id']:
                return {
                    'ok': 'You can not change yourself!'
                } 
            alreadyUser = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'users': new_user['_id']}]}).count()
            if alreadyUser == 0:
                return {
                    'ok': 'An unexpected error occured!'
                    } 
            alreadyTeacher = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'teachers': new_user['_id']}]}).count()
            if alreadyTeacher > 0:
                return {
                    'ok': 'Already a teacher!'
                } 

            mycol = mongo.db["subjects"]
            edited_subject = { "$addToSet": { "teachers": new_user['_id'] } }
            mycol.update_one(current_subject, edited_subject)
            current_subject2 = subjects.find_one({'_id': obj_subject})
            edited_subject2 = { "$pull": { "users": new_user['_id'] } }
            mycol.update_one(current_subject2, edited_subject2)

            new_subject = subjects.find_one({'_id': obj_subject})
            allusers = new_subject['users']
            usersIns = []
            for userid in allusers:
                obj_user = ObjectId(userid)
                userInfo = users.find_one({'_id': obj_user})
                usersIns.append({"name": userInfo['username'], "image": userInfo['photo']})
            allteachers = new_subject['teachers']
            teachersIns = []
            for teacherid in allteachers:
                obj_teacher = ObjectId(teacherid)
                teacherInfo = users.find_one({'_id': obj_teacher})
                teachersIns.append({"name": teacherInfo['username'], "image": teacherInfo['photo']})
            return {
                'ok': '0',
                'users': usersIns,
                'teachers': teachersIns
            }
    return {
        'ok': 'An unexpected error occured!'
    } 


@institution.route('/makeUserSubject', methods=['POST'])
@jwt_required()
def makeUserSubject():
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    id = request.json.get('id')
    username = request.json.get('username')

    subjects = mongo.db.subjects
    obj_subject = ObjectId(id)
    current_subject = subjects.find_one({'_id': obj_subject})


    if current_subject is not None:
        isTeacher = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'teachers': user['_id']}]}).count()
        if isTeacher == 0:
            return {
                'ok': 'You are not a teacher!'
                } 
        new_user = users.find_one({'username': username})
        if new_user is not None:
            if new_user['_id'] == user['_id']:
                return {
                    'ok': 'You can not change yourself!'
                } 
            alreadyTeacher = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'teachers': new_user['_id']}]}).count()
            if alreadyTeacher == 0:
                return {
                    'ok': 'An unexpected error occured!'
                    } 
            alreadyUser = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'users': new_user['_id']}]}).count()
            if alreadyUser > 0:
                return {
                    'ok': 'Already a user!'
                } 

            mycol = mongo.db["subjects"]
            edited_subject = { "$addToSet": { "users": new_user['_id'] } }
            mycol.update_one(current_subject, edited_subject)
            current_subject2 = subjects.find_one({'_id': obj_subject})
            edited_subject2 = { "$pull": { "teachers": new_user['_id'] } }
            mycol.update_one(current_subject2, edited_subject2)

            new_subject = subjects.find_one({'_id': obj_subject})
            allusers = new_subject['users']
            usersIns = []
            for userid in allusers:
                obj_user = ObjectId(userid)
                userInfo = users.find_one({'_id': obj_user})
                usersIns.append({"name": userInfo['username'], "image": userInfo['photo']})
            allteachers = new_subject['teachers']
            teachersIns = []
            for teacherid in allteachers:
                obj_teacher = ObjectId(teacherid)
                teacherInfo = users.find_one({'_id': obj_teacher})
                teachersIns.append({"name": teacherInfo['username'], "image": teacherInfo['photo']})
            return {
                'ok': '0',
                'users': usersIns,
                'teachers': teachersIns
            }
    return {
        'ok': 'An unexpected error occured!'
    }


@institution.route('/subjectPageInfo', methods=['POST'])
@jwt_required()
def subjectPageInfo():
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    id = request.json.get('id')

    subjects = mongo.db.subjects
    obj_subject = ObjectId(id)
    current_subject = subjects.find_one({'_id': obj_subject})

    pageNumber = request.json.get('pageNumber')
    nPerPage = 12

    if current_subject is not None:
        isTeacher = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'teachers': user['_id']}]}).count()
        if isTeacher > 0:
            role = "teacher"
        else:
            role = "user"
        
        institutions = mongo.db.institutions
        current_institution = institutions.find_one({'_id': current_subject['institution']})

        posts = mongo.db.posts

        postsNr = posts.find({'subject': current_subject['_id']}).count()
        nr = postsNr / nPerPage
        if(int(nr) < nr):
            nrPages = int(nr) + 1
        else:
            nrPages = int(nr)

        allPosts = posts.find({'subject': current_subject['_id']}).sort('date').skip(nPerPage *(pageNumber-1)).limit(nPerPage)
        postList = []
        for post in allPosts:
            postUser = users.find_one({'_id': post['op']})
            nameUser = postUser['firstname'] + " " + postUser['lastname']
            
            postList.append({"username": postUser['username'], "name": nameUser, "icon": postUser['photo'], "title": post['title'], "description": post['description'], "date": post['date'], "idPost": str(post['_id'])})

        isIn = isInSubject(id, str(user['_id']))

        return {
        'ok': '0',
        'subject': current_subject['name'],
        'institution': current_institution['name'],
        'institutionId': str(current_institution['_id']),
        'role': role,
        'postList': postList,
        'pages': nrPages,
        'isIn': isIn
        }

    return {
        'ok': '1'
    }


@institution.route('/getPostInfo', methods=['POST'])
@jwt_required()
def getPostInfo():
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    id = request.json.get('id') 

    pageNumber = request.json.get('pageNumber')
    nPerPage = 6

    posts = mongo.db.posts
    obj_post = ObjectId(id)
    current_post = posts.find_one({'_id': obj_post})

    subjects = mongo.db.subjects
    obj_subject = ObjectId(current_post['subject'])
    current_subject = subjects.find_one({'_id': obj_subject})

    if current_post is not None:
        hasMessage = current_subject["message"]
        isTeacher = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'teachers': user['_id']}]}).count()
        if isTeacher > 0:
            role = "teacher"
        else:
            role = "user"
                
        messages = mongo.db.messages
        postsNr =  messages.find({'post': current_post['_id']}).count()
        nr = postsNr / nPerPage
        if(int(nr) < nr):
            nrPages = int(nr) + 1
        else:
            nrPages = int(nr)

        allMessages = messages.find({'post': current_post['_id']}).sort("date").skip(nPerPage *(pageNumber-1)).limit(nPerPage)
        messagesList = []
        for message in allMessages:
            messageUser = users.find_one({'_id': message['user']})
            nameUser = messageUser['firstname'] + " " + messageUser['lastname']
            if(user['username'] == messageUser['username']):
                currentUser = True
            else:
                currentUser = False
            messagesList.append({"username": messageUser['username'], "name": nameUser, "icon": messageUser['photo'], "text": message['message'], "date": message['date'], "currentUser": currentUser, "idMessage": str(message['_id'])})

        isIn = isInSubject(str(current_subject['_id']), str(user['_id']))
        return {
        'ok': '0',
        'title': current_post['title'],
        'idSubject': str(current_subject['_id']),
        'subject': current_subject['name'],
        'role': role,
        'hasMessages': hasMessage, 
        'messagesList': messagesList,
        'pages': nrPages,
        'isIn': isIn
        }
    return {
        'ok': '1',
    }


@institution.route('/sendMessage', methods=['POST'])
@jwt_required()
def sendMessage():
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    id = request.json.get('id') 
    message = request.json.get('message') 

    pageNumber = request.json.get('pageNumber')
    nPerPage = 6

    posts = mongo.db.posts
    obj_post = ObjectId(id)
    current_post = posts.find_one({'_id': obj_post})

    subjects = mongo.db.subjects
    obj_subject = ObjectId(current_post['subject'])
    current_subject = subjects.find_one({'_id': obj_subject})

    if current_post is not None:
        hasMessage = current_subject["message"]
        isTeacher = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'teachers': user['_id']}]}).count()
        if isTeacher > 0:
            role = "teacher"
        else:
            role = "user"
        
        if(hasMessage or (hasMessage == False and role == "teacher")):
            messagesAdd = mongo.db.messages
            messagesAdd.insert({'user': user['_id'], 'post': current_post['_id'], 'message': message, 'files': [], 'date': datetime.now() })
        
        messages = mongo.db.messages
        postsNr =  messages.find({'post': current_post['_id']}).count()
        nr = postsNr / nPerPage
        if(int(nr) < nr):
            nrPages = int(nr) + 1
        else:
            nrPages = int(nr)

        allMessages = messages.find({'post': current_post['_id']}).sort("date").skip(nPerPage *(nrPages-1)).limit(nPerPage)
        messagesList = []
        for message in allMessages:
            messageUser = users.find_one({'_id': message['user']})
            nameUser = messageUser['firstname'] + " " + messageUser['lastname']
            if(user['username'] == messageUser['username']):
                currentUser = True
            else:
                currentUser = False
            messagesList.append({"username": messageUser['username'], "name": nameUser, "icon": messageUser['photo'], "text": message['message'], "date": message['date'], "currentUser": currentUser, "idMessage": str(message['_id'])})

        return {
        'ok': '0',
        'messagesList': messagesList,
        'pages': nrPages
        }
    return {
        'ok': '1',
    }


@institution.route('/refreshMessages', methods=['POST'])
@jwt_required()
def refreshMessages():
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    id = request.json.get('id') 

    posts = mongo.db.posts
    obj_post = ObjectId(id)
    current_post = posts.find_one({'_id': obj_post})

    pageNumber = request.json.get('pageNumber')
    nPerPage = 6

    if current_post is not None:        
        messages = mongo.db.messages
        postsNr =  messages.find({'post': current_post['_id']}).count()
        nr = postsNr / nPerPage
        if(int(nr) < nr):
            nrPages = int(nr) + 1
        else:
            nrPages = int(nr)

        allMessages = messages.find({'post': current_post['_id']}).sort("date").skip(nPerPage *(pageNumber-1)).limit(nPerPage)
        messagesList = []
        for message in allMessages:
            messageUser = users.find_one({'_id': message['user']})
            nameUser = messageUser['firstname'] + " " + messageUser['lastname']
            if(user['username'] == messageUser['username']):
                currentUser = True
            else:
                currentUser = False
            messagesList.append({"username": messageUser['username'], "name": nameUser, "icon": messageUser['photo'], "text": message['message'], "date": message['date'], "currentUser": currentUser, "idMessage": str(message['_id'])})

        return {
        'ok': '0',
        'messagesList': messagesList,
        'pages': nrPages
        }
    return {
        'ok': '1',
    }


@institution.route('/deleteMessage', methods=['DELETE'])
@jwt_required()
def deleteMessage():
    id_message = request.json.get('idMessage')
    
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    messages = mongo.db.messages
    obj_message = ObjectId(id_message)
    current_message = messages.find_one({'_id': obj_message})
    if current_message is not None:
        if user['_id'] == current_message['user']:
            messages.delete_one({'_id': obj_message})  

            id = request.json.get('id') 

            posts = mongo.db.posts
            obj_post = ObjectId(id)
            current_post = posts.find_one({'_id': obj_post})

            pageNumber = request.json.get('pageNumber')
            nPerPage = 6

            if current_post is not None:        
                messages = mongo.db.messages
                postsNr =  messages.find({'post': current_post['_id']}).count()
                nr = postsNr / nPerPage
                if(int(nr) < nr):
                    nrPages = int(nr) + 1
                else:
                    nrPages = int(nr)

                allMessages = messages.find({'post': current_post['_id']}).sort("date").skip(nPerPage *(pageNumber-1)).limit(nPerPage)
                messagesList = []
                for message in allMessages:
                    messageUser = users.find_one({'_id': message['user']})
                    nameUser = messageUser['firstname'] + " " + messageUser['lastname']
                    if(user['username'] == messageUser['username']):
                        currentUser = True
                    else:
                        currentUser = False
                  
                    messagesList.append({"username": messageUser['username'], "name": nameUser, "icon": messageUser['photo'], "text": message['message'], "date": message['date'], "currentUser": currentUser, "idMessage": str(message['_id'])})
            
                return {
                    'delete': '0',
                    'messagesList': messagesList,
                    'pages': nrPages
                }
        else:
            # user is not the owner of the message
            return {
            'delete': '1'
        }
   
    return {
        'delete': '1'
        }


@institution.route('/createPost', methods=['POST'])
@jwt_required()
def createPost():
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    id = request.json.get('id') 
    title = request.json.get('title') 
    description = request.json.get('description')

    pageNumber = request.json.get('pageNumber')
    nPerPage = 12

    subjects = mongo.db.subjects
    obj_subject = ObjectId(id)
    current_subject = subjects.find_one({'_id': obj_subject})

    if current_subject is not None:
        isTeacher = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'teachers': user['_id']}]}).count()
        if isTeacher > 0:
            role = "teacher"
        else:
            role = "user"
        
        if(role == "teacher"):
            postAdd = mongo.db.posts
            postAdd.insert({'op': user['_id'], 'subject': current_subject['_id'], 'title': title, 'description': description, 'date': datetime.now() })
        
        posts = mongo.db.posts
        postsNr = posts.find({'subject': current_subject['_id']}).count()
        nr = postsNr / nPerPage
        if(int(nr) < nr):
            nrPages = int(nr) + 1
        else:
            nrPages = int(nr)

        allPosts = posts.find({'subject': current_subject['_id']}).sort('date').skip(nPerPage *(pageNumber-1)).limit(nPerPage)
        postList = []
        for post in allPosts:
            postUser = users.find_one({'_id': post['op']})
            nameUser = postUser['firstname'] + " " + postUser['lastname']
            
            postList.append({"username": postUser['username'], "name": nameUser, "icon": postUser['photo'], "title": post['title'], "description": post['description'], "date": post['date'], "idPost": str(post['_id'])})

        return {
        'ok': '0',
        'postList': postList,
        'pages': nrPages
        }
    return {
        'ok': '1',
    }


@institution.route('/refreshPosts', methods=['POST'])
@jwt_required()
def refreshPosts():
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    id = request.json.get('id') 

    subjects = mongo.db.subjects
    obj_subject = ObjectId(id)
    current_subject = subjects.find_one({'_id': obj_subject})

    pageNumber = request.json.get('pageNumber')
    nPerPage = 12

    if current_subject is not None:        
        posts = mongo.db.posts
        postsNr = posts.find({'subject': current_subject['_id']}).count()
        nr = postsNr / nPerPage
        if(int(nr) < nr):
            nrPages = int(nr) + 1
        else:
            nrPages = int(nr)

        allPosts = posts.find({'subject': current_subject['_id']}).sort('date').skip(nPerPage *(pageNumber-1)).limit(nPerPage)
        postList = []
        for post in allPosts:
            postUser = users.find_one({'_id': post['op']})
            nameUser = postUser['firstname'] + " " + postUser['lastname']
            
            postList.append({"username": postUser['username'], "name": nameUser, "icon": postUser['photo'], "title": post['title'], "description": post['description'], "date": post['date'], "idPost": str(post['_id'])})

        return {
        'ok': '0',
        'postList': postList,
        'pages': nrPages
        }
    return {
        'ok': '1',
    }


@institution.route('/saveSingleFile', methods=['POST'])
@jwt_required()
def saveSingleFile():
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    id = request.form.get('id')
    file = request.files['files']

    subjects = mongo.db.subjects
    obj_subject = ObjectId(id)
    current_subject = subjects.find_one({'_id': obj_subject})

    if current_subject is not None:
        isTeacher = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'teachers': user['_id']}]}).count()
        if isTeacher > 0:
            role = "teacher"
        else:
            role = "user"

        if file.filename != "":            
            subjectFiles = mongo.db.subjectFiles
            idFile = mongo.save_file(file.filename, file)
            obj_idFile =  ObjectId(idFile)
            subjectFiles.insert({'user': user['_id'], 'name': file.filename, 'file': obj_idFile, 'date': datetime.now(), 'subject': current_subject['_id'], 'folder': "" })
                  
            return {
                'ok': '0'
                }

    return {
        'ok': '1'
    }
    

@institution.route('/subjectFilePageInfo', methods=['POST'])
@jwt_required()
def subjectFilePageInfo():
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    id = request.json.get('id')

    subjects = mongo.db.subjects
    obj_subject = ObjectId(id)
    current_subject = subjects.find_one({'_id': obj_subject})

    if current_subject is not None:
        isTeacher = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'teachers': user['_id']}]}).count()
        if isTeacher > 0:
            role = "teacher"
        else:
            role = "user"

        subjectFiles = mongo.db.subjectFiles


        allFiles = subjectFiles.find({"$and": [ {'subject': current_subject['_id']}, {'folder': ""}]}).sort('name')
        filesList = []
        for file in allFiles:  
            fileUser = users.find_one({'_id': file['user']})
            userName = fileUser['firstname'] + " " + fileUser['lastname']
            filesList.append({"name": file['name'], "file": str(file['file']), "icon": fileUser['photo'], "nameOfUser": userName, "username": fileUser['username'], "date": file['date'], "idFile": str(file['_id'])})

        subjectFolders = mongo.db.folders
        allFolders = subjectFolders.find({'subject': current_subject['_id']}).sort('name')
        foldersList = []
        for folder in allFolders:
            folderUser = users.find_one({'_id': folder['user']})
            userNameFolder = folderUser['firstname'] + " " + folderUser['lastname']
            foldersList.append({"name": folder['name'], "icon": folderUser['photo'], "nameOfUser": userNameFolder, "username": folderUser['username'], "date": folder['date'], "idFolder": str(folder['_id'])})

        isIn = isInSubject(id, str(user['_id']))
        return {
        'ok': '0',
        'subject': current_subject['name'],
        'role': role,
        'filesList': filesList,
        'foldersList': foldersList,
        'isIn': isIn
        }

    return {
        'ok': '1'
    }


@institution.route('/createSubjectFolder', methods=['POST'])
@jwt_required()
def createSubjectFolder():
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    id = request.json.get('id')
    folderName = request.json.get('name')

    subjects = mongo.db.subjects
    obj_subject = ObjectId(id)
    current_subject = subjects.find_one({'_id': obj_subject})

    if current_subject is not None:
        isTeacher = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'teachers': user['_id']}]}).count()
        if isTeacher > 0:
            role = "teacher"
        else:
            role = "user"

        subjectFolders = mongo.db.folders
        subjectFolders.insert({'user': user['_id'], 'name': folderName, 'date': datetime.now(), 'subject': current_subject['_id']})
        
        return {
        'ok': '0'
        }

    return {
        'ok': '1'
    }


@institution.route('/folderPageInfo', methods=['POST'])
@jwt_required()
def folderPageInfo():
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    id = request.json.get('id')

    folders = mongo.db.folders
    obj_folder = ObjectId(id)
    current_folder = folders.find_one({'_id': obj_folder})

    if current_folder is not None:
        subjects = mongo.db.subjects
        current_subject = subjects.find_one({'_id': current_folder['subject']})

        isTeacher = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'teachers': user['_id']}]}).count()
        if isTeacher > 0:
            role = "teacher"
        else:
            role = "user"

        subjectFiles = mongo.db.subjectFiles

        allFiles = subjectFiles.find({"$and": [ {'subject': current_subject['_id']}, {'folder': current_folder['_id']}]}).sort('name')
        filesList = []
        for file in allFiles:  
            fileUser = users.find_one({'_id': file['user']})
            userName = fileUser['firstname'] + " " + fileUser['lastname']
            filesList.append({"name": file['name'], "file": str(file['file']), "icon": fileUser['photo'], "nameOfUser": userName, "username": fileUser['username'], "date": file['date'], "idFile": str(file['_id'])})

        isIn = isInSubject(str(current_subject['_id']), str(user['_id']))
        return {
        'ok': '0',
        'name': current_folder['name'],
        'subjectId': str(current_subject['_id']),
        'subjectName': current_subject['name'],
        'role': role,
        'filesList': filesList,
        'isIn': isIn
        }

    return {
        'ok': '1'
    }


@institution.route('/saveFolderFile', methods=['POST'])
@jwt_required()
def saveFolderFile():
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    id = request.form.get('id')
    file = request.files['files']

    folders = mongo.db.folders
    obj_folder = ObjectId(id)
    current_folder = folders.find_one({'_id': obj_folder})

    if current_folder is not None:
        subjects = mongo.db.subjects
        current_subject = subjects.find_one({'_id': current_folder['subject']})
        isTeacher = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'teachers': user['_id']}]}).count()
        if isTeacher > 0:
            role = "teacher"
        else:
            role = "user"

        if file.filename != "":
            subjectFiles = mongo.db.subjectFiles
            idFile = mongo.save_file(file.filename, file)
            obj_idFile =  ObjectId(idFile)
            subjectFiles.insert({'user': user['_id'], 'name': file.filename, 'file': obj_idFile, 'date': datetime.now(), 'subject': current_subject['_id'], 'folder': current_folder['_id'] })
                  
            return {
                'ok': '0'
                }

    return {
        'ok': '1'
    }

@institution.route('/downloadFileFilename/<idFile>', methods=['GET'])
def downloadFileFilename(idFile):
    return mongo.send_file(idFile)

@institution.route('/downloadFile/<idFile>', methods=['GET'])
def downloadFile(idFile):
    grid_fs = GridFS(mongo.db)
    mongoFiles = mongo.db.fs.files 
    obj_file = ObjectId(idFile)
    current_file = grid_fs.find_one({'_id': obj_file})
    file = mongoFiles.find_one({'_id': obj_file})
    filename = file['filename']
    response = make_response(current_file.read())
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename)
    return response


def isInInstitution(idInstitution, idUser):
    institutions = mongo.db.institutions
    obj_institution = ObjectId(idInstitution)
    users = mongo.db.users
    obj_user = ObjectId(idUser) 
    current_institution = institutions.find_one({'_id': obj_institution})
    current_user = users.find_one({'_id': obj_user})
    if current_user['_id'] == current_institution['owner']:
        return True
    alreadyUser = institutions.find({"$and": [ {'_id': current_institution['_id']}, {'users': current_user['_id']}]}).count()
    if alreadyUser > 0:
        return True
    return False


def isInSubject(idSubject, idUser):
    subjects = mongo.db.subjects
    obj_subject = ObjectId(idSubject)
    users = mongo.db.users
    obj_user = ObjectId(idUser) 
    current_subject = subjects.find_one({'_id': obj_subject})
    current_user = users.find_one({'_id': obj_user})
    isTeacher = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'teachers': current_user['_id']}]}).count()
    if isTeacher > 0:
        return True
    isUser = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'users': current_user['_id']}]}).count()
    if isUser > 0:
        return True

@institution.route('/canCreateSubject', methods=['POST'])
@jwt_required()
def canCreateSubject():
    # only owner can
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    idInstitution =  request.json.get('id')
    institutions = mongo.db.institutions
    obj_institution = ObjectId(idInstitution)
    current_institution = institutions.find_one({'_id': obj_institution})

    if user['_id'] == current_institution['owner']:
        return {
            'ok': True
        }
    return {
            'ok': False
        }


@institution.route('/userInSubject', methods=['POST'])
@jwt_required()
def userInSubject():
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    subject = request.json.get('subject')
    id =  request.json.get('id')

    if(subject):
        idSubject = id
    else:
        folders = mongo.db.folders
        obj_folder = ObjectId(id)
        current_folder = folders.find_one({'_id': obj_folder})
        idSubject = str(current_folder['subject'])

    ok = isInSubject(idSubject, str(user['_id']))
    
    return {
            'ok': ok
        }


def deletePostAndMessages(idPost):
    posts = mongo.db.posts
    obj_post = ObjectId(idPost)
    current_post = posts.find_one({'_id': obj_post})

    messages = mongo.db.messages
    messages.delete_many({'post': current_post['_id']})
    posts.delete_one({'_id': current_post['_id']})


@institution.route('/deletePost', methods=['DELETE'])
@jwt_required()
def deletePost():
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    id = request.json.get('id') 
    
    posts = mongo.db.posts
    obj_post = ObjectId(id)
    current_post = posts.find_one({'_id': obj_post})

    subjects = mongo.db.subjects
    current_subject = subjects.find_one({'_id': current_post['subject']})

    if current_subject is not None:
        isTeacher = subjects.find({"$and": [ {'_id': current_subject['_id']}, {'teachers': user['_id']}]}).count()
        if isTeacher > 0:
            role = "teacher"
        else:
            role = "user"
        
        if(role == "teacher"):
            deletePostAndMessages(id)
            return {
                'ok': '0',
            }
    return {
        'ok': '1',
    }


@institution.route('/deleteFile', methods=['DELETE'])
@jwt_required()
def deleteFile():
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    id = request.json.get('id') 
    
    subjectFiles = mongo.db.subjectFiles
    obj_subjectFile = ObjectId(id)
    current_subjectFile = subjectFiles.find_one({'_id': obj_subjectFile})

    subjects = mongo.db.subjects
    current_subject = subjects.find_one({'_id': current_subjectFile['subject']})

    if current_subjectFile is not None:
        fileId = current_subjectFile['file']
        grid_fs = GridFS(mongo.db)
        subjectFiles.delete_one({'_id': current_subjectFile['_id']})
        grid_fs.delete(fileId)

        allFiles = subjectFiles.find({"$and": [ {'subject': current_subject['_id']}, {'folder': ""}]}).sort('name')
        filesList = []
        for file in allFiles:  
            fileUser = users.find_one({'_id': file['user']})
            userName = fileUser['firstname'] + " " + fileUser['lastname']
            filesList.append({"name": file['name'], "file": str(file['file']), "icon": fileUser['photo'], "nameOfUser": userName, "username": fileUser['username'], "date": file['date'], "idFile": str(file['_id'])})

        return {
        'ok': '0',
        'filesList': filesList
        }

    return {
        'ok': '1',
    }


@institution.route('/deleteFolderFile', methods=['DELETE'])
@jwt_required()
def deleteFolderFile():
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    id = request.json.get('id') 
    
    subjectFiles = mongo.db.subjectFiles
    obj_subjectFile = ObjectId(id)
    current_subjectFile = subjectFiles.find_one({'_id': obj_subjectFile})
    folderId = current_subjectFile['folder']

    subjects = mongo.db.subjects
    current_subject = subjects.find_one({'_id': current_subjectFile['subject']})

    if current_subjectFile is not None:
        fileId = current_subjectFile['file']
        grid_fs = GridFS(mongo.db)
        subjectFiles.delete_one({'_id': current_subjectFile['_id']})
        grid_fs.delete(fileId)

        allFiles = subjectFiles.find({"$and": [ {'subject': current_subject['_id']}, {'folder': folderId}]}).sort('name')
        filesList = []
        for file in allFiles:  
            fileUser = users.find_one({'_id': file['user']})
            userName = fileUser['firstname'] + " " + fileUser['lastname']
            filesList.append({"name": file['name'], "file": str(file['file']), "icon": fileUser['photo'], "nameOfUser": userName, "username": fileUser['username'], "date": file['date'], "idFile": str(file['_id'])})

        return {
        'ok': '0',
        'filesList': filesList
        }
        
    return {
        'ok': '1',
    }


def deleteFolderWithFiles(id):
    folders = mongo.db.folders
    obj_folder = ObjectId(id)
    current_folder = folders.find_one({'_id': obj_folder})
    subjects = mongo.db.subjects
    current_subject = subjects.find_one({'_id': current_folder['subject']})
    subjectFiles = mongo.db.subjectFiles

    allFiles = subjectFiles.find({"$and": [ {'subject': current_subject['_id']}, {'folder': current_folder['_id']}]}).sort('name')
    filesList = []
    for file in allFiles: 
        filesList.append(file['file'])

    subjectFiles.delete_many({'folder': current_folder['_id']})
    grid_fs = GridFS(mongo.db)
    for file in filesList:
        grid_fs.delete(file)
    folders.delete_one({'_id': current_folder['_id']})


@institution.route('/deleteFolder', methods=['DELETE'])
@jwt_required()
def deleteFolder():
    current_user = get_jwt_identity()
    users = mongo.db.users
    user = users.find_one({'username': current_user})

    id = request.json.get('id') 
    
    folders = mongo.db.folders
    obj_folder = ObjectId(id)
    current_folder = folders.find_one({'_id': obj_folder})

    subjects = mongo.db.subjects
    current_subject = subjects.find_one({'_id': current_folder['subject']})

    if current_folder is not None:
        deleteFolderWithFiles(id)

        allFolders = folders.find({'subject': current_subject['_id']}).sort('name')
        foldersList = []
        for folder in allFolders:
            folderUser = users.find_one({'_id': folder['user']})
            userNameFolder = folderUser['firstname'] + " " + folderUser['lastname']
            foldersList.append({"name": folder['name'], "icon": folderUser['photo'], "nameOfUser": userNameFolder, "username": folderUser['username'], "date": folder['date'], "idFolder": str(folder['_id'])})

        return {
        'ok': '0',
        'foldersList': foldersList
        }
        
    return {
        'ok': '1',
    }
