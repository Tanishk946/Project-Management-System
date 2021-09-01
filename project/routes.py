import uuid
from project import app, db, bcrypt, mail
from flask import render_template, redirect, url_for, flash, request, session, send_file
from project.models import Student, Guide, CoOrdinator, User, Season, Team, FileContents, Works, SubmissionStatus
from project.forms import StudentRegisterForm, GuideRegisterForm, CoOrdinatorRegisterForm, LoginForm, SeasonForm, SeasonQueryForm, CreateTeamForm, SwapStudentsForm, AssignGuideForm, UploadFileForm, AddNewWorkForm, SubmitFileForm, AssignMarksForm, ResetPasswordForm, RequestResetForm
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from io import BytesIO
from datetime import date



@app.route('/')
@app.route('/home')
def home_page():
    return render_template("home.html")

@app.route('/login',methods=['GET','POST'])
def login_page():
    if(current_user.is_authenticated):
        if(current_user.role == 'Student'):
            return(redirect(url_for('student_dashboard_page')))
        elif(current_user.role == 'Guide'):
            return(redirect(url_for('guide_dashboard_page')))
        elif(current_user.role == 'CoOrdinator'):
            return(redirect(url_for('coordinator_dashboard_page')))

    login_form = LoginForm()

    if(request.method == 'POST'):
        if(login_form.validate_on_submit()):
            if(login_form.user_type.data == 'Student'):
                attempted_user = User.query.filter_by(email=login_form.email.data).first()
                attempted_student = Student.query.filter_by(email=login_form.email.data).first()

                if(attempted_user and attempted_student and attempted_user.check_password_correction(attempted_password=login_form.password.data)):
                    login_user(attempted_user)
                    flash(f'Success! You are Logged in as Student {attempted_user.email}', category='success')
                else:
                    flash('Invalid Credentials! Please try again', category='danger')

                return redirect(url_for('student_dashboard_page'))

            elif(login_form.user_type.data == 'Guide'):
                attempted_user = User.query.filter_by(email=login_form.email.data).first()
                attempted_guide = Guide.query.filter_by(email=login_form.email.data).first()

                if(attempted_user and attempted_guide and attempted_user.check_password_correction(attempted_password=login_form.password.data)):
                    login_user(attempted_user)
                    flash(f'Success! You are Logged in as Guide : {attempted_user.email}', category='success')
                else:
                    flash('Invalid Credentials! Please try again', category='danger')

                return redirect(url_for('guide_dashboard_page'))

            elif(login_form.user_type.data == 'CoOrdinator'):
                attempted_user = User.query.filter_by(email=login_form.email.data).first()
                attempted_coordinator = CoOrdinator.query.filter_by(email=login_form.email.data).first()

                if(attempted_user and attempted_coordinator and attempted_user.check_password_correction(attempted_password=login_form.password.data)):
                    login_user(attempted_user)
                    flash(f'Success! You are Logged in as Co-Ordinator : {attempted_user.email}', category='success')
                else:
                    flash('Invalid Credentials! Please try again', category='danger')

                return redirect(url_for('coordinator_dashboard_page'))

            return render_template("login.html",login_form = login_form)
        
    else:
        return render_template("login.html",login_form = login_form)


@app.route('/register')
def register_page():
    if(current_user.is_authenticated):
        if(current_user.role == 'Student'):
            return(redirect(url_for('student_dashboard_page')))
        elif(current_user.role == 'Guide'):
            return(redirect(url_for('guide_dashboard_page')))
        elif(current_user.role == 'CoOrdinator'):
            return(redirect(url_for('coordinator_dashboard_page')))
    
    return render_template("register.html")

