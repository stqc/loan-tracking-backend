from configs import db
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required,get_jwt
from ..models.loans_model import LoanModel
from ..models.user_model import UserModel
from ..utils.loan_amount_utils import calculate_remaining_amount, get_upcoming_emi_dates

loan_interactions = Blueprint('loan_interactions', __name__)

@loan_interactions.route('/submit_loan_info', methods=['POST'])
@jwt_required()
def submit_loan():

    data = request.get_json()
    user = get_jwt()
    user_id = user['user_id']
    loan_amount = data.get('amount')
    interest_rate = data.get('interest_rate')
    term = data.get('term')
    start_date = data.get('startDate')

    if not loan_amount or not interest_rate or not term or not start_date:
        return jsonify({"msg": "Missing required fields"}), 400
    
    try:
        with db.session.begin():
            new_loan = LoanModel(
                user_id=user_id,
                amount=loan_amount,
                interest_rate=interest_rate,
                term=term,
                date=start_date
            )
            db.session.add(new_loan)

    except Exception as e:

        db.session.rollback()
        return jsonify({"msg": "Error submitting loan information", "error": str(e)}), 400

    return jsonify({"msg": "Loan information submitted successfully"}), 200

@loan_interactions.route('/get_all_loans', methods=['GET'])
@jwt_required()
def get_all_loans():
    user = get_jwt()
    user_id = user['user_id']
    loans = db.session.execute(
        db.select(LoanModel).filter_by(user_id=user_id)
    ).scalars().all()
    
    if not loans:
        return jsonify({"loans": []}), 404
    
    parsed_loans = []
    for loan in loans:
        parsed_loan = {
            "id": loan.id,
            "amount": loan.amount,
            "interest_rate": loan.interest_rate,
            "term": loan.term,
            "startDate": loan.startDate,
            "emi": loan.emi,
            "total_amount": loan.total_amount,
        }
        parsed_loans.append(parsed_loan)

    return jsonify({"loans": parsed_loans}), 200


@loan_interactions.route('/get_loan_info/<id>', methods=['GET'])
@jwt_required()
def get_loan_info(id):

    user = get_jwt()
    user_id = user['user_id']
   
    loan_info = db.session.execute(
        db.select(LoanModel).filter_by(user_id=user_id, id=id)
    ).scalar_one_or_none()

    if not loan_info:
        return jsonify({"msg": "No loan information found"}), 404

    remaining_amount, remaining_months = calculate_remaining_amount(
        loan_info.term,
        loan_info.total_amount,
        loan_info.emi,
        loan_info.startDate
    )

    upcoming_dates = get_upcoming_emi_dates(
        loan_info.startDate,
        loan_info.term
    )

    parsed_loan = {
        "id": loan_info.id,
        "amount": loan_info.amount,
        "interest_rate": loan_info.interest_rate,
        "term": loan_info.term,
        "startDate": loan_info.startDate,
        "emi": loan_info.emi,
        "total_amount": loan_info.total_amount,
        "remaining_amount": remaining_amount,
        "remaining_months": remaining_months,
        "next_payment_dates": upcoming_dates
    }

    return jsonify({f"loan-info": parsed_loan}), 200

