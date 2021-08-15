import json
import os
from os.path import join, dirname, realpath
from flask import Flask, render_template, request, flash, url_for
from flask_session import Session
from werkzeug.utils import secure_filename, redirect
from utils import store_new_policy, get_policies_data, get_policy_wise_content, update_policy, delete_policy
import smtplib
import ssl

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/images')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET'])
def home():
    policies_data = get_policies_data()
    return render_template('index.html', policies_data=policies_data, enumerate=enumerate)


@app.route('/send_email', methods=['POST'])
def send_email():
    ssl_port = 465
    smtp_server = "smtp.gmail.com"
    receiver_email = os.environ.get('EMAIL', "lakshmi.srinivas2357@gmail.com")
    password = os.environ.get('PASSWORD', '9392447726')
    request_data = request.form.to_dict()
    sender_email = os.environ.get('EMAIL', "lakshmi.srinivas2357@gmail.com")
    name = request_data.get('name')
    mobile = request_data.get('mobile')
    email = request_data.get('email')
    message = f"""
    Subject: Insure To Secure User Contact Info \n\n
    Name: {name}
    Mobile: {mobile}
    Email: {email}
    """
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, ssl_port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    return redirect(url_for('home'))


@app.route('/api/v1/admin/', methods=['GET'])
def admin_home():
    return render_template('admin.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def send_response(status, message):
    return render_template('result.html', response=[status, message])


@app.route('/api/v1/admin/upload', methods=["GET", "POST"])
def upload_new_policy():
    if request.method == "GET":
        return render_template('upload.html')
    else:
        try:
            request_data = request.form.to_dict()
            if 'policy_img' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['policy_img']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                store_new_policy(request_data, filename)
            return send_response("Success", "Data Uploaded Successfully")
        except Exception as e:
            return send_response("Error", f"{str(e)}")


@app.route('/api/v1/admin/update', methods=['GET', 'POST'])
def update_policy_data():
    if request.method == "GET":
        policy_data = get_policy_wise_content()
        policy_names = list(policy_data.keys())
        return render_template('update.html', policy_data=json.dumps(policy_data), policy_names=policy_names)
    else:
        try:
            request_data = request.form.to_dict()
            file = request.files['policy_img']
            filename = file.filename if file.filename else None
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            update_policy(request_data, filename)
            return send_response("Success", "Data Updated Successfully")
        except Exception as e:
            return send_response("Error", f"{str(e)}")


@app.route('/api/v1/admin/delete', methods=['GET', 'POST'])
def delete_policy_data():
    if request.method == 'GET':
        policies_data = get_policy_wise_content()
        policy_names = list(policies_data.keys())
        return render_template('delete.html', policy_names=policy_names)
    else:
        try:
            request_data = request.form.to_dict()
            delete_policy(request_data)
            return send_response("Success", "Policy deleted Successfully")
        except Exception as e:
            return send_response("Error", f"{str(e)}")


if __name__ == '__main__':
    app.run(debug=True)