@app.route('/student_register', methods=['GET','POST'])
def student_register_page():
    if(current_user.is_authenticated):
        if(current_user.role == 'Student'):
            return(redirect(url_for('student_dashboard_page')))
        elif(current_user.role == 'Guide'):
            return(redirect(url_for('guide_dashboard_page')))
        elif(current_user.role == 'CoOrdinator'):
            return(redirect(url_for('coordinator_dashboard_page')))

    student_register_form = StudentRegisterForm()

    if(request.method == "POST"):
        if(student_register_form.validate_on_submit()):
            temp = student_register_form.password1.data
            
            password_hash = bcrypt.generate_password_hash(temp).decode('utf-8')

            student_to_create = Student(name=student_register_form.name.data,
                                     reg_id=student_register_form.reg_id.data,
                                     email=student_register_form.email.data,
                                     dept=student_register_form.dept.data,
                                     batch=student_register_form.batch.data,
                                     section=student_register_form.section.data,
                                     password_hash=password_hash)

            user_to_create = User(email=student_register_form.email.data,
                                  role='Student',
                                  password_hash=password_hash)

            db.session.add(student_to_create)
            db.session.add(user_to_create)
            db.session.commit()
            flash("Account Successfully Created",category="success")
            return(redirect(url_for('login_page'))) # ***
    
        if(student_register_form.errors != {}):
            for err_msg in student_register_form.errors.values():
                flash(f'There was an error with creating user : {err_msg}',category='danger')

        return render_template("student_register.html",student_register_form=student_register_form)

    else:
        return render_template("student_register.html",student_register_form=student_register_form)

@app.route('/guide_register',methods=['GET','POST'])
def guide_register_page():
    if(current_user.is_authenticated):
        if(current_user.role == 'Student'):
            return(redirect(url_for('student_dashboard_page')))
        elif(current_user.role == 'Guide'):
            return(redirect(url_for('guide_dashboard_page')))
        elif(current_user.role == 'CoOrdinator'):
            return(redirect(url_for('coordinator_dashboard_page')))

    guide_register_form = GuideRegisterForm()

    if(request.method == "POST"):
        if(guide_register_form.validate_on_submit()):
            temp = guide_register_form.password1.data

            password_hash = bcrypt.generate_password_hash(temp).decode('utf-8')

            guide_to_create = Guide(name=guide_register_form.name.data,
                                     email=guide_register_form.email.data,
                                     dept=guide_register_form.dept.data,
                                     mobile=guide_register_form.mobile.data,
                                     password_hash=password_hash)

            user_to_create = User(email=guide_register_form.email.data,
                                  role='Guide',
                                  password_hash=password_hash)

            db.session.add(guide_to_create)
            db.session.add(user_to_create)
            db.session.commit()
            flash("Account Successfully Created",category="success")
            return(redirect(url_for('login_page'))) # ***
    
        if(guide_register_form.errors != {}):
            for err_msg in guide_register_form.errors.values():
                flash(f'There was an error with creating user : {err_msg}',category='danger')

        return render_template("guide_register.html",guide_register_form=guide_register_form)

    else:
        return render_template("guide_register.html",guide_register_form=guide_register_form)
    
@app.route('/coordinator_register',methods=['GET','POST'])
def coordinator_register_page():
    if(current_user.is_authenticated):
        if(current_user.role == 'Student'):
            return(redirect(url_for('student_dashboard_page')))
        elif(current_user.role == 'Guide'):
            return(redirect(url_for('guide_dashboard_page')))
        elif(current_user.role == 'CoOrdinator'):
            return(redirect(url_for('coordinator_dashboard_page')))

    coordinator_register_form = CoOrdinatorRegisterForm()

    if(request.method == "POST"):
        if(coordinator_register_form.validate_on_submit()):
            temp = coordinator_register_form.password1.data

            password_hash = bcrypt.generate_password_hash(temp).decode('utf-8')

            coordinator_to_create = CoOrdinator(name=coordinator_register_form.name.data,
                                     email=coordinator_register_form.email.data,
                                     dept=coordinator_register_form.dept.data,
                                     mobile=coordinator_register_form.mobile.data,
                                     password_hash=password_hash)

            user_to_create = User(email=coordinator_register_form.email.data,
                                  role='CoOrdinator',
                                  password_hash=password_hash)

            db.session.add(coordinator_to_create)
            db.session.add(user_to_create)
            db.session.commit()
            flash("Account Successfully Created",category="success")
            return(redirect(url_for('login_page'))) # ***
    
        if(coordinator_register_form.errors != {}):
            for err_msg in coordinator_register_form.errors.values():
                flash(f'There was an error with creating user : {err_msg}',category='danger')

        return render_template("coordinator_register.html",coordinator_register_form=coordinator_register_form)

    else:
        return render_template("coordinator_register.html",coordinator_register_form=coordinator_register_form)
    

