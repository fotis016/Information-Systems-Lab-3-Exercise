from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response
import json

# Connect to our local MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Choose InfoSys database
db = client['InfoSys']
students = db['Students']

# Initiate Flask App
app = Flask(__name__)

# Insert Student
# Create Operation
@app.route('/insertstudent', methods=['POST'])
def insert_student():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "name" in data or not "yearOfBirth" in data or not "email" in data or not "address" in data:
        return Response("Information incompleted",status=500,mimetype="application/json")
    
    if students.find({"email":data["email"]}).count() == 0 :
        student = {"email": data['email'], "name": data['name'],  "yearOfBirth":data['yearOfBirth'],  "address":data['address']}
        # Add student to the 'students' collection
        students.insert_one(student)
        return Response("was added to the MongoDB",status=200,mimetype='application/json') 
    else:
        return Response("A user with the given email already exists",status=200,mimetype='application/json')

# Read Operations
# Get all students
@app.route('/getallstudents', methods=['GET'])
def get_all_students():
    iterable = students.find({})
    output = []
    for student in iterable:
        student['_id'] = None 
        output.append(student)
    return jsonify(output)

# Get the number of all the students in the DB 
@app.route('/getstudentcount', methods=['GET'])
def get_students_count():
    number_of_students = students.find({}).count()
    return jsonify({"Number of students": number_of_students})

# Find student by email
@app.route('/getstudent/<string:email>', methods=['GET'])
def get_student_by_email(email):
    if email == None:
        return Response("Bad request", status=500, mimetype='application/json')
    student = students.find_one({"email":email})
    if student !=None:
        student = {'_id':str(student["_id"]),'name':student["name"],'email':student["email"], 'yearOfBirth':student["yearOfBirth"]}
        return jsonify(student)
    return Response('no student found',status=500,mimetype='application/json')
    
    
    # Get all students' addresses
@app.route('/getAllStudentsAddress', methods=['GET'])
def get_student_address():
    iterable = students.find({})
    output = []
    for student in iterable:
    	if 'address' in student:
        	student = {'name':student["name"], 'address':student["address"]}
        	output.append(student)
    return jsonify(output)


# Get a student's address via email
@app.route('/getStudentsAddress/<string:email>', methods=['GET'])    
def get_student_address_byEmail(email):
     if email == None:
        return Response("Bad request", status=500, mimetype='application/json') 
     student = students.find_one({"email":email})
     if student == None:
     	return Response('no student found',status=500,mimetype='application/json')
     if 'address' in student:
     	student = {'name':student["name"], 'email':student["email"], 'address':student["address"]}
     	return jsonify(student)
     else:
     	return	Response("Student has no address registered!", status=500, mimetype='application/json') 
     	
     	    # Get all students' addresses born in the 80's
@app.route('/getEightiesAddress', methods=['GET'])
def get_student_address_80s():
    iterable = students.find({"yearOfBirth":{"$gte": 1980, "$lt":1990}})
    output = []
    for student in iterable:
    	if 'address' in student:
        	student = {'name':student["name"], 'address':student["address"], 'yearOfBirth':student["yearOfBirth"]}
        	output.append(student)
    return jsonify(output)


@app.route('/countAddress', methods=['GET'])
def get_number_of_addresses():
	number_of_students = students.count({"address":{"$exists":True}})
	return jsonify({"Number of students": number_of_students})


# Find number of students born in a certain year
@app.route('/getstudent/<int:year>', methods=['GET'])
def find_number_by_year(year):
    if year == None:
        return Response("Bad request", status=500, mimetype='application/json')
    number_of_students = students.count({"yearOfBirth":{"$eq": year}})
    return jsonify({"Number of students": number_of_students, "who were born in": year})
    
    

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
