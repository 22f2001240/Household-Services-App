from flask import Flask,render_template,request
from flask import current_app as app # get the app which we defined in the main folder
from backend.models import *


@app.route("/")
def home():
    return render_template("index.html")

#For User
@app.route("/clogin",methods=["GET","POST"])
def clogin():
    err_msg=""
    if request.method=="POST":
        email_id=request.form.get("user_name")
        pwd=request.form.get("password")
        user_obj=Customer_Info.query.filter_by(email_id=email_id,password=pwd).first()
        if user_obj:
            if user_obj.role==0:
                return render_template("admin_dashboard.html")
            elif user_obj.role==1:
                name=user_obj.full_name
                return render_template("customer_dashboard.html",name=name)
        err_msg="Invalid Login !! Please enter a valid information"
    return render_template("customer_login.html",err_msg=err_msg)

@app.route("/csignup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        email_id=request.form.get("email")
        pwd=request.form.get("password")
        name=request.form.get("name")
        phone_num=request.form.get("phone")
        adrs=request.form.get("address")
        pin=request.form.get("pincode")
        exist_user=Customer_Info.query.filter_by(email_id=email_id).first()
        if exist_user:
            return render_template("customer_signup.html",err_msg="User already Exist. Please Login!!",msg="")
        new_user_obj=Customer_Info(email_id=email_id,password=pwd,full_name=name,phone_number=phone_num,address=adrs,pin_code=pin)
        db.session.add(new_user_obj)
        db.session.commit()
        return render_template("customer_login.html",err_msg="",msg="Registration successful!")
    return render_template("customer_signup.html",err_msg="",msg="")

#For Profession
@app.route("/flogin",methods=["GET","POST"])
def flogin():
    err_msg=""
    if request.method=="POST":
        email_id=request.form.get("user_name")
        pwd=request.form.get("password")
        prof_obj=Professional_Info.query.filter_by(email_id=email_id,password=pwd).first()
        if prof_obj:
            name=prof_obj.full_name
            return render_template("professional_dashboard.html",name=name)
        err_msg="Invalid Login !! Please enter a valid information"
    return render_template("proff_login.html",err_msg=err_msg) 

@app.route("/fsignup",methods=["GET","POST"])
def fsignup():
    service_obj=Service.query.all() #list of service objects 
    if request.method=="POST":
        email_id=request.form.get("email")
        pwd=request.form.get("password")
        name=request.form.get("name")
        adrs=request.form.get("address")
        service_id=request.form.get("service") #this will give the value for particular selected object. so here its id
        exp=request.form.get("experience")
        proof=request.files["file"] #request.files is a dict like object in Flask holds file data uploaded by the customer.this will allows you to access these files directly on the server.
        file_data = proof.read()
        pin=request.form.get("pincode")
        exist_prof=Professional_Info.query.filter_by(email_id=email_id).first()
        if exist_prof:
            return render_template("professional_signup.html",err_msg="User already Exist. Please Login!!",msg="")
        new_prof_obj=Professional_Info(email_id=email_id,password=pwd,full_name=name,service_id=service_id,experience=exp,proof_doc=file_data,address=adrs,pin_code=pin)
        db.session.add(new_prof_obj)
        db.session.commit()
        return render_template("proff_login.html",err_msg="",msg="Registration successful!")
    return render_template("professional_signup.html",err_msg="",msg="",service_obj=service_obj)

