import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import request, render_template, redirect, url_for, session

from project import app
from project.com.dao.LenderDAO import LenderDAO
from project.com.dao.LoanApplicationDAO import LoanApplicationDAO
from project.com.dao.LoanDetailDAO import LoanDetailDAO
from project.com.dao.LoginDAO import LoginDAO
from project.com.vo.LoanApplicationVO import LoanApplicationVO
from project.com.vo.LoginVO import LoginVO


@app.route('/', methods=['GET', 'POST'])
def adminLoadLogin():
    try:
        session.clear()
        return render_template('admin/login.html')
    except Exception as ex:
        print(ex)


@app.route("/admin/validateLogin", methods=['POST'])
def adminValidateLogin():
    try:
        loginUserName = request.form['loginUserName']
        loginPassword = request.form['loginPassword']

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        loginVO.loginUserName = loginUserName
        loginVO.loginPassword = loginPassword

        loginVOList = loginDAO.validateLogin(loginVO)

        loginDictList = [i.as_dict() for i in loginVOList]

        print("__________________ loginDictList ______________", loginDictList)

        lenLoginDictList = len(loginDictList)

        if lenLoginDictList == 0:

            msg = 'Username Or Password is Incorrect !'

            return render_template('admin/login.html', error=msg)

        elif loginDictList[0]['loginStatus'] == "inactive":

            error_block = 'User is temporary blocked by Website Admin !'
            return render_template('admin/login.html', error_block=error_block)

        else:

            for row1 in loginDictList:

                loginId = row1['loginId']

                loginUserName = row1['loginUserName']

                loginRole = row1['loginRole']

                session['session_loginId'] = loginId

                session['session_loginUserName'] = loginUserName

                session['session_loginRole'] = loginRole

                session.permanent = True

                if loginRole == 'admin':
                    return redirect(url_for('adminLoadDashboard'))
                elif loginRole == 'lender':
                    return redirect(url_for('lenderLoadDashboard'))
                elif loginRole == 'borrower':
                    return redirect(url_for('borrowerLoadDashboard'))

    except Exception as ex:
        print(ex)


