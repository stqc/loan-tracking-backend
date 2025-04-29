from configs import db
from werkzeug.security import generate_password_hash, check_password_hash
from configs.utils.date_utils import check_age
import configs.utils.format_validation as format_validation


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    pan = db.Column(db.String(10), unique=True, nullable=False)
    aadhar = db.Column(db.String(12), unique=True, nullable=False)
    gst = db.Column(db.String(15), unique=True, nullable=False)
    udyam = db.Column(db.String(16), unique=True, nullable=False)
    loans = db.relationship('LoanModel',backref='users')

    def __init__(self,username, password, dob,pan,aadhar,gst,udyam):

        format_validation.validate_pan_format(pan)
        format_validation.validate_aadhar_format(aadhar)
        format_validation.validate_gst_format(gst)
        format_validation.validate_udyam_format(udyam)

        self.username = username
        self.password = generate_password_hash(password)
        self.dob = check_age(dob)
        self.pan = pan.upper()
        self.aadhar = aadhar
        self.gst = gst.upper()
        self.udyam = udyam.upper()

    def check_password(self, password):
        return check_password_hash(self.password, password)
