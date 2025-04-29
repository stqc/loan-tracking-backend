import re

def validate_pan_format(pan):
    pattern = r'^[A-Z]{5}\d{4}[A-Z]$'
    
    if not bool(re.match(pattern, pan.upper())):
        raise ValueError("Invalid PAN format")
    
def validate_aadhar_format(aadhar):
    pattern = r'^\d{12}$'

    if not bool(re.match(pattern, aadhar)):
        raise ValueError("Invalid Aadhar format")
    
def validate_gst_format(gst):
    pattern = r'^\d{2}[A-Z]{5}\d{4}[A-Z][A-Z\d]Z[A-Z\d]$'
    
    if not bool(re.match(pattern, gst.upper())):
        raise ValueError("Invalid GST format")
    
def validate_udyam_format(udyam):
    pattern = r'^UDYAM[A-Z]{2}\d{9}$'
    
    if not bool(re.match(pattern, udyam.upper())):
        raise ValueError("Invalid UDYAM format")