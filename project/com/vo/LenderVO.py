from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.CityVO import CityVO
from project.com.vo.LoginVO import LoginVO


class LenderVO(db.Model):
    __tablename__ = 'lendermaster'
    lenderId = db.Column('lenderId', db.Integer, primary_key=True, autoincrement=True)
    lenderName = db.Column('lenderName', db.String(200), nullable=False)
    lenderDateOfBirth = db.Column('lenderDateOfBirth', db.DATE, nullable=False)
    lenderContact = db.Column('lenderContact', db.BigInteger, nullable=False)
    lender_CityId = db.Column('lender_CityId', db.Integer, db.ForeignKey(CityVO.cityId), nullable=False)
    lender_AreaId = db.Column('lender_AreaId', db.Integer, db.ForeignKey(AreaVO.areaId), nullable=False)
    lenderPanCardFileName = db.Column('lenderPanCardFileName', db.String(100), nullable=False)
    lenderPanCardFilePath = db.Column('lenderPanCardFilePath', db.String(1000), nullable=False)
    lenderAdharCardFileName = db.Column('lenderAdharCardFileName', db.String(100), nullable=False)
    lenderAdharCardFilePath = db.Column('lenderAdharCardFilePath', db.String(1000), nullable=False)
    lenderAddress = db.Column('lenderAddress', db.String(200), nullable=False)
    lender_LoginId = db.Column('lender_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId), nullable=False)

    def as_dict(self):
        return {
            'lenderId': self.lenderId,
            'lenderName': self.lenderName,
            'lenderDateOfBirth': self.lenderDateOfBirth,
            'lenderContact': self.lenderContact,
            'lender_CityId': self.lender_CityId,
            'lender_AreaId': self.lender_AreaId,
            'lenderPanCardFileName': self.lenderPanCardFileName,
            'lenderPanCardFilePath': self.lenderPanCardFilePath,
            'lenderAdharCardFileName': self.lenderAdharCardFileName,
            'lenderAdharCardFilePath': self.lenderAdharCardFilePath,
            'lenderAddress': self.lenderAddress,
            'lender_LoginId': self.lender_LoginId

        }


db.create_all()
