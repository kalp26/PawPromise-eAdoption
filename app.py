import os,re
import uuid, random,time,io,csv
import secrets
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify,make_response
from flask_mysqldb import MySQL
import google.generativeai as genai
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message  # type: ignore
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'pawpromise'

API_KEY = "AIzaSyA_aNcMzm8DrD1Rc2XsCxWf9djCgkTHmvQ"  
genai.configure(api_key=API_KEY)

last_request_time = 0
MIN_REQUEST_INTERVAL = 3 

model = genai.GenerativeModel('gemini-1.5-pro')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pawpromise'

mysql = MySQL(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'pawpromiseeadoption@gmail.com'
app.config['MAIL_PASSWORD'] = 'plfg xpiy prne cshp'
app.config['MAIL_DEFAULT_SENDER'] = 'pawpromiseeadoption@gmail.com'

mail = Mail(app)


@app.route('/')
def index():
    return render_template('index.html')



#routes to handle authentication
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        user_type = request.form.get('login-as')
        email = request.form['email']
        password = request.form['password']

        if user_type == 'user':
            table = 'users'
            session_key = 'user_id'
            session_name = 'username'
            id_column = 'id'
            name_column = 'first_name'
        elif user_type == 'organization':
            table = 'organizations'
            session_key = 'org_id'
            session_name = 'org_name'
            id_column = 'id'
            name_column = 'org_name'
        else:
            flash('Invalid user type', 'danger')
            return redirect(url_for('signin'))

        cur = mysql.connection.cursor()
        query = f"SELECT {id_column}, {name_column}, user_type FROM {table} WHERE email = %s AND password = %s"
        cur.execute(query, (email, password))
        user = cur.fetchone()
        cur.close()

        if user:
            session[session_key] = user[0]  
            session[session_name] = user[1]
            session['user_type'] = user[2]  

            notification_count = get_unread_notification_count(user[2], user[0])
            
            welcome_message = f'Welcome back, {session[session_name]}!'
            if notification_count > 0:
                welcome_message += f' You have {notification_count} unread notifications.'
            
            flash(welcome_message, 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('signin'))

    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/send_otp', methods=['POST'])
def send_otp():
    try:
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({'status': 'error', 'message': 'Email is required'}), 400

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing_user = cur.fetchone()
        cur.close()

        if existing_user:
            return jsonify({'status': 'error', 'message': 'Email already registered'}), 400

        otp = str(random.randint(100000, 999999))
        session['otp'] = otp
        session['otp_email'] = email

        try:
            msg = Message('Your OTP Code for PawPromise Registration',recipients=[email])
            msg.body = f'Your OTP is {otp}. It is valid for 5 minutes.'
            mail.send(msg)
            return jsonify({'status': 'success', 'message': 'OTP sent successfully'})
        except Exception as e:
            print(f"Email error: {str(e)}")
            return jsonify({'status': 'error', 'message': f'Failed to send email: {str(e)}'}), 500

    except Exception as e:
        print(f"OTP send error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    try:
        data = request.get_json()
        user_otp = data.get('otp')
        email = data.get('email')

        stored_otp = session.get('otp')
        stored_email = session.get('otp_email')

        if not stored_otp or not stored_email:
            return jsonify({'status': 'error', 'message': 'OTP session expired'}), 400

        if email != stored_email:
            return jsonify({'status': 'error', 'message': 'Email mismatch'}), 400

        if user_otp != stored_otp:
            return jsonify({'status': 'error', 'message': 'Invalid OTP'}), 400

        session['otp_verified'] = True
        session.pop('otp', None)

        return jsonify({'status': 'verified'}), 200

    except Exception as e:
        print(f"OTP verification error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/check_email', methods=['POST'])
def check_email():
    data = request.json
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM users WHERE email = %s", (email,))
    user_exists = cur.fetchone()
    cur.execute("SELECT id FROM organizations WHERE email = %s", (email,))
    org_exists = cur.fetchone()
    cur.close()
    exists = user_exists is not None or org_exists is not None
    return jsonify({'exists': exists})

@app.route('/user_signup', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'POST':
        if not session.get('otp_verified'):
            flash('Email verification required!', 'danger')
            return redirect(url_for('user_signup'))

        first_name = request.form['firstName']
        last_name = request.form['lastName']
        gender = request.form['gender']
        state = request.form['states']
        city = request.form['cities']
        phone = request.form['number']
        email = request.form['email']
        password = request.form['password']

        if email != session.get('otp_email'):
            flash('Email mismatch with verification!', 'danger')
            return redirect(url_for('user_signup'))            
        password_pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,}$"
        if not re.match(password_pattern, password):
            flash('Password must be at least 8 characters with at least one capital letter, one small letter, one number, and one special character', 'danger')
            return redirect(url_for('user_signup'))

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        user_exists = cur.fetchone()
        cur.execute("SELECT id FROM organizations WHERE email = %s", (email,))
        org_exists = cur.fetchone()
        
        if user_exists or org_exists:
            flash('This email is already registered', 'danger')
            return redirect(url_for('user_signup'))

        try:
            cur.execute("""
                INSERT INTO users (first_name, last_name, gender, state, city, phone, email, password) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (first_name, last_name, gender, state, city, phone, email, password))
            mysql.connection.commit()

            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            user_id = cur.fetchone()[0]
            cur.close()

            session['user_id'] = user_id
            session['username'] = first_name
            session.pop('otp_verified', None)
            session.pop('otp_email', None)

            flash('User Registered Successfully!', 'success')
            return redirect(url_for('index'))

        except Exception as e:
            flash(f'Registration error: {str(e)}', 'danger')
            return redirect(url_for('user_signup'))

    return render_template('user-signup.html')

@app.route('/org_signup', methods=['GET', 'POST'])
def org_signup():
    if request.method == 'POST':
        if not session.get('otp_verified'):
            flash('Email verification required!', 'danger')
            return redirect(url_for('org_signup'))

        org_name = request.form['orgName']
        org_type = request.form['specialist']
        state = request.form['states']
        city = request.form['cities']
        phone = request.form['number']
        email = request.form['email']
        password = request.form['password']

        if email != session.get('otp_email'):
            flash('Email mismatch with verification!', 'danger')
            return redirect(url_for('org_signup'))           
        password_pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,}$"
        if not re.match(password_pattern, password):
            flash('Password must be at least 8 characters with at least one capital letter, one small letter, one number, and one special character', 'danger')
            return redirect(url_for('org_signup'))

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        user_exists = cur.fetchone()
        cur.execute("SELECT id FROM organizations WHERE email = %s", (email,))
        org_exists = cur.fetchone()
        
        if user_exists or org_exists:
            flash('This email is already registered', 'danger')
            return redirect(url_for('org_signup'))

        try:
            cur.execute("""
                INSERT INTO organizations (org_name, org_type, state, city, phone, email, password) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (org_name, org_type, state, city, phone, email, password))
            mysql.connection.commit()

            cur.execute("SELECT id FROM organizations WHERE email = %s", (email,))
            org_id = cur.fetchone()[0]
            cur.close()

            session['org_id'] = org_id
            session['org_name'] = org_name
            session.pop('otp_verified', None)
            session.pop('otp_email', None)

            flash('Organization Registered Successfully!', 'success')
            return redirect(url_for('index'))

        except Exception as e:
            flash(f'Registration error: {str(e)}', 'danger')
            return redirect(url_for('org_signup'))

    return render_template('org-signup.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out!', 'success')
    return redirect(url_for('index'))

@app.route('/change_password', methods=['POST'])
def change_password():
    if 'user_id' in session:
        user_type = "user"
        user_id = session['user_id']
        table = "users"
    elif 'org_id' in session:
        user_type = "organization"
        user_id = session['org_id']
        table = "organizations"
    else:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    old_password = request.form['oldPassword']
    new_password = request.form['newPassword']
    confirm_password = request.form.get('confirmPassword', '')

    if new_password != confirm_password:
        return jsonify({"status": "error", "message": "New password and confirmation do not match"}), 400

    if len(new_password) < 8:
        return jsonify({"status": "error", "message": "Password must be at least 8 characters long"}), 400

    if not (any(c.isupper() for c in new_password) and 
            any(c.islower() for c in new_password) and 
            any(c.isdigit() for c in new_password) and 
            any(c in '!@#$%^&*' for c in new_password)):
        return jsonify({
            "status": "error", 
            "message": "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character"
        }), 400

    cur = mysql.connection.cursor()

    cur.execute(f"SELECT password FROM {table} WHERE id = %s", (user_id,))
    user = cur.fetchone()

    if not user or user[0] != old_password:
        return jsonify({"status": "error", "message": "Incorrect current password"}), 400

    cur.execute(f"UPDATE {table} SET password = %s WHERE id = %s", (new_password, user_id))
    mysql.connection.commit()
    cur.close()

    return jsonify({"status": "success", "message": f"{user_type.capitalize()} password changed successfully!"})

password_reset_tokens = {}
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        user_type = request.form.get('account-type')
        email = request.form.get('email')

        if not email:
            flash('Email is required', 'danger')
            return redirect(url_for('forgot_password'))

        if user_type == 'user':
            table = 'users'
            id_column = 'id'
        elif user_type == 'organization':
            table = 'organizations'
            id_column = 'id'
        else:
            flash('Invalid account type', 'danger')
            return redirect(url_for('forgot_password'))

        cur = mysql.connection.cursor()
        query = f"SELECT {id_column} FROM {table} WHERE email = %s"
        cur.execute(query, (email,))
        user = cur.fetchone()
        cur.close()

        if not user:
            flash('If your email is registered, you will receive a password reset link shortly', 'info')
            return redirect(url_for('signin'))
        token = secrets.token_urlsafe(32)
        expiration = datetime.now() + timedelta(hours=1)
        password_reset_tokens[token] = {
            'email': email,
            'user_type': user_type,
            'expires': expiration
        }

        reset_url = url_for('reset_password', token=token, _external=True)
        
        try:
            msg = Message('Password Reset Request for PawPromise',recipients=[email])
            msg.body = f'''To reset your password, visit the following link:
{reset_url}

This link will expire in 1 hour.

If you did not make this request, please ignore this email.
'''
            mail.send(msg)
            flash('Password reset link has been sent to your email', 'success')
            return redirect(url_for('signin'))
            
        except Exception as e:
            flash(f'Failed to send email: {str(e)}', 'danger')
            return redirect(url_for('forgot_password'))

    return render_template('forgot-password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if token not in password_reset_tokens:
        flash('Invalid or expired password reset link', 'danger')
        return redirect(url_for('signin'))
    
    token_data = password_reset_tokens[token]

    if datetime.now() > token_data['expires']:
        password_reset_tokens.pop(token)
        flash('This password reset link has expired', 'danger')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('reset-password.html', token=token, user_type=token_data['user_type'])
        password_pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,}$"
        if not re.match(password_pattern, password):
            flash('Password must be at least 8 characters with at least one capital letter, one small letter, one number, and one special character', 'danger')
            return render_template('reset-password.html', token=token, user_type=token_data['user_type'])

        email = token_data['email']
        user_type = token_data['user_type']
        
        if user_type == 'user':
            table = 'users'
        elif user_type == 'organization':
            table = 'organizations'
        else:
            flash('Invalid account type', 'danger')
            return redirect(url_for('signin'))
        
        try:
            cur = mysql.connection.cursor()
            query = f"UPDATE {table} SET password = %s WHERE email = %s"
            cur.execute(query, (password, email))
            mysql.connection.commit()
            cur.close()

            password_reset_tokens.pop(token)
            
            flash('Your password has been successfully updated! You can now log in with your new password.', 'success')
            return redirect(url_for('signin'))
            
        except Exception as e:
            flash(f'Password update error: {str(e)}', 'danger')
            return render_template('reset-password.html', token=token, user_type=token_data['user_type'])

    return render_template('reset-password.html', token=token, user_type=token_data['user_type'])

@app.route('/get_user_details', methods=['GET'])
def get_user_details():
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, first_name, last_name, email, phone, state, city FROM users WHERE id = %s", (session['user_id'],))
    user = cur.fetchone()
    cur.close()

    if user:
        return jsonify({
            'id': user[0], 
            'first_name': user[1], 
            'last_name': user[2], 
            'email': user[3], 
            'phone': user[4],
            'state': user[5], 
            'city': user[6]
        })
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/update_user_details', methods=['POST'])
def update_user_details():
    user_id = request.form['user_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    phone = request.form['phone']
    state = request.form['state']
    city = request.form['city']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET first_name=%s, last_name=%s, phone=%s, state=%s, city=%s WHERE id=%s",
                (first_name, last_name, phone, state, city, user_id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Details updated successfully'})

@app.route('/get_organization_details', methods=['GET'])
def get_organization_details():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, org_name, org_type, state, city, email, phone FROM organizations WHERE id = %s", (session['org_id'],))
    org = cur.fetchone()
    cur.close()

    if org:
        return jsonify({
            'id': org[0],
            'org_name': org[1],
            'org_type': org[2],
            'state': org[3],
            'city': org[4],
            'email': org[5],
            'phone': org[6]
        })
    else:
        return jsonify({'error': 'Organization not found'}), 404

@app.route('/update_organization_details', methods=['POST'])
def update_organization_details():
    org_id = request.form['org_id']
    org_name = request.form['org_name']
    org_type = request.form['org_type']
    state = request.form['state']
    city = request.form['city']
    email = request.form['email']
    phone = request.form['phone']

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE organizations 
        SET org_name=%s, org_type=%s, state=%s, city=%s, email=%s, phone=%s 
        WHERE id=%s
    """, (org_name, org_type, state, city, email, phone, org_id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'status': 'success', 'message': 'Organization details updated successfully'})

@app.route('/org-verification')
def org_verification():
    return render_template('org-verification.html')

@app.route("/submit_org_verification", methods=["POST"])
def submit_org_verification():
    if 'org_id' not in session:
        flash("Please log in as an organization first.", "danger")
        return redirect(url_for('signin'))
    
    org_id = session['org_id']
    cur = mysql.connection.cursor()

    org_name = request.form["org_name"]
    phone = request.form["phone"]
    website = request.form.get("website", "")
    social_media = request.form.get("social_media", "")
    address = request.form["address"]
    reg_number = request.form["reg_number"]
    years_operation = request.form["years_operation"]
    org_type = request.form["org_type"]
    emergency_contact = request.form["emergency_contact"]
    rep_name = request.form["rep_name"]
    mission = request.form["mission"]

    reg_certificate = request.files["reg_certificate"]
    reg_certificate_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(reg_certificate.filename))
    reg_certificate.save(reg_certificate_path)

    tax_certificate = request.files.get("tax_certificate")
    tax_certificate_path = None
    if tax_certificate and tax_certificate.filename:
        tax_certificate_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(tax_certificate.filename))
        tax_certificate.save(tax_certificate_path)

    rep_id = request.files["rep_id"]
    rep_id_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(rep_id.filename))
    rep_id.save(rep_id_path)

    query = """
    UPDATE organizations SET 
        org_name = %s, 
        phone = %s, 
        website = %s, 
        social_media = %s, 
        address = %s, 
        reg_number = %s, 
        years_operation = %s, 
        org_type = %s, 
        emergency_contact = %s, 
        reg_certificate = %s, 
        tax_certificate = %s, 
        rep_name = %s, 
        rep_id_proof = %s, 
        mission = %s,
        status = 'pending'
    WHERE id = %s
    """
    
    cur.execute(query, (
        org_name, phone, website, social_media, address, reg_number, 
        years_operation, org_type, emergency_contact, reg_certificate_path, 
        tax_certificate_path, rep_name, rep_id_path, mission, org_id
    ))

    mysql.connection.commit()
    cur.close()

    flash("Organization verification submitted successfully! Your verification is pending review.", "success")
    return redirect("/profile")

@app.route('/profile')
def profile():
    user = None
    reg_number = None

    if 'user_id' in session:
        user_id = session['user_id']
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT 'user' AS type, first_name, last_name, email, gender, state, city, phone FROM users WHERE id = %s",
            (user_id,))
        user = cur.fetchone()
        cur.close()

    elif 'org_id' in session:
        org_id = session['org_id']
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT 'organization' AS type, org_name, org_type, email, NULL, state, city, phone, status FROM organizations WHERE id = %s",
            (org_id,))
        user = cur.fetchone()
        cur.execute("SELECT reg_number FROM organizations WHERE id = %s", (org_id,))
        result = cur.fetchone()
        if result and result[0]:
            reg_number = result[0]
        cur.close()

    else:
        flash('Please log in to view your profile', 'danger')
        return redirect(url_for('signin'))

    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('index'))

    return render_template('profile.html', user=user, reg_number=reg_number)



# Routes to handle notifications
@app.route('/notifications')
def notifications():
    if 'user_id' in session:
        user_type = 'user'
        user_id = session['user_id']
    elif 'org_id' in session:
        user_type = 'organization'
        user_id = session['org_id']
    else:
        flash('Please login first', 'danger')
        return redirect(url_for('signin'))

    notifications = get_notifications(user_type, user_id)
    
    return render_template('notifications.html', notifications=notifications)

@app.route('/notifications/mark_read/<int:notification_id>', methods=['POST'])
def mark_read(notification_id):
    if 'user_id' not in session and 'org_id' not in session:
        return jsonify({'success': False, 'message': 'Please login first'})
    
    mark_notification_as_read(notification_id)
    
    return jsonify({'success': True})

@app.route('/notifications/mark_all_read', methods=['POST'])
def mark_all_read():
    if 'user_id' in session:
        user_type = 'user'
        user_id = session['user_id']
    elif 'org_id' in session:
        user_type = 'organization'
        user_id = session['org_id']
    else:
        return jsonify({'success': False, 'message': 'Please login first'})
    
    mark_all_notifications_as_read(user_type, user_id)
    
    return jsonify({'success': True})

@app.route('/notifications/count')
def notification_count():
    """API endpoint to get unread notification count for AJAX calls"""
    if 'user_id' in session:
        user_type = 'user'
        user_id = session['user_id']
    elif 'org_id' in session:
        user_type = 'organization'
        user_id = session['org_id']
    else:
        return jsonify({'count': 0})
    
    count = get_unread_notification_count(user_type, user_id)
    
    return jsonify({'count': count})

def get_unread_notification_count(user_type, user_id):
    """Get count of unread notifications for a user or organization"""
    cur = mysql.connection.cursor()
    
    if user_type == 'user':
        cur.execute("SELECT COUNT(*) FROM notifications WHERE user_id = %s AND is_read = 0", (user_id,))
    else:
        cur.execute("SELECT COUNT(*) FROM notifications WHERE org_id = %s AND is_read = 0", (user_id,))
    
    count = cur.fetchone()[0]
    cur.close()
    return count

def get_notifications(user_type, user_id):
    """Get all notifications for a user or organization"""
    cur = mysql.connection.cursor()
    
    if user_type == 'user':
        cur.execute(
            "SELECT id, message, type, reference_id, reference_type, is_read, created_at "
            "FROM notifications WHERE user_id = %s ORDER BY created_at DESC", 
            (user_id,)
        )
    else:
        cur.execute(
            "SELECT id, message, type, reference_id, reference_type, is_read, created_at "
            "FROM notifications WHERE org_id = %s ORDER BY created_at DESC", 
            (user_id,)
        )
    
    notifications = cur.fetchall()
    cur.close()

    formatted_notifications = []
    for notif in notifications:
        time_diff = datetime.now() - notif[6]
        
        if time_diff.days == 0:
            if time_diff.seconds < 60:
                time_str = "just now"
            elif time_diff.seconds < 3600:
                time_str = f"{time_diff.seconds // 60} minutes ago"
            else:
                time_str = f"{time_diff.seconds // 3600} hours ago"
        elif time_diff.days == 1:
            time_str = "yesterday"
        elif time_diff.days < 30:
            time_str = f"{time_diff.days} days ago"
        elif time_diff.days < 365:
            time_str = f"{time_diff.days // 30} months ago"
        else:
            time_str = f"{time_diff.days // 365} years ago"
        
        formatted_notifications.append({
            'id': notif[0],
            'message': notif[1],
            'type': notif[2],
            'reference_id': notif[3],
            'reference_type': notif[4],
            'is_read': bool(notif[5]),
            'created_at': notif[6],
            'time_ago': time_str
        }) 
    return formatted_notifications

def mark_notification_as_read(notification_id):
    """Mark a notification as read"""
    cur = mysql.connection.cursor()
    cur.execute("UPDATE notifications SET is_read = 1 WHERE id = %s", (notification_id,))
    mysql.connection.commit()
    cur.close()

def mark_all_notifications_as_read(user_type, user_id):
    """Mark all notifications as read for a user or organization"""
    cur = mysql.connection.cursor()
    
    if user_type == 'user':
        cur.execute("UPDATE notifications SET is_read = 1 WHERE user_id = %s", (user_id,))
    else:
        cur.execute("UPDATE notifications SET is_read = 1 WHERE org_id = %s", (user_id,))
    mysql.connection.commit()
    cur.close()

@app.route('/notifications/delete/<int:notification_id>', methods=['POST'])
def delete_notification(notification_id):
    """Delete a specific notification"""
    if 'user_id' not in session and 'org_id' not in session:
        return jsonify({'success': False, 'message': 'Please login first'})
    delete_notification_by_id(notification_id)
    return jsonify({'success': True})

@app.route('/notifications/delete_all', methods=['POST'])
def delete_all_notifications():
    """Delete all notifications for the current user or organization"""
    if 'user_id' in session:
        user_type = 'user'
        user_id = session['user_id']
    elif 'org_id' in session:
        user_type = 'organization'
        user_id = session['org_id']
    else:
        return jsonify({'success': False, 'message': 'Please login first'})
    delete_all_notifications_for_user(user_type, user_id)
    return jsonify({'success': True})


def delete_notification_by_id(notification_id):
    """Delete a notification by its ID"""
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM notifications WHERE id = %s", (notification_id,))
    mysql.connection.commit()
    cur.close()

def delete_all_notifications_for_user(user_type, user_id):
    """Delete all notifications for a user or organization"""
    cur = mysql.connection.cursor()
    
    if user_type == 'user':
        cur.execute("DELETE FROM notifications WHERE user_id = %s", (user_id,))
    else:
        cur.execute("DELETE FROM notifications WHERE org_id = %s", (user_id,))
    
    mysql.connection.commit()
    cur.close()



# Route for contact us form submission
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        if not name or not email or not phone or not message:
            flash("All fields are required!", "danger")
            return redirect('/')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contact_messages (name, email, phone, message) VALUES (%s, %s, %s, %s)",
                    (name, email, phone, message))
        mysql.connection.commit()
        cur.close()

        flash("Message sent successfully!", "success")
        return redirect(url_for('index'))
    


# Routes for share your story page
@app.route('/upload', methods=['POST'])
def upload():
    if 'user_id' not in session and 'org_id' not in session:
        flash('Please log in first', 'danger')
        return redirect(url_for('signin'))

    if 'image' not in request.files:
        flash('No image uploaded', 'danger')
        return redirect(url_for('Share_your_story'))

    file = request.files['image']
    caption = request.form.get('caption', '')

    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('Share_your_story'))

    upload_folder = 'static/uploads/'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    ext = os.path.splitext(file.filename)[1]  
    unique_filename = f"{uuid.uuid4().hex}{ext}"  
    file_path = os.path.join(upload_folder, unique_filename)
    file.save(file_path)  
    cur = mysql.connection.cursor()
    
    if 'user_id' in session:
        cur.execute("INSERT INTO posts (user_id, org_id, image, caption) VALUES (%s, NULL, %s, %s)",
                    (session['user_id'], unique_filename, caption))
    else:
        cur.execute("INSERT INTO posts (user_id, org_id, image, caption) VALUES (NULL, %s, %s, %s)",
                    (session['org_id'], unique_filename, caption))
    
    mysql.connection.commit()
    cur.close()

    flash('Story uploaded successfully!', 'success')
    return redirect(url_for('Share_your_story'))

@app.route('/like/<int:post_id>', methods=['POST'])
def like_story(post_id):
    if 'user_id' not in session and 'org_id' not in session:
        return jsonify({"error": "Not logged in"}), 403
    cur = mysql.connection.cursor()

    if 'user_id' in session:
        user_id = session['user_id']
        org_id = None
        cur.execute("SELECT id FROM likes WHERE user_id = %s AND org_id IS NULL AND post_id = %s", 
                    (user_id, post_id))
    else:
        user_id = None
        org_id = session['org_id']
        cur.execute("SELECT id FROM likes WHERE org_id = %s AND user_id IS NULL AND post_id = %s", 
                    (org_id, post_id))
    
    like = cur.fetchone()

    if like:
        if 'user_id' in session:
            cur.execute("DELETE FROM likes WHERE user_id = %s AND org_id IS NULL AND post_id = %s", 
                        (user_id, post_id))
        else:
            cur.execute("DELETE FROM likes WHERE org_id = %s AND user_id IS NULL AND post_id = %s", 
                        (org_id, post_id))
        
        mysql.connection.commit()
        status = "unliked"
    else:
        cur.execute("INSERT INTO likes (user_id, org_id, post_id) VALUES (%s, %s, %s)", 
                    (user_id, org_id, post_id))
        mysql.connection.commit()
        status = "liked"

    cur.execute("SELECT COUNT(*) FROM likes WHERE post_id = %s", (post_id,))
    like_count = cur.fetchone()[0]
    cur.close()

    return jsonify({"status": status, "likes": like_count})

@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if 'user_id' not in session and 'org_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    user_type = session.get('user_type', 'user')
    user_id = session.get('user_id')
    org_id = session.get('org_id')
    cur = mysql.connection.cursor()

    try:
        if user_type == 'user':
            cur.execute("SELECT user_id FROM posts WHERE id = %s", (post_id,))
            post_owner = cur.fetchone()
            if not post_owner or post_owner[0] != user_id:
                return jsonify({'success': False, 'error': 'Not authorized'}), 403
        else:
            cur.execute("SELECT org_id FROM posts WHERE id = %s", (post_id,))
            post_owner = cur.fetchone()
            if not post_owner or post_owner[0] != org_id:
                return jsonify({'success': False, 'error': 'Not authorized'}), 403

        cur.execute("DELETE FROM posts WHERE id = %s", (post_id,))
        mysql.connection.commit()

        return jsonify({'success': True})

    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

    finally:
        cur.close()

@app.route('/comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    if 'user_id' not in session and 'org_id' not in session:
        return jsonify({'error': 'You must be logged in to comment'}), 403

    comment_text = request.form.get('comment')
    if not comment_text:
        return jsonify({'error': 'Comment cannot be empty'}), 400

    cur = mysql.connection.cursor()

    if 'user_id' in session:
        user_id = session['user_id']
        org_id = None
        poster_type = 'user'
    else:
        user_id = None
        org_id = session['org_id']
        poster_type = 'organization'

    cur.execute("INSERT INTO comments (post_id, user_id, org_id, text) VALUES (%s, %s, %s, %s)", 
                (post_id, user_id, org_id, comment_text))
    mysql.connection.commit()

    if poster_type == 'user':
        cur.execute("SELECT first_name, last_name FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        first_name = user[0]
        last_name = user[1] if user[1] else ''
    else:
        cur.execute("SELECT org_name FROM organizations WHERE id = %s", (org_id,))
        org = cur.fetchone()
        first_name = org[0] if org else 'Organization'
        last_name = ''
    
    comment_id = cur.lastrowid
    cur.close()

    return jsonify({
        'id': comment_id,
        'comment': comment_text,
        'first_name': first_name,
        'last_name': last_name,
        'user_id': user_id,
        'org_id': org_id,
        'commenter_type': poster_type
    })

@app.route('/delete_comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    if 'user_id' not in session and 'org_id' not in session:
        return jsonify({'error': 'You must be logged in to delete comments'}), 403
    
    cur = mysql.connection.cursor()
    
    try:
        if 'user_id' in session:
            user_id = session['user_id']
            cur.execute("SELECT user_id FROM comments WHERE id = %s", (comment_id,))
            result = cur.fetchone()
            
            if result and result[0] == user_id:
                cur.execute("DELETE FROM comments WHERE id = %s", (comment_id,))
                mysql.connection.commit()
                return jsonify({'success': True})
        
        elif 'org_id' in session:
            org_id = session['org_id']
            cur.execute("SELECT org_id FROM comments WHERE id = %s", (comment_id,))
            result = cur.fetchone()
            
            if result and result[0] == org_id:
                cur.execute("DELETE FROM comments WHERE id = %s", (comment_id,))
                mysql.connection.commit()
                return jsonify({'success': True})
        
        return jsonify({'error': 'Unauthorized'}), 403
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        cur.close()


@app.route('/Share-your-story')
def Share_your_story():
    if 'user_id' not in session and 'org_id' not in session:
        return redirect('/signin')
    cur = mysql.connection.cursor()

    if 'user_id' in session:
        user_id = session['user_id']
        org_id = None
        cur.execute("SELECT profile_pic, username FROM users WHERE id = %s", (user_id,))
        user_data = cur.fetchone()
        profile_pic = user_data[0] if user_data and user_data[0] else "uplods/default.jpg"
        username = user_data[1] if user_data and user_data[1] else None
    else:
        user_id = None
        org_id = session['org_id']
        cur.execute("SELECT profile_pic, username FROM organizations WHERE id = %s", (org_id,))
        org_data = cur.fetchone()
        profile_pic = org_data[0] if org_data and org_data[0] else "uplods/default.jpg"
        username = org_data[1] if org_data and org_data[1] else None
    username_default = 'pawpromise'
    if 'user_id' in session:
        username_needs_update = not username or username == username_default
    else:
        username_needs_update = not username
    if username_needs_update:
        cur.close()
        return render_template('Share-your-story.html', 
                            posts=[], 
                            user_id=user_id, 
                            org_id=org_id, 
                            profile_pic=profile_pic,
                            user_type='user' if 'user_id' in session else 'organization',
                            username_needs_update=username_needs_update,
                            current_username=username)

    if 'user_id' in session:
        cur.execute("""
            SELECT p.id, p.image, p.caption, 
                CASE 
                    WHEN p.user_id IS NOT NULL THEN COALESCE(u.username, CONCAT(u.first_name, ' ', u.last_name)) 
                    WHEN p.org_id IS NOT NULL THEN COALESCE(o.username, o.org_name) 
                END AS username,
                CASE 
                    WHEN p.user_id IS NOT NULL THEN u.profile_pic 
                    WHEN p.org_id IS NOT NULL THEN o.profile_pic 
                END AS profile_pic,
                (SELECT COUNT(*) FROM likes WHERE post_id = p.id) AS like_count,
                (SELECT COUNT(*) FROM likes WHERE post_id = p.id AND user_id = %s AND org_id IS NULL) AS user_liked,
                p.created_at,
                CASE 
                    WHEN p.user_id IS NOT NULL THEN 'user' 
                    WHEN p.org_id IS NOT NULL THEN 'organization' 
                END AS poster_type,
                COALESCE(p.user_id, p.org_id) AS poster_id
            FROM posts p
            LEFT JOIN users u ON p.user_id = u.id
            LEFT JOIN organizations o ON p.org_id = o.id
            ORDER BY p.created_at DESC
        """, (user_id,))
    else:
        cur.execute("""
            SELECT p.id, p.image, p.caption, 
                CASE 
                    WHEN p.user_id IS NOT NULL THEN COALESCE(u.username, CONCAT(u.first_name, ' ', u.last_name)) 
                    WHEN p.org_id IS NOT NULL THEN COALESCE(o.username, o.org_name) 
                END AS username,
                CASE 
                    WHEN p.user_id IS NOT NULL THEN u.profile_pic 
                    WHEN p.org_id IS NOT NULL THEN o.profile_pic 
                END AS profile_pic,
                (SELECT COUNT(*) FROM likes WHERE post_id = p.id) AS like_count,
                (SELECT COUNT(*) FROM likes WHERE post_id = p.id AND org_id = %s AND user_id IS NULL) AS user_liked,
                p.created_at,
                CASE 
                    WHEN p.user_id IS NOT NULL THEN 'user' 
                    WHEN p.org_id IS NOT NULL THEN 'organization' 
                END AS poster_type,
                COALESCE(p.user_id, p.org_id) AS poster_id
            FROM posts p
            LEFT JOIN users u ON p.user_id = u.id
            LEFT JOIN organizations o ON p.org_id = o.id
            ORDER BY p.created_at DESC
        """, (org_id,))

    posts = cur.fetchall()
    posts_data = []
    for post in posts:
        post_data = {
            'id': post[0],
            'image': post[1],
            'caption': post[2],
            'username': post[3],
            'profile_pic': post[4] if post[4] else "uplods/default.jpg",
            'like_count': post[5],
            'user_liked': post[6] > 0,
            'time_ago': format_time_ago(post[7]),
            'poster_type': post[8],
            'poster_id': post[9],
            'comments': []
        }
        cur.execute("""
            SELECT c.id, c.text, 
                CASE 
                    WHEN c.user_id IS NOT NULL THEN COALESCE(u.username, CONCAT(u.first_name, ' ', u.last_name)) 
                    WHEN c.org_id IS NOT NULL THEN COALESCE(o.username, o.org_name) 
                END AS username,
                c.user_id, c.org_id,
                CASE 
                    WHEN c.user_id IS NOT NULL THEN 'user' 
                    WHEN c.org_id IS NOT NULL THEN 'organization' 
                END AS commenter_type,
                c.created_at
            FROM comments c
            LEFT JOIN users u ON c.user_id = u.id
            LEFT JOIN organizations o ON c.org_id = o.id
            WHERE c.post_id = %s
            ORDER BY c.id DESC
        """, (post[0],))
        comments = cur.fetchall()

        post_data['comments'] = [
            {
                'id': c[0], 
                'text': c[1], 
                'username': c[2], 
                'user_id': c[3],
                'org_id': c[4],
                'commenter_type': c[5],
                'time_ago': format_time_ago(c[6])
            }
            for c in comments
        ]

        posts_data.append(post_data)

    cur.close()

    return render_template('Share-your-story.html', 
                          posts=posts_data, 
                          user_id=user_id, 
                          org_id=org_id, 
                          profile_pic=profile_pic,
                          user_type='user' if 'user_id' in session else 'organization',
                          username_needs_update=username_needs_update,
                          current_username=username)


UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/Sys-profile')
def Sys_profile():
    if 'user_id' not in session and 'org_id' not in session:
        flash('Please log in first', 'danger')
        return redirect(url_for('signin'))

    user_type = session.get('user_type', 'user')
    user_id = session.get('user_id', None)
    org_id = session.get('org_id', None)
    cur = mysql.connection.cursor()

    if user_type == 'user':
        cur.execute("SELECT profile_pic, slogan, username FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        
        cur.execute("""
            SELECT id, image, caption, created_at 
            FROM posts 
            WHERE user_id = %s
            ORDER BY created_at DESC
        """, (user_id,))
        
        slogan_field = user[1] if user and user[1] else "No slogan set"
    else:
        cur.execute("SELECT profile_pic, mission, username FROM organizations WHERE id = %s", (org_id,))
        user = cur.fetchone()
        
        cur.execute("""
            SELECT id, image, caption, created_at 
            FROM posts 
            WHERE org_id = %s
            ORDER BY created_at DESC
        """, (org_id,))
        
        slogan_field = user[1] if user and user[1] else "No mission statement set"

    posts = cur.fetchall()
    posts_data = [
        {
            'id': post[0],
            'image': post[1],
            'caption': post[2],
            'created_at': post[3],
            'time_ago': format_time_ago(post[3])
        } for post in posts
    ]
    
    profile_pic = user[0] if user and user[0] else 'default.jpg'

    
    user_data = {
        'username': user[2] if user and user[2] else '',
        'profile_pic': profile_pic,
        'slogan': user[1] if user and user[1] else "No slogan set",
    }
    username_needs_update = not user_data['username']
    cur.close()

    return render_template("Sys-profile.html", 
                          user_data=user_data, 
                          posts=posts_data, 
                          username_needs_update=username_needs_update,
                          user_type=user_type)

@app.route('/get_post_details/<int:post_id>')
def get_post_details(post_id):
    if 'user_id' not in session and 'org_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    user_type = session.get('user_type', 'user')
    user_id = session.get('user_id')
    org_id = session.get('org_id')
    
    cur = mysql.connection.cursor()
    query = """
        SELECT p.id, p.image, p.caption, 
            COALESCE(p.user_id, p.org_id) as poster_id,
            CASE 
                WHEN p.user_id IS NOT NULL THEN (SELECT username FROM users WHERE id = p.user_id)
                ELSE (SELECT username FROM organizations WHERE id = p.org_id)
            END as username,
            CASE 
                WHEN p.user_id IS NOT NULL THEN (SELECT profile_pic FROM users WHERE id = p.user_id)
                ELSE (SELECT profile_pic FROM organizations WHERE id = p.org_id)
            END as profile_pic,
            (SELECT COUNT(*) FROM likes WHERE post_id = p.id) AS like_count,
            p.created_at,
            CASE 
                WHEN p.user_id IS NOT NULL THEN 'user'
                ELSE 'organization'
            END as poster_type
        FROM posts p
        WHERE p.id = %s
    """
    cur.execute(query, (post_id,))
    post = cur.fetchone()
    
    if not post:
        cur.close()
        return jsonify({'error': 'Post not found'}), 404

    if user_type == 'user':
        cur.execute("SELECT COUNT(*) FROM likes WHERE post_id = %s AND user_id = %s", (post_id, user_id))
    else:
        cur.execute("SELECT COUNT(*) FROM likes WHERE post_id = %s AND org_id = %s", (post_id, org_id))
    
    user_liked = cur.fetchone()[0] > 0

    cur.execute("""
        SELECT c.id, c.text, 
            COALESCE(u.first_name, o.org_name) as commenter_first_name,
            COALESCE(u.last_name, '') as commenter_last_name,
            c.user_id, c.org_id, c.created_at,
            CASE 
                WHEN c.user_id IS NOT NULL THEN 'user'
                ELSE 'organization'
            END as commenter_type
        FROM comments c
        LEFT JOIN users u ON c.user_id = u.id
        LEFT JOIN organizations o ON c.org_id = o.id
        WHERE c.post_id = %s
        ORDER BY c.created_at DESC
    """, (post_id,))
    comments = cur.fetchall()
    cur.close()

    comments_data = [
        {
            'id': comment[0],
            'text': comment[1],
            'first_name': comment[2],
            'last_name': comment[3],
            'user_id': comment[4],
            'org_id': comment[5],
            'time_ago': format_time_ago(comment[6]),
            'commenter_type': comment[7]
        } for comment in comments
    ]
    
    post_data = {
        'id': post[0],
        'image': post[1],
        'caption': post[2],
        'poster_id': post[3],
        'username': post[4],
        'profile_pic': post[5] if post[5] else 'default.jpg',
        'like_count': post[6],
        'user_liked': user_liked,
        'comments': comments_data,
        'time_ago': format_time_ago(post[7]),
        'poster_type': post[8]
    }
    
    return jsonify(post_data)

def format_time_ago(created_at):
    if not created_at:
        return ""

    if isinstance(created_at, str):
        from datetime import datetime
        created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')

    from datetime import datetime, timedelta
    now = datetime.now()
    diff = now - created_at
    if diff < timedelta(minutes=1):
        return "just now"
    elif diff < timedelta(hours=1):
        minutes = int(diff.total_seconds() / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif diff < timedelta(days=1):
        hours = int(diff.total_seconds() / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff < timedelta(days=7):
        days = diff.days
        return f"{days} day{'s' if days != 1 else ''} ago"
    else:
        return created_at.strftime('%b %d, %Y')

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session and 'org_id' not in session:
        flash("You need to be logged in to edit your profile.", "danger")
        return redirect(url_for('signin'))

    user_type = session.get('user_type', 'user')
    user_id = session.get('user_id')
    org_id = session.get('org_id')
    slogan = request.form.get('slogan')
    image_file = request.files.get('profileImage')
    username = request.form.get('username')
    cur = mysql.connection.cursor()

    if username:
        cur.execute("""
            (SELECT id FROM users WHERE username = %s AND id != %s)
            UNION
            (SELECT id FROM organizations WHERE username = %s AND id != %s)
        """, (username, user_id or 0, username, org_id or 0))
        
        if cur.fetchone():
            flash("Username already taken. Please choose another.", "danger")
            return redirect(url_for('Sys_profile'))

    if user_type == 'user':
        updates = []
        params = []
        
        if username:
            updates.append("username = %s")
            params.append(username)
        if slogan:
            updates.append("slogan = %s")
            params.append(slogan)     
        if image_file and image_file.filename:
            if allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(filepath)
                updates.append("profile_pic = %s")
                params.append(filename)      
        if updates:
            query = "UPDATE users SET " + ", ".join(updates) + " WHERE id = %s"
            params.append(user_id)
            cur.execute(query, tuple(params))
            mysql.connection.commit()
    else:
        updates = []
        params = []
        
        if username:
            updates.append("username = %s")
            params.append(username)
        if slogan:
            updates.append("mission = %s")
            params.append(slogan)
        if image_file and image_file.filename:
            if allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(filepath)
                updates.append("profile_pic = %s")
                params.append(filename)     
        if updates:
            query = "UPDATE organizations SET " + ", ".join(updates) + " WHERE id = %s"
            params.append(org_id)
            cur.execute(query, tuple(params))
            mysql.connection.commit()

    cur.close()
    flash("Profile updated successfully!", "success")
    return redirect(url_for('Sys_profile'))

@app.route('/search', methods=['GET'])
def search():
    if 'user_id' not in session and 'org_id' not in session:
        flash('Please log in first', 'danger')
        return redirect(url_for('signin'))    
    query = request.args.get('q', '')
    
    if not query:
        return render_template('search_results.html', results=[], query='')
    
    cur = mysql.connection.cursor()
    search_query = f"%{query}%"

    cur.execute("""
        (SELECT id, username, profile_pic, 'user' as type, 
         CONCAT(first_name, ' ', last_name) as display_name
         FROM users 
         WHERE (username LIKE %s OR CONCAT(first_name, ' ', last_name) LIKE %s))
        UNION
        (SELECT id, username, profile_pic, 'org' as type, org_name as display_name
         FROM organizations 
         WHERE (username LIKE %s OR org_name LIKE %s))
    """, (search_query, search_query, search_query, search_query))
    
    results = []
    for result in cur.fetchall():
        results.append({
            'id': result[0],
            'username': result[1],
            'profile_pic': result[2] if result[2] else 'default.jpg',
            'type': result[3],
            'display_name': result[4]
        })
    
    cur.close()
    return render_template('search_results.html', results=results, query=query)

@app.route('/suggest_users', methods=['GET'])
def suggest_users():
    if 'user_id' not in session and 'org_id' not in session:
        return jsonify([])
    
    query = request.args.get('q', '')
    
    if not query or len(query) < 1:
        return jsonify([])
    
    cur = mysql.connection.cursor()
    search_query = f"%{query}%"

    cur.execute("""
        (SELECT username, profile_pic, 'user' as type
        FROM users 
        WHERE username IS NOT NULL 
        AND username != ''
        AND (username LIKE %s OR CONCAT(first_name, ' ', last_name) LIKE %s))
        UNION
        (SELECT username, profile_pic, 'org' as type
        FROM organizations
        WHERE username IS NOT NULL
        AND username != ''
        AND (username LIKE %s OR org_name LIKE %s))
        LIMIT 10
    """, (search_query, search_query, search_query, search_query))
    
    suggestions = []
    for result in cur.fetchall():
        username, profile_pic, type = result
        suggestions.append({
            'username': username,
            'profile_pic': profile_pic if profile_pic else 'default.jpg',
            'type': type
        })
    
    cur.close()
    
    return jsonify(suggestions)

@app.route('/user/<username>')
def view_user_profile(username):
    if 'user_id' not in session and 'org_id' not in session:
        flash('Please log in first', 'danger')
        return redirect(url_for('signin'))
    
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, profile_pic, slogan, username, 'user' as type 
        FROM users 
        WHERE username = %s
    """, (username,))
    profile = cur.fetchone()

    if not profile:
        cur.execute("""
            SELECT id, profile_pic, mission as slogan, username, 'org' as type 
            FROM organizations 
            WHERE username = %s
        """, (username,))
        profile = cur.fetchone()
    
    if not profile:
        flash('Profile not found', 'danger')
        return redirect(url_for('Sys_profile'))
    
    profile_id, profile_pic, slogan, username, profile_type = profile

    if profile_type == 'user':
        cur.execute("""
            SELECT id, image, caption, created_at 
            FROM posts 
            WHERE user_id = %s
            ORDER BY created_at DESC
        """, (profile_id,))
    else:
        cur.execute("""
            SELECT id, image, caption, created_at 
            FROM posts 
            WHERE org_id = %s
            ORDER BY created_at DESC
        """, (profile_id,)) 
    posts = cur.fetchall()

    posts_data = [
        {
            'id': post[0],
            'image': post[1],
            'caption': post[2],
            'time_ago': format_time_ago(post[3])
        } for post in posts
    ]
    user_data = {
        'username': username,
        'profile_pic': profile_pic if profile_pic else 'uplods/default.jpg',
        'slogan': slogan if slogan else "No slogan set",
        'type': profile_type
    }

    if profile_type == 'user':
        is_own_profile = 'user_id' in session and session['user_id'] == profile_id
    else:
        is_own_profile = 'org_id' in session and session['org_id'] == profile_id
    cur.close()
    
    return render_template("view_profile.html", 
                         user_data=user_data, 
                         posts=posts_data, 
                         is_own_profile=is_own_profile)

@app.route('/check_username', methods=['POST'])
def check_username():
    username = request.json.get('username')
    if not username:
        return jsonify({'status': 'error', 'message': 'No username provided'})
    
    cur = mysql.connection.cursor()
    cur.execute("""
        (SELECT id FROM users WHERE username = %s)
        UNION
        (SELECT id FROM organizations WHERE username = %s)
    """, (username, username))
    
    existing_user = cur.fetchone()
    cur.close()
    
    if existing_user:
        if 'user_id' in session:
            cur = mysql.connection.cursor()
            cur.execute("SELECT id FROM users WHERE username = %s AND id = %s", 
                       (username, session['user_id']))
            is_own = cur.fetchone()
            cur.close()
            if is_own:
                return jsonify({'status': 'success', 'message': 'Username available'})
        if 'org_id' in session:
            cur = mysql.connection.cursor()
            cur.execute("SELECT id FROM organizations WHERE username = %s AND id = %s", 
                        (username, session['org_id']))
            is_own = cur.fetchone()
            cur.close()
            if is_own:
                return jsonify({'status': 'success', 'message': 'Username available'})
        return jsonify({'status': 'error', 'message': 'Username already taken'})
    else:
        return jsonify({'status': 'success', 'message': 'Username available'})
    
upload_folder = os.path.join(app.root_path, 'static', 'uploads')
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)



# Route for the pet meetup
@app.route('/pet_meetup')
def pet_meetup():
    user_id = session.get('user_id')
    org_id = session.get('org_id')

    if not user_id and not org_id:
        return redirect('/signin')

    return render_template('pet-meetup.html')

@app.route('/add-event', methods=['GET', 'POST'])
def add_event():
    user_id = session.get('user_id')
    org_id = session.get('org_id')
    user_type = session.get('user_type')

    if not user_id and not org_id:
        flash('Please log in to register an event', 'danger')
        return redirect(url_for('signin'))

    if request.method == 'POST':
        if user_id:
            organizer_id = user_id
            organizer_type = request.form.get('organizer_type')
            user_type = 'user'
            organizer_name = request.form.get('organizer_name')
        else:
            organizer_id = org_id
            organizer_type = request.form.get('organizer_type')
            user_type = 'organization'
            organizer_name = request.form.get('organizer_name')
        event_name = request.form.get('event_name')
        event_description = request.form.get('event_description')
        event_datetime = request.form.get('event_datetime')
        if event_datetime:
            try:
                event_date = datetime.strptime(event_datetime, '%Y-%m-%dT%H:%M')
                if event_date < datetime.now():
                    flash('Please select a future date for the event', 'danger')
                    return render_template('add-event.html')
            except ValueError:
                flash('Invalid date format', 'danger')
                return render_template('add-event.html')
        else:
            flash('Event date is required', 'danger')
            return render_template('add-event.html')
        event_duration = request.form.get('event_duration')
        event_location = request.form.get('event_location')
        google_maps_link = request.form.get('google_maps_link')
        event_type = request.form.get('event_type')
        allowed_pet_types = request.form.get('allowed_pet_types')
        pet_limit = request.form.get('pet_limit')
        max_participants = request.form.get('max_participants')
        event_poster = request.files.get('event_poster')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        sponsors = request.form.get('sponsors')
        rules = request.form.get('rules')

        upload_folder = os.path.join('static', 'uploads')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        poster_filename = None
        if event_poster and event_poster.filename:
            secure_filename_str = secure_filename(event_poster.filename)
            poster_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{secure_filename_str}"
            poster_path = os.path.join(upload_folder, poster_filename)
            event_poster.save(poster_path)
            poster_filename = os.path.join('static','uploads', poster_filename)

        try:
            cursor = mysql.connection.cursor()
            cursor.execute("""
                INSERT INTO events (organizer_id, user_type, event_name, event_description, event_datetime,
                                   event_duration, event_location, google_maps_link, event_type, allowed_pet_types,
                                   pet_limit, max_participants, event_poster, organizer_name, organizer_type, email,
                                   phone, address, sponsors, rules)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                organizer_id, user_type, event_name, event_description, event_datetime, event_duration,
                event_location, google_maps_link, event_type, allowed_pet_types, pet_limit, max_participants,
                poster_filename, organizer_name, organizer_type, email, phone, address, sponsors, rules
            ))
            mysql.connection.commit()
            flash('Your event has been submitted successfully!', 'success')
            return redirect(url_for('pet_meetup'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'An error occurred while submitting your event: {str(e)}', 'danger')
        finally:
            cursor.close()

    return render_template('add-event.html')

@app.route("/past-event")
def past_event():
    try:
        event_type = request.args.get('event_type', '')
        date_range = request.args.get('date_range', '')
        current_datetime = datetime.now()

        query = """
            SELECT id, organizer_id, event_name, event_description, event_datetime, event_duration, event_location,
                   google_maps_link, event_type, allowed_pet_types, pet_limit, max_participants, event_poster,
                   organizer_name, organizer_type, email, phone, address, sponsors, rules, status, user_type
            FROM events
            WHERE status = 'approved' AND event_datetime < %s
        """
        query_params = [current_datetime]

        if event_type:
            query += " AND event_type = %s"
            query_params.append(event_type)

        if date_range:
            current_date = current_datetime.strftime('%Y-%m-%d')
            if date_range == 'today':
                query += " AND DATE(event_datetime) = %s"
                query_params.append(current_date)
            elif date_range == 'week':
                query += " AND YEARWEEK(event_datetime, 1) = YEARWEEK(%s, 1)"
                query_params.append(current_date)
            elif date_range == 'month':
                query += " AND YEAR(event_datetime) = YEAR(%s) AND MONTH(event_datetime) = MONTH(%s)"
                query_params.append(current_date)
                query_params.append(current_date)
        query += " ORDER BY event_datetime DESC"

        cursor = mysql.connection.cursor()
        cursor.execute(query, query_params)
        meetups_data = cursor.fetchall()
        cursor.close()

        meetups_list = []
        for meetup in meetups_data:
            poster_path = meetup[12]

            meetups_list.append({
                "id": meetup[0],
                "organizer_id": meetup[1],
                "event_name": meetup[2],
                "event_description": meetup[3],
                "event_datetime": meetup[4],
                "event_duration": meetup[5],
                "event_location": meetup[6],
                "google_maps_link": meetup[7],
                "event_type": meetup[8],
                "allowed_pet_types": meetup[9],
                "pet_limit": meetup[10],
                "max_participants": meetup[11],
                "event_poster": poster_path,
                "organizer_name": meetup[13],
                "organizer_type": meetup[14],
                "email": meetup[15],
                "phone": meetup[16],
                "address": meetup[17],
                "sponsors": meetup[18],
                "rules": meetup[19],
                "status": meetup[20],
                "user_type": meetup[21]
            })
        return render_template("past-event.html", meetups=meetups_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/upcoming-event")
def upcoming_event():
    try:
        event_type = request.args.get('event_type', '')
        date_range = request.args.get('date_range', '')
        current_datetime = datetime.now()

        query = """
            SELECT e.id, e.organizer_id, e.event_name, e.event_description, e.event_datetime, 
                   e.event_duration, e.event_location, e.google_maps_link, e.event_type, 
                   e.allowed_pet_types, e.pet_limit, e.max_participants, e.event_poster,
                   e.organizer_name, e.organizer_type, e.email, e.phone, e.address, 
                   e.sponsors, e.rules, e.status, e.user_type,
                   u.first_name as user_first_name
            FROM events e
            LEFT JOIN users u ON e.organizer_id = u.id
            WHERE e.status = 'approved' AND e.event_datetime >= %s
        """
        query_params = [current_datetime]

        if event_type:
            query += " AND e.event_type = %s"
            query_params.append(event_type)

        if date_range:
            current_date = current_datetime.strftime('%Y-%m-%d')
            if date_range == 'today':
                query += " AND DATE(e.event_datetime) = %s"
                query_params.append(current_date)
            elif date_range == 'week':
                query += " AND YEARWEEK(e.event_datetime, 1) = YEARWEEK(%s, 1)"
                query_params.append(current_date)
            elif date_range == 'month':
                query += " AND YEAR(e.event_datetime) = YEAR(%s) AND MONTH(e.event_datetime) = MONTH(%s)"
                query_params.append(current_date)
                query_params.append(current_date)

        query += " ORDER BY e.event_datetime ASC"

        cursor = mysql.connection.cursor()
        cursor.execute(query, query_params)
        events_data = cursor.fetchall()

        events_list = []
        for event in events_data:
            event_id = event[0]

            cursor.execute("SELECT COUNT(*) FROM meetup_participants WHERE meetup_id = %s", (event_id,))
            participants_count = cursor.fetchone()[0]

            user_has_joined = False
            if 'user_id' in session:
                user_id = session['user_id']
                cursor.execute("SELECT id FROM meetup_participants WHERE meetup_id = %s AND user_id = %s", 
                               (event_id, user_id))
                user_has_joined = cursor.fetchone() is not None

            poster_path = event[12]

            events_list.append({
                "id": event[0],
                "organizer_id": event[1],
                "event_name": event[2],
                "event_description": event[3],
                "event_datetime": event[4],
                "event_duration": event[5],
                "event_location": event[6],
                "google_maps_link": event[7],
                "event_type": event[8],
                "allowed_pet_types": event[9],
                "pet_limit": event[10],
                "max_participants": event[11],
                "event_poster": poster_path,
                "organizer_name": event[13],
                "organizer_type": event[14],
                "email": event[15],
                "phone": event[16],
                "address": event[17],
                "sponsors": event[18],
                "rules": event[19],
                "status": event[20],
                "user_type": event[21],
                "participants_count": participants_count,
                "user_has_joined": user_has_joined
            })

        cursor.close()
        return render_template("upcoming-event.html", meetups=events_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/meetup/<int:meetup_id>")
def meetup_detail(meetup_id):
    try:
        referrer = request.referrer
        back_url = url_for("pet_meetup")
        is_past_event = False

        if referrer:
            if "past-event" in referrer:
                back_url = url_for("past_event")
                is_past_event = True
            elif "upcoming-event" in referrer:
                back_url = url_for("upcoming_event")

        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT id, organizer_id, event_name, event_description, event_datetime, event_duration, event_location,
                   google_maps_link, event_type, allowed_pet_types, pet_limit, max_participants, event_poster,
                   organizer_name, organizer_type, email, phone, address, sponsors, rules, status, user_type
            FROM events
            WHERE id = %s
        """, (meetup_id,))

        meetup_data = cursor.fetchone()
        cursor.close()

        if not meetup_data:
            flash("Meetup not found", "error")
            return redirect(url_for("pet_meetup"))

        meetup = {
            "id": meetup_data[0],
            "organizer_id": meetup_data[1],
            "event_name": meetup_data[2],
            "event_description": meetup_data[3],
            "event_datetime": meetup_data[4],
            "event_duration": meetup_data[5],
            "event_location": meetup_data[6],
            "google_maps_link": meetup_data[7],
            "event_type": meetup_data[8],
            "allowed_pet_types": meetup_data[9],
            "pet_limit": meetup_data[10],
            "max_participants": meetup_data[11],
            "event_poster": os.path.basename(meetup_data[12]) if meetup_data[12] else None,
            "organizer_name": meetup_data[13],
            "organizer_type": meetup_data[14],
            "email": meetup_data[15],
            "phone": meetup_data[16],
            "address": meetup_data[17],
            "sponsors": meetup_data[18],
            "rules": meetup_data[19],
            "status": meetup_data[20],
            "user_type": meetup_data[21]
        }
        if datetime.now() > meetup["event_datetime"]:
            is_past_event = True

        return render_template("meetup-detail.html", meetup=meetup, back_url=back_url, is_past_event=is_past_event)

    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for("pet_meetup"))
    
@app.route('/check-join-status/<int:meetup_id>')
def check_join_status(meetup_id):
    if 'user_id' not in session:
        return jsonify({'joined': False})
    
    user_id = session['user_id']
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM meetup_participants WHERE meetup_id = %s AND user_id = %s", 
                   (meetup_id, user_id))
        
        result = cur.fetchone()
        cur.close()
        
        return jsonify({'joined': result is not None})
    except Exception as e:
        if 'cur' in locals():
            cur.close()
        return jsonify({'joined': False, 'error': str(e)})
    
@app.route('/meetup/join/<int:meetup_id>', methods=['POST'])
def join_meetup(meetup_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please login as a user to join meetups'})
    
    if 'org_id' in session:
        return jsonify({'success': False, 'message': 'Organizations cannot join meetups'})
    
    user_id = session['user_id']
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT e.id, e.event_name, e.event_datetime, e.max_participants, e.organizer_id, e.user_type 
            FROM events e 
            WHERE e.id = %s AND e.status = 'approved'
        """, (meetup_id,))
        
        meetup = cur.fetchone()
        
        if not meetup:
            cur.close()
            return jsonify({'success': False, 'message': 'Event not found or not approved'})
        if meetup[5] == 'user' and meetup[4] == user_id:
            cur.close()
            return jsonify({'success': False, 'message': 'You cannot join your own event'})
        if meetup[2] < datetime.now():
            cur.close()
            return jsonify({'success': False, 'message': 'Cannot join past events'})
        cur.execute("SELECT id FROM meetup_participants WHERE meetup_id = %s AND user_id = %s", (meetup_id, user_id))
        already_joined = cur.fetchone()
        
        if already_joined:
            cur.close()
            return jsonify({'success': False, 'message': 'You have already joined this event'})
        cur.execute("SELECT COUNT(*) FROM meetup_participants WHERE meetup_id = %s", (meetup_id,))
        current_participants = cur.fetchone()[0]

        max_participants = meetup[3]
        if current_participants >= max_participants:
            cur.close()
            return jsonify({'success': False, 'message': 'Event is already full'})

        cur.execute("INSERT INTO meetup_participants (meetup_id, user_id, joined_at) VALUES (%s, %s, %s)", 
                  (meetup_id, user_id, datetime.now()))

        cur.execute("SELECT first_name, last_name FROM users WHERE id = %s", (user_id,))
        user_data = cur.fetchone()
        user_name = f"{user_data[0]} {user_data[1]}"
        organizer_id = meetup[4]  
        organizer_type = meetup[5]
        event_name = meetup[1]
        
        notification_message = f"{user_name} has joined your event: {event_name}"

        if organizer_type == 'user':
            cur.execute("""
                INSERT INTO notifications (user_id, org_id, message, type, reference_id, reference_type, created_at) 
                VALUES (%s, NULL, %s, %s, %s, %s, %s)
            """, (organizer_id, notification_message, 'join', meetup_id, 'meetup', datetime.now()))
        else:
            cur.execute("""
                INSERT INTO notifications (user_id, org_id, message, type, reference_id, reference_type, created_at) 
                VALUES (NULL, %s, %s, %s, %s, %s, %s)
            """, (organizer_id, notification_message, 'join', meetup_id, 'meetup', datetime.now()))
        mysql.connection.commit()
        cur.execute("SELECT COUNT(*) FROM meetup_participants WHERE meetup_id = %s", (meetup_id,))
        new_count = cur.fetchone()[0]
        cur.close()
        return jsonify({
            'success': True, 
            'message': 'Successfully joined event', 
            'new_count': new_count
        })
    
    except Exception as e:
        print(f"Error in join_meetup: {str(e)}")
        if 'cur' in locals():
            cur.close()
        return jsonify({'success': False, 'message': f'Error joining event: {str(e)}'})

@app.route('/meetup/unjoin/<int:meetup_id>', methods=['POST'])
def unjoin_meetup(meetup_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please login to leave this event'})
    
    user_id = session['user_id']
    
    try:
        cur = mysql.connection.cursor()

        cur.execute("""
            SELECT e.id, e.event_name, e.event_datetime, e.max_participants, e.organizer_id, e.user_type
            FROM events e 
            WHERE e.id = %s AND e.status = 'approved'
        """, (meetup_id,))
        
        meetup = cur.fetchone()
        
        if not meetup:
            cur.close()
            return jsonify({'success': False, 'message': 'Event not found or not approved'})
        if meetup[5] == 'user' and meetup[4] == user_id:
            cur.close()
            return jsonify({'success': False, 'message': 'Organizers cannot leave their own events'})
        cur.execute("SELECT id FROM meetup_participants WHERE meetup_id = %s AND user_id = %s", 
                   (meetup_id, user_id))
        participant = cur.fetchone()
        
        if not participant:
            cur.close()
            return jsonify({'success': False, 'message': 'You are not a participant in this event'})
        if meetup[2] < datetime.now():
            cur.close()
            return jsonify({'success': False, 'message': 'Cannot leave past events'})
        cur.execute("DELETE FROM meetup_participants WHERE meetup_id = %s AND user_id = %s", 
                   (meetup_id, user_id))
        cur.execute("SELECT first_name, last_name FROM users WHERE id = %s", (user_id,))
        user_data = cur.fetchone()
        user_name = f"{user_data[0]} {user_data[1]}"

        organizer_id = meetup[4]
        organizer_type = meetup[5]
        event_name = meetup[1]
        
        notification_message = f"{user_name} has left your event: {event_name}"
        if organizer_type == 'user':
            cur.execute("""
                INSERT INTO notifications (user_id, org_id, message, type, reference_id, reference_type, created_at) 
                VALUES (%s, NULL, %s, %s, %s, %s, %s)
            """, (organizer_id, notification_message, 'leave', meetup_id, 'meetup', datetime.now()))
        else:
            cur.execute("""
                INSERT INTO notifications (user_id, org_id, message, type, reference_id, reference_type, created_at) 
                VALUES (NULL, %s, %s, %s, %s, %s, %s)
            """, (organizer_id, notification_message, 'leave', meetup_id, 'meetup', datetime.now()))  
        mysql.connection.commit()
        cur.execute("SELECT COUNT(*) FROM meetup_participants WHERE meetup_id = %s", (meetup_id,))
        new_count = cur.fetchone()[0]
        
        cur.close()
        return jsonify({
            'success': True, 
            'message': 'Successfully left the event', 
            'new_count': new_count,
            'max_participants': meetup[3]
        })
    
    except Exception as e:
        print(f"Error in unjoin_meetup: {str(e)}")
        if 'cur' in locals():
            cur.close()
        return jsonify({'success': False, 'message': f'Error leaving event: {str(e)}'})

@app.route('/event/<int:event_id>/participants')
def event_participants(event_id):
    if 'user_id' not in session and 'org_id' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('signin'))
    referrer = request.referrer
    back_url = url_for("pet_meetup")
    is_past_event = False

    if referrer:
        if "past-event" in referrer:
            back_url = url_for("past_event")
            is_past_event = True 
        elif "upcoming-event" in referrer:
            back_url = url_for("upcoming_event")
    cur = mysql.connection.cursor()

    if 'user_id' in session:
        cur.execute("""
            SELECT e.*, u.first_name, u.last_name, u.email, u.phone
            FROM events e 
            LEFT JOIN users u ON e.organizer_id = u.id 
            WHERE e.id = %s
        """, (event_id,))
    else:
        cur.execute("""
            SELECT e.*, u.first_name, u.last_name, u.email, u.phone
            FROM events e 
            LEFT JOIN users u ON e.organizer_id = u.id 
            WHERE e.id = %s AND e.status = 'approved'
        """, (event_id,))
    event = cur.fetchone()
    
    if not event:
        cur.close()
        flash('Event not found or you do not have permission to view it', 'danger')
        return redirect(url_for('upcoming_event'))
    columns = [col[0] for col in cur.description]
    organizer_id_index = columns.index('organizer_id')
    status_index = columns.index('status')

    is_creator = False
    if 'user_id' in session and event[organizer_id_index] == session['user_id']:
        is_creator = True
    if not is_creator and event[status_index] != 'approved':
        cur.close()
        flash('You do not have permission to view the participants of this event', 'danger')
        return redirect(url_for('upcoming_event'))
    cur.execute("""
        SELECT u.id, u.first_name, u.last_name, u.phone, ep.joined_at 
        FROM meetup_participants ep
        JOIN users u ON ep.user_id = u.id
        WHERE ep.meetup_id = %s
        ORDER BY ep.joined_at ASC
    """, (event_id,))
    
    participants = []
    for participant in cur.fetchall():
        participants.append({
            'id': participant[0],
            'name': f"{participant[1]} {participant[2]}",
            'phone': participant[3],
            'joined_at': participant[4]
        })
    
    cur.close()
    
    return render_template('participants.html', meetup=event,
                            participants=participants, 
                            is_creator=is_creator,
                            back_url=back_url,
                            is_past_event=is_past_event)

@app.route('/event/<int:event_id>/participants/export')
def export_participants(event_id):
    if 'user_id' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('signin'))
    
    user_id = session['user_id']
    cur = mysql.connection.cursor()
    cur.execute("SELECT organizer_id, event_name FROM events WHERE id = %s", (event_id,))
    event = cur.fetchone()
    
    if not event or event[0] != user_id:
        cur.close()
        flash('You do not have permission to export this data', 'danger')
        return redirect(url_for('upcoming_event'))

    cur.execute("""
        SELECT u.id, u.first_name, u.last_name, u.email, u.phone, ep.joined_at 
        FROM meetup_participants ep
        JOIN users u ON ep.user_id = u.id
        WHERE ep.meetup_id = %s
        ORDER BY ep.joined_at ASC
    """, (event_id,))
    participants = cur.fetchall()
    cur.close()
    export_format = request.args.get('format', 'csv')
    
    if export_format == 'csv':
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(['ID', 'First Name', 'Last Name', 'Email', 'Phone', 'Joined At'])

        for participant in participants:
            writer.writerow([
                participant[0],
                participant[1],
                participant[2],
                participant[3],
                participant[4],
                participant[5].strftime('%Y-%m-%d %H:%M:%S')
            ])

        response = make_response(output.getvalue())
        response.headers['Content-Disposition'] = f'attachment; filename={event[1]}_participants.csv'
        response.headers['Content-type'] = 'text/csv'
        
        return response
    
    elif export_format == 'pdf':
        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        elements.append(Paragraph(f"Participants List - {event[1]}", styles['Title']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
        elements.append(Spacer(1, 12))

        data = [['ID', 'Name', 'Email', 'Phone', 'Joined Date']]
        
        for participant in participants:
            data.append([
                str(participant[0]),
                f"{participant[1]} {participant[2]}",
                participant[3],
                participant[4],
                participant[5].strftime('%Y-%m-%d %H:%M')
            ])

        table = Table(data, colWidths=[40, 100, 150, 100, 100])
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.orange),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        table.setStyle(table_style)   
        elements.append(table)
        doc.build(elements)

        pdf_data = buffer.getvalue()
        buffer.close()
        response = make_response(pdf_data)
        response.headers['Content-Disposition'] = f'attachment; filename={event[1]}_participants.pdf'
        response.headers['Content-type'] = 'application/pdf'
        return response
    else:
        flash('Unsupported export format', 'danger')
        return redirect(url_for('event_participants', event_id=event_id))
    


# Route for the pet adoption
@app.route('/pet_adoption')
def pet_adoption():
    user_id = session.get('user_id')
    org_id = session.get('org_id')

    if not user_id and not org_id:
        return redirect('/signin')
    return render_template('pet-adoption.html')

@app.route("/adoption-detail")
def adoption_detail():
    try:
        breed = request.args.get('breed')
        species = request.args.get('species')
        location = request.args.get('location')
        
        current_user_id = session.get('user_id', None)

        query = """
            SELECT id, owner_id, owner_type, full_name, contact_number, email, location,
                   pet_name, species, breed, age, gender, reason, pet_image, reg_certificate,
                   vaccination_records, climate_suitability, energy_level, social_compatibility,
                   status, created_at
            FROM pets
            WHERE status = 'approved'
        """
        query_params = []
        if species:
            query += " AND species = %s"
            query_params.append(species)
        if breed:
            query += " AND breed LIKE %s"
            query_params.append(f"%{breed}%")
        if location:
            query += " AND location LIKE %s"
            query_params.append(f"%{location}%")
        
        if current_user_id:
            query += " ORDER BY CASE WHEN owner_id = %s AND owner_type = 'user' THEN 0 ELSE 1 END, created_at DESC"
            query_params.append(current_user_id)
        else:
            query += " ORDER BY created_at DESC"
            
        cursor = mysql.connection.cursor()
        cursor.execute(query, query_params)
        pets_data = cursor.fetchall()

        pet_list = []
        for pet in pets_data:
            owner_id = pet[1]
            owner_type = pet[2]
            owner_name = "Unknown"
            is_owner = current_user_id and str(owner_id) == str(current_user_id) and owner_type == 'user'
            
            if owner_type == 'user':
                cursor.execute("SELECT first_name FROM users WHERE id = %s", (owner_id,))
                user_data = cursor.fetchone()
                if user_data:
                    owner_name = user_data[0]
            elif owner_type == 'organization':
                cursor.execute("SELECT org_name FROM organizations WHERE id = %s", (owner_id,))
                org_data = cursor.fetchone()
                if org_data:
                    owner_name = org_data[0]

            pet_list.append({
                "id": pet[0],
                "owner_id": pet[1],
                "owner_type": pet[2],
                "owner_name": owner_name,
                "full_name": pet[3],
                "contact_number": pet[4],
                "email": pet[5],
                "location": pet[6],
                "pet_name": pet[7],
                "species": pet[8],
                "breed": pet[9],
                "age": pet[10],
                "gender": pet[11],
                "reason": pet[12],
                "pet_image": pet[13],
                "reg_certificate": pet[14],
                "vaccination_records": pet[15],
                "climate_suitability": pet[16],
                "energy_level": pet[17],
                "social_compatibility": pet[18],
                "status": pet[19],
                "created_at": pet[20],
                "is_owner": is_owner
            })
        cursor.close()
        return render_template("adoption-detail.html", pets=pet_list, current_user_id=current_user_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/remove-pet/<int:pet_id>", methods=["POST"])
def remove_pet(pet_id):
    try:
        if 'user_id' not in session:
            flash("You need to login to remove a pet", "error")
            return redirect(url_for('login'))
        
        user_id = session['user_id']
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT owner_id, owner_type FROM pets WHERE id = %s", (pet_id,))
        pet_data = cursor.fetchone()
        
        if not pet_data:
            flash("Pet not found", "error")
            return redirect(url_for('adoption_detail'))
        
        owner_id, owner_type = pet_data
        
        if str(owner_id) != str(user_id) or owner_type != 'user':
            flash("You don't have permission to remove this pet", "error")
            return redirect(url_for('adoption_detail'))
        
        cursor.execute("UPDATE pets SET status = 'removed' WHERE id = %s", (pet_id,))
        mysql.connection.commit()
        cursor.close()
        
        flash("Pet has been successfully removed from the listing", "success")
        return redirect(url_for('adoption_detail'))
        
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('adoption_detail'))

@app.route("/pet/<int:pet_id>")
def pet_detail(pet_id):
    try:
        referrer = request.referrer
        back_url = referrer if referrer else url_for("adoption_detail")
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT id, owner_id, owner_type, full_name, contact_number, email, location,
                   pet_name, species, breed, age, gender, reason, pet_image, reg_certificate,
                   vaccination_records, climate_suitability, energy_level, social_compatibility,
                   status, created_at
            FROM pets
            WHERE id = %s AND status = 'approved'
        """, (pet_id,))
        pet_data = cursor.fetchone()

        if not pet_data:
            flash("Pet not found or not approved for adoption.", "error")
            return redirect(url_for("adoption_detail"))
        owner_id = pet_data[1]
        owner_type = pet_data[2]
        owner_name = "Unknown"
        if owner_type == 'user':
            cursor.execute("SELECT first_name FROM users WHERE id = %s", (owner_id,))
            user_data = cursor.fetchone()
            if user_data:
                owner_name = user_data[0]
        elif owner_type == 'organization':
            cursor.execute("SELECT org_name FROM organizations WHERE id = %s", (owner_id,))
            org_data = cursor.fetchone()
            if org_data:
                owner_name = org_data[0]

        pet = {
            "id": pet_data[0],
            "owner_id": pet_data[1],
            "owner_type": pet_data[2],
            "owner_name": owner_name,
            "full_name": pet_data[3],
            "contact_number": pet_data[4],
            "email": pet_data[5],
            "location": pet_data[6],
            "pet_name": pet_data[7],
            "species": pet_data[8],
            "breed": pet_data[9],
            "age": pet_data[10],
            "gender": pet_data[11],
            "reason": pet_data[12],
            "pet_image": pet_data[13],
            "reg_certificate": pet_data[14],
            "vaccination_records": pet_data[15],
            "climate_suitability": pet_data[16],
            "energy_level": pet_data[17],
            "social_compatibility": pet_data[18],
            "status": pet_data[19],
            "created_at": pet_data[20]
        }

        cursor.close()
        return render_template("adoption-detail-view.html", pet=pet, back_url=back_url)

    except Exception as e:
        app.logger.error(f"Error loading pet detail: {str(e)}")
        flash("An error occurred while loading the pet details.", "error")
        return redirect(url_for("adoption_detail"))

@app.route('/pet-selling', methods=['GET', 'POST'])
def pet_selling():
    if request.method == 'POST':
        if 'user_id' in session:
            owner_id = session['user_id']
            owner_type = 'user'
        elif 'org_id' in session:
            owner_id = session['org_id']
            owner_type = 'organization'
        else:
            flash('You must be logged in to rehome a pet!', 'danger')
            return redirect(url_for('signin'))
        full_name = request.form['full_name']
        contact_number = request.form['contact_number']
        email = request.form['email']
        location = request.form['location']
        pet_name = request.form['pet_name']
        species = request.form['species']
        breed = request.form.get('breed', '')
        age = request.form['age']
        gender = request.form['gender']
        reason = request.form['reason']
        climate_suitability = request.form['climate']
        energy_level = request.form['energy_level']
        social_compatibility = request.form['social_compatibility']
        pet_image = request.files['pet_image']
        reg_certificate = request.files['reg_certificate']
        vaccination_records = request.files['vaccination_records']
        pet_image_filename = None
        reg_certificate_filename = None
        vaccination_records_filename = None

        if pet_image:
            pet_image_filename = secure_filename(f"{uuid.uuid4()}_{pet_image.filename}")
            pet_image.save(os.path.join(app.config['UPLOAD_FOLDER'], pet_image_filename))
        if reg_certificate:
            reg_certificate_filename = secure_filename(f"{uuid.uuid4()}_{reg_certificate.filename}")
            reg_certificate.save(os.path.join(app.config['UPLOAD_FOLDER'], reg_certificate_filename))
        if vaccination_records:
            vaccination_records_filename = secure_filename(f"{uuid.uuid4()}_{vaccination_records.filename}")
            vaccination_records.save(os.path.join(app.config['UPLOAD_FOLDER'], vaccination_records_filename))
        cur = mysql.connection.cursor()
        query = """
        INSERT INTO pets 
        (owner_id, owner_type, full_name, contact_number, email, location, pet_name, species, breed, age, gender, reason, 
        pet_image, reg_certificate, vaccination_records, climate_suitability, energy_level, social_compatibility, status) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'pending')
        """
        values = (
            owner_id, owner_type, full_name, contact_number, email, location, pet_name, species, breed, age, gender,
            reason,
            pet_image_filename, reg_certificate_filename, vaccination_records_filename, climate_suitability,
            energy_level, social_compatibility
        )
        cur.execute(query, values)
        mysql.connection.commit()
        cur.close()
        flash('Your pet submission has been sent for review!', 'success')
        return redirect(url_for('pet_adoption'))
    return render_template('pet-selling.html')

@app.route('/pet-adoption-form', methods=['GET', 'POST'])
def pet_adoption_form():
    pet_id = request.args.get('pet_id', '')
    pet_details = None
    if pet_id:
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT id, pet_name, species, breed
                FROM pets
                WHERE id = %s AND status = 'approved'
            """, (pet_id,))
            result = cur.fetchone()
            if result:
                pet_details = {
                    'id': result[0],
                    'name': result[1],
                    'species': result[2],
                    'breed': result[3]
                }
            cur.close()
        except Exception as e:
            print(f"Error fetching pet details: {e}")
    
    if request.method == 'POST':
        if 'user_id' in session:
            user_id = session['user_id']
            org_id = None
        elif 'org_id' in session:
            user_id = None
            org_id = session['org_id']
        else:
            flash('Please log in to submit an adoption application.', 'danger')
            return redirect(url_for('signin'))

        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        street_address = request.form['street_address']
        apartment = request.form['apartment']
        country = request.form['country']
        state = request.form['state']
        city = request.form['city']
        postal_code = request.form['postal_code']
        home_ownership = request.form['home_ownership']
        landlord_pet_policy = request.form.get('landlord_pet_policy', '')
        pet_name_id = request.form['pet_name_id']
        reason_adoption = request.form['reason_adoption']
        prior_experience = request.form['prior_experience']
        current_pets = request.form['current_pets']
        financial_preparedness = request.form['financial_preparedness']
        emergency_plan = request.form['emergency_plan']
        contact_method = request.form['contact_method']
        visit_pet = request.form['visit_pet']
        additional_message = request.form.get('additional_message', '')

        cur = mysql.connection.cursor()
        query = """
            INSERT INTO pet_adoption_forms (
                user_id, org_id, full_name, email, phone, street_address, apartment, country, state, city, postal_code,
                home_ownership, landlord_pet_policy, pet_name_id, reason_adoption, prior_experience, current_pets,
                financial_preparedness, emergency_plan, contact_method, visit_pet, additional_message
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
        """
        values = (
            user_id, org_id, full_name, email, phone, street_address, apartment, country, state, city, postal_code,
            home_ownership, landlord_pet_policy, pet_name_id, reason_adoption, prior_experience, current_pets,
            financial_preparedness, emergency_plan, contact_method, visit_pet, additional_message
        )
        cur.execute(query, values)
        mysql.connection.commit()
        cur.execute("""
            SELECT u.email AS owner_email
            FROM pets p
            JOIN users u ON p.owner_id = u.id
            WHERE p.id = %s
        """, (pet_name_id,))
        result = cur.fetchone()
        cur.close()

        if result:
            owner_email = result[0]
            subject = "New Adoption Application Received"
            body = f"""
            A new adoption application has been submitted for your pet.

            Applicant Details:
            Name: {full_name}
            Email: {email}
            Phone: {phone}
            Address: {street_address}, {apartment}, {city}, {state}, {country} - {postal_code}
            Reason for Adoption: {reason_adoption}
            Prior Experience: {prior_experience}
            Other Pets: {current_pets}
            Financial Preparedness: {financial_preparedness}
            Emergency Plan: {emergency_plan}
            Preferred Contact Method: {contact_method}
            Willing to Visit Pet: {visit_pet}

            Additional Message:
            {additional_message}
            """
            try:
                msg = Message(subject, recipients=[owner_email], body=body)
                mail.send(msg)
            except Exception as e:
                print(f"Email sending failed: {e}")

        flash('Adoption form submitted successfully!', 'success')
        return redirect(url_for('adoption_detail'))

    return render_template('adopting-form.html', pet_id=pet_id, pet_details=pet_details)





# Route for the about us
@app.route('/about')
def about():
    return render_template('about.html')



# Routes for the kindness corner
@app.route('/kindness-corner')
def kindness_corner():
    return render_template('kindness-corner.html')

@app.route('/kindness-corner-form', methods=['GET', 'POST'])
def kindness_corner_form():
    if request.method == 'GET':
        if 'org_id' not in session:
            if 'user_id' in session:
                flash('Only verified organizations can create fundraisers.', 'warning')
                return redirect(url_for('kindness_corner'))
            else:
                flash('Please login as an organization to create a fundraiser', 'warning')
                return redirect(url_for('login'))
        return render_template('kindness-corner-form.html')

    if request.method == 'POST':
        if 'org_id' not in session:
            flash('Only verified organizations can create fundraisers.', 'warning')
            return redirect(url_for('kindness_corner'))

        try:
            title = request.form['title']
            brief_description = request.form['brief_description']
            start_date = request.form['start_date']
            end_date = request.form['end_date']

            from datetime import datetime
            today = datetime.now().date()
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()

            if start_date_obj < today:
                flash('Start date cannot be in the past.', 'danger')
                return redirect(url_for('kindness_corner_form'))
            if end_date_obj < start_date_obj:
                flash('End date must be after start date.', 'danger')
                return redirect(url_for('kindness_corner_form'))
            funds_usage = request.form['fund_usage']
            beneficiaries = request.form['beneficiaries']
            animals_helped = request.form['animals_helped']
            previous_efforts = request.form['previous_efforts']
            proof_document = request.files['proof_document']
            donation_qr = request.files['donation_qr']
            if proof_document and allowed_file(proof_document.filename):
                proof_filename = secure_filename(proof_document.filename)
                proof_document.save(os.path.join(app.config['UPLOAD_FOLDER'], proof_filename))
            else:
                flash('Invalid proof document file', 'danger')
                return redirect(url_for('kindness_corner_form'))
            if donation_qr and allowed_file(donation_qr.filename):
                qr_filename = secure_filename(donation_qr.filename)
                donation_qr.save(os.path.join(app.config['UPLOAD_FOLDER'], qr_filename))
            else:
                flash('Invalid QR code file', 'danger')
                return redirect(url_for('kindness_corner_form'))
            upi_id = request.form['upi_id']
            donor_message = request.form.get('donor_message', '')
            social_media = request.form.get('social_media', '')
            website = request.form.get('website', '')
            endorsements = request.form.get('endorsements', '')
            volunteer_info = request.form.get('volunteers', '')
            emergency_contact = request.form.get('emergency_contact', '')

            if 'user_id' in session:
                creator_id = session['user_id']
                creator_type = 'user'
            else:
                creator_id = session['org_id']
                creator_type = 'organization'
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO fundraisers (
                    creator_id, creator_type, title, brief_description,
                    start_date, end_date, funds_usage, beneficiaries, 
                    animals_helped, previous_efforts, proof_document, donation_qr, upi_id, 
                    donor_message, social_media, website, endorsements, volunteer_info, 
                    emergency_contact, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                creator_id, creator_type, title, brief_description,
                start_date, end_date, funds_usage, beneficiaries,
                animals_helped, previous_efforts, proof_filename, qr_filename, upi_id,
                donor_message, social_media, website, endorsements, volunteer_info,
                emergency_contact, 'pending'
            ))
            mysql.connection.commit()
            cur.close()

            flash('Fundraiser submitted successfully! It will be reviewed by our administrators.', 'success')
            return redirect(url_for('kindness_corner'))

        except Exception as e:
            flash(f'Error submitting fundraiser: {str(e)}', 'danger')
            return redirect(url_for('kindness_corner_form'))

@app.route("/fundraisers")
def fundraisers():
    try:
        creator_type = request.args.get('creator_type', '')
        time_left = request.args.get('time_left', '')
        current_date = datetime.now().date()

        query = """
            SELECT id, creator_id, creator_type, title, brief_description, start_date, end_date,
                   funds_usage, beneficiaries, animals_helped, previous_efforts, proof_document,
                   donation_qr, upi_id, donor_message, social_media, website, endorsements,
                   volunteer_info, emergency_contact, status, created_at
            FROM fundraisers
            WHERE status = 'approved' AND end_date >= %s AND start_date <= %s
        """
        query_params = [current_date, current_date]

        if creator_type:
            query += " AND creator_type = %s"
            query_params.append(creator_type)
        if time_left:
            if time_left == 'urgent':
                urgent_date = current_date + timedelta(days=3)
                query += " AND end_date <= %s"
                query_params.append(urgent_date)
            elif time_left == 'week':
                week_date = current_date + timedelta(days=7)
                query += " AND end_date <= %s"
                query_params.append(week_date)
            elif time_left == 'month':
                month_date = current_date + timedelta(days=30)
                query += " AND end_date <= %s"
                query_params.append(month_date)
        query += " ORDER BY end_date ASC"
        cursor = mysql.connection.cursor()
        cursor.execute(query, query_params)
        fundraisers_data = cursor.fetchall()
        fundraiser_list = []
        for fundraiser in fundraisers_data:
            creator_id = fundraiser[1]
            creator_type = fundraiser[2]
            creator_name = "Unknown"
            if creator_type == 'user':
                cursor.execute("SELECT first_name FROM users WHERE id = %s", (creator_id,))
                user_data = cursor.fetchone()
                if user_data:
                    creator_name = user_data[0]
            else:
                cursor.execute("SELECT org_name FROM organizations WHERE id = %s", (creator_id,))
                org_data = cursor.fetchone()
                if org_data:
                    creator_name = org_data[0]
            end_date = fundraiser[6]
            days_remaining = (end_date - current_date).days

            fundraiser_list.append({
                "id": fundraiser[0],
                "creator_id": fundraiser[1],
                "creator_type": fundraiser[2],
                "creator_name": creator_name,
                "title": fundraiser[3],
                "brief_description": fundraiser[4],
                "start_date": fundraiser[5],
                "end_date": fundraiser[6],
                "days_remaining": days_remaining,
                "funds_usage": fundraiser[7],
                "beneficiaries": fundraiser[8],
                "animals_helped": fundraiser[9],
                "previous_efforts": fundraiser[10],
                "proof_document": fundraiser[11],
                "donation_qr": fundraiser[12],
                "upi_id": fundraiser[13],
                "donor_message": fundraiser[14],
                "social_media": fundraiser[15],
                "website": fundraiser[16],
                "endorsements": fundraiser[17],
                "volunteer_info": fundraiser[18],
                "emergency_contact": fundraiser[19],
                "status": fundraiser[20],
                "created_at": fundraiser[21]
            })
        cursor.close()
        return render_template("fundraisers.html", fundraisers=fundraiser_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/fundraiser/<int:fundraiser_id>")
def fundraiser_detail(fundraiser_id):
    try:
        referrer = request.referrer
        back_url = referrer if referrer else url_for("fundraisers")
        current_date = datetime.now().date()

        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT id, creator_id, creator_type, title, brief_description, start_date, end_date,
                   funds_usage, beneficiaries, animals_helped, previous_efforts, proof_document,
                   donation_qr, upi_id, donor_message, social_media, website, endorsements,
                   volunteer_info, emergency_contact, status, created_at
            FROM fundraisers
            WHERE id = %s AND status = 'approved' AND start_date <= %s
        """, (fundraiser_id, current_date))
        fundraiser_data = cursor.fetchone()

        if not fundraiser_data:
            flash("Fundraiser not found, not approved, or has not started yet", "error")
            return redirect(url_for("fundraisers"))
        creator_id = fundraiser_data[1]
        creator_type = fundraiser_data[2]
        creator_name = "Unknown"
        if creator_type == 'user':
            cursor.execute("SELECT first_name FROM users WHERE id = %s", (creator_id,))
            user_data = cursor.fetchone()
            if user_data:
                creator_name = user_data[0]
        else:
            cursor.execute("SELECT org_name FROM organizations WHERE id = %s", (creator_id,))
            org_data = cursor.fetchone()
            if org_data:
                creator_name = org_data[0]
        end_date = fundraiser_data[6]
        days_remaining = (end_date - current_date).days

        fundraiser = {
            "id": fundraiser_data[0],
            "creator_id": fundraiser_data[1],
            "creator_type": fundraiser_data[2],
            "creator_name": creator_name,
            "title": fundraiser_data[3],
            "brief_description": fundraiser_data[4],
            "start_date": fundraiser_data[5],
            "end_date": fundraiser_data[6],
            "days_remaining": days_remaining,
            "funds_usage": fundraiser_data[7],
            "beneficiaries": fundraiser_data[8],
            "animals_helped": fundraiser_data[9],
            "previous_efforts": fundraiser_data[10],
            "proof_document": fundraiser_data[11],
            "donation_qr": fundraiser_data[12],
            "upi_id": fundraiser_data[13],
            "donor_message": fundraiser_data[14],
            "social_media": fundraiser_data[15],
            "website": fundraiser_data[16],
            "endorsements": fundraiser_data[17],
            "volunteer_info": fundraiser_data[18],
            "emergency_contact": fundraiser_data[19],
        }
        cursor.close()
        return render_template("fundraiser-detail.html", fundraiser=fundraiser, back_url=back_url)

    except Exception as e:
        app.logger.error(f"Error loading fundraiser details: {str(e)}")
        flash(f"An error occurred while loading the fundraiser details", "error")
        return redirect(url_for("fundraisers"))



# Routes for chatbot
@app.route('/chatbot')
def chatbot():
    user_id = session.get('user_id')
    org_id = session.get('org_id')
    if not user_id and not org_id:
        flash('Please log in to use the chat feature', 'warning')
        return redirect(url_for('signin'))
    chat_sessions = get_user_chat_sessions(user_id, org_id)
    active_session_id = request.args.get('session_id')

    if not active_session_id and chat_sessions:
        active_session_id = chat_sessions[0]['id']
    if not active_session_id:
        active_session_id = create_new_chat_session(user_id, org_id)
    messages = get_chat_messages(active_session_id)
    
    return render_template(
        'chatbot.html', 
        chat_sessions=chat_sessions,
        active_session_id=active_session_id,
        messages=messages
    )

@app.route('/new_chat', methods=['POST'])
def new_chat():
    user_id = session.get('user_id')
    org_id = session.get('org_id')
    
    if not user_id and not org_id:
        return jsonify({'status': 'error', 'message': 'User not logged in'})
    session_id = create_new_chat_session(user_id, org_id)
    
    return jsonify({
        'status': 'success',
        'session_id': session_id
    })

@app.route('/rename_chat', methods=['POST'])
def rename_chat():
    data = request.json
    session_id = data.get('session_id')
    new_name = data.get('name')
    user_id = session.get('user_id')
    org_id = session.get('org_id')
    
    if not validate_chat_ownership(session_id, user_id, org_id):
        return jsonify({'status': 'error', 'message': 'Unauthorized'})
    
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE chat_sessions 
        SET session_name = %s
        WHERE id = %s
    """, (new_name, session_id))
    mysql.connection.commit()
    cur.close()
    
    return jsonify({'status': 'success'})

@app.route('/delete_chat', methods=['POST'])
def delete_chat():
    data = request.json
    session_id = data.get('session_id')
    user_id = session.get('user_id')
    org_id = session.get('org_id')
    
    if not validate_chat_ownership(session_id, user_id, org_id):
        return jsonify({'status': 'error', 'message': 'Unauthorized'})
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM chat_sessions WHERE id = %s", (session_id,))
    mysql.connection.commit()
    cur.close()
    
    return jsonify({'status': 'success'})

@app.route('/chat', methods=['POST'])
def chat():
    global last_request_time
    current_time = time.time()
    time_since_last_request = current_time - last_request_time
    
    if time_since_last_request < MIN_REQUEST_INTERVAL:
        time.sleep(MIN_REQUEST_INTERVAL - time_since_last_request)
    
    last_request_time = time.time()
    data = request.json
    user_input = data.get('message', '')
    session_id = data.get('session_id')
    user_id = session.get('user_id')
    org_id = session.get('org_id')
    
    if not user_id and not org_id:
        return jsonify({'response': 'Please log in to use the chat feature'})
    if not validate_chat_ownership(session_id, user_id, org_id):
        return jsonify({'response': 'Unauthorized chat session'})
    if not user_input:
        return jsonify({'response': 'Empty message received'})
    
    try:
        save_message(session_id, user_input, is_bot=False)
        update_chat_session_timestamp(session_id)
        model = genai.GenerativeModel('gemini-1.5-pro')

        pet_prompt = f"""
        As a pet assistant chatbot called PawPromise, I only answer questions about dogs, cats, and other pets.
        
        User question: {user_input}
        
        If this question is not about pets, I'll politely explain that I can only discuss pet-related topics.
        Otherwise, I'll provide a helpful, concise response about pet care, health, behavior, or information.
        My responses should be friendly and conversational but brief (under 150 words).
        DO NOT use markdown formatting like asterisks for emphasis or bullet points. Use plain text only.
        """
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 300,
        }
        response = model.generate_content(
            pet_prompt,
            generation_config=generation_config
        )
        bot_response = response.text
        bot_response = bot_response.replace('***', '').replace('**', '')
        bot_response = bot_response.replace('* ', '• ')
        save_message(session_id, bot_response, is_bot=True)
        
        return jsonify({'response': bot_response})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'response': f'Sorry, I encountered an error. Please try again later.'})

def get_user_chat_sessions(user_id, org_id):
    """Get a user's chat sessions, ordered by last_updated"""
    cur = mysql.connection.cursor()
    
    if user_id:
        cur.execute("""
            SELECT id, session_name, created_at, last_updated 
            FROM chat_sessions 
            WHERE user_id = %s AND created_at > DATE_SUB(NOW(), INTERVAL 3 DAY)
            ORDER BY last_updated DESC
        """, (user_id,))
    else:
        cur.execute("""
            SELECT id, session_name, created_at, last_updated 
            FROM chat_sessions 
            WHERE org_id = %s AND created_at > DATE_SUB(NOW(), INTERVAL 3 DAY)
            ORDER BY last_updated DESC
        """, (org_id,))
    
    sessions = []
    for row in cur.fetchall():
        sessions.append({
            'id': row[0],
            'name': row[1],
            'created_at': row[2],
            'last_updated': row[3]
        })
    cur.close()
    return sessions

def create_new_chat_session(user_id, org_id):
    """Create a new chat session and return its ID"""
    cur = mysql.connection.cursor()
    
    if user_id:
        cur.execute("""
            INSERT INTO chat_sessions (user_id, session_name)
            VALUES (%s, 'New Chat')
        """, (user_id,))
    else:
        cur.execute("""
            INSERT INTO chat_sessions (org_id, session_name)
            VALUES (%s, 'New Chat')
        """, (org_id,))
    mysql.connection.commit()
    session_id = cur.lastrowid
    cur.close()
    save_message(
        session_id, 
        "Hi there! I'm your PawPromise pet assistant. I can answer questions about dogs, cats, and other pets. How can I help you today?",
        is_bot=True
    )
    return session_id

def get_chat_messages(session_id):
    """Get all messages for a chat session"""
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT message, is_bot, timestamp
        FROM chat_messages
        WHERE session_id = %s
        ORDER BY timestamp ASC
    """, (session_id,))
    
    messages = []
    for row in cur.fetchall():
        messages.append({
            'text': row[0],
            'is_bot': bool(row[1]),
            'timestamp': row[2]
        })
    
    cur.close()
    return messages

def save_message(session_id, message, is_bot):
    """Save a message to the database"""
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO chat_messages (session_id, message, is_bot)
        VALUES (%s, %s, %s)
    """, (session_id, message, is_bot))
    mysql.connection.commit()
    cur.close()

def update_chat_session_timestamp(session_id):
    """Update the last_updated timestamp for a chat session"""
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE chat_sessions
        SET last_updated = CURRENT_TIMESTAMP
        WHERE id = %s
    """, (session_id,))
    mysql.connection.commit()
    cur.close()

def validate_chat_ownership(session_id, user_id, org_id):
    """Check if a user owns a chat session"""
    if not session_id:
        return False
    cur = mysql.connection.cursor()
    
    if user_id:
        cur.execute("""
            SELECT id FROM chat_sessions
            WHERE id = %s AND user_id = %s
        """, (session_id, user_id))
    else:
        cur.execute("""
            SELECT id FROM chat_sessions
            WHERE id = %s AND org_id = %s
        """, (session_id, org_id)) 
    result = cur.fetchone()
    cur.close()
    
    return result is not None

@app.route('/get_chat_messages')
def get_chat_messages_api():
    session_id = request.args.get('session_id')
    user_id = session.get('user_id')
    org_id = session.get('org_id')
    
    if not validate_chat_ownership(session_id, user_id, org_id):
        return jsonify([])
    messages = get_chat_messages(session_id)
    return jsonify(messages)

if __name__ == '__main__':
    app.run(port=5000,debug=True)