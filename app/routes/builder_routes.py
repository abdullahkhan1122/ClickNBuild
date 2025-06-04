from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify
from app import db
from app.models import User, Project, Builder, Bid, Client, Review,Payment
from app.models import VendorMarketplace
from werkzeug.utils import secure_filename
import os


builder_bp = Blueprint('builder', __name__)  # No url_prefix

# -------------------- BUILDER ROUTES ---------------------

@builder_bp.route('/builder-homepage')
def builder_homepage():
    products = VendorMarketplace.query.limit(3).all()  # Get only 4 products
    return render_template('builder/builder_homepage.html', products=products)



@builder_bp.route('/posted-projects')
def builder_posted_projects():
    user_email = session.get('user_email')
    user = db.session.query(User).filter_by(email=user_email).first()
    builder = db.session.query(Builder).filter_by(user_id=user.user_id).first()

    # Get all project IDs the builder has already bid on
    existing_bids = db.session.query(Bid.project_id).filter_by(builder_id=builder.builder_id).all()
    bid_project_ids = [bid.project_id for bid in existing_bids]

    projects = db.session.query(Project).filter(Project.status.in_(['Open', 'Pending'])).all()
    return render_template('builder/builder_posted_projects.html', projects=projects, bid_project_ids=bid_project_ids)


@builder_bp.route('/builder-dashboard')
def builder_dashboard():
    user_email = session.get('user_email')
    user = User.query.filter_by(email=user_email).first()
    builder = Builder.query.filter_by(user_id=user.user_id).first()

    # Counts
    active_bids = Bid.query.filter_by(builder_id=builder.builder_id, status='Pending').count()
    accepted_bids = Bid.query.filter_by(builder_id=builder.builder_id, status='Accepted').count()
    rejected_bids = Bid.query.filter_by(builder_id=builder.builder_id, status='Rejected').count()
    
    # ✅ Count projects where this builder has been assigned (i.e., won)
    won_projects = Project.query.filter_by(assigned_to=builder.builder_id).count()

    # ✅ Get recent bids with related project info
    recent_bids = db.session.query(Bid, Project)\
        .join(Project, Bid.project_id == Project.project_id)\
        .filter(Bid.builder_id == builder.builder_id)\
        .order_by(Bid.bid_id.desc()).limit(5).all()

    return render_template('builder/builder_dashboard.html',
                           user=user,
                           active_bids=active_bids,
                           accepted_bids=accepted_bids,
                           rejected_bids=rejected_bids,
                           won_projects=won_projects,
                           recent_bids=recent_bids)




@builder_bp.route('/builder-marketplace')
def builder_marketplace():
    products = VendorMarketplace.query.all()
    return render_template('builder/builder_marketplace.html', products=[p.to_dict() for p in products])


@builder_bp.route('/builder-profile')
def builder_profile():
    if 'user_email' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('auth.signup'))
    
    user = User.query.filter_by(email=session['user_email']).first()
    builder = Builder.query.filter_by(user_id=user.user_id).first()
    
    return render_template('builder/builder_profile.html', user=user, builder=builder)


@builder_bp.route('/builder-projects')
def builder_projects():
    user_email = session.get('user_email')
    user = db.session.query(User).filter_by(email=user_email).first()
    builder = db.session.query(Builder).filter_by(user_id=user.user_id).first()

    # Get all project IDs the builder has already bid on
    existing_bids = db.session.query(Bid.project_id).filter_by(builder_id=builder.builder_id).all()
    bid_project_ids = [bid.project_id for bid in existing_bids]

    projects = db.session.query(Project).filter(Project.status.in_(['Open', 'Pending', 'Active', 'Completed'])).all()
    user_id = session['user_id']
    reviews = Review.query.filter_by(reviewer_id=user_id).all()
    return render_template('builder/builder_projects.html', projects=projects, reviews=reviews, bid_project_ids=bid_project_ids, builder=builder)


