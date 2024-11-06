from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

#Entity 1 - Customer table
class Customer_Info(db.Model):
    __tablename__="customer_info"
    id=db.Column(db.Integer,primary_key=True)
    email_id=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    full_name=db.Column(db.String,nullable=False)
    phone_number=db.Column(db.Integer,nullable=False)
    role=db.Column(db.Integer,default=1) #for customer its 1 . for admin its 0 
    address=db.Column(db.String,nullable=False)
    pin_code=db.Column(db.Integer,nullable=False)
    blocked_status=db.Column(db.Integer,default=0) #not blocked=0, 1-blocked
    service_requests=db.relationship("Service_Request",cascade="all,delete",backref="customer_info",lazy=True)


#Entity 2 - Professional table
class Professional_Info(db.Model):
    __tablename__="professional_info"
    id=db.Column(db.Integer,primary_key=True)
    email_id=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    full_name=db.Column(db.String,nullable=False)
    experience=db.Column(db.Integer,nullable=False)
    proof_doc=db.Column(db.String,nullable=False)
    address=db.Column(db.String,nullable=False)
    pin_code=db.Column(db.Integer,nullable=False)
    service_id=db.Column(db.Integer,db.ForeignKey("service.id"))
    rating=db.Column(db.Integer,default=0)
    price=db.Column(db.Integer,nullable=True)
    profile_status=db.Column(db.Integer,default=0) #not accepted yet=0 ,accepted=1
    blocked_status=db.Column(db.Integer,default=0) #not blocked=0, 1-blocked
    service_requests=db.relationship("Service_Request",cascade="all,delete",backref="professional_info",lazy=True)

# Entity 3 - Service table
class Service(db.Model):
    __tablename__="service"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    basic_price=db.Column(db.Integer,nullable=False)
    Description=db.Column(db.String,nullable=False)
    professionals=db.relationship("Professional_Info",cascade="all,delete",backref="service",lazy=True)
    service_requests=db.relationship("Service_Request",cascade="all,delete",backref="service",lazy=True)

# Entity 4 - Service request table
class Service_Request(db.Model):
    __tablename__="service_request"
    id=db.Column(db.Integer,primary_key=True)
    service_id=db.Column(db.Integer,db.ForeignKey("service.id"),nullable=False)
    customer_id=db.Column(db.Integer,db.ForeignKey("customer_info.id"),nullable=False)
    professional_id=db.Column(db.Integer,db.ForeignKey("professional_info.id"),nullable=False)
    date_of_request=db.Column(db.DateTime,nullable=True)
    date_of_completion=db.Column(db.Date,nullable=True)
    service_status=db.Column(db.String,nullable=False) #only requested,assigned or closed
    remarks=db.Column(db.String,nullable=True)
