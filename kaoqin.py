
from time import sleep

import cv2
import face_recognition
from numpy import array


from mssql import MsSql


def inputinfo(uid,name,face_encoding):

    rsp=MsSql()
    date ={
        'uid': uid,
        'name':name,
        'face_encoding':face_encoding
    }
    keys=','.join(date.keys())
    values=','.join(['%s']*len(date))
    table='code_user'

    rsp.exec_insert("insert into {table}({keys}) values ({values})".format(table=table,keys=keys,values=values),tuple(date.values()))  #增
    # sql="insert into {table}({keys}) values ({values}) ".format(table=table,keys=keys,values=values)

def saveinfo():

    cap = cv2.VideoCapture(0)
    uid=input("请输入工号：")
    name=input("请输入姓名：")

    while(1):
        # get a frame
        ret, frame = cap.read()
        # show a frame
        cv2.imshow("capture", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite("./image/{}.jpg".format(uid), frame)

            image = face_recognition.load_image_file("./image/{}.jpg".format(uid))
            face_encoding = face_recognition.face_encodings(image)[0]
            print(face_encoding,type(face_encoding))
            #face_encoding_str=' ',join(face_encoding)
            #print(face_encoding_str)
            sleep(1)

            inputinfo(uid,name,str(face_encoding))

            break
    cap.release()
    cv2.destroyAllWindows()

def compare_faces(face_encodings):
    rsp=MsSql()
    face_names=[]
    known_names=[]
    known_faces_encoding=[]
    known_faces=rsp.execquery("select face_encoding from code_user")

    for i in range(len(known_faces)):
        known_faces_encoding.append(array(known_faces[i][0]))

        #print(known_faces_encoding[i])

    known_face_names=rsp.execquery("select name from code_user")
    for i in range(len(known_face_names)):
        known_names.append(known_face_names[i][0])

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_faces_encoding, face_encoding)
        name='Unknown'
        if True in matches:
           first_match_index = matches.index(True)
           name = known_face_names[first_match_index]

        face_names.append(name)
    return face_names



if __name__ == '__main__':
    video_capture = cv2.VideoCapture(0)
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    while True:
    # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            # sleep(1)
            if len(face_encodings)>0:
                face_names=compare_faces(face_encodings)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

    # saveinfo()