@builder_bp.route('/builder-proposals')
def builder_proposals():
    user_email = session.get('user_email')
    user = db.session.query(User).filter_by(email=user_email).first()
    builder = db.session.query(Builder).filter_by(user_id=user.user_id).first()

    # Join Bid and Project
    bids = db.session.query(Bid, Project).join(Project, Bid.project_id == Project.project_id)\
        .filter(Bid.builder_id == builder.builder_id).all()

    return render_template('builder/builder_sent_proposals.html', bids=bids)


@builder_bp.route('/builder/payments')
def builder_payments():
    if 'user_id' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('auth.signup'))

    user = User.query.get(session['user_id'])
    builder = Builder.query.filter_by(user_id=user.user_id).first()

    if not builder:
        flash('Builder profile not found.', 'danger')
        return redirect(url_for('auth.signup'))

    # Get assigned projects and related payments
    projects_with_payments = db.session.query(Project, Payment, Client, User)\
        .join(Payment, Project.project_id == Payment.project_id)\
        .join(Client, Project.client_id == Client.client_id)\
        .join(User, Client.user_id == User.user_id)\
        .filter(Project.assigned_to == builder.builder_id)\
        .all()

    return render_template(
        'builder/builder_payments.html',
        projects_with_payments=projects_with_payments
    )



@builder_bp.route('/builder-reviews')
def builder_reviews():
    if 'user_id' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('auth.signup'))

    user = User.query.get(session['user_id'])
    builder = Builder.query.filter_by(user_id=user.user_id).first()
    
    if not builder:
        flash('Builder profile not found.', 'danger')
        return redirect(url_for('auth.signup'))
    
    # Get reviews where the current user is the reviewee and the reviewer is a client
    reviews = db.session.query(Review, Project, User)\
        .join(Project, Review.project_id == Project.project_id)\
        .join(User, Review.reviewer_id == User.user_id)\
        .filter(Review.reviewee_id == user.user_id)\
        .filter(Review.role == 'client')\
        .all()
    
    return render_template('builder/builder_reviews.html', reviews=reviews)


# -------------------- PLACE BID (legacy page) ---------------------

@builder_bp.route('/place-bid/<int:project_id>', methods=['GET', 'POST'])
def placeBid(project_id):
    project = db.session.query(Project).filter_by(project_id=project_id).first()
    if not project:
        flash('Project not found.', 'danger')
        return redirect(url_for('builder.builder_projects'))

    if request.method == 'POST':
        estimated_cost = request.form.get('estimated_cost')
        timeline = request.form.get('timeline')
        proposal = request.form.get('proposal')

        user_email = session.get('user_email')
        user = db.session.query(User).filter_by(email=user_email).first()
        builder = db.session.query(Builder).filter_by(user_id=user.user_id).first()
        if not builder:
            flash('Builder profile not found.', 'danger')
            return redirect(url_for('auth.signup'))

        new_bid = Bid(
            project_id    = project.project_id,
            builder_id    = builder.builder_id,
            estimated_cost= estimated_cost,
            timeline      = timeline,
            proposal      = proposal,
            status        = "Pending"
        )
        db.session.add(new_bid)
        db.session.commit()

        flash('Your bid has been submitted successfully!', 'success')
        return redirect(url_for('builder.builder_projects'))

    return render_template('builder/place_bid.html', project=project)


# -------------------- AJAX SUBMIT ROUTE ---------------------

@builder_bp.route('/submit-bid', methods=['POST'])
def submit_bid():
    try:
        project_id = request.form.get('project_id')
        estimated_cost = request.form.get('estimated_cost')
        timeline = request.form.get('timeline')
        proposal = request.form.get('proposal')

        # Get current logged-in builder
        user_email = session.get('user_email')
        user = db.session.query(User).filter_by(email=user_email).first()
        if not user:
            return jsonify(success=False, message="User not logged in"), 401

        builder = db.session.query(Builder).filter_by(user_id=user.user_id).first()
        if not builder:
            return jsonify(success=False, message="Builder profile not found"), 404

        # Check if already placed bid on this project
        existing_bid = db.session.query(Bid).filter_by(
            builder_id=builder.builder_id,
            project_id=project_id
        ).first()

        if existing_bid:
            return jsonify(success=False, message="You have already placed a bid on this project.")

        # If no existing bid, create new bid
        new_bid = Bid(
            project_id=project_id,
            builder_id=builder.builder_id,
            estimated_cost=estimated_cost,
            timeline=timeline,
            proposal=proposal,
            status="Pending"
        )
        db.session.add(new_bid)
        db.session.commit()

        return jsonify(success=True)
    
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, message=str(e)), 500

