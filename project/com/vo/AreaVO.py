from project import db
from project.com.vo.CityVO import CityVO


class AreaVO(db.Model):
    __tablename__ = 'areamaster'
    areaId = db.Column('areaId', db.Integer, primary_key=True, autoincrement=True)
    areaName = db.Column('areaName', db.String(100), nullable=False)
    areaPincode = db.Column('areaPincode', db.Integer, nullable=False)
    area_CityId = db.Column('area_CityId', db.Integer, db.ForeignKey(CityVO.cityId))

    def as_dict(self):
        return {
            'areaId': self.areaId,
            'areaName': self.areaName,
            'areaPincode': self.areaPincode,
            'area_CityId': self.area_CityId
        }


db.create_all()
