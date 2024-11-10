from flask import Flask,render_template,request,redirect,flash,url_for
from flask import current_app as app # get the app which we defined in the main folder
from backend.models import *
from datetime import datetime
import os

@app.route("/")
def home():
    service_obj=Service.query.all()
    return render_template("index.html",service_obj=service_obj)

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
                return  redirect("/admin_dashboard")                    
            elif user_obj.role==1:
                if user_obj.blocked_status == 1:
                    err_msg="Sorry .You have been knocked Out !!"
                    return render_template("customer_login.html",err_msg=err_msg)
                return redirect(url_for('customer_dashboard',cust_id=user_obj.id))
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
            if prof_obj.blocked_status == 1:
                err_msg="Sorry .You have been knocked Out  !!"
                return render_template("proff_login.html",err_msg=err_msg)
            if prof_obj.profile_status == 0: #Not yet accepted the request
                err_msg="Waiting for the approval from admin. Please wait !!"
                return render_template("proff_login.html",err_msg=err_msg)
            prof_id=prof_obj.id
            return redirect(url_for('professional_dashboard',prof_id=prof_id))
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
    req_list=Service_Request.query.all()
    service_dict={service.id:service for service in Service.query.all()}
    cust_dict={cust_obj.id:cust_obj for cust_obj in Customer_Info.query.all()}
    prof_dict={prof_obj.id:prof_obj for prof_obj in Professional_Info.query.all()}
    return render_template ("admin_dashboard.html",professionals=prof_dict,customers=cust_dict,req_objs=req_list,service_list=service_list,prof_list=prof_list,service_dict=service_dict)

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
    cust_dict={cust_obj.id:cust_obj for cust_obj in Customer_Info.query.all()}
    prof_dict={prof_obj.id:prof_obj for prof_obj in Professional_Info.query.all()}
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

#Block a professional by admin 
@app.route('/block_prof/<int:prof_id>')
def block_prof(prof_id):
    prof_obj=Professional_Info.query.get(prof_id)
    prof_obj.blocked_status=1
    db.session.commit()
    return redirect("/admin_dashboard")

#UnBlock a professional by admin 
@app.route('/unblock_prof/<int:prof_id>')
def unblock_prof(prof_id):
    prof_obj=Professional_Info.query.get(prof_id)
    prof_obj.blocked_status=0
    db.session.commit()
    return redirect("/admin_dashboard")

#For each professional view by admin
@app.route('/professional/<int:prof_id>')
def professional(prof_id):
    professional=Professional_Info.query.get(prof_id)
    service=Service.query.filter_by(id=professional.service_id).first()
    service_name=service.name
    return render_template("prof_profile(admin).html",prof=professional,name=service_name)

#Search tab for admin
@app.route('/search_tab_admin',methods=['GET','POST'])
def search_tab_admin():
    suggestions = []
    categ=""
    if request.method == 'POST':
        categ=request.form.get('category')
        search_val = request.form.get('search_val')
        if categ == "Services":
            suggestions=Service.query.filter(Service.name.ilike(f'%{search_val}%')).all() #for case sensitive short words.
        elif categ == "Service Requests": 
            status=["requested","accepted","rejected","closed"]
            for word in status:
                if word.startswith(search_val.lower()):
                    suggestions.append(word)
        elif categ == "Customers": 
            status=["blocked","active"]
            for word in status:
                if word.startswith(search_val.lower()):
                    suggestions.append(word)
        elif categ == "Professionals": 
            status=["blocked","active","requested"]
            for word in status:
                if word.startswith(search_val.lower()):
                    suggestions.append(word)
    return render_template("search_tab_admin.html",suggestions=suggestions,categ=categ)

#for  service search by name (admin)
@app.route('/service_details/<ser_name>')
def service_details(ser_name):
    service_obj=Service.query.filter_by(name=ser_name).first()
    return render_template("service_details.html",service=service_obj)

