from project import db


class CityVO(db.Model):
    __tablename__ = 'citymaster'
    cityId = db.Column('cityId', db.Integer, primary_key=True, autoincrement=True)
    cityName = db.Column('cityName', db.String(100))
    cityDescription = db.Column('cityDescription', db.String(1000))

    def as_dict(self):
        return {
            'cityId': self.cityId,
            'cityName': self.cityName,
            'cityDescription': self.cityDescription
        }


db.create_all()
