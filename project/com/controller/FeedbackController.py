from datetime import datetime

from flask import request, render_template, redirect, url_for, session

from project import app
from project.com.controller.LoginController import adminLogoutSession, adminLoginSession
from project.com.dao.FeedbackDAO import FeedbackDAO
from project.com.vo.FeedbackVO import FeedbackVO


# ----------------------- Lender Side -----------------------------------

@app.route('/lender/loadFeedback', methods=['GET'])
def lenderLoadFeedback():
    try:
        if adminLoginSession() == 'lender':
            return render_template('lender/addFeedback.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/lender/insertFeedback', methods=['POST'])
def lenderInsertFeedbcak():
    try:
        if adminLoginSession() == 'lender':
            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()

            feedbackSubject = request.form['feedbackSubject']
            feedbackDescription = request.form['feedbackDescription']
            feedbackRating = request.form['feedbackRating']

            now = datetime.now()

            feedbackDate = now.date()
            feedbackTime = now.strftime("%I:%M:%S %p")

            feedbackVO.feedbackSubject = feedbackSubject
            feedbackVO.feedbackDescription = feedbackDescription
            feedbackVO.feedbackRating = feedbackRating
            feedbackVO.feedbackDate = feedbackDate
            feedbackVO.feedbackTime = feedbackTime
            feedbackVO.feedbackFrom_LoginId = session['session_loginId']

            feedbackDAO.insertFeedback(feedbackVO)

            return redirect(url_for('lenderViewFeedback'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/lender/viewFeedback', methods=['GET'])
def lenderViewFeedback():
    try:
        if adminLoginSession() == 'lender':
            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackVO.feedbackFrom_LoginId = session['session_loginId']

            FeedbackList = feedbackDAO.viewFeedback(feedbackVO)

            print("__________________", FeedbackList)

            return render_template('lender/viewFeedback.html', FeedbackList=FeedbackList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/lender/deleteFeedback', methods=['GET'])
def lenderDeleteFeedback():
    try:
        if adminLoginSession() == 'lender':
            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackId = request.args.get('feedbackId')

            feedbackVO.feedbackId = feedbackId
            feedbackDAO.deleteFeedback(feedbackVO)

            return redirect(url_for('lenderViewFeedback'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


# ----------------------- Borrower Side -----------------------------------


@app.route('/borrower/loadFeedback', methods=['GET'])
def borrowerLoadFeedback():
    try:
        if adminLoginSession() == 'borrower':
            return render_template('borrower/addFeedback.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/borrower/insertFeedback', methods=['POST'])
def borrowerInsertFeedback():
    try:
        if adminLoginSession() == 'borrower':
            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()

            feedbackSubject = request.form['feedbackSubject']
            feedbackDescription = request.form['feedbackDescription']
            feedbackRating = request.form['feedbackRating']

            now = datetime.now()

            feedbackDate = now.date()
            feedbackTime = now.strftime("%I:%M:%S %p")

            feedbackVO.feedbackSubject = feedbackSubject
            feedbackVO.feedbackDescription = feedbackDescription
            feedbackVO.feedbackRating = feedbackRating
            feedbackVO.feedbackDate = feedbackDate
            feedbackVO.feedbackTime = feedbackTime
            feedbackVO.feedbackFrom_LoginId = session['session_loginId']

            feedbackDAO.insertFeedback(feedbackVO)

            return redirect(url_for('borrowerViewFeedback'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/borrower/viewFeedback', methods=['GET'])
def borrowerViewFeedback():
    try:
        if adminLoginSession() == 'borrower':
            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackVO.feedbackFrom_LoginId = session['session_loginId']

            FeedbackVOList = feedbackDAO.viewFeedback(feedbackVO)

            print("__________________", FeedbackVOList)

            return render_template('borrower/viewFeedback.html', FeedbackVOList=FeedbackVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/borrower/deleteFeedback', methods=['GET'])
def borrowerDeleteFeedback():
    try:
        if adminLoginSession() == 'borrower':
            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackId = request.args.get('feedbackId')

            feedbackVO.feedbackId = feedbackId
            feedbackDAO.deleteFeedback(feedbackVO)

            return redirect(url_for('borrowerViewFeedback'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


# ----------------------- Admin Side -----------------------------------


@app.route('/admin/viewFeedback', methods=['GET'])
def adminViewFeedback():
    try:
        if adminLoginSession() == 'admin':
            feedbackDAO = FeedbackDAO()

            FeedbackVOList = feedbackDAO.adminViewFeedback()

            print("__________________", FeedbackVOList)

            return render_template('admin/viewFeedback.html', FeedbackVOList=FeedbackVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/reviewFeedback')
def adminReviewFeedback():
    try:
        if adminLoginSession() == 'admin':
            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()

            feedbackId = request.args.get('feedbackId')
            feedbackTo_LoginId = session['session_loginId']

            feedbackVO.feedbackId = feedbackId
            feedbackVO.feedbackTo_LoginId = feedbackTo_LoginId

            feedbackDAO.adminReviewFeedback(feedbackVO)

            return redirect(url_for('adminViewFeedback'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
