from project import db
from project.com.vo.CityVO import CityVO


class CityDAO:
    def insertCity(self, cityVO):
        db.session.add(cityVO)
        db.session.commit()

    def viewCity(self):
        cityList = CityVO.query.all()

        return cityList

    def deleteCity(self, cityVO):
        cityList = CityVO.query.get(cityVO.cityId)

        db.session.delete(cityList)

        db.session.commit()

    def editCity(self, cityVO):
        cityList = CityVO.query.filter_by(cityId=cityVO.cityId).all()

        return cityList

    def updateCity(self, cityVO):
        db.session.merge(cityVO)

        db.session.commit()
