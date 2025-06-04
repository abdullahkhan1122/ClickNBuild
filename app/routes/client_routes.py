from flask import Blueprint, render_template, session, redirect, url_for, flash, request, current_app as app, jsonify
import os
from werkzeug.utils import secure_filename
from sqlalchemy import text
from app import db
from app.models import User, Project, Client, ProjectImage,Builder,Bid, Review, Contact,Payment
from app.models import VendorMarketplace
from flask_login import login_required
import stripe


client_bp = Blueprint('client', __name__)

# ---------- CLIENT ROUTES ------------
@client_bp.route('/')
def websiteHomepage():

    # Get client reviews with user and project info
    client_reviews = db.session.query(Review, User.username)\
        .join(User, Review.reviewer_id == User.user_id)\
        .filter(Review.role == 'client')\
        .order_by(Review.created_at.desc())\
        .limit(5)\
        .all()
    
    # Format the data for template
    reviews = [{
        'comment': review.comment,
        'username': username,
        'rating': review.rating,
        'created_at': review.created_at
    } for review, username in client_reviews]
    
    builders = Builder.query.join(User).add_columns(
        User.username, User.email, User.phone, User.role,
        Builder.rating, Builder.total_projects, Builder.total_earning
    ).all()
    return render_template('client/main_website_page.html', builders=builders , reviews=reviews)

@client_bp.route('/contact', methods=['POST'])
def contact_form():
    name = request.form.get('name')
    email = request.form.get('email')
    description = request.form.get('description')

    if name and email and description:
        new_contact = Contact(name=name, email=email, description=description)
        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for('client.websiteHomepage'))

    else:

      return redirect(url_for('client.websiteHomepage'))

@client_bp.route('/signup-form')
def signupForm():
    return render_template('auth/signup_form.html')

@client_bp.route('/client-homepage')
def clientHomepage():
    products = VendorMarketplace.query.limit(3).all()  # Get only 4 products
    return render_template('client/homepage.html', products=products)


@client_bp.route('/dashboard')
def dashboard():
    user_email = session.get('user_email')
    user_role = session.get('role')

    if not user_email or not user_role:
        flash('Please login first.', 'danger')
        return redirect(url_for('auth.signup'))

    if user_role != 'Client':
        flash('Unauthorized access. Only Clients allowed.', 'danger')
        return redirect(url_for('auth.signup'))

    user = db.session.query(User).filter_by(email=user_email).first()
    client = db.session.query(Client).filter_by(user_id=user.user_id).first()

    if not client:
        flash('Client profile not found.', 'danger')
        return redirect(url_for('auth.signup'))

    projects = db.session.query(Project).filter(Project.status.in_(['Open', 'Pending', 'Active', 'Completed'])).all()

    active_count = len([p for p in projects if p.status == 'Open'])
    pending_count = len([p for p in projects if p.status == 'Pending'])
    completed_count = len([p for p in projects if p.status == 'Completed'])
    total_budget = sum([p.budget for p in projects])

    return render_template('client/dashboard.html',
                           user=user,
                           projects=projects,
                           active_count=active_count,
                           pending_count=pending_count,
                           completed_count=completed_count,
                           total_budget=total_budget)



@client_bp.route('/marketplace')
def marketplace():
    products = VendorMarketplace.query.all()
    return render_template('client/marketplace.html', products=[p.to_dict() for p in products])



@client_bp.route('/profile')
def profile():
    user_email = session.get('user_email')

    if not user_email:
        flash('Please login first.', 'danger')
        return redirect(url_for('auth.signup'))

    # Fetch user
    user = db.session.query(User).filter_by(email=user_email).first()

    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('auth.signup'))

    # Fetch client profile
    client = db.session.query(Client).filter_by(user_id=user.user_id).first()

    if not client:
        flash('Client profile not found.', 'danger')
        return redirect(url_for('auth.signup'))

    return render_template('client/profile.html', user=user, client=client)


@client_bp.route('/my_projects')
def my_projects():
    user_email = session.get('user_email')

    if not user_email:
        flash('Please login first.', 'danger')
        return redirect(url_for('auth.signup'))

    user = db.session.query(User).filter_by(email=user_email).first()

    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('auth.signup'))

    client = db.session.query(Client).filter_by(user_id=user.user_id).first()

    if not client:
        flash('Client profile not found.', 'danger')
        return redirect(url_for('auth.signup'))

    # Get projects with builder information if assigned
    projects_with_builders = db.session.query(Project, Builder, User)\
        .outerjoin(Builder, Project.assigned_to == Builder.builder_id)\
        .outerjoin(User, Builder.user_id == User.user_id)\
        .filter(Project.client_id == client.client_id)\
        .all()

    # Get accepted bids for each project
    project_bids = {}
    for project, builder, builder_user in projects_with_builders:
        if project.assigned_to:
            bid = Bid.query.filter_by(
                project_id=project.project_id,
                builder_id=project.assigned_to,
                status='Accepted'
            ).first()
            if bid:
                project_bids[project.project_id] = bid

    user_id = session['user_id']
    reviews = Review.query.filter_by(reviewer_id=user_id).all()

    return render_template('client/my_projects.html', 
                         projects_with_builders=projects_with_builders,
                         project_bids=project_bids,
                         reviews=reviews)

