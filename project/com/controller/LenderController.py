import os
import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd
from flask import request, render_template, redirect, session, url_for, jsonify
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler, LabelEncoder
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.AreaDAO import AreaDAO
from project.com.dao.CityDAO import CityDAO
from project.com.dao.LenderDAO import LenderDAO
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.PreviousLoanDAO import PreviousLoanDAO
from project.com.vo.AreaVO import AreaVO
from project.com.vo.CityVO import CityVO
from project.com.vo.LenderVO import LenderVO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.PreviousLoanVO import PreviousLoanVO


@app.route('/lender/loadRegister')
def lenderLoadRegister():
    try:
        cityDAO = CityDAO()
        cityVOList = cityDAO.viewCity()

        areaDAO = AreaDAO()
        areaVOList = areaDAO.viewArea()

        return render_template('lender/register.html', cityVOList=cityVOList, areaVOList=areaVOList)
    except Exception as ex:
        print(ex)


@app.route('/lender/insertRegister', methods=['POST'])
def lenderInsertRegister():
    try:

        UPLOAD_FOLDER = 'project/static/userResources/lenderIdentityData/'
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        lenderVO = LenderVO()
        lenderDAO = LenderDAO()

        loginUserName = request.form['loginUserName']

        lenderName = request.form['lenderName']
        lenderDateOfBirth = request.form['lenderDateOfBirth']
        lenderContact = request.form['lenderContact']
        lender_CityId = request.form['lender_CityId']
        lender_AreaId = request.form['lender_AreaId']
        lenderAddress = request.form['lenderAddress']

        lenderPanCard = request.files['lenderPanCard']
        lenderAdharCard = request.files['lenderAdharCard']

        lenderPanCardFileName = secure_filename(lenderPanCard.filename)
        lenderAdharCardFileName = secure_filename(lenderAdharCard.filename)

        lenderPanCardFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
        lenderAdharCardFilePath = os.path.join(app.config['UPLOAD_FOLDER'])

        lenderPanCard.save(os.path.join(lenderPanCardFilePath, lenderPanCardFileName))
        lenderAdharCard.save(os.path.join(lenderAdharCardFilePath, lenderAdharCardFileName))

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
        loginVO.loginRole = "lender"
        loginVO.loginStatus = "active"

        loginDAO.insertLogin(loginVO)

        lenderVO.lenderName = lenderName
        lenderVO.lenderDateOfBirth = lenderDateOfBirth
        lenderVO.lenderContact = lenderContact
        lenderVO.lender_CityId = lender_CityId
        lenderVO.lender_AreaId = lender_AreaId
        lenderVO.lenderPanCardFileName = lenderPanCardFileName
        lenderVO.lenderPanCardFilePath = lenderPanCardFilePath.replace("project", "..")
        lenderVO.lenderAdharCardFileName = lenderAdharCardFileName
        lenderVO.lenderAdharCardFilePath = lenderAdharCardFilePath.replace("project", "..")
        lenderVO.lenderAddress = lenderAddress
        lenderVO.lender_LoginId = loginVO.loginId

        lenderDAO.insertLender(lenderVO)
        server.quit()

        return redirect('/')

    except Exception as ex:
        print(ex)


def dataPreprocessing(df, columnName):
    le = LabelEncoder()

    le.fit(df[columnName])

    df[columnName] = le.transform(df[columnName])


