
from flask import Flask, render_template, url_for, request, session, redirect, flash
from flask_pymongo import PyMongo
import bcrypt


app = Flask(__name__, static_url_path='static')
app.secret_key = 'school'

app.config['MONGO_DBNAME'] = 'Login'
app.config[
    'MONGO_URI'] = 'mongodb+srv://Diana:DianaBalog@clusterschool.xiuru.mongodb.net/SmartSchool?retryWrites=true&w=majority'

mongo = PyMongo(app)


@app.route('/')
def home():
    if is_loggedin():
        if is_teacher():
            return render_template('teacher.html')
        else:
            if is_student():
                return render_template('student.html')
            else:
                if is_admin():
                    return render_template('admin.html')
    else:
        return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/teacher')
def teacher():
    if is_loggedin():
        if is_teacher():
            return render_template('teacher.html')
        else:
            return "You are not a teacher!"
    else:
        return "You are not logged in!"


@app.route('/student')
def student():
    if is_loggedin():
        if not is_student():
            return "You don't have permission!"
    else:
        return "You are not logged in!"
    return render_template('student.html')


@app.route('/teams', methods=['POST', 'GET'])
def display_teams():
    if is_loggedin():
        if not is_student():
            return "You don't have permission!"
    else:
        return "You are not logged in!"
    teams = mongo.db.teams.find()
    return render_template('display_teams.html', teams=teams)


@app.route('/admin')
def admin():
    if is_loggedin():
        if is_admin():
            return render_template('admin.html')
        else:
            return "You are not an admin!"
    else:
        return "You are not logged in!"


def is_loggedin():
    return session.get('username') is not None


def is_admin():
    users = mongo.db.users
    user = users.find_one({'username': session['username']})
    return user['role'] == 'admin'


def is_student():
    users = mongo.db.users
    user = users.find_one({'username': session['username']})
    return user['role'] == 'student'


def is_teacher():
    users = mongo.db.users
    user = users.find_one({'username': session['username']})
    return user['role'] == 'teacher'


@app.route('/loginaction', methods=['POST'])
def loginaction():
    users = mongo.db.users
    login_user = users.find_one({'username': request.form['username']})
    if login_user:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            if login_user['role'] == 'admin':
                return redirect(url_for('admin'))
            else:
                if login_user['role'] == 'teacher':
                    return redirect(url_for('teacher'))
                else:
                    if login_user['role'] == 'student':
                        return redirect(url_for('student'))
    flash('Invalid username or password!')
    return render_template("login.html")


@app.route('/teacherregister', methods=['POST', 'GET'])
def teacherregister():
    if is_loggedin():
        if not is_admin():
            return "You don't have permission!"
    else:
        return "You are not logged in!"

    global role
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'username': request.form['username']})
        if existing_user is None:
            hashpassword = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'username': request.form['username'], 'password': hashpassword, 'role': 'teacher',
                          'firstname': request.form['firstname'], 'lastname': request.form['lastname']})
            flash('Teacher account created!')
        else:
            flash('That username already exists!')
    if is_admin():
        role = "admin"
    return render_template('teacher_register.html', userrole=role)


@app.route('/studentregister', methods=['POST', 'GET'])
def studentregister():
    if is_loggedin():
        if not is_teacher() and not is_admin():
            return "You don't have permission!"
    else:
        return "You are not logged in!"

    global role
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'username': request.form['username']})
        if existing_user is None:
            hashpassword = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'username': request.form['username'], 'password': hashpassword, 'role': 'student',
                          'firstname': request.form['firstname'], 'lastname': request.form['lastname'], 'teams': []})
            flash('Student account created!')
        else:
            flash('That username already exists!')
    if is_teacher():
        role = "teacher"
    else:
        if is_admin():
            role = "admin"
    return render_template('student_register.html', userrole=role)


@app.route('/adminregister', methods=['POST', 'GET'])
def adminregister():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'username': request.form['username']})
        if existing_user is None:
            hashpassword = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'username': request.form['username'], 'password': hashpassword, 'role': 'admin',
                          'firstname': request.form['firstname'], 'lastname': request.form['lastname']})
            return redirect(url_for('home'))
        flash('That username already exists!')
    return render_template('admin_register.html')