#for request search by status (admin)
@app.route('/request_status/<status>')
def request_status(status):
    cust_dict={cust_obj.id:cust_obj for cust_obj in Customer_Info.query.all()}
    prof_dict={prof_obj.id:prof_obj for prof_obj in Professional_Info.query.all()}
    status_dict={'requested':0,'accepted':1,"rejected":2,"closed":3}
    stat_dict={0:'Requested',1:'Accepted',2:"Rejected",3:"Closed"}
    serv_status=status_dict[status]
    req_stat=stat_dict[serv_status]
    req_objs=Service_Request.query.filter_by(service_status=serv_status).all()
    return render_template("request_details.html",req_objs=req_objs,req_stat=req_stat,customers=cust_dict,professionals=prof_dict)

#for customer search by status (admin)
@app.route('/customer_status/<status>')
def customer_status(status):
    status_dict={'active':0,'blocked':1}
    stat=status_dict[status]
    cust_objs=Customer_Info.query.filter(Customer_Info.blocked_status==stat,Customer_Info.role==1).all()
    stat_dict={0:'Active',1:'Blocked'}
    cust_status=stat_dict[stat]
    return render_template("customer_details.html",cust_objs=cust_objs,cust_status=cust_status)

#for professional search by status (admin)
@app.route('/professional_status/<status>')
def professional_status(status):
    if status == 'blocked':
        stat='Blocked'
        prof_objs=Professional_Info.query.filter_by(blocked_status=1).all()
    elif status == 'requested':    
        stat="Requested"
        prof_objs=Professional_Info.query.filter_by(profile_status=0).all()
    else:
        stat="Active"
        prof_objs=Professional_Info.query.filter(Professional_Info.profile_status==1,Professional_Info.blocked_status==0).all()
    service_dict={service.id:service for service in Service.query.all()}
    return render_template("professional_details.html",service_dict=service_dict,prof_objs=prof_objs,stat=stat)

#for summary to admin
@app.route('/summary_admin')
def summary_admin():
    service_name=[]
    service_req_count=db.session.query(Service_Request.service_id,db.func.count(Service_Request.id).label('service_count')).group_by(Service_Request.service_id).all() #list of typle (id,count)
    service_id=[req.service_id for req in service_req_count]
    serv_count=[req.service_count for req in service_req_count]
    rating_counts=db.session.query(Service_Request.rating,db.func.count(Service_Request.id).label('r_count')).filter(Service_Request.service_status==3).group_by(Service_Request.rating).all()
    ratings=[rate.rating for rate in rating_counts]
    rating_count=[rate.r_count for rate in rating_counts]
    for serv in service_id:
        service_obj=Service.query.get(serv)
        service_name.append(service_obj.name)
    return render_template("summary_admin.html",service_name=service_name,serv_count=serv_count,ratings=ratings,rating_count=rating_count)


#dashboard for professional
@app.route("/professional_dashboard/<int:prof_id>",methods=["GET","POST"])
def professional_dashboard(prof_id):
    prof_obj=Professional_Info.query.get(prof_id)
    ser_req_list=Service_Request.query.filter_by(professional_id=prof_id).all()
    cust_dict={cust_obj.id:cust_obj for cust_obj in Customer_Info.query.all()}
    service_dict={service.id:service for service in Service.query.all()}
    if ser_req_list !=[]:
        rating_list=[]
        req_list=[]
        closedreq_list=[]
        for req in ser_req_list:
            if req.rating != 0:
                rating_list.append(int(req.rating))
            if req.service_status == 0:
                req_list.append(req)
            elif req.service_status == 3:
                closedreq_list.append(req)
        if len(rating_list) != 0:
            rating=sum(rating_list)/len(rating_list)
            prof_obj.rating=rating
            db.session.commit()
        return render_template("professional_dashboard.html",closedreq_list=closedreq_list,prof_obj=prof_obj,req_list=req_list,cust_dict=cust_dict,service_dict=service_dict)

    return render_template("professional_dashboard.html",prof_obj=prof_obj)

