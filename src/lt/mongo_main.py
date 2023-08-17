from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from flask_paginate import Pagination, get_page_args

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["school"]
departments_collection = db['departments']
classes_collection = db['classes']
students_collection = db['students']
departments_collection.delete_many({})
classes_collection.delete_many({})
students_collection.delete_many({})
sample_departments = [
    {"name": "Department of Computer Science", "majors": ["Computer Science", "Software Engineering"]},
    {"name": "Department of Electrical Engineering", "majors": ["Electrical Engineering", "Electronic Engineering"]}
]
sample_classes = [
    {"name": "Class A", "department": "Department of Computer Science"},
    {"name": "Class B", "department": "Department of Electrical Engineering"},
]
sample_students = [
    {
        "id": 1,
        "name": "Linh Ho",
        "birthday": "2001-05-15",
        "activity_class": "Class B",
        "department_name": "Department of Computer Science",
        "major_name": "Computer Science",
        "GPA": 3.5
    },
    {
        "id": 2,
        "name": "John",
        "birthday": "1999-05-15",
        "activity_class": "Class B",
        "department_name": "Department of Computer Science",
        "major_name": "Computer Science",
        "GPA": 3.5
    },
    {
        "id": 3,
        "name": "Emma",
        "birthday": "2000-09-30",
        "activity_class": "Class A",
        "department_name": "Department of Computer Science",
        "major_name": "Software Engineering",
        "GPA": 3.2
    },
    {
        "id": 4,
        "name": "Alex",
        "birthday": "1998-07-20",
        "activity_class": "Class B",
        "department_name": "Department of Electrical Engineering",
        "major_name": "Electronic Engineering",
        "GPA": 3.8
    },
    {
        "id": 5,
        "name": "Sophia",
        "birthday": "2002-03-10",
        "activity_class": "Class A",
        "department_name": "Department of Computer Science",
        "major_name": "Software Engineering",
        "GPA": 3.9
    },
    {
        "id": 6,
        "name": "Daniel",
        "birthday": "2001-11-25",
        "activity_class": "Class B",
        "department_name": "Department of Computer Science",
        "major_name": "Computer Science",
        "GPA": 3.6
    },
    {
        "id": 7,
        "name": "Olivia",
        "birthday": "2000-08-05",
        "activity_class": "Class A",
        "department_name": "Department of Electrical Engineering",
        "major_name": "Electrical Engineering",
        "GPA": 3.4
    },
    {
        "id": 8,
        "name": "William",
        "birthday": "1999-06-18",
        "activity_class": "Class B",
        "department_name": "Department of Electrical Engineering",
        "major_name": "Electronic Engineering",
        "GPA": 3.1
    },
    {
        "id": 9,
        "name": "Ava",
        "birthday": "2002-04-14",
        "activity_class": "Class A",
        "department_name": "Department of Computer Science",
        "major_name": "Computer Science",
        "GPA": 3.7
    },
    {
        "id": 10,
        "name": "James",
        "birthday": "2001-10-08",
        "activity_class": "Class B",
        "department_name": "Department of Computer Science",
        "major_name": "Software Engineering",
        "GPA": 3.2
    },
    {
        "id": 11,
        "name": "Mia",
        "birthday": "1998-12-28",
        "activity_class": "Class A",
        "department_name": "Department of Electrical Engineering",
        "major_name": "Electronic Engineering",
        "GPA": 3.5
    },
    {
        "id": 12,
        "name": "John Doe",
        "birthday": "2000-01-01",
        "activity_class": "Class A",
        "department_name": "Computer Science",
        "major_name": "Software Engineering",
        "GPA": 3.7
    },
    {
        "id": 13,
        "name": "Jane Smith",
        "birthday": "1999-05-15",
        "activity_class": "Class A",
        "department_name": "Electrical Engineering",
        "major_name": "Power Systems",
        "GPA": 3.9
    }
]
departments_collection.insert_many(sample_departments)
classes_collection.insert_many(sample_classes)
students_collection.insert_many(sample_students)


@app.route("/", methods=["GET"])
def show_students():
    # Query all students
    return render_template('index.html')


@app.route('/fetch_students', methods=['POST'])
def fetch_students():
    page = int(request.json.get('page', 1))
    search_term = request.json.get('searchTerm', '')
    # Define how many students to display per page
    per_page = 10
    # Query students based on search criteria and pagination
    query = {}
    if search_term:
        query = {"name": {"$regex": search_term, "$options": "i"}}
    students = list(students_collection.find(query).skip((page - 1) * per_page).limit(per_page))
    total_students = students_collection.count_documents(query)
    total_pages = (total_students // per_page) + 1 if total_students % per_page > 0 else total_students // per_page
    for student in students:
        del student['_id']
    print(students)
    return jsonify({'students': students, 'total_pages': total_pages})


@app.route('/update/<int:student_id>', methods=['GET', 'POST'])
def update_student(student_id):
    if request.method == 'POST':
        name = request.form['name']
        birthday = request.form['birthday']
        activity_class = request.form['activity_class']
        department_name = request.form['department_name']
        major_name = request.form['major_name']

        students_collection.update_one(
            {'id': student_id},
            {
                '$set': {
                    'name': name,
                    'birthday': birthday,
                    'activity_class': activity_class,
                    'department_name': department_name,
                    'major_name': major_name,
                }
            }
        )
        return redirect(url_for('show_students'))
    student = students_collection.find_one({"id": student_id})
    departments = departments_collection.find()
    classes = classes_collection.find()
    return render_template('update_student.html', student=student, departments=departments, classes=classes)


@app.route('/delete', methods=['DELETE'])
def delete_students():
    student_ids = request.json.get('studentIds')
    student_ids = [int(i) for i in student_ids]
    print(f"delete students: {student_ids}")
    # Delete the selected students
    students_collection.delete_many({'id': {'$in': student_ids}})
    return jsonify({'message': 'Students deleted successfully'})


@app.route('/majors/<dep>', methods=['GET'])
def get_majors(dep):
    department = departments_collection.find_one({"name": dep})
    if department:
        majors = department.get('majors', [])
    else:
        majors = []
    return jsonify({'majors': majors})


@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        birthday = request.form['birthday']
        activity_class = request.form['activity_class']
        department_name = request.form['department']
        major_name = request.form['major']
        GPA = float(request.form.get('GPA', 0))
        max_students = students_collection.count_documents({})
        new_student = {
            "id": max_students + 1,
            "name": name,
            "birthday": birthday,
            "activity_class": activity_class,
            "department_name": department_name,
            "major_name": major_name,
            "GPA": GPA
        }

        students_collection.insert_one(new_student)
        return redirect(url_for('show_students'))

    departments = departments_collection.find()
    classes = classes_collection.find()
    return render_template('add_student.html', departments=departments, classes=classes)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
