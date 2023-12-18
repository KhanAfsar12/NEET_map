from flask import Flask, jsonify, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from openpyxl import load_workbook

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/account'
db = SQLAlchemy(app)


data_subject = db.Table('data_subject',
                        db.Column('college_code', db.Integer, db.ForeignKey('College.CODE')),
                        db.Column('subject_course_code', db.Integer, db.ForeignKey('Course.Course_code'))
                        )


class Data(db.Model):
    __tablename__ = 'College'
    SR_NO = db.Column(db.Integer)
    CODE = db.Column(db.Integer, primary_key=True)
    INSTITUTE_NAME = db.Column(db.String(2500))
    Following = db.relationship('Subject', secondary=data_subject, backref='followers')

    def __repr__(self):
        return f'<Data: {self.INSTITUTE_NAME}'



class Subject(db.Model):
    __tablename__ = 'Course'
    SR_no = db.Column(db.Integer)
    Course_code = db.Column(db.Integer, primary_key=True)
    Course_name = db.Column(db.String(1000))
    
    def __repr__(self):
        return f'<Subject: {self.Course_name}'



@app.route('/come', methods=['POST'])
def index():
    if request.method == "POST":
        file1 = request.files['size']
        wb = load_workbook(file1)
        sheet1 = wb.active

        for row in sheet1.iter_rows(min_row=3, values_only=True):
            excel_data1 = Subject(SR_no=row[0], Course_code=row[1], Course_name=str(row[2]))
            db.session.add(excel_data1)
        db.session.commit()
    return {1:"Afsar Khan"}


@app.route('/map', methods=["POST"])
def reduce():
    if request.method=="POST":
        file = request.files['file']
        workbook = load_workbook(file)
        sheet = workbook.active

        for row in sheet.iter_rows(min_row=2, values_only=True):
            excel_data = Data(SR_NO=row[0], CODE=row[1], INSTITUTE_NAME=str(row[2]))
            db.session.add(excel_data)
        db.session.commit()
    return "hello"

if __name__ == '__main__':
    app.run(debug=True)
    