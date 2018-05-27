from flask import Response, jsonify, request
from FaceRecognizer.Services.FaceRecognizer import FaceRecognizer
from FaceRecognizer.Services.CameraService import CameraService
from app.recognition import app_recognition
from app.recognition.resource import Recognition_Resource

faceRecongnizer = FaceRecognizer()
recognitionResource=Recognition_Resource()
url_cam=None


@app_recognition.route('/add_cam', methods=['POST'])
def add_cam():
    global url_cam
    url_cam=recognitionResource.get_url_cam(request.json)
    return jsonify({'message':'Success'})

@app_recognition.route('/video_feed')
def video_feed():
    return Response(recognitionResource.capture(CameraService(url_cam)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app_recognition.route('/video_recog')
def video_recog():
    return Response(recognitionResource.recognition(CameraService(url_cam)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app_recognition.route('/trainining_yml', methods=['POST'])
def trainining_yml():
    faceRecongnizer.train_classifier_lbph()
    return jsonify({'message': 'Success'})

