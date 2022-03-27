from flask import render_template, request, session, redirect, url_for, jsonify

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.LoanDetailDAO import LoanDetailDAO
from project.com.vo.LoanDetailVO import LoanDetailVO


# ----------------------- Lender Side -----------------------------------

@app.route('/lender/loadLoanDetail', methods=['GET'])
def lenderLoadLoanDetail():
    try:
        if adminLoginSession() == 'lender':
            return render_template('lender/addLoanDetail.html')
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/lender/insertLoanDetail', methods=['POST'])
def lenderInsertLoanDetail():
    try:
        if adminLoginSession() == 'lender':

            loanDetailVO = LoanDetailVO()
            loanDetailDAO = LoanDetailDAO()

            loanAmount = request.form['loanAmount']
            loanRate = request.form['loanRate']
            loanDuration = request.form['loanDuration']
            loanEMI = request.form['loanEMI']

            loanDetailVO.loanAmount = loanAmount
            loanDetailVO.loanRate = loanRate
            loanDetailVO.loanDuration = loanDuration
            loanDetailVO.loanEMI = loanEMI
            loanDetailVO.loan_LoginId = session['session_loginId']

            loanDetailDAO.insertLoanDetail(loanDetailVO)

            return redirect(url_for('lenderViewLoanDetail'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/lender/viewLoanDetail', methods=['GET'])
def lenderViewLoanDetail():
    try:
        if adminLoginSession() == 'lender':

            loanDetailVO = LoanDetailVO()
            loanDetailDAO = LoanDetailDAO()

            loanDetailVO.loan_LoginId = session['session_loginId']

            loanDetailVOList = loanDetailDAO.lenderViewLoanDetail(loanDetailVO)

            print("loanDetailVOList", loanDetailVOList)

            return render_template('lender/viewLoanDetail.html', loanDetailVOList=loanDetailVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/lender/deleteLoanDetail', methods=['GET'])
def lenderDeleteLoanDetail():
    try:
        if adminLoginSession() == 'lender':
            loanDetailVO = LoanDetailVO()
            loanDetailDAO = LoanDetailDAO()

            loanId = request.args.get('loanId')

            loanDetailVO.loanId = loanId

            loanDetailDAO.deleteLoanDetail(loanDetailVO)

            return redirect(url_for('lenderViewLoanDetail'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


# ----------------------- Borrower Side -----------------------------------



@app.route('/borrower/viewLoanDetail', methods=['GET'])
def borrowerViewLoanDetail():
    try:
        if adminLoginSession() == 'borrower':

            loanDetailVO = LoanDetailVO()
            loanDetailDAO = LoanDetailDAO()

            loanId = request.args.get("loanId")

            loanDetailVO.loanId = loanId

            loanDetailList = loanDetailDAO.borrowerViewLoanDetail(loanDetailVO)

            print("________loanDetailList__________", loanDetailList)

            return render_template('borrower/viewLoanDetail.html', loanDetailList=loanDetailList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


# ----------------------- Admin Side -----------------------------------



@app.route('/admin/ajaxGetGraphData', methods=['GET'])
def adminViewLoanDetail():
    try:
        if adminLoginSession() == 'admin':

            loanDetailVO = LoanDetailVO()
            loanDetailDAO = LoanDetailDAO()

            index_lender_LoginId = request.args.get("index_lender_LoginId")

            loanDetailVO.loan_LoginId = index_lender_LoginId

            ajaxGraphDataList = loanDetailDAO.adminGetGraphData(loanDetailVO)

            print("________ajaxGraphDataList__________", ajaxGraphDataList)

            graphDict = {}
            counter = False
            if len(ajaxGraphDataList) != 0:
                counter = True

                dict1 = {}
                for i in ajaxGraphDataList:
                    dict1[i.loanId] = {"loanAmount": i.loanAmount, "loanRate": i.loanRate,
                                       "loanDuration": i.loanDuration, "loanEMI": i.loanEMI}

                graphDict.update(dict1)
            print('graphDict>>>', graphDict)
            if counter:
                response = {'responseKey': graphDict}
                print('response>>>>>>>>', response)

            else:
                response = {'responseKey': 'Error'}

            return jsonify(response)

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)