#To see the professional's profile by professional to edit
@app.route('/prof_profile/<int:prof_id>',methods=['GET','POST'])
def prof_profile(prof_id):
    prof_obj=Professional_Info.query.get(prof_id)
    service_dict={service_obj.id:service_obj for service_obj in Service.query.all()}
    if request.method=='POST':
        email_id=request.form.get("email")
        pwd=request.form.get("password")
        name=request.form.get("name")
        adrs=request.form.get("address")
        service_name=request.form.get("service") 
        exp=request.form.get("experience")
        pin=request.form.get("pincode")
        service_obj=Service.query.filter_by(name=service_name).first()
        service_id=service_obj.id
        prof_obj.email_id=email_id
        prof_obj.password=pwd
        prof_obj.full_name=name
        prof_obj.service_id=service_id
        prof_obj.experience=exp
        prof_obj.address=adrs
        prof_obj.pin_code=pin
        db.session.commit()
        return render_template("professional_profile.html",prof_obj=prof_obj,service_dict=service_dict,msg='Succefully Saved')
    return render_template("professional_profile.html",prof_obj=prof_obj,service_dict=service_dict,msg="")

#Accept the service request
@app.route('/accept_req/<int:req_id>/<int:prof_id>')
def accept_req(req_id,prof_id):
    req=Service_Request.query.get(req_id)
    req.service_status=1
    db.session.commit()
    return redirect(url_for('professional_dashboard',prof_id=prof_id))

#Reject a service request
@app.route('/reject_req/<int:req_id>/<int:prof_id>')
def reject_req(req_id,prof_id):
    req=Service_Request.query.get(req_id)
    req.service_status=2
    db.session.commit()
    return redirect(url_for('professional_dashboard',prof_id=prof_id))

#For search tab for professional
@app.route('/search_tab_prof/<int:prof_id>',methods=['GET','POST'])
def search_tab_prof(prof_id):
    prof_obj=Professional_Info.query.get(prof_id)
    suggestions = []
    categ=''
    if request.method == 'POST':
        categ=request.form.get('category')
        search_val = request.form.get('search_val')
        if categ == "Location":
            cust_objects=Customer_Info.query.filter(Customer_Info.address.ilike(f'%{search_val}%'),Customer_Info.role==1).all()
            if cust_objects !=[]:
                for cust in cust_objects:
                    if cust.address not in suggestions and cust.blocked_status == 0:
                        suggestions.append(cust.address)
        elif categ == "Pin Code":
            cust_objects=Customer_Info.query.filter(Customer_Info.pin_code.ilike(f'%{search_val}%'),Customer_Info.role==1).all()
            if cust_objects !=[]:
                for cust in cust_objects:
                    if cust.pin_code not in suggestions and cust.blocked_status == 0:
                        suggestions.append(cust.pin_code)
        elif categ == "Date":
            serv_req_objects=Service_Request.query.filter(Service_Request.service_date.ilike(f'%{search_val}%'),Customer_Info.role==1).all()
            if serv_req_objects !=[]:
                for req in serv_req_objects:
                    if req.service_date not in suggestions:
                        suggestions.append(req.service_date)
            
    return render_template("search_tab_prof.html",prof_obj=prof_obj,suggestions=suggestions,categ=categ)

#for location based search by prof of customer
@app.route('/loc_custs/<loc>/<int:prof_id>')
def loc_custs(loc,prof_id):
    cust_obj=Customer_Info.query.filter(Customer_Info.address==loc,Customer_Info.blocked_status==0,Customer_Info.role==1).all()
    prof_obj=Professional_Info.query.get(prof_id)
    return render_template("search_based_cust.html",customers=cust_obj,prof_obj=prof_obj)

#for pincode based search by prof of customer
@app.route('/pin_custs/<pin>/<int:prof_id>')
def pin_custs(pin,prof_id):
    cust_obj=Customer_Info.query.filter(Customer_Info.pin_code==pin,Customer_Info.blocked_status==0,Customer_Info.role==1).all()
    prof_obj=Professional_Info.query.get(prof_id)
    return render_template("search_based_cust.html",customers=cust_obj,prof_obj=prof_obj)

