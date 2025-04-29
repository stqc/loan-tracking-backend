from configs import db
from configs.utils.date_utils import validate_past_date

class LoanModel(db.Model):
    __tablename__ = "loans"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    term = db.Column(db.Integer, nullable=False) #in months
    startDate = db.Column(db.Date, nullable=False)
    emi = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)

    def __init__(self, user_id, amount, interest_rate, term,date):

        self.user_id = user_id
        self.amount = float(amount)
        self.interest_rate = float(interest_rate)
        self.term = int(term)
        self.startDate = validate_past_date(date)
        self.emi,self.total_amount = self.calculate_emi(interest_rate/100,term,amount)

    @staticmethod
    def calculate_emi(interest_rate,term,amount):

        time_in_years = term / 12
        interest= amount*interest_rate*time_in_years
        total_amount = amount + interest
        emi = total_amount / term
        return emi, total_amount