@app.route('/admin/loadDashboard', methods=['GET'])
def adminLoadDashboard():
    try:
        if adminLoginSession() == 'admin':
            lenderDAO = LenderDAO()
            lenderVOList = lenderDAO.adminViewLender()

            loanApplicationDAO = LoanApplicationDAO()
            data = loanApplicationDAO.viewData()
            # totalAmount, totalApplication, totalLender, totalBorrower
            print(">>>>>>>data>>>>>>>>>>>>>>>", data)

            if len(data[0]) and len(data[1]) and len(data[2]) and len(data[3]) != 0:
                totalLender = len(data[2])
                totalBorrower = len(data[3])
                totalVisitors = totalLender + totalBorrower

                if len(data[1]) == 1:
                    totalApprovedLoan = data[1][0][1]
                    totalPendingLoan = 0
                    totalRejectLoan = 0
                    totalApplication = totalApprovedLoan
                elif len(data[1]) == 2:
                    totalApprovedLoan = data[1][0][1]
                    totalPendingLoan = data[1][1][1]
                    totalRejectLoan = 0
                    totalApplication = totalApprovedLoan + totalPendingLoan
                else:
                    totalApprovedLoan = data[1][0][1]
                    totalPendingLoan = data[1][1][1]
                    totalRejectLoan = data[1][2][1]
                    totalApplication = totalApprovedLoan + totalPendingLoan + totalRejectLoan

                totalApprovedamount = 0
                for i in data[0]:
                    totalApprovedamount = totalApprovedamount + i[1]

                dictData = {"totalApprovedamount": totalApprovedamount, "totalVisitors": totalVisitors,
                            "totalLender": totalLender, "totalBorrower": totalBorrower,
                            "totalApplication": totalApplication, "totalApprovedLoan": totalApprovedLoan,
                            "totalPendingLoan": totalPendingLoan, "totalRejectLoan": totalRejectLoan}

                return render_template('admin/index.html', dictData=dictData, lenderVOList=lenderVOList)

            return render_template('admin/index.html', lenderVOList=lenderVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/lender/loadDashboard', methods=['GET'])
def lenderLoadDashboard():
    try:
        if adminLoginSession() == 'lender':
            loanApplicationVO = LoanApplicationVO()
            loanApplicationDAO = LoanApplicationDAO()

            loanApplicationVO.applicationTo_LoginId = session['session_loginId']

            loanApplicationVO.applicationStatus = 'pending'

            loanApplicationVOList = loanApplicationDAO.lenderIndexViewLoanApplication(loanApplicationVO)

            print("loanApplicationVOList", loanApplicationVOList)

            return render_template('lender/index.html', loanApplicationVOList=loanApplicationVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/borrower/loadDashboard', methods=['GET'])
def borrowerLoadDashboard():
    try:
        if adminLoginSession() == 'borrower':

            loanDetailDAO = LoanDetailDAO()

            loanDetailVOList = loanDetailDAO.borrowerIndexViewLoanDetail()

            print("loanDetailVOList", loanDetailVOList)

            return render_template('borrower/index.html', loanDetailVOList=loanDetailVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/loginSession')
def adminLoginSession():
    try:
        if 'session_loginId' and 'session_loginRole' in session:

            if session['session_loginRole'] == 'admin':

                return 'admin'

            elif session['session_loginRole'] == 'borrower':

                return 'borrower'

            elif session['session_loginRole'] == 'lender':

                return 'lender'

            print("<<<<<<<<<<<<<<<<True>>>>>>>>>>>>>>>>>>>>")

        else:

            print("<<<<<<<<<<<<<<<<False>>>>>>>>>>>>>>>>>>>>")

            return False

    except Exception as ex:
        print(ex)


@app.route("/admin/logoutSession", methods=['GET'])
def adminLogoutSession():
    try:
        session.clear()
        return redirect(url_for('adminLoadLogin'))

    except Exception as ex:
        print(ex)


@app.route('/admin/updateLenderLoginStatus', methods=['GET'])
def adminUpdateLenderLoginStatus():
    try:
        if adminLoginSession() == 'admin':
            loginVO = LoginVO()
            loginDAO = LoginDAO()

            loginId = request.args.get('loginId')
            loginStatus = request.args.get('loginStatus')

            print("loginId>>>>>>>>>>>>>", loginId)
            print("status>>>>>>>>>>>>>", loginStatus)

            loginVO.loginId = loginId
            if loginStatus == 'active':
                loginVO.loginStatus = 'inactive'
            if loginStatus == 'inactive':
                loginVO.loginStatus = 'active'

            loginDAO.updateLogin(loginVO)

            return redirect(url_for('adminViewLender'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/updateBorrowerLoginStatus', methods=['GET'])
def adminUpdateBorrowerLoginStatus():
    try:
        if adminLoginSession() == 'admin':
            loginVO = LoginVO()
            loginDAO = LoginDAO()

            loginId = request.args.get('loginId')
            loginStatus = request.args.get('loginStatus')

            print("loginId>>>>>>>>>>>>>", loginId)
            print("status>>>>>>>>>>>>>", loginStatus)

            loginVO.loginId = loginId
            if loginStatus == 'active':
                loginVO.loginStatus = 'inactive'
            if loginStatus == 'inactive':
                loginVO.loginStatus = 'active'

            loginDAO.updateLogin(loginVO)

            return redirect(url_for('adminViewBorrower'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route("/admin/loadForgotPassword")
def adminForgotPassword():
    try:
        return render_template("admin/addForgotPassword.html")
    except Exception as ex:
        print(ex)


@app.route("/admin/generateOTP", methods=["post"])
def adminGenerateOTP():
    try:
        loginDAO = LoginDAO()
        loginVO = LoginVO()

        loginUserName = request.form['loginUserName']

        loginVO.loginUserName = loginUserName

        loginVOList = loginDAO.validateLoginUserName(loginVO)
        print("loginVOList >>>>>>>>>>>>>>>>>>> ", loginVOList)

        loginDictList = [i.as_dict() for i in loginVOList]

        print("__________________ loginDictList ______________", loginDictList)

        lenLoginDictList = len(loginDictList)

        if lenLoginDictList == 0:
            msg = "Please enter valid username !"
            return render_template("admin/addForgotPassword.html", msg=msg)

        else:
            session["session_loginUserName"] = loginDictList[0]['loginUserName']
            session["session_loginId"] = loginDictList[0]['loginId']

            OTP = ''.join((random.choice(string.digits)) for x in range(4))
            session["session_OTP"] = OTP

            sender = "p2ploans2020@gmail.com"

            receiver = loginUserName

            msg = MIMEMultipart()

            msg['From'] = sender

            msg['To'] = receiver

            msg['Subject'] = "Reset Password"

            msg.attach(MIMEText(OTP, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login(sender, "finalyear2020")

            text = msg.as_string()

            server.sendmail(sender, receiver, text)

            server.quit()

            return render_template("admin/addOTP.html")

    except Exception as ex:
        print(ex)


@app.route("/admin/validateOTP", methods=['post'])
def adminValidateOTP():
    try:
        loginOTP = request.form["loginOTP"]

        loginUserName = session["session_loginUserName"]

        if session["session_OTP"] == loginOTP:

            loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

            print("loginPassword=" + loginPassword)

            sender = "p2ploans2020@gmail.com"

            receiver = loginUserName

            msg = MIMEMultipart()

            msg['From'] = sender

            msg['To'] = receiver

            msg['Subject'] = "NEW PASSWORD"

            msg.attach(MIMEText(loginPassword, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login(sender, "finalyear2020")

            text = msg.as_string()

            server.sendmail(sender, receiver, text)
            server.quit()

            loginVO = LoginVO()
            loginDAO = LoginDAO()

            loginVO.loginId = session['session_loginId']
            loginVO.loginPassword = loginPassword
            loginDAO.updateLogin(loginVO)

            return render_template("admin/login.html")
        else:
            msg = "Please enter correct OTP sent to you!"
            return render_template("admin/addOTP.html", msg=msg)

    except Exception as ex:
        print(ex)
