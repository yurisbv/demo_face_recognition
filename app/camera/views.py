from flask import jsonify, request
from FaceRecognizer.Services.CameraService import CameraService
from app.camera import app_camera
from app.camera.resource import Camera_Resource
import cv2
import base64


cam=None
url_cam=None
cameraResource=Camera_Resource()

@app_camera.route('/set_cam')
def set_cam():
    global cam
    if(cam!=None):
        return jsonify({'message':'success', 'cameraType': cam['type'], 'cameraIp': cam['ip'], 'cameraPort': cam['port'], 'cameraUrl' : cam['url']})
    else:
        return jsonify({'message':'success', 'cameraType': 'local'})

@app_camera.route('/save_cam', methods=['POST'])
def save_cam():
    global cam
    cam=request.json
    # global url_cam

    cam = cameraResource.set_url_cam(cam)

    cam['status'] = cameraResource.test_cam(CameraService(cam['url']))

    if(cam['status']==False):
        cam=None
        return jsonify({'message': 'success'})

    return jsonify({'message':'success', 'status':str(cam['status']), 'cameraUrl' : cam['url']})