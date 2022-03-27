from project import db
from project.com.vo.FeedbackVO import FeedbackVO
from project.com.vo.LoginVO import LoginVO


class FeedbackDAO:
    def insertFeedback(self, feedbackVO):
        db.session.add(feedbackVO)
        db.session.commit()

    def viewFeedback(self, feedbackVO):
        feedbackList = FeedbackVO.query.filter_by(feedbackFrom_LoginId=feedbackVO.feedbackFrom_LoginId)

        return feedbackList

    def deleteFeedback(self, feedbackVO):
        feedbackList = feedbackVO.query.get(feedbackVO.feedbackId)

        db.session.delete(feedbackList)

        db.session.commit()

    def adminViewFeedback(self):
        feedbackList = db.session.query(FeedbackVO, LoginVO). \
            join(LoginVO, FeedbackVO.feedbackFrom_LoginId == LoginVO.loginId).all()

        return feedbackList

    def adminReviewFeedback(self, feedbackVO):
        db.session.merge(feedbackVO)
        db.session.commit()