@app.route("/logout")
def logout_page():
    logout_user()
    flash("You Have Been Logged Out!", category="info")
    return(redirect(url_for('home_page')))

@app.route("/coordinator_dashboard",methods=['GET','POST'])
@login_required
def coordinator_dashboard_page():
    coordinator = CoOrdinator.query.filter_by(email=current_user.email).first()
    seasons = Season.query.filter_by(coordinator=current_user.email)

    season_form = SeasonForm()
    if(request.method == 'POST'):
        if(season_form.validate_on_submit()):

            if(coordinator.can_create(season_form.batch.data+season_form.dept.data)):
                season_to_create = Season(batch=season_form.batch.data+season_form.dept.data,
                                      coordinator=current_user.email)

                coordinator.update_coordinator_for(season_form.batch.data+season_form.dept.data)
                db.session.add(season_to_create)
                db.session.commit()
                flash(f'Season for {season_form.batch.data} {season_form.dept.data} has been created',category='success')
                return(redirect(url_for('coordinator_dashboard_page')))   

            else:
                flash('Season Already Exists',category='danger') 
            
        if(season_form.errors != {}):
            for err_msg in season_form.errors.values():
                flash(f'There was an error with creating Season : {err_msg}',category='danger')

        return(render_template("coordinator_dashboard.html",coordinator=coordinator,seasons=seasons,season_form=season_form))

    if(request.method == 'GET'):
        return(render_template("coordinator_dashboard.html",coordinator=coordinator,seasons=seasons,season_form=season_form))

@app.route('/edit_batch/<batch_name>',methods=['GET','POST'])
@login_required
def edit_batch_page(batch_name):
    batch=batch_name[0:4]
    dept=batch_name[4::]
    coordinator = CoOrdinator.query.filter_by(email=current_user.email).first()

    create_team_form = CreateTeamForm()
    
    create_team_form.members.choices = [(student.email,student.name+' '+student.reg_id) for student in Student.query.filter_by(batch=batch,dept=dept,team=None).all()]

    swap_students_form = SwapStudentsForm()
    swap_students_form.student1.choices = [(student.email,student.name+' '+student.reg_id) for student in Student.query.filter(Student.batch==batch,Student.dept==dept,Student.team != None).all()]
    swap_students_form.student2.choices = [(student.email,student.name+' '+student.reg_id) for student in Student.query.filter(Student.batch==batch,Student.dept==dept,Student.team != None).all()]

    if(request.method == 'POST'):
        if(create_team_form.validate_on_submit()):
            my_team_name = batch_name+'-'+create_team_form.team.data
            if(coordinator.can_create_team(my_team_name)):
                data = []
                for i in create_team_form.members.data:
                    data.append(i)
                    current_student = Student.query.filter_by(email=i).first()
                    current_student.team = my_team_name

                my_string = '*'.join(data)
                team_to_create = Team(team=my_team_name,
                                      members=my_string,
                                      batch=batch,
                                      dept=dept)

                db.session.add(team_to_create)
                db.session.commit()
                flash(f'Team for {my_string} has been created',category='success')
                return(redirect(url_for('coordinator_dashboard_page')))
            
            else:
                flash(f'Team Name {create_team_form.team.data} Already Exists',category='danger')

        elif(swap_students_form.validate_on_submit()):
            
            s1,s2 = swap_students_form.student1.data,swap_students_form.student2.data
            std1 = Student.query.filter_by(email=s1).first()
            std2 = Student.query.filter_by(email=s2).first()

            coordinator.swap_students(std1,std2)

            flash(f'Given Students have been Swapped Teams',category='success')
            return(redirect(url_for('coordinator_dashboard_page')))

        if(create_team_form.errors != {}):
            for err_msg in create_team_form.errors.values():
                flash(f'There was an error in Creating Teams : {err_msg}',category='danger')

        if(swap_students_form.errors != {}):
            for err_msg in swap_students_form.errors.values():
                flash(f'There was an error in Swapping Students : {err_msg}',category='danger')
        
        return(render_template('edit_batch.html',coordinator=coordinator,create_team_form=create_team_form,swap_students_form=swap_students_form))

    if(request.method == 'GET'):
        return(render_template('edit_batch.html',coordinator=coordinator,create_team_form=create_team_form,swap_students_form=swap_students_form))

