from datetime import datetime

from flask import request, session, redirect, url_for, render_template

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.LoanApplicationDAO import LoanApplicationDAO
from project.com.dao.LoginDAO import LoginDAO
from project.com.vo.LoanApplicationVO import LoanApplicationVO

# ----------------------- Borrower Side -----------------------------------
from project.com.vo.LoanDetailVO import LoanDetailVO


@app.route('/borrower/insertLoanApplication', methods=['POST'])
def borrowerInsertLoanApplication():
    try:
        if adminLoginSession() == 'borrower':
            loanApplicationVO = LoanApplicationVO()
            loanApplicationDAO = LoanApplicationDAO()

            now = datetime.now()
            applicationDate = now.date()
            applicationTime = now.strftime("%I:%M:%S %p")

            loanId = request.form['loanId']

            loanApplicationVO.application_LoanId = loanId
            loanApplicationVO.applicationDate = applicationDate
            loanApplicationVO.applicationTime = applicationTime
            loanApplicationVO.applicationStatus = "pending"
            loanApplicationVO.scrapingStatus = "pending"

            loanApplicationVO.applicationFrom_LoginId = session['session_loginId']

            loanApplicationDAO.borrowerInsertLoanApplication(loanApplicationVO)

            return redirect(url_for('borrowerViewLoanApplication'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/borrower/viewLoanApplication', methods=['GET'])
def borrowerViewLoanApplication():
    try:
        if adminLoginSession() == 'borrower':
            loanApplicationVO = LoanApplicationVO()
            loanApplicationDAO = LoanApplicationDAO()

            loanApplicationVO.applicationFrom_LoginId = session['session_loginId']

            loanApplicationVOList = loanApplicationDAO.borrowerViewLoanApplication(loanApplicationVO)

            print("loanApplicationVOList", loanApplicationVOList)

            return render_template('borrower/viewLoanApplication.html', loanApplicationVOList=loanApplicationVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


# ----------------------- Lender Side -----------------------------------

@app.route('/lender/viewLoanApplication', methods=['GET'])
def lenderViewLoanApplication():
    try:
        if adminLoginSession() == 'lender':
            loanApplicationVO = LoanApplicationVO()
            loanApplicationDAO = LoanApplicationDAO()

            loanId = request.args.get('loanId')

            loanApplicationVO.application_LoanId = loanId
            loanApplicationVO.applicationTo_LoginId = session['session_loginId']
            loanApplicationVO.applicationStatus = 'approve'

            loanApplicationVOList = loanApplicationDAO.lenderViewLoanApplication(loanApplicationVO)

            print("........ loanApplicationVOList .........", loanApplicationVOList)

            return render_template('lender/viewLoanApplication.html',
                                   loanApplicationVOList=loanApplicationVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/lender/updateLoanApplication', methods=['POST'])
def lenderUpdateLoanApplication():
    try:
        if adminLoginSession() == 'lender':
            loanApplicationVO = LoanApplicationVO()
            loanApplicationDAO = LoanApplicationDAO()

            now = datetime.now()
            applicationApprovalDate = now.date()
            applicationApprovalTime = now.strftime("%I:%M:%S %p")

            applicationId = request.form['applicationId']

            loanApplicationVO.applicationId = applicationId
            if request.form['submit'] == 'approve':
                loanApplicationVO.applicationStatus = "approve"
            elif request.form['submit'] == 'reject':
                loanApplicationVO.applicationStatus = "reject"

            loanApplicationVO.applicationTo_LoginId = session['session_loginId']
            loanApplicationVO.applicationApprovalDate = applicationApprovalDate
            loanApplicationVO.applicationApprovalTime = applicationApprovalTime

            loanApplicationDAO.lenderUpdateLoanApplication(loanApplicationVO)

            return redirect(url_for('lenderLoadDashboard'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


# ----------------------- Admin Side -----------------------------------

@app.route('/admin/viewLoanApplication', methods=['GET'])
def adminViewLoanApplication():
    try:
        if adminLoginSession() == 'admin':

            loanApplicationDAO = LoanApplicationDAO()
            loginDAO = LoginDAO()

            loanApplicationVOList = loanApplicationDAO.adminViewLoanApplication()
            loginVOList = loginDAO.viewLogin()

            print("loanApplicationVOList", loanApplicationVOList)
            print("loginVOList", loginVOList)
            return render_template('admin/viewLoanApplication.html', loanApplicationVOList=loanApplicationVOList,
                                   loginVOList=loginVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
