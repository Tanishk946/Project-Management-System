from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, SelectMultipleField, IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from project.models import Student, Guide, CoOrdinator, User, Season, Team

def number_check(form,field):
    if(field.data.isdigit() == False):
        raise(ValidationError(f'{field.name} must be a Valid Number'))

def password_check(form,field):

    k = field.data
    if(len(k) < 8):
        raise(ValidationError(f'{field.name} must be at least 8 characters'))
    l,u,d,sp = 0,0,0,0
    
    for i in k:
        if(ord(i) >= 48 and ord(i) <= 57):
            d = 1
        elif(ord(i) >= 65 and ord(i) <= 90):
            u = 1
        elif(ord(i) >= 97 and ord(i) <= 122):
            l = 1
        elif( (ord(i) >= 32 and ord(i) <= 47) or (ord(i) >= 58 and ord(i) <= 64) or (ord(i) >= 91 and ord(i) <= 96) or (ord(i) >= 123 and ord(i) <= 126)):
            sp = 1

    if(l == 0 or d == 0 or u == 0 or sp == 0):
        raise(ValidationError('Password must contain UpperCase, LowerCase, Digit and Special Char'))

def regnum_check(form,field):
    k = field.data

    if(len(k) != 12):
        raise(ValidationError('Registration Number must be of 12 Characters'))
        return(None)

    if( (k[0] != '3') or (k[1:3].isdigit() == False) or (k[3] != '1') or (k[4] != '2') or (k[5] != '6') or (k[6] != '5')):
        raise(ValidationError('Invalid Registration Number'))
        return(None)

    if(k.isdigit() == False):
        if(k.count('L') > 1):
            raise(ValidationError('Invalid Registration Number'))
            return(None)
        
        for i in k:
            if( (ord(i) >= 65 and ord(i) <= 90) or (ord(i) >= 97 and ord(i) <= 122)):
                if(ord(i) != ord('L')):
                    raise(ValidationError('Invalid Registration Number'))
                    return(None)
                
                elif(ord(i) == ord('l')):
                    raise(ValidationError('L must be in capitals for Lateral Students'))
                    return(None)
            
class StudentRegisterForm(FlaskForm):

    def validate_reg_id(self,reg_id_to_check):
        student = Student.query.filter_by(reg_id=reg_id_to_check.data).first()
        if(student):
            raise(ValidationError('User with given Registration Number already Exists! Try Another Registration Number'))
    
    def validate_email(self,email_to_check):
        email = Student.query.filter_by(email=email_to_check.data).first()
        if(email):
            raise(ValidationError('Student with given Email already Exists! Try Another Email'))
        
        if('anits.edu.in' not in email_to_check.data):
            raise(ValidationError('Email must be related to ANITS College'))

    name = StringField(label='Name : ',validators=[DataRequired(),Length(max=50)])
    email = StringField(label='Email : ',validators=[DataRequired(),Email(),Length(max=50)])
    reg_id = StringField(label='Register No : ',validators=[DataRequired(),regnum_check])

    dept = SelectField(label='Dept : ',choices=[('CSE','CSE'),('IT','IT'),('ECE','ECE'),('EEE','EEE'),('MECH','MECH'),('CHEM','CHEM'),('CIVIL','CIVIL')],validators=[DataRequired()])
    
    batch = SelectField(label='Batch : ',choices=[('2018','2018-2022'),('2019','2019-2023'),('2020','2020-2024'),('2021','2021-2025')],validators=[DataRequired()])
    
    section = SelectField(label='Section : ',choices=[('A','A'),('B','B'),('C','C'),('D','D')],validators=[DataRequired()])
    
    password1 = PasswordField(label='Password : ',validators=[DataRequired(),Length(min=8,max=80),password_check])
    password2 = PasswordField(label='Confirm Password : ',validators=[EqualTo('password1','Confirm Password Should match with Password'),DataRequired(),Length(min=8,max=80)])

    submit = SubmitField(label='Submit')

class GuideRegisterForm(FlaskForm):

    def validate_email(self,email_to_check):
        email = Guide.query.filter_by(email=email_to_check.data).first()
        if(email):
            raise(ValidationError('Guide with given Email already Exists! Try Another Email'))
        
        if('anits.edu.in' not in email_to_check.data):
            raise(ValidationError('Email must be related to ANITS College'))
    
    name = StringField(label='Name : ',validators=[DataRequired(),Length(max=50)])
    email = StringField(label='Email : ',validators=[DataRequired(),Email(),Length(max=50)])

    dept = SelectField(label='Dept : ',choices=[('CSE','CSE'),('IT','IT'),('ECE','ECE'),('EEE','EEE'),('MECH','MECH'),('CHEM','CHEM'),('CIVIL','CIVIL')],validators=[DataRequired()])

    mobile = StringField(label='Mobile : ',validators=[DataRequired(),Length(min=10,max=10),number_check])

    password1 = PasswordField(label='Password : ',validators=[DataRequired(),Length(min=8,max=80),password_check])
    password2 = PasswordField(label='Confirm Password : ',validators=[EqualTo('password1','Confirm Password Should match with Password'),DataRequired(),Length(min=8,max=80)])

    submit = SubmitField(label='Submit')

