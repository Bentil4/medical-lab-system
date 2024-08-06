from flask import Blueprint, request, jsonify
from app import db, bcrypt
from app.models import User
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or not role:
        return jsonify({"msg": "Missing required fields"}), 400

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"msg": "User already exists"}), 400

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password_hash=password_hash, role=role)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Missing required fields"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.user_id)
    refresh_token = create_refresh_token(identity=user.user_id)

    return jsonify(access_token=access_token, refresh_token=refresh_token), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)

    return jsonify(access_token=access_token), 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # JWTs are stateless, so no action is required to "logout" a user on the server side.
    return jsonify({"msg": "User logged out successfully"}), 200
