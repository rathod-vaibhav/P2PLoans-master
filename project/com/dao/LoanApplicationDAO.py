from sqlalchemy import func

from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.BorrowerVO import BorrowerVO
from project.com.vo.CityVO import CityVO
from project.com.vo.LenderVO import LenderVO
from project.com.vo.LoanApplicationVO import LoanApplicationVO
from project.com.vo.LoanDetailVO import LoanDetailVO
from project.com.vo.LoginVO import LoginVO


class LoanApplicationDAO:
    # --------------------- borrower Side ----------------------
    def borrowerInsertLoanApplication(self, loanApplicationVO):
        db.session.add(loanApplicationVO)
        db.session.commit()

    def borrowerViewLoanApplication(self, loanApplicationVO):
        loanApplicationList = db.session.query(LoanApplicationVO, LoanDetailVO, LoginVO, LenderVO, CityVO, AreaVO). \
            join(LoanDetailVO, LoanApplicationVO.application_LoanId == LoanDetailVO.loanId). \
            join(LoginVO, LoanDetailVO.loan_LoginId == LoginVO.loginId). \
            join(LenderVO, LoginVO.loginId == LenderVO.lender_LoginId). \
            join(CityVO, LenderVO.lender_CityId == CityVO.cityId). \
            join(AreaVO, LenderVO.lender_AreaId == AreaVO.areaId). \
            filter(LoanApplicationVO.applicationFrom_LoginId == loanApplicationVO.applicationFrom_LoginId).all()
        return loanApplicationList

    # ------------- lender Side --------------------------

    def lenderIndexViewLoanApplication(self, loanApplicationVO):
        loanApplicationList = db.session.query(LoanApplicationVO, LoanDetailVO, LoginVO, BorrowerVO, CityVO, AreaVO). \
            join(LoanDetailVO, LoanApplicationVO.application_LoanId == LoanDetailVO.loanId). \
            join(LoginVO, LoanApplicationVO.applicationFrom_LoginId == LoginVO.loginId). \
            join(BorrowerVO, LoginVO.loginId == BorrowerVO.borrower_LoginId). \
            join(CityVO, BorrowerVO.borrower_CityId == CityVO.cityId). \
            join(AreaVO, BorrowerVO.borrower_AreaId == AreaVO.areaId). \
            filter(LoanApplicationVO.application_LoanId == LoanDetailVO.loanId). \
            filter(LoanDetailVO.loan_LoginId == loanApplicationVO.applicationTo_LoginId). \
            filter(LoanApplicationVO.applicationStatus == loanApplicationVO.applicationStatus).all()
        return loanApplicationList

    def lenderViewApprovelCount(self):
        loanApprovalsStatusList = []
        approveStatus = db.session.query(LoanApplicationVO.applicationFrom_LoginId,
                                         func.count(LoanApplicationVO.applicationStatus)). \
            filter_by(applicationStatus="approve"). \
            group_by(LoanApplicationVO.applicationFrom_LoginId).all()

        rejectStatus = db.session.query(LoanApplicationVO.applicationFrom_LoginId,
                                        func.count(LoanApplicationVO.applicationStatus)). \
            filter_by(applicationStatus="reject"). \
            group_by(LoanApplicationVO.applicationFrom_LoginId).all()

        return approveStatus, rejectStatus

    def lenderUpdateLoanApplication(self, loanApplicationVO):
        db.session.merge(loanApplicationVO)
        db.session.commit()

    def lenderViewLoanApplication(self, loanApplicationVO):
        loanApproveApplicationList = db.session.query(LoanApplicationVO, LoanDetailVO, LoginVO, BorrowerVO, CityVO,
                                                      AreaVO). \
            join(LoanDetailVO, LoanApplicationVO.application_LoanId == LoanDetailVO.loanId). \
            join(LoginVO, LoanApplicationVO.applicationFrom_LoginId == LoginVO.loginId). \
            join(BorrowerVO, LoginVO.loginId == BorrowerVO.borrower_LoginId). \
            join(CityVO, BorrowerVO.borrower_CityId == CityVO.cityId). \
            join(AreaVO, BorrowerVO.borrower_AreaId == AreaVO.areaId). \
            filter(LoanApplicationVO.application_LoanId == loanApplicationVO.application_LoanId). \
            filter(LoanApplicationVO.applicationTo_LoginId == loanApplicationVO.applicationTo_LoginId). \
            filter(LoanApplicationVO.applicationStatus == loanApplicationVO.applicationStatus).all()
        return loanApproveApplicationList

    def adminViewLoanApplication(self):
        loanApplicationList = db.session.query(LoanApplicationVO, LoanDetailVO, LoginVO) \
            .join(LoanDetailVO, LoanApplicationVO.application_LoanId == LoanDetailVO.loanId) \
            .join(LoginVO, LoanApplicationVO.applicationFrom_LoginId == LoginVO.loginId).all()

        print(loanApplicationList)

        return loanApplicationList

    def insertScrapingStatus(self, loanApplicationVO):
        db.session.merge(loanApplicationVO)
        db.session.commit()

    # ------------- lender Side --------------------------

    def viewData(self):
        data = []

        totalAmount = db.session.query(LoanApplicationVO.application_LoanId,
                                       func.sum(LoanDetailVO.loanAmount)). \
            join(LoanDetailVO, LoanApplicationVO.application_LoanId == LoanDetailVO.loanId). \
            filter(LoanApplicationVO.applicationStatus == "approve"). \
            group_by(LoanDetailVO.loanId).all()
        data.append(totalAmount)

        totalApplication = db.session.query(LoanApplicationVO.applicationStatus,
                                            func.count(LoanApplicationVO.applicationStatus),
                                            ).group_by(
            LoanApplicationVO.applicationStatus).all()
        data.append(totalApplication)

        totalLender = db.session.query(LenderVO).all()
        data.append(totalLender)

        totalBorrower = db.session.query(BorrowerVO).all()
        data.append(totalBorrower)

        return data