@app.route('/view_student/<batch_name>',methods=['GET','POST'])
@login_required
def view_student_page(batch_name):
    batch = batch_name[0:4]
    dept = batch_name[4::]
    students = Student.query.filter_by(batch=batch,dept=dept)
    return render_template("view_student.html",students=students)

@app.route('/assign_guides/<batch_name>',methods=['GET','POST'])
@login_required
def assign_guides_page(batch_name):
    batch = batch_name[0:4]
    dept = batch_name[4::]
    coordinator = CoOrdinator.query.filter_by(email=current_user.email).first()

    assign_guide_form = AssignGuideForm()
    assign_guide_form.guide.choices = [('','')] + [(guide.email,guide.name) for guide in Guide.query.filter_by(dept=dept).all()]

    assign_guide_form.team.choices = [('','')] + [(t.team,t.team) for t in Team.query.filter_by(dept=dept,guide=None,batch=batch).all()]

    if(request.method == 'POST'):
        if(assign_guide_form.validate_on_submit()):

            coordinator.link_student_guide_team(assign_guide_form.team.data,assign_guide_form.guide.data)
            db.session.commit()
            flash(f'Guide : {assign_guide_form.guide.data} has been assigned to Team : {assign_guide_form.team.data}',category='success')
            return(redirect(url_for('coordinator_dashboard_page')))
        
        if(assign_guide_form.errors != {}):
            for err_msg in assign_guide_form.errors.values():
                flash(f'There was an error in assigning the Guides : {err_msg}',category='danger')
        
        return(render_template("assign_guides.html",assign_guide_form=assign_guide_form))

    if(request.method == 'GET'):
        return(render_template("assign_guides.html",assign_guide_form=assign_guide_form))

@app.route("/guide_dashboard")
@login_required
def guide_dashboard_page():
    guide = Guide.query.filter_by(email=current_user.email).first()
    my_teams = Team.query.filter_by(guide=current_user.email).all()

    return(render_template("guide_dashboard.html",guide=guide,my_teams=my_teams))

@app.route('/view_team/<team_name>')
@login_required
def view_team_page(team_name):
    current_team = Student.query.filter_by(team=team_name).all()
    guide = Student.query.filter_by(team=team_name).first().guide

    return(render_template("view_team.html",team_name=team_name,current_team=current_team,guide=guide))

@app.route('/dummy_file_upload',methods=['GET','POST'])
def dummy_file_page():
    
    upload_file_form = UploadFileForm()
    files = FileContents.query.all()

    if(request.method == 'POST'):
        if(upload_file_form.validate_on_submit()):
            if(request.files):

                file = request.files['file']
                filename = file.filename
                newFile = FileContents(name=filename,data=file.read())
                db.session.add(newFile)
                db.session.commit()

                return(redirect(url_for('dummy_file_page')))
    
        return(render_template('dummy_file_upload.html',upload_file_form=upload_file_form,files=files))

    return(render_template('dummy_file_upload.html',upload_file_form=upload_file_form,files=files))

@app.route('/download_guide_file/<work_id>/<file_name>')
def download_guide_file_page(work_id,file_name):
    file_data = Works.query.filter_by(id=work_id).first()
    return(send_file(BytesIO(file_data.any_file),attachment_filename=file_name))