from app.models import User, Project, Builder, Bid

@client_bp.route('/proposals')
def proposals():
    user_email = session.get('user_email')
    user = db.session.query(User).filter_by(email=user_email).first()
    client = db.session.query(Client).filter_by(user_id=user.user_id).first()

    bids = db.session.query(Bid, Builder, User, Project)\
        .join(Builder, Bid.builder_id == Builder.builder_id)\
        .join(User, Builder.user_id == User.user_id)\
        .join(Project, Bid.project_id == Project.project_id)\
        .filter(Project.client_id == client.client_id)\
        .all()

    return render_template('client/proposals.html', bids=bids)



@client_bp.route('/reviews')
def reviews():
    if 'user_id' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('auth.signup'))

    user = User.query.get(session['user_id'])
    client = Client.query.filter_by(user_id=user.user_id).first()

    if not client:
        flash('Client profile not found.', 'danger')
        return redirect(url_for('auth.signup'))

    # Get reviews where the current user is the reviewee and the reviewer is a builder
    reviews = db.session.query(Review, Project, User)\
        .join(Project, Review.project_id == Project.project_id)\
        .join(User, Review.reviewer_id == User.user_id)\
        .filter(Review.reviewee_id == user.user_id)\
        .filter(Review.role == 'builder')\
        .all()

    return render_template('client/reviews.html', reviews=reviews)

@client_bp.route('/support')
def support():
    if 'user_email' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('auth.signup'))
    return render_template('client/support.html')

@client_bp.route('/submit_support_request', methods=['POST'])
def submit_support_request():
    if 'user_email' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('auth.signup'))
        
    subject = request.form.get('subject')
    message = request.form.get('message')
    
    # Here you can add logic to save the support request to a database
    # or send it via email
    
    flash('Your support request has been submitted successfully!', 'success')
    return redirect(url_for('client.support'))

@client_bp.route('/newproject', methods=['GET', 'POST'])
def addNewProject():
    if request.method == 'POST':
        title = request.form.get('title')
        project_type = request.form.get('projectType')
        location = request.form.get('location')
        description = request.form.get('description')
        budget = request.form.get('budget')
        timeline = request.form.get('timeline')

        user_email = session.get('user_email')
        if not user_email:
            flash('Please login first.', 'danger')
            return redirect(url_for('auth.signup'))

        client = db.session.query(Client).join(User, Client.user_id == User.user_id).filter(User.email == user_email).first()

        if not client:
            flash('Client profile not found. Please complete registration.', 'danger')
            return redirect(url_for('auth.signup'))

        # Save main project
        new_project = Project(
            client_id=client.client_id,
            title=title,
            description=description,
            project_type=project_type,
            budget=int(budget),
            location=location,
            timeline=int(timeline),
            status="Pending"
        )
        db.session.add(new_project)
        db.session.commit()

        # Save uploaded images
        files = request.files.getlist('project_images')
        upload_folder = os.path.join(app.root_path, 'static/uploads')

        for file in files:
            if file and file.filename:
                filename = secure_filename(file.filename)
                save_path = os.path.join(upload_folder, filename)
                file.save(save_path)

                new_image = ProjectImage(
                    project_id=new_project.project_id,
                    image_path='uploads/' + filename
                )
                db.session.add(new_image)

        db.session.commit()

        flash('Project and images saved successfully!', 'success')
        return redirect(url_for('client.my_projects'))

    return render_template('client/new_project.html')


#/*----------------------UPDATE PROFILE NEW------------------------------*/

@client_bp.route('/update-profile', methods=['POST'])
def update_profile():
    if 'user_email' not in session:
        flash('You must be logged in to update profile.', 'danger')
        return redirect(url_for('auth.signup'))

    user_email = session['user_email']
    user = User.query.filter_by(email=user_email).first()
    client = Client.query.filter_by(user_id=user.user_id).first()

    if user and client:
        # Update User table
        new_phone = request.form.get('phone')
        if new_phone:
            user.phone = new_phone

        # Update Client table
        client.location = request.form.get('location')
        client.company_name = request.form.get('company_name')
        client.about = request.form.get('about')

        # Save uploaded profile picture properly
        if 'profile_picture' in request.files:
            profile_picture = request.files['profile_picture']
            if profile_picture.filename != '':
                filename = secure_filename(profile_picture.filename)
                
                upload_folder = os.path.join(app.root_path, 'static', 'uploads')
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)

                upload_path = os.path.join(upload_folder, filename)
                profile_picture.save(upload_path)

                client.profile_picture = f'uploads/{filename}'

        db.session.commit()
        flash('Profile updated successfully!', 'success')
    else:
        flash('User or Client profile not found.', 'danger')

    return redirect(url_for('client.profile'))

