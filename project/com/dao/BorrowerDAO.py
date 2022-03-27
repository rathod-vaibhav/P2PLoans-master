from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.BorrowerVO import BorrowerVO
from project.com.vo.CityVO import CityVO
from project.com.vo.LoginVO import LoginVO


class BorrowerDAO:
    def insertBorrower(self, borrowerVO):
        db.session.add(borrowerVO)

        db.session.commit()

    def adminViewBorrower(self):
        borrowerVOList = db.session.query(BorrowerVO, LoginVO, CityVO, AreaVO). \
            join(LoginVO, BorrowerVO.borrower_LoginId == LoginVO.loginId, ). \
            join(CityVO, BorrowerVO.borrower_CityId == CityVO.cityId). \
            join(AreaVO, BorrowerVO.borrower_AreaId == AreaVO.areaId).all()
        return borrowerVOList

    def viewProfile(self, borrowerVO):
        borrowerList = db.session.query(BorrowerVO, LoginVO, CityVO, AreaVO). \
            join(LoginVO, BorrowerVO.borrower_LoginId == LoginVO.loginId, ). \
            join(CityVO, BorrowerVO.borrower_CityId == CityVO.cityId). \
            join(AreaVO, BorrowerVO.borrower_AreaId == AreaVO.areaId). \
            filter(BorrowerVO.borrower_LoginId == borrowerVO.borrower_LoginId).all()
        return borrowerList

    def updateBorrower(self, borrowerVO):
        db.session.merge(borrowerVO)
        db.session.commit()
