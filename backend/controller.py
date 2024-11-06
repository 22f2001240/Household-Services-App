from flask import Flask,render_template,request,redirect,flash,url_for
from flask import current_app as app # get the app which we defined in the main folder
from backend.models import *
from datetime import datetime
import os


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
                return  redirect("/admin_dashboard")                      #render_template ("admin_dashboard.html")
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
        file=request.files["file"] #request.files is a dict like object in Flask holds file data uploaded by the customer.this will allows you to access these files directly on the server.
        filename=file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        pin=request.form.get("pincode")
        exist_prof=Professional_Info.query.filter_by(email_id=email_id).first()
        if exist_prof:
            return render_template("professional_signup.html",err_msg="User already Exist. Please Login!!",msg="")
        new_prof_obj=Professional_Info(email_id=email_id,password=pwd,full_name=name,service_id=service_id,experience=exp,proof_doc=filename,address=adrs,pin_code=pin)
        db.session.add(new_prof_obj)
        db.session.commit()
        return render_template("proff_login.html",err_msg="",msg="Registration successful!")
    return render_template("professional_signup.html",err_msg="",msg="",service_obj=service_obj)

#for showing the service in admin page
@app.route("/admin_dashboard",methods=["GET","POST"])
def admin_dashboard():
    service_list=Service.query.all()
    prof_list=Professional_Info.query.all()
    service_dict={service.id:service for service in Service.query.all()}
    category=request.form.get('category')
    return render_template ("admin_dashboard.html",service_list=service_list,prof_list=prof_list,service_dict=service_dict)

#for each service page edit
@app.route("/edit_service/<int:service_id>",methods=["GET","POST"])
def edit_service(service_id):
    service_obj=Service.query.get(service_id)
    if request.method=="POST":
        new_name=request.form.get("name")
        new_price=request.form.get("price")
        new_descr=request.form.get("descrip")
        service_obj.name=new_name
        service_obj.basic_price=new_price
        service_obj.Description=new_descr
        db.session.commit()
        return redirect("/admin_dashboard")
    return render_template("service_page.html",service=service_obj)

#delete a service from admin
@app.route("/delete_service/<int:service_id>")
def delete_service(service_id):
    service_obj=Service.query.get(service_id)
    if service_obj:
        db.session.delete(service_obj)
        db.session.commit()
    return redirect("/admin_dashboard")

#add a new service from admin
@app.route("/add_service",methods=["GET","POST"])
def add_service():
    service_obj=Service.query.all()
    if request.method=="POST":
        name=request.form.get("service_name")
        price=request.form.get("price")
        descr=request.form.get("description")
        exist=False
        for service in service_obj:
            if service.name==name:
                exist=True
        if exist:
            return render_template("new_service(admin).html",msg="Service already exist!!")
        else:
            new_service=Service(name=name,basic_price=price,Description=descr)
            db.session.add(new_service)
            db.session.commit()
            return redirect('/admin_dashboard')
    return render_template("new_service(admin).html",msg="")

#all service requests for a service
@app.route("/service_request/<int:service_id>")
def service_request(service_id):
    serv_obj=Service.query.get(service_id)
    serv_name=serv_obj.name
    service_requests=Service_Request.query.filter_by(service_id=service_id).all()
    prof_dict={prof_obj.id:prof_obj for prof_obj in Professional_Info.query.all()} #profession_dict {profession_id:profession obj}
    cust_dict={cust_obj.id:cust_obj for cust_obj in Customer_Info.query.all()}
    return render_template("service_request.html",serv_name=serv_name,customer=cust_dict,service_requests=service_requests,professionals=prof_dict)

#Display the file
@app.route('/display_file/<filename>')
def display_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(file_path, 'r',encoding='UTF-32') as f:
        file_content = f.read()
    return render_template('display_file.html', content=file_content, filename=filename)

#approve a professional's request by admin
@app.route('/approve_prof/<int:prof_id>')
def approve_prof(prof_id):
    prof_obj=Professional_Info.query.get(prof_id)
    prof_obj.profile_status=1
    db.session.commit()
    return redirect("/admin_dashboard")

#reject a professional's request by admin 
@app.route('/reject_prof/<int:prof_id>')
def reject_prof(prof_id):
    prof_obj=Professional_Info.query.get(prof_id)
    db.session.delete(prof_obj)
    db.session.commit()
    return redirect("/admin_dashboard")

#Block a professional's request by admin 
@app.route('/block_prof/<int:prof_id>')
def block_prof(prof_id):
    prof_obj=Professional_Info.query.get(prof_id)
    prof_obj.blocked_status=1
    db.session.commit()
    return redirect("/admin_dashboard")

#For each professional view by admin
@app.route('/professional/<int:prof_id>')
def professional(prof_id):
    professional=Professional_Info.query.get(prof_id)
    service=Service.query.filter_by(id=professional.service_id).first()
    service_name=service.name
    return render_template("prof_profile(admin).html",prof=professional,name=service_name)

#For seachrch on Service by admin
@app.route('/services_search',methods=["GET","POST"])
def services_search():
    suggestions = []
    if request.method == 'POST':
        search_val = request.form.get('search_val')
        # Query the database using ILIKE for case-insensitive search
        suggestions=Service.query.filter(Service.name.ilike(f'%{search_val}%')).all()
    return render_template("services_search.html",suggestions=suggestions)

#for  service search by name (admin)
@app.route('/service_details/<ser_name>')
def service_details(ser_name):
    service_obj=Service.query.filter_by(name=ser_name).first()
    return render_template("service_details.html",service=service_obj)