@client_bp.route('/client/accept-bid/<int:bid_id>', methods=['POST'])
def accept_bid(bid_id):
    bid = Bid.query.get(bid_id)
    if not bid:
        flash('Bid not found.', 'danger')
        return redirect(url_for('client.proposals'))

    project = Project.query.get(bid.project_id)
    if not project:
        flash('Project not found.', 'danger')
        return redirect(url_for('client.proposals'))

    # Mark the bid and project as accepted/active
    bid.status = 'Accepted'
    project.assigned_to = bid.builder_id
    project.status = 'Active'

 
    existing_payment = Payment.query.filter_by(project_id=project.project_id).first()
    if not existing_payment:
        payment = Payment(
            project_id=project.project_id,
            client_id=project.client_id,
            amount_due=bid.estimated_cost,
            status='Pending'
        )
        db.session.add(payment)

    db.session.commit()
    flash('Bid accepted and payment created successfully.', 'success')
    return redirect(url_for('client.proposals'))


@client_bp.route('/client/reject-bid/<int:bid_id>', methods=['POST'])
def reject_bid(bid_id):
    bid = Bid.query.get(bid_id)
    if bid:
        bid.status = 'Rejected'
        db.session.commit()
        flash('Bid rejected.', 'info')
    else:
        flash('Bid not found.', 'danger')
    return redirect(url_for('client.proposals'))

@client_bp.route('/client/complete-project/<int:project_id>', methods=['POST'])
def complete_project(project_id):
    project = Project.query.get(project_id)
    if project:
        if project.client_completed:
            flash('You have already marked this project as complete.', 'info')
        else:
            project.client_completed = True
            if project.builder_completed:
                project.status = 'Completed'
                # Update the corresponding bid status to 'Completed'
                bid = Bid.query.filter_by(project_id=project_id, builder_id=project.assigned_to).first()
                if bid:
                    bid.status = 'Completed'
            db.session.commit()
            flash('You have marked this project as complete. Waiting for the builder.' if not project.builder_completed else 'Project marked as completed!', 'success')
    else:
        flash('Project not found.', 'danger')
    return redirect(url_for('client.my_projects'))

@client_bp.route('/client/submit_review/<int:project_id>', methods=['POST'])
def submit_review(project_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Please login first.'})

    try:
        project = Project.query.get_or_404(project_id)
        
        # Check if user has already reviewed this project
        existing_review = Review.query.filter_by(
            project_id=project_id,
            reviewer_id=session['user_id']
        ).first()
        
        if existing_review:
            return jsonify({'success': False, 'error': 'You have already reviewed this project.'})

        # Get the builder's user_id from the project
        builder = Builder.query.get(project.assigned_to)
        if not builder:
            return jsonify({'success': False, 'error': 'Builder not found.'})

        rating = request.form.get('rating')
        comment = request.form.get('comment')

        if not rating or not comment:
            return jsonify({'success': False, 'error': 'Both rating and comment are required.'})

        try:
            rating = int(rating)
            if not 1 <= rating <= 5:
                return jsonify({'success': False, 'error': 'Rating must be between 1 and 5.'})
        except ValueError:
            return jsonify({'success': False, 'error': 'Invalid rating value.'})

        # Create and save the review
        new_review = Review(
            project_id=project_id,
            reviewer_id=session['user_id'],
            reviewee_id=builder.user_id,
            rating=rating,
            comment=comment,
            role='client'
        )
        
        # Update builder's rating
        builder.rating = (builder.rating * builder.total_projects + rating) / (builder.total_projects + 1)
        
        db.session.add(new_review)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Review submitted successfully!'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@client_bp.route('/create-checkout-session/<int:payment_id>', methods=['POST'])
def create_checkout_session(payment_id):
    payment = Payment.query.get(payment_id)
    if not payment or payment.status == 'Paid':
        flash("Invalid payment ID or already paid.", "danger")
        return redirect(url_for('client.payments'))

    stripe.api_key = app.config['STRIPE_SECRET_KEY']

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'unit_amount': int(payment.amount_due * 100),  # adjust for your currency
                'product_data': {
                    'name': f'Project #{payment.project_id} Payment',
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('client.payment_success', payment_id=payment_id, _external=True),
        cancel_url=url_for('client.payments', _external=True),
    )

    return redirect(session.url, code=303)

@client_bp.route('/payment-success/<int:payment_id>')
def payment_success(payment_id):
    payment = Payment.query.get(payment_id)
    if payment and payment.status != 'Paid':
        payment.status = 'Paid'
        db.session.commit()
        flash('Payment completed successfully.', 'success')
    return redirect(url_for('client.payments'))

@client_bp.route('/payments')
def payments():
    if 'user_id' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('auth.signup'))

    user = User.query.get(session['user_id'])
    client = Client.query.filter_by(user_id=user.user_id).first()

    if not client:
        flash('Client profile not found.', 'danger')
        return redirect(url_for('auth.signup'))

    payments = Payment.query.filter_by(client_id=client.client_id).all()
    return render_template('client/payments.html', payments=payments)
