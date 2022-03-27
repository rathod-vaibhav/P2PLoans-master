import os
import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import request, render_template, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.AreaDAO import AreaDAO
from project.com.dao.BorrowerDAO import BorrowerDAO
from project.com.dao.CityDAO import CityDAO
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.PreviousLoanDAO import PreviousLoanDAO
from project.com.vo.AreaVO import AreaVO
from project.com.vo.BorrowerVO import BorrowerVO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.PreviousLoanVO import PreviousLoanVO


@app.route('/borrower/loadRegister')
def borrowerLoadRegister():
    try:
        cityDAO = CityDAO()
        cityVOList = cityDAO.viewCity()

        areaDAO = AreaDAO()
        areaVOList = areaDAO.viewArea()

        return render_template('borrower/register.html', cityVOList=cityVOList, areaVOList=areaVOList)
    except Exception as ex:
        print(ex)


@app.route('/borrower/insertRegister', methods=['POST'])
def borrowerInsertRegister():
    try:
        UPLOAD_FOLDER = 'project/static/userResources/borrowerIdentityData/'
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        PREVIOUS_LOAN_FOLDER = 'project/static/adminResources/previousLoan/'
        app.config['PREVIOUS_LOAN_FOLDER'] = PREVIOUS_LOAN_FOLDER

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        borrowerVO = BorrowerVO()
        borrowerDAO = BorrowerDAO()

        previousLoanVO = PreviousLoanVO()
        previousLoanDAO = PreviousLoanDAO()

        loginUserName = request.form['loginUserName']

        borrowerName = request.form['borrowerName']
        borrowerDateOfBirth = request.form['borrowerDateOfBirth']
        borrowerContact = request.form['borrowerContact']
        borrower_CityId = request.form['borrower_CityId']
        borrower_AreaId = request.form['borrower_AreaId']
        borrowerAddress = request.form['borrowerAddress']
        borrowerSocialMediaLink = request.form['borrowerSocialMediaLink']

        borrowerPanCard = request.files['borrowerPanCard']
        borrowerAdharCard = request.files['borrowerAdharCard']
        borrowerPreviousLoan = request.files['borrowerPreviousLoan']

        borrowerPanCardFileName = secure_filename(borrowerPanCard.filename)
        borrowerAdharCardFileName = secure_filename(borrowerAdharCard.filename)
        borrowerPreviousLoanFileName = secure_filename(borrowerPreviousLoan.filename)

        borrowerPanCardFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
        borrowerAdharCardFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
        borrowerPreviousLoanFilePath = os.path.join(app.config['PREVIOUS_LOAN_FOLDER'])

        borrowerPanCard.save(os.path.join(borrowerPanCardFilePath, borrowerPanCardFileName))
        borrowerAdharCard.save(os.path.join(borrowerAdharCardFilePath, borrowerAdharCardFileName))
        borrowerPreviousLoan.save(os.path.join(borrowerPreviousLoanFilePath, borrowerPreviousLoanFileName))

        loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

        print("loginPassword=" + loginPassword)

        sender = "p2ploans2020@gmail.com"

        receiver = loginUserName

        msg = MIMEMultipart()

        msg['From'] = sender

        msg['To'] = receiver

        msg['Subject'] = "PYTHON PASSWORD"

        msg.attach(MIMEText(loginPassword, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()

        server.login(sender, "<password of email account>")

        text = msg.as_string()

        server.sendmail(sender, receiver, text)

        loginVO.loginUserName = loginUserName
        loginVO.loginPassword = loginPassword
        loginVO.loginRole = "borrower"
        loginVO.loginStatus = "active"

        loginDAO.insertLogin(loginVO)

        borrowerVO.borrowerName = borrowerName
        borrowerVO.borrowerDateOfBirth = borrowerDateOfBirth
        borrowerVO.borrowerContact = borrowerContact
        borrowerVO.borrower_CityId = borrower_CityId
        borrowerVO.borrower_AreaId = borrower_AreaId
        borrowerVO.borrowerPanCardFileName = borrowerPanCardFileName
        borrowerVO.borrowerPanCardFilePath = borrowerPanCardFilePath.replace("project", "..")
        borrowerVO.borrowerAdharCardFileName = borrowerAdharCardFileName
        borrowerVO.borrowerAdharCardFilePath = borrowerAdharCardFilePath.replace("project", "..")
        borrowerVO.borrowerAddress = borrowerAddress
        borrowerVO.borrowerSocialMediaLink = borrowerSocialMediaLink
        borrowerVO.borrower_LoginId = loginVO.loginId

        borrowerDAO.insertBorrower(borrowerVO)

        previousLoanVO.previousLoanFileName = borrowerPreviousLoanFileName
        previousLoanVO.previousLoanFilePath = borrowerPreviousLoanFilePath.replace("project", "..")
        previousLoanVO.previousLoanFrom_LoginId = loginVO.loginId

        previousLoanDAO.insertPreviousLoan(previousLoanVO)

        server.quit()

        return redirect('/')

    except Exception as ex:
        print(ex)


@app.route("/borrower/loadResetPassword", methods=['GET'])
def borrowerLoadResetPassword():
    try:
        if adminLoginSession() == 'borrower':
            return render_template('borrower/addResetPassword.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route("/borrower/insertResetPassword", methods=['POST'])
def borrowerInsertResetPassword():
    try:
        if adminLoginSession() == 'borrower':

            loginVO = LoginVO()
            loginDAO = LoginDAO()

            oldPassword = request.form['oldPassword']
            newPassword = request.form['newPassword']
            conformPassword = request.form['conformPassword']

            loginVO.loginUserName = session['session_loginUserName']
            loginVO.loginRole = session['session_loginRole']
            loginVO.loginPassword = oldPassword

            loginVOList = loginDAO.validateLogin(loginVO)

            loginDictList = [i.as_dict() for i in loginVOList]

            print("__________________ loginDictList ______________", loginDictList)

            lenLoginDictList = len(loginDictList)

            if lenLoginDictList == 0:
                oldPassword_error = "Please enter validate Old Password !"
                return render_template("borrower/addResetPassword.html", oldPassword_error=oldPassword_error)

            elif newPassword != conformPassword:
                newPassword_erro = "Password and Conform Password not match, Try again."
                return render_template('borrower/addResetPassword.html', newPassword_erro=newPassword_erro)
            else:
                loginVO.loginId = session['session_loginId']
                loginVO.loginPassword = newPassword
                loginDAO.updateLogin(loginVO)
                return redirect(url_for("borrowerLoadDashboard"))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route("/borrower/editProfile", methods=['GET'])
def borrowerEditProfile():
    try:
        if adminLoginSession() == 'borrower':
            loginVO = LoginVO()
            loginDAO = LoginDAO()

            borrowerVO = BorrowerVO()
            borrowerDAO = BorrowerDAO()

            cityDAO = CityDAO()
            cityVOList = cityDAO.viewCity()

            areaDAO = AreaDAO()
            areaVOList = areaDAO.viewArea()

            borrowerVO.borrower_LoginId = session['session_loginId']

            borrowerVOList = borrowerDAO.viewProfile(borrowerVO)

            return render_template('borrower/editProfile.html', cityVOList=cityVOList, areaVOList=areaVOList,
                                   borrowerVOList=borrowerVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route("/borrower/updateProfile", methods=['POST'])
def borrowerUpdateProfile():
    try:
        if adminLoginSession() == 'borrower':
            loginVO = LoginVO()
            loginDAO = LoginDAO()

            borrowerVO = BorrowerVO()
            borrowerDAO = BorrowerDAO()

            borrowerId = request.form['borrowerId']
            borrowerName = request.form['borrowerName']
            borrowerDateOfBirth = request.form['borrowerDateOfBirth']
            loginUserName = request.form['loginUserName']
            borrowerContact = request.form['borrowerContact']
            borrower_CityId = request.form['borrower_CityId']
            borrower_AreaId = request.form['borrower_AreaId']
            borrowerAddress = request.form['borrowerAddress']
            borrowerSocialMediaLink = request.form['borrowerSocialMediaLink']

            borrowerVO.borrowerId = borrowerId
            borrowerVO.borrowerName = borrowerName
            borrowerVO.borrowerDateOfBirth = borrowerDateOfBirth
            borrowerVO.borrowerContact = borrowerContact
            borrowerVO.borrower_CityId = borrower_CityId
            borrowerVO.borrower_AreaId = borrower_AreaId
            borrowerVO.borrowerAddress = borrowerAddress
            borrowerVO.borrowerSocialMediaLink = borrowerSocialMediaLink

            borrowerDAO.updateBorrower(borrowerVO)

            if loginUserName != session['session_loginUserName']:
                loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

                print("loginPassword=" + loginPassword)

                sender = "p2ploans2020@gmail.com"

                receiver = loginUserName

                msg = MIMEMultipart()

                msg['From'] = sender

                msg['To'] = receiver

                msg['Subject'] = "PYTHON PASSWORD"

                msg.attach(MIMEText(loginPassword, 'plain'))

                server = smtplib.SMTP('smtp.gmail.com', 587)

                server.starttls()

                server.login(sender, "finalyear2020")

                text = msg.as_string()

                server.sendmail(sender, receiver, text)

                loginVO.loginId = session['session_loginId']
                loginVO.loginUserName = loginUserName
                loginVO.loginPassword = loginPassword
                loginDAO.updateLogin(loginVO)
                return redirect(url_for('adminLoadLogin'))

            return redirect(url_for('borrowerLoadDashboard'))

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route("/borrower/viewAboutUs", methods=['GET'])
def borrowerViewAboutUs():
    try:
        if adminLoginSession() == 'borrower':
            return render_template('borrower/viewAboutUs.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


# ----------------------- Admin Side -----------------------------------

@app.route('/admin/viewBorrower', methods=['GET'])
def adminViewBorrower():
    try:
        if adminLoginSession() == 'admin':
            borrowerDAO = BorrowerDAO()

            borrowerVOList = borrowerDAO.adminViewBorrower()

            print("++++borrowerVOList++", borrowerVOList)

            return render_template('admin/viewBorrower.html', borrowerVOList=borrowerVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
