from project import db
from project.com.vo.LoginVO import LoginVO


class PreviousLoanVO(db.Model):
    __tablename__ = 'previousloanmaster'
    previousLoanId = db.Column('previousLoanId', db.Integer, primary_key=True, autoincrement=True)
    previousLoanFileName = db.Column('previousLoanFileName', db.String(1000))
    previousLoanFilePath = db.Column('previousLoanFilePath', db.String(1000))
    outputFilePath = db.Column('outputFilePath', db.String(1000))
    outputFileName = db.Column('outputFileName', db.String(1000))
    previousLoanFrom_LoginId = db.Column('previousLoanFrom_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId),
                                         nullable=False)

    def as_dict(self):
        return {
            'previousLoanId': self.previousLoanId,
            'previousLoanFileName': self.previousLoanFileName,
            'previousLoanFilePath': self.previousLoanFilePath,
            'outputFilePath': self.outputFilePath,
            'outputFileName': self.outputFileName,
            'previousLoanFrom_LoginId': self.previousLoanFrom_LoginId

        }


db.create_all()
