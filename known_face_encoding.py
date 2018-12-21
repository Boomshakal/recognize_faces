import face_recognition

biden_image = face_recognition.load_image_file("biden.jpg")
obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
print(obama_face_encoding)
