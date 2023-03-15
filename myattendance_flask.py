import os
import csv
import numpy as np
from datetime import date
from datetime import datetime
import cv2
import numpy as np
from PIL import Image
from flask_mysqldb import MySQL
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for,flash


#### Defining Flask App
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'student_attendance'

mysql = MySQL(app)

def path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


def datetoday():
    return date.today().strftime("%m_%d_%y")

def datetoday2():
    return date.today().strftime("%d-%B-%Y")

def totalreg():
    return len(os.listdir('Dataset/faces'))

def path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

vid_cam = cv2.VideoCapture(0)
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Student_id = input("Enter face ID: ")
count = 0

path_exists("training_data/")


def get_attendance(date=None):
    cursor = mysql.connection.cursor()
    if date:
        query = "SELECT userid, user_name, date, time FROM take_attendance WHERE date = %s"
        cursor.execute(query, (date,))
    else:
        query = "SELECT userid, user_name, date, time FROM take_attendance"
        cursor.execute(query)
    attendance_details = cursor.fetchall()
    print("attendance_details in function are ",attendance_details)
    cursor.close()
    return attendance_details
def training():
    import cv2
    import os
    import numpy as np
    from PIL import Image

    def path_exists(path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)

    print("Training started")

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    def getImagesAndLabels(path):
        faceSamples = []
        ids = []
        # print("faceSamples:", faceSamples, "ids:", ids)

        for foldername in os.listdir(path):
            folderpath = os.path.join(path, foldername)
            if not os.path.isdir(folderpath):
                continue

            id = int(foldername.split('_')[1])
            print("id is", id)

            for filename in os.listdir(folderpath):
                if not filename.endswith('.jpg'):
                    continue

                imagePath = os.path.join(folderpath, filename)
                # print("imagePath:",imagePath)
                PIL_img = Image.open(imagePath).convert('L')
                img_numpy = np.array(PIL_img, 'uint8')

                faces = detector.detectMultiScale(img_numpy)
                # print("faces:", faces)
                if len(faces) == 0:
                    continue
                for (x, y, w, h) in faces:
                    faceSamples.append(img_numpy[y:y + h, x:x + w])
                    ids.append(id)

        # print("ids before return",ids)

        return faceSamples, ids

    faces, ids = getImagesAndLabels('Dataset/faces/')
    print("ids:", ids)

    recognizer.train(faces, np.array(ids))

    path_exists('saved_model/')
    recognizer.write('saved_model/s_model.yml')

    print('Training Finish')

# @app.route('/home')
# def home():
#     return render_template('home.html')


@app.route('/', methods=['GET', 'POST'])
def Login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print("username in login", username)
        print("password in login", password)

        conn = mysql.connection
        cursor = conn.cursor()

        query = f"SELECT * FROM user_signup WHERE username='{username}'"
        cursor.execute(query)
        result = cursor.fetchone()
        print('result is ', result)

        if result is None:
            error = 'Invalid username or password'
        elif result[6] != password:
            error = 'Invalid username or password'
        else:
            return redirect(f'/User?name={username}')

        cursor.close()
    return render_template('Login.html', error=error)
@app.route('/User', methods=['GET', 'POST'])
def User():
    name = request.args.get('name')
    password=request.args.get('password')
    print("password",password)

    return render_template('User.html',name=name)


@app.route('/adminlogin', methods=['GET', 'POST'])
def Adminlogin():
    error = None
    if request.method == 'POST':
        print('Login action')
        username = request.form['admin_name']
        password = request.form['password']
        # Connect to the database
        conn = mysql.connection
        cursor = conn.cursor()

        # Execute the SELECT query to fetch admin data
        query = f"SELECT * FROM admin WHERE admin_uname='{username}'"
        cursor.execute(query)
        result = cursor.fetchone()
        print(result)
        cursor.close()
        # Check if the admin exists in the database and the password is correct
        if result and result[2] == password:
            return redirect('/admin')
        else:
            error = 'Incorrect Username or Password'
            return render_template("Adlogin.html", error=error)

    return render_template("Adlogin.html", error=error)

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        # Get the date from the form
        date_str = request.form['date']
        print("date is ",date_str)
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Filter attendance details based on the date
        attendance_details = get_attendance(date=date)
    else:
        # If no date is provided, show all attendance details
        attendance_details = get_attendance()

    # Render the template with the attendance details
    return render_template('Attendance.html', attendance_details=attendance_details)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['Username']
        name = request.form['Name']
        userid = request.form['Userid']
        phonenumber = request.form['phonenumber']
        std = request.form['std']
        password = request.form['password']

        print("username",username)
        print("name",name)
        print("userid",userid)
        print("phonenumber",phonenumber)
        print("std",std)
        print("password",password)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user_signup (username,name,userid,phone_no,std,password) VALUES (%s,%s,%s,%s,%s,%s)", (username,name,userid,phonenumber,std,password))
        mysql.connection.commit()
        cur.close()
        return redirect('/')

        # Do something with the form data

    return render_template('Signup.html')

