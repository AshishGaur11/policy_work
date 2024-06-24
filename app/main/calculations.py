from datetime import date

def calculate_projected_benefits(policy):
    premium = policy.modal_premium * policy.pt
    dob_year = policy.dob.year
    age = date.today().year - dob_year
    projected_benefits = policy.sum_assured * (1 + (premium / policy.sum_assured) ** policy.pt)
    return premium, age, projected_benefits
