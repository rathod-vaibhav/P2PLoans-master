from project import db
from project.com.vo.LoginVO import LoginVO


class FeedbackVO(db.Model):
    __tablename__ = 'feedbackmaster'
    feedbackId = db.Column('feedbackId', db.Integer, primary_key=True, autoincrement=True)
    feedbackSubject = db.Column('feedbackSubject', db.String(100))
    feedbackDescription = db.Column('feedbackDescription', db.String(1000))
    feedbackRating = db.Column('feedbackRating', db.Integer)
    feedbackDate = db.Column('feedbackDate', db.DATE)
    feedbackTime = db.Column('feedbackTime', db.String(100))
    feedbackTo_LoginId = db.Column('feedbackTo_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))
    feedbackFrom_LoginId = db.Column('feedbackFrom_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'feedbackId': self.feedbackId,
            'feedbackSubject': self.feedbackSubject,
            'feedbackDescription': self.feedbackDescription,
            'feedbackRating': self.feedbackRating,
            'feedbackDate': self.feedbackDdate,
            'feedbackTime': self.feedbackTime,
            'feedbackTo_LoginId': self.feedbackTo_LoginId,
            'feedbackFrom_LoginId': self.feedbackFrom_LoginId

        }


db.create_all()
