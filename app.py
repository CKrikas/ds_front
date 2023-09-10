from flask import Flask, render_template, request, redirect, url_for, session
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
CORS(app, supports_credentials=True)

BASE_URL = "http://localhost:8080"

# Create a session object to persist cookies across requests
session_requests = requests.Session()

@app.route('/')
def index():
    if 'user' in session:
        if any(role['name'] == 'ADMIN' for role in session['user']['roles']):
            return redirect('/admin/dashboard')
    return render_template('login.html')

@app.route('/user/login', methods=['POST'])
def login():
    data = {
        "amka": request.form['amka'],
        "password": request.form['password']
    }
    response = session_requests.post(f"{BASE_URL}/user/login", json=data)
    if response.status_code == 200:
        session['user'] = response.json()
        return redirect('/admin/dashboard')
    return redirect('/')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user' not in session or not any(role['name'] == 'ADMIN' for role in session['user']['roles']):
        return redirect('/')
    response = session_requests.get(f"{BASE_URL}/user/all")
    if response.status_code == 200 and 'application/json' in response.headers['Content-Type']:
        users = response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        users = []
    return render_template('admin_dashboard.html', users=users)

@app.route('/user/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        data = {
            "name": request.form['name'],
            "surname": request.form['surname'],
            "amka": request.form['amka'],
            "afm": request.form['afm'],
            "password": request.form['password']
        }
        userType = request.form['userType']
        response = session_requests.post(f"{BASE_URL}/user/createUser?userType={userType}", json=data)
        if response.status_code == 200:
            return redirect('/admin/dashboard')
        else:
            return "Error creating user", 400
    return render_template('create_user.html')

@app.route('/user/chooseUpdateMethod', methods=['GET', 'POST'])
def choose_update_method():
    if request.method == 'POST':
        method = request.form['method']
        if method == 'id':
            return redirect(url_for('find_user_by_id'))
        elif method == 'amka':
            return redirect(url_for('find_user_by_amka'))
    return render_template('choose_update_method.html')

@app.route('/user/findById', methods=['GET', 'POST'])
def find_user_by_id():
    if request.method == 'POST':
        user_id = request.form['id']
        return redirect(url_for('update_user', id=user_id))
    return render_template('find_by_id.html')


@app.route('/user/findByAmka', methods=['GET', 'POST'])
def find_user_by_amka():
    if request.method == 'POST':
        amka = request.form['amka']
        user = session_requests.get(f"{BASE_URL}/user/viewUserByAmka/{amka}").json()
        if user:
            return redirect(url_for('update_user', id=user['id']))
        else:
            return "User not found", 404
    return render_template('find_by_amka.html')

@app.route('/user/update/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    if request.method == 'POST':
        data = {
            "name": request.form['name'],
            "surname": request.form['surname'],
            "amka": request.form['amka'],
            "afm": request.form['afm'],
            "password": request.form['password']
        }
        newUserType = request.form['newUserType']
        response = session_requests.put(f"{BASE_URL}/user/updateUser/{id}?newUserType={newUserType}", json=data)
        if response.status_code == 200:
            return redirect('/admin/dashboard')
        else:
            return "Error updating user", 400
    user_response = session_requests.get(f"{BASE_URL}/user/viewUser/{id}")
    if user_response.status_code == 200:
        user = user_response.json()
        return render_template('update_user.html', user=user)
    else:
        return "User not found", 404

@app.route('/user/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    session_requests.delete(f"{BASE_URL}/user/deleteUser/{id}")
    return redirect('/admin/dashboard')


@app.route('/user/logout')
def logout():
    session_requests.post(f"{BASE_URL}/user/logout")
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(host="localhost", port=4000, debug=True)
