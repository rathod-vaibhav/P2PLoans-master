from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.CityVO import CityVO


class AreaDAO:
    def insertArea(self, areaVo):
        db.session.add(areaVo)

        db.session.commit()

    def viewArea(self):
        areaList = db.session.query(AreaVO, CityVO).join(CityVO, AreaVO.area_CityId == CityVO.cityId).all()

        return areaList

    def deleteArea(self, areaId):
        areaList = AreaVO.query.get(areaId)

        db.session.delete(areaList)

        db.session.commit()

    def editArea(self, areaVO):
        areaList = AreaVO.query.filter_by(areaId=areaVO.areaId)

        return areaList

    def updateArea(self, areaVO):
        db.session.merge(areaVO)

        db.session.commit()

    def ajaxAreaProduct(self, areaVo):
        ajaxProductAreaList = AreaVO.query.filter_by(area_CityId=areaVo.area_CityId).all()

        return ajaxProductAreaList
