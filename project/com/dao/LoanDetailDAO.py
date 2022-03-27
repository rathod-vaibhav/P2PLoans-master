from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.CityVO import CityVO
from project.com.vo.LenderVO import LenderVO
from project.com.vo.LoanDetailVO import LoanDetailVO
from project.com.vo.LoginVO import LoginVO


class LoanDetailDAO:
    # ----------------- lender side ----------------------------
    def insertLoanDetail(self, loanDetailVO):
        db.session.add(loanDetailVO)
        db.session.commit()

    def lenderViewLoanDetail(self, loanDetailVO):
        loanDetailList = db.session.query(LoanDetailVO) \
            .filter(LoanDetailVO.loan_LoginId == loanDetailVO.loan_LoginId).all()

        return loanDetailList

    def deleteLoanDetail(self, loanDetailVO):
        loanDetailList = LoanDetailVO.query.get(loanDetailVO.loanId)
        db.session.delete(loanDetailList)
        db.session.commit()
        return loanDetailList

    def borrowerIndexViewLoanDetail(self):
        loanDetailList = db.session.query(LoanDetailVO, LoginVO, LenderVO, CityVO, AreaVO). \
            join(LoginVO, LoanDetailVO.loan_LoginId == LoginVO.loginId). \
            join(LenderVO, LoginVO.loginId == LenderVO.lender_LoginId). \
            join(CityVO, LenderVO.lender_CityId == CityVO.cityId). \
            join(AreaVO, LenderVO.lender_AreaId == AreaVO.areaId).all()
        return loanDetailList

    def borrowerViewLoanDetail(self, loanDetailVO):
        loanDetaiList = db.session.query(LoanDetailVO, LoginVO, LenderVO, CityVO, AreaVO). \
            filter(LoanDetailVO.loan_LoginId == LoginVO.loginId). \
            filter(LoginVO.loginId == LenderVO.lender_LoginId). \
            filter(LenderVO.lender_CityId == CityVO.cityId). \
            filter(LenderVO.lender_AreaId == AreaVO.areaId). \
            filter(LoanDetailVO.loanId == loanDetailVO.loanId).all()
        return loanDetaiList

    def adminGetGraphData(self, loanDetailVO):
        index_lender_LoginId = LoanDetailVO.query \
            .filter(LoanDetailVO.loan_LoginId == loanDetailVO.loan_LoginId).all()
        return index_lender_LoginId