#for date based search by prof of customer
@app.route('/date_custs/<date>/<int:prof_id>')
def date_custs(date,prof_id):
    requests=Service_Request.query.filter(Service_Request.service_date==date,Service_Request.professional_id==prof_id).all()
    prof_obj=Professional_Info.query.get(prof_id)
    cust_dict={cust.id:cust for cust in Customer_Info.query.all()}
    service_dict={service.id:service for service in Service.query.all()}
    return render_template("search_based_req.html",serv_dict=service_dict,requests=requests,cust_dict=cust_dict,prof_obj=prof_obj)

#for summary to professional
@app.route('/summary_professional/<int:prof_id>')
def summary_professional(prof_id):
    prof_obj=Professional_Info.query.get(prof_id)
    service_stat_req=db.session.query(Service_Request.service_status,db.func.count(Service_Request.id).label('service_status_count')).filter(Service_Request.professional_id==prof_id).group_by(Service_Request.service_status).all() 
    stat=[req.service_status for req in service_stat_req]
    stat_dict={0:"Requested",1:"Accepted",2:"Rejected",3:"Closed"}
    status=[]
    for x in stat:
        status.append(stat_dict[x])
    req_stat_count=[req.service_status_count for req in service_stat_req]
    service_reviews=db.session.query(Service_Request.rating,db.func.count(Service_Request.id).label('service_rating_count')).filter(Service_Request.professional_id==prof_id,Service_Request.service_status==3).group_by(Service_Request.rating).all() 
    ratings=[req.rating for req in service_reviews]
    rating_count=[req.service_rating_count for req in service_reviews]
    return render_template("summary_professional.html",prof_obj=prof_obj,status=status,req_stat_count=req_stat_count,ratings=ratings,rating_count=rating_count)

#Dashboard for Customer
@app.route("/customer_dashboard/<int:cust_id>",methods=["GET","POST"])
def customer_dashboard(cust_id):
    cust_obj=Customer_Info.query.get(cust_id)
    serv_req=Service_Request.query.filter_by(customer_id=cust_id).all()
    service_obj=Service.query.all()
    prof_dict={prof_obj.id:prof_obj for prof_obj in Professional_Info.query.all()}
    service_dict={service.id:service for service in Service.query.all()}
    return render_template("customer_dashboard.html",prof_dict=prof_dict,serv_dict=service_dict,serv_req=serv_req,cust_obj=cust_obj,serv_obj=service_obj)

#Best services for Customer from each card
@app.route("/best_service/<int:serv_id>/<int:cust_id>")
def best_service(serv_id,cust_id):
    prof_obj_list=Professional_Info.query.filter(Professional_Info.service_id==serv_id,Professional_Info.blocked_status==0,Professional_Info.profile_status==1).all()
    serv_obj=Service.query.get(serv_id)
    cust_obj=Customer_Info.query.get(cust_id)
    return render_template("best_service.html",prof_objs=prof_obj_list,serv_obj=serv_obj,cust_obj=cust_obj)

#Book a service by customer
@app.route("/book_service/<int:serv_id>/<int:prof_id>/<int:cust_id>",methods=["GET","POST"])
def book_service(serv_id,prof_id,cust_id):  
    date=''
    cust_obj=Customer_Info.query.get(cust_id)
    if request.method=='POST':
        service_date=datetime.strptime(request.form.get('date'),'%Y-%m-%d').date()
        requirements=request.form.get('requirement')
        new_req=Service_Request(service_id=serv_id,customer_id=cust_id,professional_id=prof_id,service_date=service_date,service_description=requirements)
        db.session.add(new_req)
        db.session.commit()
        return redirect(url_for('customer_dashboard',cust_id=cust_id))
    return render_template("book_service.html",date=date,cust_obj=cust_obj)

#Cancel a service request by customer
@app.route("/cancel_req/<int:req_id>")
def cancel_req(req_id):
    req_obj=Service_Request.query.get(req_id)
    cust_id=req_obj.customer_id
    db.session.delete(req_obj)
    db.session.commit()
    return redirect(url_for('customer_dashboard',cust_id=cust_id))

