from configs import db
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, set_access_cookies,unset_jwt_cookies,create_refresh_token,set_refresh_cookies,jwt_required,get_jwt
from ..models.user_model import UserModel

user_login_sign_up = Blueprint('user_login_sign_up', __name__)

@user_login_sign_up.route('/sign_up', methods=['POST'])
def user_signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    dob = data.get('dob')
    pan = data.get('pan')
    aadhar = data.get('aadhar')
    gst = data.get('gst')
    udyam = data.get('udyam')
    
    if not username or not password or not dob or not pan or not aadhar or not gst or not udyam:
        return jsonify({"msg": "Missing required fields"}), 400

    try:
        with db.session.begin():
            new_user = UserModel(
                username=username,
                password=password,
                dob=dob,
                pan=pan,
                aadhar=aadhar,
                gst=gst,
                udyam=udyam
            )
            db.session.add(new_user)

    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error creating user", "error": str(e)}), 400

    return jsonify({"msg": "User created successfully"}), 201

@user_login_sign_up.route('/login', methods=['POST'])
def user_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Missing required fields"}), 400

    user = UserModel.query.filter_by(username=username).first()

    if user and user.check_password(password):
        
        access_token = create_access_token(identity=user.username,additional_claims={"user_id": user.id})
        refresh_token = create_refresh_token(identity=user.username,additional_claims={"user_id": user.id})
        
        resp = jsonify({"msg": "Login successful"})
        
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        
        return resp, 200
    else:
        return jsonify({"msg": "Invalid credentials"}), 401
    
@user_login_sign_up.route('/logout', methods=['POST'])
def user_logout():
    resp = jsonify({"msg": "Logout successful"})
    unset_jwt_cookies(resp)
    return resp, 200

@user_login_sign_up.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    
    user = get_jwt()
    user_id = user['user_id']
    access_token = create_access_token(identity=user['sub'],additional_claims={"user_id": user_id})
    resp = jsonify({"msg": "Token refreshed"})
    set_access_cookies(resp, access_token)
    
    return resp, 200
    
