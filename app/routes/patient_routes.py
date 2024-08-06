from flask import Blueprint, request, jsonify
from app import db
from app.models import Patient
from flask_jwt_extended import jwt_required, get_jwt_identity

patient_bp = Blueprint('patient_bp', __name__)


@patient_bp.route('/', methods=['POST'])
@jwt_required()
def add_patient():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    date_of_birth = data.get('date_of_birth')
    gender = data.get('gender')
    contact_info = data.get('contact_info')
    address = data.get('address')
    medical_history = data.get('medical_history')

    new_patient = Patient(
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date_of_birth,
        gender=gender,
        contact_info=contact_info,
        address=address,
        medical_history=medical_history
    )

    db.session.add(new_patient)
    db.session.commit()

    return jsonify({"msg": "Patient added successfully"}), 201


@patient_bp.route('/', methods=['GET'])
@jwt_required()
def get_patients():
    patients = Patient.query.all()
    patients_list = [{
        "patient_id": patient.patient_id,
        "first_name": patient.first_name,
        "last_name": patient.last_name,
        "date_of_birth": patient.date_of_birth,
        "gender": patient.gender,
        "contact_info": patient.contact_info,
        "address": patient.address,
        "medical_history": patient.medical_history
    } for patient in patients]

    return jsonify(patients_list), 200


@patient_bp.route('/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    patient_data = {
        "patient_id": patient.patient_id,
        "first_name": patient.first_name,
        "last_name": patient.last_name,
        "date_of_birth": patient.date_of_birth,
        "gender": patient.gender,
        "contact_info": patient.contact_info,
        "address": patient.address,
        "medical_history": patient.medical_history
    }

    return jsonify(patient_data), 200


@patient_bp.route('/<int:patient_id>', methods=['PUT'])
@jwt_required()
def update_patient(patient_id):
    data = request.get_json()
    patient = Patient.query.get_or_404(patient_id)

    patient.first_name = data.get('first_name', patient.first_name)
    patient.last_name = data.get('last_name', patient.last_name)
    patient.date_of_birth = data.get('date_of_birth', patient.date_of_birth)
    patient.gender = data.get('gender', patient.gender)
    patient.contact_info = data.get('contact_info', patient.contact_info)
    patient.address = data.get('address', patient.address)
    patient.medical_history = data.get('medical_history', patient.medical_history)

    db.session.commit()

    return jsonify({"msg": "Patient updated successfully"}), 200


@patient_bp.route('/<int:patient_id>', methods=['DELETE'])
@jwt_required()
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()

    return jsonify({"msg": "Patient deleted successfully"}), 200
