from project import db, login_manager, app
from project import bcrypt
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return(User.query.get(int(user_id)))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(length=50),nullable=False)
    role = db.Column(db.String(length=20),nullable=False)
    password_hash = db.Column(db.String(length=100),nullable=False)

    def get_reset_token(self,expires_sec=3600):
        s=Serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s=Serializer(app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def check_password_correction(self,attempted_password):
        return(bcrypt.check_password_hash(self.password_hash,attempted_password))
    
class Student(db.Model,UserMixin):
    name = db.Column(db.String(length=50),nullable=False)
    email = db.Column(db.String(length=50),primary_key=True)
    reg_id = db.Column(db.String(length=13),nullable=False,unique=True)
    dept = db.Column(db.String(length=7),nullable=False)
    batch = db.Column(db.String(length=15),nullable=False)
    section = db.Column(db.String(length=2),nullable=False)
    password_hash = db.Column(db.String(length=100),nullable=False)
    guide = db.Column(db.String(length=50),nullable=True)
    team = db.Column(db.String(length=50),nullable=True)

    def check_password_correction(self,attempted_password):
        return(bcrypt.check_password_hash(self.password_hash,attempted_password))
    
class Guide(db.Model,UserMixin):
    name = db.Column(db.String(length=50),nullable=False)
    email = db.Column(db.String(length=50),primary_key=True)
    dept = db.Column(db.String(length=7),nullable=False)
    mobile = db.Column(db.String(length=10),nullable=False)
    password_hash = db.Column(db.String(length=100),nullable=False)
    guide_for = db.Column(db.String(length=5000))

    def check_password_correction(self,attempted_password):
        return(bcrypt.check_password_hash(self.password_hash,attempted_password))

class CoOrdinator(db.Model,UserMixin):
    name = db.Column(db.String(length=50),nullable=False)
    email = db.Column(db.String(length=50),primary_key=True)
    dept = db.Column(db.String(length=7),nullable=False)
    mobile = db.Column(db.String(length=10),nullable=False)
    password_hash = db.Column(db.String(length=100),nullable=False)
    coordinator_for = db.Column(db.String(length=1000),nullable=True)

    def check_password_correction(self,attempted_password):
        return(bcrypt.check_password_hash(self.password_hash,attempted_password))

    def can_create(self,batch_name):
        data = []
        temp = self.coordinator_for
        if(temp != None and temp != ''):
            data = list(temp.split('*'))
        
        if(batch_name in data):
            return(False)
        
        dummy = Season.query.filter_by(batch=batch_name).first()
        if(dummy):
            return(False)
        
        return(True)
    
    def update_coordinator_for(self,batch_name):
        data = []
        temp = self.coordinator_for
        if(temp != None and temp != ''):
            data = list(temp.split('*'))
        
        data.append(batch_name)
        replacer = '*'.join(data)

        self.coordinator_for = replacer

        db.session.commit()
    
    def swap_students(self,student1_obj,student2_obj):

        s1,s2 = student1_obj.email,student2_obj.email
        t1,t2 = student1_obj.team,student2_obj.team
        data1,data2 = [],[]

        team1_obj = Team.query.filter_by(team=t1).first()
        team2_obj = Team.query.filter_by(team=t2).first()

        temp1 = team1_obj.members
        temp2 = team2_obj.members

        if(temp1 != None and temp1 != ''):
            data1 = list(temp1.split('*'))
        if(temp2 != None and temp2 != ''):
            data2 = list(temp2.split('*'))
        
        if(s1 in data1):
            del(data1[data1.index(s1)])
        if(s2 in data2):
            del(data2[data2.index(s2)])
        
        data1.append(s2)
        data2.append(s1)

        replacer1 = '*'.join(data1)
        replacer2 = '*'.join(data2)

        student1_obj.team = t2
        student2_obj.team = t1

        team1_obj.members = replacer1
        team2_obj.members = replacer2

        db.session.commit()
    
    def can_create_team(self,team_name):

        checker = Team.query.filter_by(team=team_name).first()

        if(checker):
            return(False)
        else:
            return(True)
    
    def link_student_guide_team(self,team,guide):

        data = []
        team_obj = Team.query.filter_by(team=team).first()
        temp = team_obj.members

        if(temp != None and temp != ''):
            data = list(temp.split('*'))
        
        for i in data:
            student = Student.query.filter_by(email=i).first()
            student.guide = guide
        
        data = []
        guide_obj = Guide.query.filter_by(email=guide).first()

        temp = guide_obj.guide_for
        if(temp != None and temp != ''):
            data = list(temp.split('*'))
        
        data.append(team)
        replacer = '*'.join(data)

        guide_obj.guide_for = replacer

        team_obj.guide = guide

        db.session.commit()

class Season(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    batch = db.Column(db.String(length=20),unique=True,nullable=False)
    coordinator = db.Column(db.String(length=50),nullable=False)

class Team(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    team = db.Column(db.String(length=20),nullable=False,unique=True)
    members = db.Column(db.String(length=200),nullable=False)
    guide = db.Column(db.String(length=20))
    dept = db.Column(db.String(length=10),nullable=False)
    batch = db.Column(db.String(length=6),nullable=False)

class FileContents(db.Model):

    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)

class Works(db.Model):

    id = db.Column(db.Integer(),primary_key=True)
    work_name = db.Column(db.String(length=30),nullable=False)
    work_description = db.Column(db.String(length=150),nullable=False)
    date_given = db.Column(db.String(length=10),nullable=False)
    any_file = db.Column(db.LargeBinary)
    file_name = db.Column(db.String(length=50),nullable=False)
    guide = db.Column(db.String(length=50),nullable=False)
    team_assigned = db.Column(db.String(length=20),nullable=False)

class SubmissionStatus(db.Model):

    id = db.Column(db.Integer(),primary_key=True)
    work_id = db.Column(db.Integer(),nullable=False)
    student = db.Column(db.String(length=100),nullable=False)
    guide = db.Column(db.String(length=100),nullable=False)
    date_given = db.Column(db.String(length=10),nullable=False)
    date_submitted = db.Column(db.String(length=10),nullable=False)
    any_file = db.Column(db.LargeBinary)
    file_attached = db.Column(db.LargeBinary)
    did_submit = db.Column(db.String(length=5),nullable=False,default='NO')
    marks_given = db.Column(db.Integer(),nullable=False,default=-1)
    work_name = db.Column(db.String(length=20),nullable=False)
    work_description = db.Column(db.String(length=200),nullable=False)
    any_file_name = db.Column(db.String(length=50))
    submitted_file_name = db.Column(db.String(length=50))

