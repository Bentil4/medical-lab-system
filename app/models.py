from app import db
from datetime import datetime, timezone
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
class Patient(db.Model):
    patient_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    contact_info = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    medical_history = db.Column(db.Text, nullable=True)

class LabTechnician(db.Model):
    technician_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    contact_info = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50), nullable=False)
class Test(db.Model):
    test_id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    normal_range = db.Column(db.String(50), nullable=False)
    unit = db.Column(db.String(20), nullable=False)

class Sample(db.Model):
    sample_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('test_order.order_id'), nullable=False)
    sample_type = db.Column(db.String(50), nullable=False)
    collection_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    collected_by = db.Column(db.Integer, db.ForeignKey('lab_technician.technician_id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    storage_location = db.Column(db.String(100), nullable=True)
