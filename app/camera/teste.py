import cv2

image_faces = []

video = cv2.VideoCapture('http://192.168.15.229:4747/mjpegfeed')
while True:
    imagem, frame = video.read()  # imagem == True e Frame == True ???

    frame_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('video', frame)

    if cv2.waitKey(1) == ord('f'):
        break

        # limpar_registros_video(video