@app.route('/add_work/<team_name>',methods=['GET','POST'])
@login_required
def add_work_page(team_name):
    guide = Guide.query.filter_by(email=current_user.email).first()
    add_new_work_form = AddNewWorkForm()
    s = date.today()
    today_date = str(s.day) + '-' + str(s.month) + '-' + str(s.year) 

    previous_works = Works.query.filter_by(guide=guide.email,team_assigned=team_name)

    if(request.method == 'POST'):
        if(add_new_work_form.validate_on_submit()):
            file_name = 'No File Attached'
            my_file = None
            if(request.files['file']):
                my_file = request.files['file']
                file_name = my_file.filename
                k = my_file.read()
                work_to_assign = Works(work_name=add_new_work_form.work_name.data,
                                      work_description=add_new_work_form.work_description.data,
                                      date_given=today_date,
                                      any_file=k,
                                      file_name=file_name,
                                      guide=guide.email,
                                      team_assigned=team_name)
                db.session.add(work_to_assign)
                db.session.commit()

                work_id = Works.query.order_by(Works.id.desc()).first().id
                team_mates = Team.query.filter_by(team=team_name).first().members
                team_mates = list(team_mates.split('*'))

                for i in team_mates:
                    sub = SubmissionStatus(work_id=work_id,
                                           student=i,
                                           work_name=add_new_work_form.work_name.data,
                                           work_description=add_new_work_form.work_description.data,
                                           guide=guide.email,
                                           date_given=today_date,
                                           any_file=k,
                                           any_file_name=file_name,
                                           date_submitted='Not Yet')
                    db.session.add(sub)
                
                db.session.commit()
                flash('Work Assigned Successfully',category='success')
                return(redirect(url_for('guide_dashboard_page')))

            else:
                work_to_assign = Works(work_name=add_new_work_form.work_name.data,
                                      work_description=add_new_work_form.work_description.data,
                                      date_given=today_date,
                                      any_file=None,
                                      file_name=file_name,
                                      guide=guide.email,
                                      team_assigned=team_name)
                db.session.add(work_to_assign)
                db.session.commit()
                
                work_id = Works.query.order_by(Works.id.desc()).first().id
                team_mates = Team.query.filter_by(team=team_name).first().members
                team_mates = list(team_mates.split('*'))

                for i in team_mates:
                    sub = SubmissionStatus(work_id=work_id,
                                           student=i,
                                           work_name=add_new_work_form.work_name.data,
                                           work_description=add_new_work_form.work_description.data,
                                           guide=guide.email,
                                           date_given=today_date,
                                           any_file=None,
                                           any_file_name = file_name,
                                           date_submitted='Not Yet')
                    db.session.add(sub)
                
                db.session.commit()
                flash('Work Assigned Successfully',category='success')
                return(redirect(url_for('guide_dashboard_page')))

            if(add_new_work_form.errors != {}):
                for err_msg in add_new_work_form.errors.values():
                    flash(f'There was an error in assigning the work : {err_msg}',category='danger')
        
            return(render_template('add_work.html',team_name=team_name,guide=guide,add_new_work_form=add_new_work_form,previous_works=previous_works))

    if(request.method == 'GET'):
        return(render_template('add_work.html',team_name=team_name,guide=guide,add_new_work_form=add_new_work_form,previous_works=previous_works))

@app.route('/view_status/<team_name>/<work_id>',methods=['GET','POST'])
def view_status_page(team_name,work_id):

    submission_pending_students = SubmissionStatus.query.filter_by(did_submit='NO',work_id=work_id).all()
    
    pending_for_correction = SubmissionStatus.query.filter_by(did_submit='YES',work_id=work_id,marks_given=-1).all()
    
    completed_corrections = SubmissionStatus.query.filter(SubmissionStatus.did_submit == 'YES',SubmissionStatus.work_id == work_id,SubmissionStatus.marks_given != 1).all()

    return(render_template("view_status.html",team_name=team_name,work_id=work_id,submission_pending_students=submission_pending_students,pending_for_correction=pending_for_correction,completed_corrections=completed_corrections))

@app.route("/student_dashboard")
@login_required
def student_dashboard_page():
    student = Student.query.filter_by(email=current_user.email).first()
    pending_works = SubmissionStatus.query.filter_by(student=student.email,guide=student.guide,did_submit='NO').all()
    completed_works = SubmissionStatus.query.filter_by(student=student.email,guide=student.guide,did_submit='YES').all()

    return(render_template("student_dashboard.html",student=student,pending_works=pending_works,completed_works=completed_works))

