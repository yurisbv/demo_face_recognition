from flask import jsonify, request, json
from app.user import app_user
from app.recognition.resource import Recognition_Resource
from app.user.resource import User_Resource
from FaceRecognizer.Services.UserManager import UserManager
from FaceRecognizer.Services.FileManager import FileManager
import cv2
import base64

userManager = UserManager()
fileManager = FileManager()
image_faces=[]
userResource = User_Resource()

@app_user.route('/add_image', methods=['POST'])
def add_image():
    image_faces.append(Recognition_Resource.last_frame)
    ret, jsonImage=cv2.imencode('.jpg', Recognition_Resource.last_frame)
    jpg_as_text = base64.b64encode(jsonImage.tobytes())
    jpg_as_text=jpg_as_text.decode('ascii')
    return jsonify({'message': 'Success', 'image_face': json.dumps(jpg_as_text)})

@app_user.route('/clear_image_faces')
def clear_image_faces():
    image_faces.clear()
    return jsonify({'message':'Success'})

@app_user.route('/remove_image', methods=['POST'])
def remove_image():
    image_faces.pop(len(image_faces)-1)
    return jsonify({'message': 'Success'})

@app_user.route('/search', methods=['POST'])
def search():
    try:
        image_faces.clear()
        user=userManager.get_user_by_id(request.json)
        return jsonify({'message':'Success', 'user':user.get_json()})
    except:
        return None

@app_user.route('/save_user', methods=['POST'])
def save_user():
    user = request.json
    id=int(fileManager.get_last_id())+1
    userManager.create_user(id, user['name'])
    user = userManager.get_user_by_id(id)
    fileManager.save_image(image_faces, user)
    image_faces.clear()
    user=None
    return jsonify({'message': 'Success', 'id':id})

@app_user.route('/edit_user', methods=['POST'])
def edit_user():
    user = request.json
    id = user['id']
    fileManager.clear_photos(id)
    userManager.edit_user_name(id, user['name'])
    user = userManager.get_user_by_id(id)
    fileManager.save_image(image_faces, user)
    image_faces.clear()
    user = None
    return jsonify({'message': 'Success'})

@app_user.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
    userManager.delete_user(id)
    return jsonify({'message': 'Success'})

@app_user.route('/load_faces', methods=['POST'])
def get_faces():
    image_faces.clear()
    faces=fileManager.get_faces(request.json)
    faces=userResource.faces_to_b64(faces, image_faces)
    return jsonify({'message': 'Success', 'faces':faces})