@app.route('/admin', methods=['GET', 'POST'])
def Admin():
    return render_template('home.html')
@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('Attendance_search.html')


#### This function will run when we add a new user
@app.route('/add', methods=['GET', 'POST'])
def add_students():
    root_folder = "Dataset/faces/"

    while True:
        student_id = request.form['newuserid']
        student_name = request.form['newusername']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user_details (userid, user_name) VALUES (%s, %s)", (student_id, student_name))
        mysql.connection.commit()
        cur.close()

        path = os.path.join(root_folder, f"{student_name}_{student_id}")
        print(path)
        if not os.path.isdir(path):
            os.makedirs(path)
        count = 0
        while True:
            _, frame = vid_cam.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                count += 1
                filename = os.path.join(path, f"{student_name}_{count}.jpg")
                cv2.imwrite(filename, gray[y:y + h, x:x + w])
                cv2.putText(frame, f"Data collected {count} out of 100", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                            2, cv2.LINE_AA)
            cv2.imshow('frame', frame)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif count >= 100:
                break

        vid_cam.release()
        cv2.destroyAllWindows()
        print("Training Started")
        training()
        print("Training Finished")

    return render_template('home.html')
@app.route('/start', methods=['GET'])
def start():

    def path_exists(path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)


    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path_exists("saved_model/")
    recognizer.read('saved_model/s_model.yml')
    cascade = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascade)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cam = cv2.VideoCapture(0)

    detected_ids = []

    folder_path = "Dataset/faces/"
    delimiter = "_"
    student_dict = {}
    print(student_dict)

    for folder_name in os.listdir(folder_path):
        # split the folder name by the delimiter and get the student ID and name
        student_name, student_id = folder_name.split(delimiter)
        print(student_id, student_name)
        # add the student ID and name to the dictionary
        student_dict[student_id] = student_name
        # append the dictionary with the student ID and name
        student_dict = {**student_dict, student_id: student_name}

    print(student_dict)

    csv_file = open('attendance.csv', 'a', newline='')
    csv_writer = csv.writer(csv_file)

    if os.stat('attendance.csv').st_size == 0:
        csv_writer.writerow(['ID', 'Name', 'Date and Time'])

    while True:

        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x - 20, y - 20), (x + w + 20, y + h + 20), (0, 255, 0), 4)
            Id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            print("id,confidence is", Id, confidence)
            if str(Id) in student_dict:
                name = student_dict[str(Id)]
                print("name is", name)
                confidence_level = round(100 - confidence, 2)
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor = mysql.connection.cursor()

                sql = "SELECT COUNT(*) FROM take_attendance WHERE userid = %s AND date = %s"
                val = (Id, current_time.split()[0])
                cursor.execute(sql, val)
                result = cursor.fetchone()[0]

                # If user already exists, update their details
                if result > 0:
                    sql = "UPDATE take_attendance SET user_name = %s, time = %s WHERE userid = %s AND date = %s"
                    val = (name, current_time.split()[1], Id, current_time.split()[0])
                    cursor.execute(sql, val)
                    mysql.connection.commit()
                    cursor.close()
                    print("details updated")

                # If user does not exist, insert their details
                else:
                    sql = "INSERT INTO take_attendance (userid, user_name, date, time) VALUES (%s, %s, %s, %s)"
                    val = (Id, name, current_time.split()[0], current_time.split()[1])
                    cursor.execute(sql, val)
                    mysql.connection.commit()
                    cursor.close()
                    print("details added")
            else:
                name = "Unknown"
                confidence_level = round(100 - confidence, 2)

            if Id not in detected_ids:
                detected_ids.append(Id)
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                csv_writer.writerow([Id, name, current_time])

            cv2.rectangle(frame, (x - 22, y - 90), (x + w + 22, y - 22), (0, 255, 0), -1)
            cv2.putText(frame, name + ' ' + str(confidence_level) + '%', (x, y - 40), font, 1, (255, 255, 255), 3)

        cv2.imshow('im', frame)



        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cam.release()
    csv_file.close()
    cv2
    return render_template('home.html', totalreg=totalreg(),
                           datetoday2=datetoday2(),
                           id=Id, name=name, date=current_time.split()[0], time=current_time.split()[1])

if __name__ == '__main__':
    app.run(debug=True)