#Closing a service request by customer
@app.route("/closing_req/<int:req_id>",methods=['GET','POST'])
def closing_req(req_id):
    req_obj=Service_Request.query.get(req_id)
    cust_id=req_obj.customer_id
    cust_obj=Customer_Info.query.get(cust_id)
    prof_dict={prof_obj.id:prof_obj for prof_obj in Professional_Info.query.all()}
    service_dict={service.id:service for service in Service.query.all()}
    if request.method=="POST":
        rating=request.form.get('rating')
        remark=request.form.get('remark')
        req_obj.service_status=3 #closed
        if rating:
            req_obj.rating=rating
        if remark:
            req_obj.remarks=remark
        db.session.commit()
        prof_id=req_obj.professional_id
        ser_req_list=Service_Request.query.filter_by(professional_id=prof_id).all()
        if ser_req_list !=[]:
            rating_list=[]
            for req in ser_req_list:
                if req.rating != 0:
                    rating_list.append(int(req.rating))
            if len(rating_list) != 0:
                rating=sum(rating_list)/len(rating_list)
                prof_dict[prof_id].rating=rating
                db.session.commit()
        return redirect(url_for('customer_dashboard',cust_id=cust_id))
    return render_template('service_remark.html',cust_obj=cust_obj,req_obj=req_obj,prof_dict=prof_dict,serv_dict=service_dict)

#Edit a service request by customer
@app.route("/edit_req_date/<int:req_id>",methods=['GET','POST'])
def edit_req_date(req_id):
    prof_dict={prof_obj.id:prof_obj for prof_obj in Professional_Info.query.all()}
    service_dict={service.id:service for service in Service.query.all()}
    req_obj=Service_Request.query.get(req_id)
    cust_id=req_obj.customer_id
    cust_obj=Customer_Info.query.get(cust_id)
    if request.method=="POST":
        new_date=datetime.strptime(request.form.get('date'),'%Y-%m-%d').date()
        req_obj.service_date=new_date
        db.session.commit()
        return redirect(url_for('customer_dashboard',cust_id=cust_id))
    return render_template("edit_req.html",req_obj=req_obj,service_dict=service_dict,prof_dict=prof_dict,cust_obj=cust_obj)

#Edit closed service request by customer
@app.route("/edit_closed_req/<int:req_id>",methods=['GET','POST'])
def edit_closed_req(req_id):
    req_obj=Service_Request.query.get(req_id)
    cust_id=req_obj.customer_id
    cust_obj=Customer_Info.query.get(cust_id)
    prof_dict={prof_obj.id:prof_obj for prof_obj in Professional_Info.query.all()}
    service_dict={service.id:service for service in Service.query.all()}
    if request.method=="POST":
        new_rating=request.form.get('rating')
        new_remark=request.form.get('remark')
        req_obj.remarks=new_remark
        req_obj.rating=new_rating
        db.session.commit()
        prof_id=req_obj.professional_id
        ser_req_list=Service_Request.query.filter_by(professional_id=prof_id).all()
        if ser_req_list !=[]:
            rating_list=[]
            for req in ser_req_list:
                if req.rating != 0:
                    rating_list.append(int(req.rating))
            if len(rating_list) != 0:
                rating=sum(rating_list)/len(rating_list)
                prof_dict[prof_id].rating=rating
                db.session.commit()
        return redirect(url_for('customer_dashboard',cust_id=cust_id))
    return render_template("edit_closed_req.html",req_obj=req_obj,service_dict=service_dict,prof_dict=prof_dict,cust_obj=cust_obj)

