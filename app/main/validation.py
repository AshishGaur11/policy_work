def validate_inputs(dob, gender, sum_assured, modal_premium, premium_frequency, pt, ppt):
    # Implement input validation logic here
    if pt < 10 or pt > 20:
        return False
    if ppt < 5 or ppt > 10:
        return False
    if modal_premium < 10000 or modal_premium > 50000:
        return False
    if pt <= ppt:
        return False
    if premium_frequency not in ['Yearly', 'Half-Yearly', 'Monthly']:
        return False
    if sum_assured < 50000 or sum_assured > 5000000:
        return False
    # Add more validation checks as needed
    return True