@builder_bp.route('/edit-bid/<int:bid_id>', methods=['GET', 'POST'])
def edit_bid(bid_id):
    bid = db.session.query(Bid).filter_by(bid_id=bid_id).first()
    if request.method == 'POST':
        bid.estimated_cost = request.form.get('estimated_cost')
        bid.timeline = request.form.get('timeline')
        bid.proposal = request.form.get('proposal')
        db.session.commit()
        flash('Bid updated successfully!', 'success')
        return redirect(url_for('builder.builder_proposals'))
    
    return render_template('builder/edit_bid.html', bid=bid)

@builder_bp.route('/delete-bid/<int:bid_id>', methods=['POST'])
def delete_bid(bid_id):
    bid = db.session.query(Bid).filter_by(bid_id=bid_id).first()
    db.session.delete(bid)
    db.session.commit()
    flash('Bid deleted.', 'success')
    return redirect(url_for('builder.builder_proposals'))

@builder_bp.route('/builder/complete-project/<int:project_id>', methods=['POST'])
def complete_project(project_id):
    project = Project.query.get(project_id)
    if project:
        if project.builder_completed:
            flash('You have already marked this project as complete.', 'info')
        else:
            project.builder_completed = True
            if project.client_completed:
                project.status = 'Completed'
                # Update the corresponding bid status to 'Completed'
                bid = Bid.query.filter_by(project_id=project_id, builder_id=project.assigned_to).first()
                if bid:
                    bid.status = 'Completed'
            db.session.commit()
            flash('You have marked this project as complete. Waiting for the client.' if not project.client_completed else 'Project marked as completed!', 'success')
    else:
        flash('Project not found.', 'danger')
    return redirect(url_for('builder.builder_projects'))

@builder_bp.route('/builder/submit_review/<int:project_id>', methods=['POST'])
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
        
        # Get the client's user_id
        client = Client.query.get(project.client_id)
        if not client:
            return jsonify({'success': False, 'error': 'Client not found.'})

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
            reviewee_id=client.user_id,
            rating=rating,
            comment=comment,
            role='builder'
        )
        
        db.session.add(new_review)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Review submitted successfully!'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})




@builder_bp.route('/profile')
def profile():
    if 'user_email' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('auth.signup'))
    
    user = User.query.filter_by(email=session['user_email']).first()
    builder = Builder.query.filter_by(user_id=user.user_id).first()
    
    return render_template('builder/profile.html', user=user, builder=builder)

@builder_bp.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_email' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('auth.signup'))
    
    user = User.query.filter_by(email=session['user_email']).first()
    builder = Builder.query.filter_by(user_id=user.user_id).first()
    
    # Update user information
    user.phone = request.form.get('phone')
    
    # Update builder information
    builder.location = request.form.get('location')
    builder.company_name = request.form.get('company_name')
    builder.specialization = request.form.get('specialization')
    builder.experience = request.form.get('experience')
    builder.about = request.form.get('about')
    
    # Handle profile picture upload
    if 'profile_picture' in request.files:
        file = request.files['profile_picture']
        if file and file.filename:
            filename = secure_filename(file.filename)
            # Save to app/static/uploads/profile_pictures/
            save_path = os.path.join('app', 'static', 'uploads', 'profile_pictures', filename)
            file.save(save_path)
            # Store only the relative path in the DB
            builder.profile_picture = f'uploads/profile_pictures/{filename}'
    
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('builder.builder_profile'))
