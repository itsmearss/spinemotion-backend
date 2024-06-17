from app import db, jwt, mail
import secrets
from flask_mail import Mail, Message
from argon2 import PasswordHasher
from flask import jsonify, url_for, render_template, make_response

def get_profile(email):
    try:
        user = db.db.users.find_one({"email": email})
    
        if not user:
            return {
                'message': 'Pengguna tidak ditemukan'
            }, 404
            
        return {
            'message': 'success',
            'data': {
                'id': str(user["_id"]),
                'fullname': user["fullname"],
                'email': user["email"],
                'no_hp': user["no_hp"],
                'photo': user["photo"],
            }
        }, 200
    
    except Exception as e:
        return {'message' : f"Error {e}"}, 500
    

def forgot_password_user(data):
    try:
        email = data["email"]
    
        user = db.db.users.find_one({"email": email})
        
        if not user:
            return {
                "message": "Email tidak terdaftar"
            }, 404
        
        verification_token = secrets.token_urlsafe(32)
        
        token = {
            "email": email,
            "token": verification_token
        }
        
        db.db.token.insert_one(token)
        
        confirmation_url = url_for('user.reset_password_view', token=verification_token, _external=True)
        
        msg = Message(subject="Reser Your Password - SpineMotion", sender="spinemotionapp@gmail.com", recipients=[email])
        msg.html = render_template("reset-password.html", url=confirmation_url)
        
        mail.send(msg)
        
        return {'message' : "Berhasil meminta reset password, silahkan cek email"}, 200
    
    except Exception as e:
        return {'message' : f"Error {e}"}, 500
    
def reset_password_view_user(token):
    try:
        token = db.db.token.find_one({"token": token})
        if not token:
            return {
                'message':'Token not found'
            }, 404
        
        email = token["email"]
        user = db.db.users.find_one({"email": email})
        if not user:
            return {
                "message": "User not found"
            }, 404
        
        response = make_response(render_template('form-reset-password.html', email=user["email"]), 200)
        response.headers["Content-Type"] = "text/html"
        return response
    except Exception as e:
        return {
            "message": f"Error {e}"
        }, 500

def reset_password_user(password, confirm_password, email):
    try:
        user = db.db.users.find_one({"email": email})
        
        if not user:
            return {
                "message": "Pengguna tidak ditemukan"
            }, 404
            
        if password != confirm_password:
            return {
                "message": "Password tidak sesuai"
            }
        
        new_password = PasswordHasher().hash(password)
        
        update_password = {
            "password": new_password
        }
        
        try:
            db.db.users.update_one({"email": email}, {"$set": update_password})
            response = make_response(render_template('response.html', success=True, message='Password has been reset successfully'), 200)
            response.headers['Content-Type'] = 'text/html'
            return response
        
        except:    
            response = make_response(render_template('response.html', success=False, message='Reset password failed'), 400)
            response.headers['Content-Type'] = 'text/html'
            return response
    except Exception as e:
        return {
            "message": f"Error {e}"
        }, 500