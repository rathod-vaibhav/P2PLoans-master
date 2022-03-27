import os
from datetime import datetime

from flask import request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLogoutSession, adminLoginSession
from project.com.dao.ComplainDAO import ComplainDAO
from project.com.vo.ComplainVO import ComplainVO


# ----------------------- Lender Side -----------------------------------

@app.route('/lender/loadComplain', methods=['GET'])
def lenderLoadComplain():
    try:
        if adminLoginSession() == 'lender':
            return render_template('lender/addComplain.html')
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/lender/insertComplain', methods=['POST'])
def lenderInsertComplain():
    try:
        if adminLoginSession() == 'lender':
            UPLOAD_FOLDER = 'project/static/adminResources/complain/'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainSubject = request.form['complainSubject']
            complainDescription = request.form['complainDescription']

            now = datetime.now()
            complainDate = now.date()
            complainTime = now.strftime("%I:%M:%S %p")

            complainFile = request.files['complainFile']

            if complainFile.filename != '':
                complainFileName = secure_filename(complainFile.filename)
                complainFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
                complainFile.save(os.path.join(complainFilePath, complainFileName))
                complainVO.complainFileName = complainFileName
                complainVO.complainFilePath = complainFilePath.replace("project", "..")

            complainVO.complainSubject = complainSubject
            complainVO.complainDescription = complainDescription
            complainVO.complainDate = complainDate
            complainVO.complainTime = complainTime
            complainVO.complainStatus = "pending"
            complainVO.complainFrom_LoginId = session['session_loginId']

            complainDAO.insertComplain(complainVO)

            return redirect(url_for('lenderViewComplain'))
        else:
            return adminLogoutSession()


    except Exception as ex:
        print(ex)


@app.route('/lender/viewComplain', methods=['GET'])
def lenderViewComplain():
    try:
        if adminLoginSession() == 'lender':
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainVO.complainFrom_LoginId = session['session_loginId']

            complainList = complainDAO.viewComplain(complainVO)

            print("__________________", complainList)

            return render_template('lender/viewComplain.html', complainList=complainList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/lender/deleteComplain', methods=['GET'])
def lenderDeleteComplain():
    try:
        if adminLoginSession() == 'lender':
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainId = request.args.get('complainId')

            complainVO.complainId = complainId

            complainList = complainDAO.deleteComplain(complainVO)

            if complainList.complainFileName != None:
                path_lender = complainList.complainFilePath.replace("..", "project") + complainList.complainFileName
                os.remove(path_lender)

            if complainList.complainStatus == 'replied':
                path_admin = complainList.replyFilePath.replace("..", "project") + complainList.replyFileName
                os.remove(path_admin)

            return redirect(url_for('lenderViewComplain'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


# ----------------------- Borrower Side -----------------------------------

@app.route('/borrower/loadComplain', methods=['GET'])
def borrowerLoadComplain():
    try:
        if adminLoginSession() == 'borrower':
            return render_template('borrower/addComplain.html')
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/borrower/insertComplain', methods=['POST'])
def borrowerInsertComplain():
    try:
        if adminLoginSession() == 'borrower':
            UPLOAD_FOLDER = 'project/static/adminResources/complain/'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainSubject = request.form['complainSubject']
            complainDescription = request.form['complainDescription']

            now = datetime.now()
            complainDate = now.date()
            complainTime = now.strftime("%I:%M:%S %p")

            complainFile = request.files['complainFile']

            if complainFile.filename != '':
                complainFileName = secure_filename(complainFile.filename)
                complainFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
                complainFile.save(os.path.join(complainFilePath, complainFileName))
                complainVO.complainFileName = complainFileName
                complainVO.complainFilePath = complainFilePath.replace("project", "..")

            complainVO.complainSubject = complainSubject
            complainVO.complainDescription = complainDescription
            complainVO.complainDate = complainDate
            complainVO.complainTime = complainTime
            complainVO.complainStatus = "pending"
            complainVO.complainFrom_LoginId = session['session_loginId']

            complainDAO.insertComplain(complainVO)

            return redirect(url_for('borrowerViewComplain'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/borrower/viewComplain', methods=['GET'])
def borrowerViewComplain():
    try:
        if adminLoginSession() == 'borrower':
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainVO.complainFrom_LoginId = session['session_loginId']

            complainList = complainDAO.viewComplain(complainVO)

            print("__________________", complainList)

            return render_template('borrower/viewComplain.html', complainList=complainList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/borrower/deleteComplain', methods=['GET'])
def borrowerDeleteComplain():
    try:
        if adminLoginSession() == 'borrower':
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainId = request.args.get('complainId')

            complainVO.complainId = complainId

            complainList = complainDAO.deleteComplain(complainVO)

            if complainList.complainFileName != None:
                path_borrower = complainList.complainFilePath.replace("..", "project") + complainList.complainFileName
                os.remove(path_borrower)

            if complainList.complainStatus == 'replied':
                path_admin = complainList.replyFilePath.replace("..", "project") + complainList.replyFileName
                os.remove(path_admin)

            return redirect(url_for('borrowerViewComplain'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


# ----------------------- Admin Side -----------------------------------

@app.route('/admin/viewComplain', methods=['GET'])
def adminViewComplain():
    try:
        if adminLoginSession() == 'admin':
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainVO.complainStatus = "pending"

            complainList = complainDAO.adminViewComplain(complainVO)

            print("__________________", complainList)

            return render_template('admin/viewComplain.html', complainList=complainList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/loadComplainReply', methods=['GET'])
def adminLoadComplainReply():
    try:
        if adminLoginSession() == 'admin':
            complainVO = ComplainVO()
            complainId = request.args.get("complainId")
            complainVO.complainId = complainId

            return render_template('admin/addComplainReply.html', complainId=complainVO.complainId)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/insertComplainReply', methods=['POST'])
def adminInsertComplainReplay():
    try:
        if adminLoginSession() == 'admin':
            UPLOAD_FOLDER = 'project/static/adminResources/reply/'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainId = request.form['complainId']
            replySubject = request.form['replySubject']
            replyMessage = request.form['replyMessage']

            now = datetime.now()
            replyDate = now.date()
            replyTime = now.strftime("%I:%M:%S %p")

            replyFile = request.files['replyFile']

            if replyFile.filename != '':
                replyFileName = secure_filename(replyFile.filename)
                replyFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
                replyFile.save(os.path.join(replyFilePath, replyFileName))
                complainVO.replyFileName = replyFileName
                complainVO.replyFilePath = replyFilePath.replace("project", "..")

            complainVO.complainId = complainId
            complainVO.replySubject = replySubject
            complainVO.replyMessage = replyMessage
            complainVO.replyDate = replyDate
            complainVO.replyTime = replyTime
            complainVO.complainTo_LoginId = session['session_loginId']
            complainVO.complainStatus = 'replied'

            complainDAO.adminInsertReply(complainVO)

            return redirect(url_for('adminViewComplain'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)