@app.route('/create-team', methods=['POST', 'GET'])
def create_team():
    if is_loggedin():
        if not is_teacher():
            return "You don't have permission!"
    else:
        return "You are not logged in!"

    if request.method == 'POST':
        teams = mongo.db.teams
        existing_team = teams.find_one({'name': request.form['name']})
        if existing_team is None:
            password = request.form['password']
            hashpassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            team_image = request.files['image']
            if team_image.filename != "":
                mongo.save_file(team_image.filename, team_image)
                img = team_image.filename
            else:
                img = "nophoto.png"

            teams.insert({'name': request.form['name'], 'description': request.form['description'],
                          'password': hashpassword, 'image': img, 'teacher': session['username'], 'students': [],
                          'tests': [], 'files': []})
            flash('Team created!')
        else:
            flash('That name already exists!')
    return render_template('create_team.html')


@app.route('/myteams')
def myteams():
    userteams = []
    if is_loggedin():
        if not is_teacher():
            return "You don't have permission!"
    else:
        return "You are not logged in!"

    teams = mongo.db.teams.find()
    for team in teams:
        if team['teacher'] == session['username']:
            userteams.append(team)
    return render_template('my_teams.html', teams=userteams)


@app.route('/jointeam/<name>', methods=['POST', 'GET'])
def jointeam(name):
    if is_loggedin():
        if not is_student():
            return "You don't have permission!"
    else:
        return "You are not logged in!"

    teams = mongo.db.teams
    existing_team = teams.find_one({'name': name})
    team_students = existing_team['students']
    for student in team_students:
        if student == session['username']:
            return render_template('team.html', role='student', team=existing_team)

    if bcrypt.hashpw(request.form['password'].encode('utf-8'), existing_team['password']) == existing_team['password']:
        team_students.append(session['username'])
        teams.update_one({"name": name}, {"$set": {'students': team_students}})
        users = mongo.db.users
        existing_user = users.find_one({'username': session['username']})
        student_teams = existing_user['teams']
        student_teams.append(name)
        users.update_one({"username": session['username']}, {"$set": {'teams': student_teams}})
        return render_template('team.html', role='student', team=existing_team)
    else:
        flash('Incorrect password!')
        return render_template("join_team.html", name=name)


@app.route('/enterteam/<name>', methods=['POST', 'GET'])
def enterteam(name):
    if is_loggedin():
        if not is_student():
            return "You don't have permission!"
    else:
        return "You are not logged in!"
    teams = mongo.db.teams
    existing_team = teams.find_one({'name': name})
    team_students = existing_team['students']
    for student in team_students:
        if student == session['username']:
            return render_template('team.html', role='student', team=existing_team)
    return render_template('join_team.html', name=name)


@app.route('/student-teams')
def studentteams():
    studentteams = []
    if is_loggedin():
        if not is_student():
            return "You don't have permission!"
    else:
        return "You are not logged in!"

    teams = mongo.db.teams
    students = mongo.db.users
    student = students.find_one({'username': session['username']})

    for team in student['teams']:
        stud_team = teams.find_one({'name': team})
        studentteams.append(stud_team)
    return render_template('student_teams.html', teams=studentteams)


def has_team(name):
    teams = mongo.db.teams
    team = teams.find_one({'name': name})
    if team['teacher'] == session['username']:
        return True
    for student in team['students']:
        if student == session['username']:
            return True
    return False


@app.route('/team/<name>', methods=['POST', 'GET'])
def team(name):
    if is_loggedin():
        if not is_teacher() and not is_student():
            return "You don't have permission!"
    else:
        return "You are not logged in!"
    global role
    if is_teacher():
        role = "teacher"
    else:
        if is_student():
            role = "student"
    teams = mongo.db.teams
    team = teams.find_one({'name': name})

    if not has_team(name):
        return "You don't have permission!"

    return render_template('team.html', role=role, team=team)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)


if __name__ == '__main__':
    app.run(debug=True)


@app.route('/test')
def test():
    return {
      'resultStatus': 'SUCCESS',
      'message': "Smart School"
      }
