from project import db
from project.com.vo.LoanApplicationVO import LoanApplicationVO
from project.com.vo.PreviousLoanVO import PreviousLoanVO


class PreviousLoanDAO:
    def insertPreviousLoan(self, previousLoanVO):
        db.session.add(previousLoanVO)

        db.session.commit()

    def viewApprovelCount(self, previousLoanVO):
        loanApprovalsStatusList = []

        approveStatus = db.session.query(LoanApplicationVO). \
            filter(LoanApplicationVO.applicationFrom_LoginId == previousLoanVO.previousLoanFrome_LoginId). \
            filter(LoanApplicationVO.applicationStatus == 'approve').count()
        loanApprovalsStatusList.append(approveStatus)

        rejectStatus = db.session.query(LoanApplicationVO). \
            filter(LoanApplicationVO.applicationFrom_LoginId == previousLoanVO.previousLoanFrome_LoginId). \
            filter(LoanApplicationVO.applicationStatus == 'reject').count()
        loanApprovalsStatusList.append(rejectStatus)

        return loanApprovalsStatusList

    def viewPreviousLoanRecord(self, previousLoanVO):
        previouseLoanRecordList = db.session.query(PreviousLoanVO). \
            filter(PreviousLoanVO.previousLoanFrom_LoginId == previousLoanVO.previousLoanFrome_LoginId).all()

        return previouseLoanRecordList

    def readFile(self, previousLoanVO):
        readFile = db.session.query(PreviousLoanVO). \
            filter(PreviousLoanVO.previousLoanFrom_LoginId == previousLoanVO.previousLoanFrome_LoginId).all()

        return readFile

    def insertPredictionOutput(self, previousLoanVO):
        db.session.merge(previousLoanVO)
        db.session.commit()

    def viewPredictionOutput(self, previousLoanVO):
        predictionOutputList = db.session.query(PreviousLoanVO). \
            filter(PreviousLoanVO.previousLoanFrom_LoginId == previousLoanVO.previousLoanFrome_LoginId).all()
        return predictionOutputList