class CoOrdinatorRegisterForm(FlaskForm):
    
    def validate_email(self,email_to_check):
        email = CoOrdinator.query.filter_by(email=email_to_check.data).first()
        if(email):
            raise(ValidationError('Co-Ordinator with given Email already Exists! Try Another Email'))
        
        if('anits.edu.in' not in email_to_check.data):
            raise(ValidationError('Email must be related to ANITS College'))
    
    name = StringField(label='Name : ',validators=[DataRequired(),Length(max=50)])
    email = StringField(label='Email : ',validators=[DataRequired(),Email(),Length(max=50)])

    dept = SelectField(label='Dept : ',choices=[('CSE','CSE'),('IT','IT'),('ECE','ECE'),('EEE','EEE'),('MECH','MECH'),('CHEM','CHEM'),('CIVIL','CIVIL')],validators=[DataRequired()])

    mobile = StringField(label='Mobile : ',validators=[DataRequired(),Length(min=10,max=10),number_check])

    password1 = PasswordField(label='Password : ',validators=[DataRequired(),Length(min=8,max=80),password_check])
    password2 = PasswordField(label='Confirm Password : ',validators=[EqualTo('password1','Confirm Password Should match with Password'),DataRequired(),Length(min=8,max=80)])

    submit = SubmitField(label='Submit')

class LoginForm(FlaskForm):

    email = StringField(label='Email : ',validators=[DataRequired(),Email()])
    password = PasswordField(label='Password : ',validators=[DataRequired()])
    user_type = SelectField(label='Login As : ',choices=[('Student','Student'),('Guide','Guide'),('CoOrdinator','CoOrdinator')],validators=[DataRequired()])

    submit = SubmitField(label='Submit')

class SeasonForm(FlaskForm):

    def validate_batchdept(self,batch_to_check):
        
        batchdept = Season.query.filter_by(batch=batch_to_check.data).first()
        if(batchdept):
            raise(ValidationError(f'Batch Already Exists'))

    batch = SelectField(label='Batch : ',choices=[('2018','2018-2022'),('2019','2019-2023'),('2020','2020-2024'),('2021','2021-2025')],validators=[DataRequired()])

    dept = SelectField(label='Dept : ',choices=[('CSE','CSE'),('IT','IT'),('ECE','ECE'),('EEE','EEE'),('MECH','MECH'),('CHEM','CHEM'),('CIVIL','CIVIL')],validators=[DataRequired()])

    submit = SubmitField(label='Create')

class SeasonQueryForm(FlaskForm):

    seasons = SelectField(label='Season : ',choices=[],validators=[DataRequired()])
    submit = SubmitField(label='Submit')

class CreateTeamForm(FlaskForm):

    team = StringField(label='Team Name : ',validators=[DataRequired()])
    CGPA = SelectField(label='CGPA',choices=[('>8.5'),('7.0 to 8.5'),('<7.0')],validators=[DataRequired()])
    members = SelectMultipleField(label='Hold Control for Multi-Select',choices=[],validators=[DataRequired()])
    submit = SubmitField(label='Create')

class SwapStudentsForm(FlaskForm):

    student1 = SelectField(label='Student 1 : ',validators=[DataRequired()])
    student2 = SelectField(label='Student 2 : ',validators=[DataRequired()])
    submit = SubmitField(label='Swap Students')

class AssignGuideForm(FlaskForm):

    team = SelectField(label='Select Team to be Assigned : ',validators=[DataRequired()])
    guide = SelectField(label='Select Guide to be Assigned : ',validators=[DataRequired()])
    submit = SubmitField(label='Assign')

class UploadFileForm(FlaskForm):
    submit = SubmitField(label='Upload File')

class AddNewWorkForm(FlaskForm):
    work_name = StringField(label='Work Name',validators=[DataRequired()])
    work_description = StringField(label='Work Description',validators=[DataRequired()])
    submit = SubmitField(label='Assign')

class SubmitFileForm(FlaskForm):
    submit = SubmitField(label='Submit')

class AssignMarksForm(FlaskForm):
    marks = IntegerField(validators=[DataRequired('Marks must be a number')])
    submit = SubmitField(label='Assign')

class RequestResetForm(FlaskForm):
    email = StringField(label='Email : ',validators=[DataRequired(),Email(),Length(max=50)])
    submit = SubmitField(label='Request Password Reset')
    def validate_email(self,email_to_check):
        email = Student.query.filter_by(email=email_to_check.data).first()
        if email is None:
            raise(ValidationError('Email Not Found in the database. Please Register!!!'))

class ResetPasswordForm(FlaskForm):
    password1 = PasswordField(label='Password : ',validators=[DataRequired(),Length(min=8,max=80),password_check])
    password2 = PasswordField(label='Confirm Password : ',validators=[EqualTo('password1','Confirm Password Should match with Password'),DataRequired(),Length(min=8,max=80)])
    submit = SubmitField(label='Reset Password')

