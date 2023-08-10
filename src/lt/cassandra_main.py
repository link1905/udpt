from colorama import Fore
from flask import Flask, render_template, request, redirect, url_for, jsonify
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement, dict_factory, tuple_factory, BatchStatement
import uuid

app = Flask(__name__)

# Cassandra connection
cluster = Cluster(['localhost'])
session = cluster.connect('students_keyspace')


@app.route("/", methods=["GET"])
def show_students():
    # Query all students
    return render_template('index_cassandra.html')


@app.route('/fetch_students', methods=['POST'])
def fetch_students():
    search_term = request.json.get('searchTerm', {
        'filter': 'all'
    })
    per_page = 10
    page = int(request.json.get('page', 1))
    skip = (page - 1) * per_page
    wheres = []
    print("search term", search_term)
    if search_term['filter'] == 'all':
        table = 'students'
    else:
        f = search_term["filter"]
        table = f'students_by_{f}'
        value = search_term['value']
        wheres.append(f"{f} = '{value}'")
    where = ""
    if len(wheres) == 1:
        where = f"WHERE {wheres[0]}"
    elif len(wheres) > 1:
        where = f"WHERE {' AND '.join(wheres)}"
    query = f'SELECT * FROM {table} {where} LIMIT {per_page}'
    print(Fore.GREEN + query)
    session.row_factory = tuple_factory
    result = session.execute(f'SELECT COUNT(id) AS COUNT FROM {table} {where}')
    total_students = result.one()[0]
    # print("count", total_students)
    session.row_factory = dict_factory
    students = []
    if total_students > skip:
        students = list(session.execute(query))[skip:]
    # print("students", students)
    for student in students:
        birthdate = student['birthday'].date()
        formatted_birthdate = birthdate.strftime("%Y-%m-%d")
        student['birthday'] = formatted_birthdate
        student['GPA'] = student['gpa']
    total_pages = (total_students // per_page) + 1 if total_students % per_page > 0 else total_students // per_page
    return jsonify({'students': students, 'total_pages': total_pages})


@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        birthday = request.form['birthday']
        activity_class = request.form['activity_class']
        department_name = request.form['department']
        major_name = request.form['major']
        GPA = float(request.form.get('GPA', 0))

        # Generate a unique ID for the new student
        student_id = uuid.uuid4()
        # Insert student record into Cassandra
        add_student_to_tables(student_id, name, birthday, activity_class, department_name, major_name, GPA)
        return redirect(url_for('show_students'))

    # Query classes and departments for dropdowns
    return render_template('add_student.html', classes=fetch_class(), departments=fetch_department())


def add_student_to_tables(student_id, name, birthday, activity_class, department_name, major_name, GPA):
    add_student_to_table("students", student_id, name, birthday, activity_class, department_name, major_name, GPA)
    add_student_to_table("students_by_activity_class", student_id, name, birthday, activity_class, department_name,
                         major_name, GPA)
    add_student_to_table("students_by_department_name", student_id, name, birthday, activity_class, department_name,
                         major_name, GPA)


def add_student_to_table(table, student_id, name, birthday, activity_class, department_name, major_name, GPA):
    statement = session.prepare(f"INSERT INTO {table} "
                                "(id, name, birthday, activity_class, department_name, major_name, GPA) "
                                "VALUES (?, ?, ?, ?, ?, ?, ?)")
    print(Fore.CYAN + statement.query_string)
    session.execute(statement, (student_id, name, birthday, activity_class, department_name, major_name, GPA))


def get_student(student_id):
    statement = SimpleStatement("SELECT * FROM students WHERE id = %s")
    print(Fore.GREEN + statement.query_string)
    session.row_factory = dict_factory
    result = session.execute(statement, [student_id])
    student = result.one()
    print(Fore.GREEN, student)
    return student


@app.route('/update/<uuid:student_id>', methods=['GET', 'POST'])
def update_student(student_id):
    if request.method == 'POST':
        name = request.form['name']
        birthday = request.form['birthday']
        activity_class = request.form['activity_class']
        department_name = request.form['department_name']
        major_name = request.form['major_name']
        student = get_student(student_id)
        statements = []
        # Update student record in Cassandra
        statements.append(
            session.prepare("UPDATE students "
                            "SET name = ?, birthday = ?, activity_class = ?, department_name = ?, major_name = ?, GPA = ? "
                            "WHERE id = ?"))
        dep = student['department_name']
        if department_name != dep:
            session.execute(f"DELETE FROM students_by_department_name WHERE department_name = '{dep}' AND id = {student_id}")
            statements.append(
                session.prepare("INSERT INTO students_by_department_name(name, birthday, activity_class, department_name, major_name, GPA, id) "
                                "VALUES (?, ?, ?, ?, ?, ?, ?)"))
        cl = student['activity_class']
        if activity_class != cl:
            session.execute(f"DELETE FROM students_by_activity_class WHERE activity_class = '{cl}' AND id = {student_id}")
            statements.append(
                session.prepare("INSERT INTO students_by_activity_class (name, birthday, activity_class, department_name, major_name, GPA, id) "
                                "VALUES (?, ?, ?, ?, ?, ?, ?)"))
        GPA = student['gpa']
        for statement in statements:
            print(Fore.YELLOW + statement.query_string)
            session.execute(statement, (name, birthday, activity_class, department_name, major_name, GPA, student_id))
        return redirect(url_for('show_students'))

    # Query student by ID
    student = get_student(student_id)
    classes_dict = fetch_class()
    departments_dict = fetch_department()
    classes = [{'name': r['name']} for r in classes_dict]
    departments = [{'name': r['name']} for r in departments_dict]
    return render_template('update_student.html', student=student, classes=classes, departments=departments)


# Route to fetch majors based on selected department using Ajax
@app.route('/majors/<dep>', methods=['GET'])
def get_majors(dep):
    statement = SimpleStatement("SELECT majors FROM departments WHERE name = %s")
    session.row_factory = tuple_factory
    result = session.execute(statement, [dep])
    majors = result.one()
    if majors:
        majors = list(majors[0])
    else:
        majors = []
    return jsonify({'majors': majors})


def fetch_class():
    statement = SimpleStatement("SELECT * FROM classes")
    session.row_factory = dict_factory
    return session.execute(statement)


@app.route('/activity_class', methods=['GET'])
def fetch_class_name():
    result = fetch_class()
    classes = [r['name'] for r in result]
    return jsonify(classes)


def fetch_department():
    statement = SimpleStatement("SELECT * FROM departments")
    session.row_factory = dict_factory
    return session.execute(statement)


@app.route('/department_name', methods=['GET'])
def fetch_department_name():
    result = fetch_department()
    departments = [r['name'] for r in result]
    return jsonify(departments)


@app.route('/delete', methods=['DELETE'])
def delete_students():
    student_ids = request.json.get('studentIds')
    student_ids = [uuid.UUID(s) for s in student_ids]
    print(Fore.RED, student_ids)
    delete_students_internal(student_ids)
    return jsonify({'message': 'Students deleted successfully'})


def delete_student(student_id):
    student = get_student(student_id)
    statements = []
    dep = student['department_name']
    act_class = student['activity_class']
    statements.append(
        session.prepare(f"DELETE FROM students WHERE id = {student_id}"))
    statements.append(
        session.prepare(
            f"DELETE FROM students_by_department_name WHERE department_name = '{dep}' AND id = {student_id}"))
    statements.append(
        session.prepare(
            f"DELETE FROM students_by_activity_class WHERE activity_class = '{act_class}' AND id = {student_id}"))
    for s in statements:
        print(Fore.RED + s.query_string)
        session.execute(s)


def delete_students_internal(student_ids):
    print(f"delete students: {student_ids}")
    for student_id in student_ids:
        delete_student(student_id)


if __name__ == '__main__':
    session.execute('TRUNCATE TABLE students')
    session.execute('TRUNCATE TABLE students_by_department_name')
    session.execute('TRUNCATE TABLE students_by_activity_class')
    add_student_to_tables(student_id=uuid.uuid4(),
                          name="Linh",
                          birthday="2001-01-02",
                          activity_class="Class A",
                          department_name="Department of Electrical Engineering",
                          major_name="Electrical Engineering",
                          GPA=3)

    add_student_to_tables(student_id=uuid.uuid4(),
                          name="John",
                          birthday="1999-05-15",
                          activity_class="Class B",
                          department_name="Department of Computer Science",
                          major_name="Computer Science",
                          GPA=3.5)

    add_student_to_tables(student_id=uuid.uuid4(),
                          name="Emma",
                          birthday="2000-09-30",
                          activity_class="Class A",
                          department_name="Department of Computer Science",
                          major_name="Software Engineering",
                          GPA=3.2)

    add_student_to_tables(student_id=uuid.uuid4(),
                          name="Alex",
                          birthday="1998-07-20",
                          activity_class="Class B",
                          department_name="Department of Electrical Engineering",
                          major_name="Electronic Engineering",
                          GPA=3.8)

    add_student_to_tables(student_id=uuid.uuid4(),
                          name="Sophia",
                          birthday="2002-03-10",
                          activity_class="Class A",
                          department_name="Department of Computer Science",
                          major_name="Software Engineering",
                          GPA=3.9)

    add_student_to_tables(student_id=uuid.uuid4(),
                          name="Daniel",
                          birthday="2001-11-25",
                          activity_class="Class B",
                          department_name="Department of Computer Science",
                          major_name="Computer Science",
                          GPA=3.6)

    add_student_to_tables(student_id=uuid.uuid4(),
                          name="Olivia",
                          birthday="2000-08-05",
                          activity_class="Class A",
                          department_name="Department of Electrical Engineering",
                          major_name="Electrical Engineering",
                          GPA=3.4)

    add_student_to_tables(student_id=uuid.uuid4(),
                          name="William",
                          birthday="1999-06-18",
                          activity_class="Class B",
                          department_name="Department of Electrical Engineering",
                          major_name="Electronic Engineering",
                          GPA=3.1)

    add_student_to_tables(student_id=uuid.uuid4(),
                          name="Ava",
                          birthday="2002-04-14",
                          activity_class="Class A",
                          department_name="Department of Computer Science",
                          major_name="Computer Science",
                          GPA=3.7)

    add_student_to_tables(student_id=uuid.uuid4(),
                          name="James",
                          birthday="2001-10-08",
                          activity_class="Class B",
                          department_name="Department of Computer Science",
                          major_name="Software Engineering",
                          GPA=3.2)

    add_student_to_tables(student_id=uuid.uuid4(),
                          name="Mia",
                          birthday="1998-12-28",
                          activity_class="Class A",
                          department_name="Department of Electrical Engineering",
                          major_name="Electronic Engineering",
                          GPA=3.5)
    app.run(debug=True, port=8081)
