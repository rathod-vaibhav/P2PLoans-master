from project import db
from project.com.vo.LoginVO import LoginVO


class LoanDetailVO(db.Model):
    __tablename__ = 'loandetailmaster'
    loanId = db.Column('loanId', db.Integer, primary_key=True, autoincrement=True)
    loanAmount = db.Column('loanAmount', db.Integer)
    loanRate = db.Column('loanRate', db.Integer)
    loanDuration = db.Column('loanDuration', db.Integer)
    loanEMI = db.Column('loanEMI', db.Integer)
    loan_LoginId = db.Column('loan_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'loanId': self.loanId,
            'loanAmount': self.loanAmount,
            'loanRate': self.loanRate,
            'loanDuration': self.loanDuration,
            'loanEMI': self.loanEMI,
            'loan_LoginId': self.loan_LoginId
        }


db.create_all()
