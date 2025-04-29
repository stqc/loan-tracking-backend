from datetime import datetime, timedelta

def parse_date(date_str):
        try:
            formatted_date = datetime.strptime(date_str, '%d-%m-%Y').date()
        except:
            raise ValueError("Date of birth must be in the format DD-MM-YYYY")
        
        return formatted_date

def check_age(date_str):       
    formatted_date = parse_date(date_str)
    today = datetime.now().date()

    if formatted_date >today:
            raise ValueError("Date of birth cannot be in the future")
    if formatted_date >= today - timedelta(days=365*18):
            raise ValueError("User must be at least 18 years old")  

    return formatted_date

def validate_past_date(date_str):
        formatted_date = parse_date(date_str)
        today = datetime.now().date()
        
        if formatted_date > today:
                raise ValueError("Date cannot be in the future")
        
        return formatted_date