@app.route('/lender/viewPrediction', methods=['GET'])
def lenderViewPrediction():
    try:
        if adminLoginSession() == 'lender':

            previousLoanVO = PreviousLoanVO()
            previousLoanDAO = PreviousLoanDAO()

            previousLoanVO.previousLoanFrome_LoginId = request.args.get('applicationFrom_LoginId')

            loanApprovalsStatusVOList = previousLoanDAO.viewApprovelCount(previousLoanVO)

            previouseLoanRecordVOList = previousLoanDAO.viewPreviousLoanRecord(previousLoanVO)

            readfileVOList = previousLoanDAO.readFile(previousLoanVO)

            print("readfileVOList>>>>>>>>>>", readfileVOList)

            file = readfileVOList[0].previousLoanFilePath.replace("..", "project") + readfileVOList[
                0].previousLoanFileName

            previousLoanId = readfileVOList[0].previousLoanId

            print("file>>>>>>>>>>>\n", file)

            dtest = pd.read_csv(file)

            print("dtest>>>>>>>>\n", dtest)

            slc = StandardScaler()

            job_lib = joblib.load(r'project/static/adminResources/modelDump/loan.pkl')

            dataPreprocessing(dtest, 'Gender')
            print("Gender>>>>>>>>>>", dtest['Gender'])

            dataPreprocessing(dtest, 'Married')
            print("Married>>>>>>>>", dtest['Married'])

            dataPreprocessing(dtest, 'Education')
            print("Education>>>>>>>", dtest['Education'])

            dataPreprocessing(dtest, 'Self_Employed')
            print("Self_Employed>>>>>>>>>>", dtest['Self_Employed'])

            dataPreprocessing(dtest, 'Dependents')
            print("Dependents>>>>>>>>>>", dtest['Dependents'])

            dataPreprocessing(dtest, 'Property_Area')
            print("Property_Area>>>>>>>>>>", dtest['Property_Area'])

            dtest['Gender'] = dtest['Gender'].fillna(dtest['Gender'].dropna().mode().values[0])
            print("Gender>>>>>>>>>>", dtest['Gender'])

            dtest['Dependents'] = dtest['Dependents'].fillna(dtest['Dependents'].dropna().mode().values[0])

            print("Dependents>>>>>>>>>>", dtest['Dependents'])

            dtest['Self_Employed'] = dtest['Self_Employed'].fillna(dtest['Self_Employed'].dropna().mode().values[0])
            print("Self_Employed>>>>>>>>>>", dtest['Self_Employed'])

            dtest['LoanAmount'] = dtest['LoanAmount'].fillna(dtest['LoanAmount'].dropna().mode().values[0])
            print("LoanAmount>>>>>>>>>>", dtest['LoanAmount'])

            dtest['Loan_Amount_Term'] = dtest['Loan_Amount_Term'].fillna(
                dtest['Loan_Amount_Term'].dropna().mode().values[0])
            print("Loan_Amount_Term>>>>>>>>>>", dtest['Loan_Amount_Term'])

            dtest['Credit_History'] = dtest['Credit_History'].fillna(dtest['Credit_History'].dropna().mode().values[0])
            print("Credit_History>>>>>>>>>>", dtest['Credit_History'])

            X_test = dtest.iloc[:, 1:]
            print("X_test>>>>>>>>>>>>", X_test)

            X_test = pd.get_dummies(X_test)
            print("dummy>>>X_test>>>>>>>>>>>", X_test)

            X_test_std = slc.fit_transform(X_test)
            print('X_test_std>>>>>>>>', X_test_std)

            y_test_pred = job_lib.predict(X_test_std)
            print('y_test_pred>>>>>>>', y_test_pred)

            dtest['Loan_Status'] = y_test_pred
            df_final = dtest.drop(
                ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'ApplicantIncome',
                 'CoapplicantIncome',
                 'LoanAmount', 'Loan_Amount_Term', 'Credit_History', 'Property_Area'], axis=1)

            df_final['Loan_Status'] = df_final['Loan_Status'].map({0: 'N', 1: 'Y'})

            df_final.to_csv(file.replace(".csv", "") + "_output" + ".csv",
                            index=False)

            print(df_final)

            previousLoanVO.outputFileName = readfileVOList[0].previousLoanFileName.replace(".csv",
                                                                                           "") + "_output" + ".csv"
            previousLoanVO.outputFilePath = readfileVOList[0].previousLoanFilePath
            previousLoanVO.previousLoanId = previousLoanId

            previousLoanDAO.insertPredictionOutput(previousLoanVO)

            predictionOutputVOList = previousLoanDAO.viewPredictionOutput(previousLoanVO)

            return render_template('lender/viewPrediction.html', loanApprovalsStatusVOList=loanApprovalsStatusVOList,
                                   previouseLoanRecordVOList=previouseLoanRecordVOList,
                                   predictionOutputVOList=predictionOutputVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route("/lender/loadResetPassword", methods=['GET'])
def lenderLoadResetPassword():
    try:
        if adminLoginSession() == 'lender':
            return render_template('lender/addResetPassword.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route("/lender/insertResetPassword", methods=['POST'])
def lenderInsertResetPassword():
    try:
        if adminLoginSession() == 'lender':

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
                return render_template("lender/addResetPassword.html", oldPassword_error=oldPassword_error)

            elif newPassword != conformPassword:
                newPassword_erro = "Password and Conform Password not match, Try again."
                return render_template('lender/addResetPassword.html', newPassword_erro=newPassword_erro)
            else:
                loginVO.loginId = session['session_loginId']
                loginVO.loginPassword = newPassword
                loginDAO.updateLogin(loginVO)
                return redirect(url_for("lenderLoadDashboard"))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route("/lender/editProfile", methods=['GET'])
def lenderEditProfile():
    try:
        if adminLoginSession() == 'lender':
            loginVO = LoginVO()
            loginDAO = LoginDAO()

            lenderVO = LenderVO()
            lenderDAO = LenderDAO()

            cityDAO = CityDAO()
            cityVOList = cityDAO.viewCity()

            areaDAO = AreaDAO()
            areaVOList = areaDAO.viewArea()

            lenderVO.lender_LoginId = session['session_loginId']

            lenderVOList = lenderDAO.viewProfile(lenderVO)

            print(">>>>>>>>>>>>>>lenderVOList>>>>>>>>>>>>>>>>", lenderVOList)

            return render_template('lender/editProfile.html', cityVOList=cityVOList, areaVOList=areaVOList,
                                   lenderVOList=lenderVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route("/lender/updateProfile", methods=['POST'])
def lenderUpdateProfile():
    try:
        if adminLoginSession() == 'lender':
            loginVO = LoginVO()
            loginDAO = LoginDAO()

            lenderVO = LenderVO()
            lenderDAO = LenderDAO()

            lenderId = request.form['lenderId']
            lenderName = request.form['lenderName']
            lenderDateOfBirth = request.form['lenderDateOfBirth']
            loginUserName = request.form['loginUserName']
            lenderContact = request.form['lenderContact']
            lender_CityId = request.form['lender_CityId']
            lender_AreaId = request.form['lender_AreaId']
            lenderAddress = request.form['lenderAddress']

            lenderVO.lenderId = lenderId
            lenderVO.lenderName = lenderName
            lenderVO.lenderDateOfBirth = lenderDateOfBirth
            lenderVO.lenderContact = lenderContact
            lenderVO.lender_CityId = lender_CityId
            lenderVO.lender_AreaId = lender_AreaId
            lenderVO.lenderAddress = lenderAddress

            lenderDAO.updateLender(lenderVO)

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

            return redirect(url_for('lenderLoadDashboard'))

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route("/lender/viewAboutUs", methods=['GET'])
def lenderViewAboutUs():
    try:
        if adminLoginSession() == 'lender':
            return render_template('lender/viewAboutUs.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


# ----------------------- Admin Side -----------------------------------


@app.route('/admin/viewLender', methods=['GET'])
def adminViewLender():
    try:
        if adminLoginSession() == 'admin':
            lenderDAO = LenderDAO()

            lenderVOList = lenderDAO.adminViewLender()

            print("++++lenderVOList++", lenderVOList)

            return render_template('admin/viewLender.html', lenderVOList=lenderVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
