from app import db
from sqlalchemy import UniqueConstraint
from datetime import datetime

class User(db.Model):
    __tablename__ = 'USER'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(600), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(50), nullable=False)

class Client(db.Model):
    __tablename__ = 'CLIENT'

    client_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'))
    location = db.Column(db.String(255))
    company_name = db.Column(db.String(255))
    about = db.Column(db.Text)
    profile_picture = db.Column(db.String(255))

    user = db.relationship('User', backref='client_profile', lazy=True)  #  Add this line

        
class Builder(db.Model):
    __tablename__ = 'BUILDERS'

    builder_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'), nullable=False)
    active_bids = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    total_projects = db.Column(db.Integer, default=0)
    total_earning = db.Column(db.Integer, default=0)

    # New profile fields
    location = db.Column(db.String(255))
    company_name = db.Column(db.String(255))
    specialization = db.Column(db.String(255))
    experience = db.Column(db.String(255))
    about = db.Column(db.Text)
    profile_picture = db.Column(db.String(255))

    user = db.relationship('User', backref='builder_profile', lazy=True)



class Project(db.Model):
    __tablename__ = 'PROJECTS'

    project_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('CLIENT.client_id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    project_type = db.Column(db.String(255), nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(255), nullable=True)
    timeline = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), default="Pending")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    assigned_to = db.Column(db.Integer, db.ForeignKey('BUILDERS.builder_id'), nullable=True)
    client_completed = db.Column(db.Boolean, default=False)
    builder_completed = db.Column(db.Boolean, default=False)

    client = db.relationship('Client', backref='projects')

class ProjectImage(db.Model):
    __tablename__ = 'project_images'
    image_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('PROJECTS.project_id'))  
    image_path = db.Column(db.String(255), nullable=False)

    project = db.relationship('Project', backref='images')

class Bid(db.Model):
    __tablename__ = 'BIDS'
    __table_args__ = (
        UniqueConstraint('project_id', 'builder_id', name='uix_builder_project'),
    )

    bid_id         = db.Column(db.Integer, primary_key=True)
    project_id     = db.Column(db.Integer, db.ForeignKey('PROJECTS.project_id'), nullable=False)
    builder_id     = db.Column(db.Integer, db.ForeignKey('BUILDERS.builder_id'), nullable=False)
    user_id        = db.Column(db.Integer, db.ForeignKey('USER.user_id'))  #  Add this line
    estimated_cost = db.Column(db.Integer, nullable=False)
    timeline       = db.Column(db.Integer, nullable=False)
    proposal       = db.Column(db.Text, nullable=False)
    status         = db.Column(db.String(50), default="Pending")
    submitted_at   = db.Column(db.DateTime, server_default=db.func.now())

    project = db.relationship('Project', backref='bids')
    builder = db.relationship('Builder', backref='bids')
    user    = db.relationship('User')  # ✅ Access user info directly







#For the Vendor Marketplace
class VendorMarketplace(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price_pkr = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=True)
    vendor_name = db.Column(db.String(100), nullable=True)
    contact_number = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    image = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {
            'product_id': self.product_id,
            'name': self.name,
            'description': self.description,
            'price_pkr': self.price_pkr,
            'category': self.category,
            'vendor_name': self.vendor_name,
            'contact_number': self.contact_number,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'image': self.image
        }



class Review(db.Model):
    __tablename__ = 'REVIEWS'
    review_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('PROJECTS.project_id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'), nullable=False)
    reviewee_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'), nullable=False)
    role = db.Column(db.String(50))  # 'client' or 'builder'
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Add these relationships (no table changes needed)
    project = db.relationship('Project', backref='reviews')
    reviewer = db.relationship('User', foreign_keys=[reviewer_id], backref='reviews_given')
    reviewee = db.relationship('User', foreign_keys=[reviewee_id], backref='reviews_received')





# Contact details         
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

class Payment(db.Model):
    __tablename__ = 'PAYMENTS'

    payment_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('PROJECTS.project_id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('CLIENT.client_id'), nullable=False)
    amount_due = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default='Pending')  # 'Pending', 'Paid'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    project = db.relationship('Project', backref='payments')
    client = db.relationship('Client', backref='payments')