#To see the customer's profile by customer to edit
@app.route('/cust_profile/<int:cust_id>',methods=['GET','POST'])
def cust_profile(cust_id):
    cust_obj=Customer_Info.query.get(cust_id)
    msg=''
    if request.method=='POST':
        email_id=request.form.get("email")
        pwd=request.form.get("password")
        name=request.form.get("name")
        adrs=request.form.get("address")
        phone=request.form.get("phone")
        pin=request.form.get("pincode")
        cust_obj.email_id=email_id
        cust_obj.password=pwd
        cust_obj.full_name=name
        cust_obj.phone_number=phone
        cust_obj.address=adrs
        cust_obj.pin_code=pin
        db.session.commit()
        msg='Succefully Saved'
    return render_template("customer_profile.html",cust_obj=cust_obj,msg=msg)

#Search tab for customer
@app.route('/search_tab_cust/<int:cust_id>',methods=['GET','POST'])
def search_tab_cust(cust_id):
    cust_obj=Customer_Info.query.get(cust_id)
    suggestions = []
    categ=''
    if request.method == 'POST':
        categ=request.form.get('category')
        search_val = request.form.get('search_val')
        if categ == "Services":
            suggestions=Service.query.filter(Service.name.ilike(f'%{search_val}%')).all()
        elif categ == "Location":
            prof_objects=Professional_Info.query.filter(Professional_Info.address.ilike(f'%{search_val}%')).all()
            if prof_objects !=[]:
                for prof in prof_objects:
                    if prof.address not in suggestions and prof.blocked_status == 0 and prof.profile_status == 1:
                        suggestions.append(prof.address)
        elif categ == "Pin Code":
            prof_objects=Professional_Info.query.filter(Professional_Info.pin_code.ilike(f'%{search_val}%')).all()
            if prof_objects !=[]:
                for prof in prof_objects:
                    if prof.pin_code not in suggestions and prof.blocked_status == 0 and prof.profile_status == 1:
                        suggestions.append(prof.pin_code)
    return render_template("search_tab_cust.html",cust_obj=cust_obj,suggestions=suggestions,categ=categ)

#for  service search by name (customer)
@app.route('/service_details_cust/<ser_name>/<int:cust_id>')
def service_details_cust(ser_name,cust_id):
    cust_obj=Customer_Info.query.get(cust_id)
    service_obj=Service.query.filter_by(name=ser_name).first()
    return render_template("service_details_cust.html",service=service_obj,cust_obj=cust_obj)

#for location based search by customers by professionals
@app.route('/loc_profs/<loc>/<int:cust_id>')
def loc_profs(loc,cust_id):
    prof_objs=Professional_Info.query.filter(Professional_Info.address==loc,Professional_Info.profile_status==1,Professional_Info.blocked_status==0).all()
    cust_obj=Customer_Info.query.get(cust_id)
    service_dict={service.id:service for service in Service.query.all()}
    return render_template("search_based_prof.html",professionals=prof_objs,cust_obj=cust_obj,service_dict=service_dict)

#for pincode based search by customers by professionals
@app.route('/pin_profs/<pin>/<int:cust_id>')
def pin_profs(pin,cust_id):
    prof_objs=Professional_Info.query.filter(Professional_Info.pin_code==pin,Professional_Info.profile_status==1,Professional_Info.blocked_status==0).all()
    cust_obj=Customer_Info.query.get(cust_id)
    service_dict={service.id:service for service in Service.query.all()}
    return render_template("search_based_prof.html",professionals=prof_objs,cust_obj=cust_obj,service_dict=service_dict)

#for summary to customer
@app.route('/summary_customer/<int:cust_id>')
def summary_customer(cust_id):
    cust_obj=Customer_Info.query.get(cust_id)
    service_stat_req=db.session.query(Service_Request.service_status,db.func.count(Service_Request.id).label('service_status_count')).filter(Service_Request.customer_id==cust_id).group_by(Service_Request.service_status).all() 
    stat=[req.service_status for req in service_stat_req]
    stat_dict={0:"Requested",1:"Accepted",2:"Rejected",3:"Closed"}
    status=[]
    for x in stat:
        status.append(stat_dict[x])
    req_stat_count=[req.service_status_count for req in service_stat_req]
    return render_template("summary_customer.html",cust_obj=cust_obj,status=status,req_stat_count=req_stat_count)
