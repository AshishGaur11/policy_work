from flask import render_template, redirect, url_for, flash, request
from app.main.models import Policy
from app.main.calculations import calculate_projected_benefits
from app.main.validation import validate_inputs
from app import db
from app.main import main_bp
from datetime import datetime
from flask_login import login_required, current_user  # Import login_required

@main_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        sum_assured = request.form.get('sum_assured')
        modal_premium = request.form.get('modal_premium')
        premium_frequency = request.form.get('premium_frequency')
        pt = request.form.get('pt')
        ppt = request.form.get('ppt')

        # Log form data
        #print(f"Form data: dob={dob}, gender={gender}, sum_assured={sum_assured}, modal_premium={modal_premium}, premium_frequency={premium_frequency}, pt={pt}, ppt={ppt}")

        # Check if required fields are present
        if not dob or not gender or not sum_assured or not modal_premium or not premium_frequency or not pt or not ppt:
            flash('All fields are required. Please check your entries and try again.', 'danger')
            return redirect(url_for('main.index'))

        # Convert and validate numeric inputs
        try:
            dob = datetime.strptime(dob, '%Y-%m-%d').date()
            sum_assured = int(sum_assured)
            modal_premium = int(modal_premium)
            pt = int(pt)
            ppt = int(ppt)
        except ValueError:
            flash('Invalid input for numeric fields. Please enter valid integers.', 'danger')
            return redirect(url_for('main.index'))

        # Validate inputs
        if validate_inputs(dob, gender, sum_assured, modal_premium, premium_frequency, pt, ppt):
            policy = Policy(dob=dob, gender=gender, sum_assured=sum_assured, modal_premium=modal_premium,
                            premium_frequency=premium_frequency, pt=pt, ppt=ppt)
            db.session.add(policy)
            db.session.commit()

            premium, age, projected_benefits = calculate_projected_benefits(policy)
            return render_template('main/illustration.html', premium=premium, age=age, projected_benefits=projected_benefits)
        else:
            return redirect(url_for('main.index'))

    return render_template('main/index.html')



'''Form data: dob=1980-07-09, gender=M, sum_assured=1500000, modal_premium=50000, premium_frequency=Monthly, pt=15, ppt=6
[2024-06-24 10:52:03,650]'''