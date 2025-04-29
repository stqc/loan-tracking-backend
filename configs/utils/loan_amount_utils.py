from datetime import datetime
from dateutil.relativedelta import relativedelta

def calculate_remaining_amount(term,total_amount,emi,start_date):

    months_passed = (datetime.now().date() - start_date).days // 30
    remaining_months = term - months_passed
    
    if remaining_months <= 0:
        return 0, 0
    
    remaining_amount = total_amount - (emi * months_passed)

    return remaining_amount, remaining_months

def get_upcoming_emi_dates(start_date, term):

    months_passed = (datetime.now().date() - start_date).days // 30
    if months_passed >= term:
        return []
    
    remaining_months = term - months_passed

    if remaining_months <= 0:
        return []

    last_paid_date = start_date + relativedelta(months=months_passed)

    upcoming_dates = []
    for i in range(remaining_months):
        upcoming_dates.append(last_paid_date + relativedelta(months=i+1))
    return upcoming_dates