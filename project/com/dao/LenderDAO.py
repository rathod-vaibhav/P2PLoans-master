from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.CityVO import CityVO
from project.com.vo.LenderVO import LenderVO
from project.com.vo.LoginVO import LoginVO


class LenderDAO:
    def insertLender(self, lenderVO):
        db.session.add(lenderVO)
        db.session.commit()

    def adminViewLender(self):
        lenderVOList = db.session.query(LenderVO, LoginVO, CityVO, AreaVO). \
            join(LoginVO, LenderVO.lender_LoginId == LoginVO.loginId, ). \
            join(CityVO, LenderVO.lender_CityId == CityVO.cityId). \
            join(AreaVO, LenderVO.lender_AreaId == AreaVO.areaId).all()
        return lenderVOList

    def viewProfile(self, lenderVO):
        lenderList = db.session.query(LenderVO, LoginVO, CityVO, AreaVO). \
            join(LoginVO, LenderVO.lender_LoginId == LoginVO.loginId, ). \
            join(CityVO, LenderVO.lender_CityId == CityVO.cityId). \
            join(AreaVO, LenderVO.lender_AreaId == AreaVO.areaId). \
            filter(LenderVO.lender_LoginId == lenderVO.lender_LoginId).all()
        return lenderList

    def updateLender(self, lenderVO):
        db.session.merge(lenderVO)
        db.session.commit()