@app.route('/add_submission/<work_id>',methods=['GET','POST'])
@login_required
def add_submission_page(work_id):
    student = Student.query.filter_by(email=current_user.email).first()
    submission = SubmissionStatus.query.filter_by(work_id=work_id,student=student.email).first()

    add_submission_form = SubmitFileForm()

    if(request.method == 'POST'):
        if(add_submission_form.validate_on_submit()):

            my_file = request.files['file']
            file_name = my_file.filename
            k = my_file.read()
            s = date.today()
            today_date = str(s.day) + '-' + str(s.month) + '-' + str(s.year)

            submission_object = SubmissionStatus.query.filter_by(work_id=work_id,student=student.email).first()
            submission_object.date_submitted = today_date
            submission_object.file_attached = k
            submission_object.did_submit = 'YES'
            submission_object.submitted_file_name = file_name

            db.session.commit()
            flash('Submission Successfully Added',category='success')
            return(redirect(url_for('student_dashboard_page')))
        
        if(add_submission_form.errors != {}):
            for err_msg in add_submission_form.errors.values():
                flash(f'There was an error in submitting the work : {err_msg}',category='danger')

        return(render_template('add_submission.html',submission=submission,student=student,add_submission_form=add_submission_form))        

    if(request.method == 'GET'):
        return(render_template('add_submission.html',submission=submission,student=student,add_submission_form=add_submission_form))

@app.route('/download_student_file/<submission_id>/<file_name>')
def download_student_file_page(submission_id,file_name):
    file_data = SubmissionStatus.query.filter_by(id=submission_id).first()
    return(send_file(BytesIO(file_data.file_attached),attachment_filename=file_name))

@app.route('/credit_marks/<submission_id>',methods=['GET','POST'])
def credit_marks_page(submission_id):
    marks_form = AssignMarksForm()
    submission = SubmissionStatus.query.filter_by(id=submission_id).first()

    if(request.method == 'POST'):
        if(marks_form.validate_on_submit()):
            current_object = SubmissionStatus.query.filter_by(id=submission_id).first()
            current_object.marks_given = marks_form.marks.data
            db.session.commit()
            flash('Marks Successfully Assigned',category='success')
            return(redirect(url_for('guide_dashboard_page')))
        
        if(marks_form.errors != {}):
            for err_msg in marks_form.errors.values():
                flash(f'There was an error in Assigning Makrs : {err_msg}',category='danger')
        
        return(render_template('credit_marks.html',marks_form=marks_form,submission=submission))

    if(request.method == 'GET'):
        return(render_template('credit_marks.html',marks_form=marks_form,submission=submission))

def send_reset_email(user):
    token=user.get_reset_token()
    msg=Message('Password Reset Request',sender='admin.18.cse@anits.edu.in',recipients=[user.email])
    msg.body=f'''To reset your password, visit the following link
{url_for('reset_token',token=token,_external=True)}

Ignore this mail if password change is unnecessary
'''
    mail.send(msg)

@app.route("/forgot_password",methods=['GET','POST'])
def forgot_password_request():
    if(current_user.is_authenticated):
        if(current_user.role == 'Student'):
            return(redirect(url_for('student_dashboard_page')))
        elif(current_user.role == 'Guide'):
            return(redirect(url_for('guide_dashboard_page')))
        elif(current_user.role == 'CoOrdinator'):
            return(redirect(url_for('coordinator_dashboard_page')))
    form=RequestResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An Email is sent to reset your password','info')
        return redirect(url_for('login_page'))
    return render_template('forgot_password.html',title='Reset Password',form=form)
    
@app.route("/forgot_password/<token>",methods=['GET','POST'])
def reset_token(token):
    if(current_user.is_authenticated):
        if(current_user.role == 'Student'):
            return(redirect(url_for('student_dashboard_page')))
        elif(current_user.role == 'Guide'):
            return(redirect(url_for('guide_dashboard_page')))
        elif(current_user.role == 'CoOrdinator'):
            return(redirect(url_for('coordinator_dashboard_page')))
    user=User.verify_reset_token(token)
    if user is None:
        flash("Reset Link Expired",'warning')
        return redirect(url_for('forgot_password_request'))
    form=ResetPasswordForm()
    if(form.validate_on_submit()):
            temp = form.password1.data
            password_hash = bcrypt.generate_password_hash(temp).decode('utf-8')
            user.password=password_hash
            db.session.commit()
            flash("Password Changed Successfully",category="success")
            return(redirect(url_for('login_page')))
    return render_template('password_reset.html',title='Reset password',form=form)    