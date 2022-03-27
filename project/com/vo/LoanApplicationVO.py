from project import db
from project.com.vo.LoanDetailVO import LoanDetailVO
from project.com.vo.LoginVO import LoginVO


class LoanApplicationVO(db.Model):
    __tablename__ = 'loanapplicationmaster'
    applicationId = db.Column('applicationId', db.Integer, primary_key=True, autoincrement=True)
    application_LoanId = db.Column('application_LoanId', db.Integer, db.ForeignKey(LoanDetailVO.loanId))
    applicationFrom_LoginId = db.Column('applicationFrom_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))
    applicationTo_LoginId = db.Column('applicationTo_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))
    applicationDate = db.Column('applicationDate', db.DATE)
    applicationTime = db.Column('applicationTime', db.String(100))
    applicationApprovalDate = db.Column('applicationApprovalDate', db.DATE)
    applicationApprovalTime = db.Column('applicationApprovalTime', db.String(100))
    applicationStatus = db.Column('applicationStatus', db.String(100))

    scrapingStatus = db.Column('scrapingStatus', db.String(100))

    def as_dict(self):
        return {
            'applicationId': self.applicationId,
            'application_LoanId': self.application_LoanId,
            'applicationFrom_LoginId': self.applicationFrom_LoginId,
            'applicationTo_LoginId': self.applicationTo_LoginId,
            'applicationDate': self.applicationDate,
            'applicationTime': self.applicationTime,
            'applicationApprovalDate': self.applicationApprovalDate,
            'applicationApprovalTime': self.applicationApprovalTime,
            'applicationStatus': self.applicationStatus,
            'scrapingStatus': self.scrapingStatus

        }


db.create_all()
