from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.CityVO import CityVO
from project.com.vo.LoginVO import LoginVO


class BorrowerVO(db.Model):
    __tablename__ = 'borrowermaster'
    borrowerId = db.Column('borrowerId', db.Integer, primary_key=True, autoincrement=True)
    borrowerName = db.Column('borrowerName', db.String(200), nullable=False)
    borrowerDateOfBirth = db.Column('borrowerDateOfBirth', db.DATE, nullable=False)
    borrowerContact = db.Column('borrowerContact', db.BigInteger, nullable=False)
    borrower_CityId = db.Column('borrower_CityId', db.Integer, db.ForeignKey(CityVO.cityId), nullable=False)
    borrower_AreaId = db.Column('borrower_AreaId', db.Integer, db.ForeignKey(AreaVO.areaId), nullable=False)
    borrowerPanCardFileName = db.Column('borrowerPanCardFileName', db.String(100), nullable=False)
    borrowerPanCardFilePath = db.Column('borrowerPanCardFilePath', db.String(1000), nullable=False)
    borrowerAdharCardFileName = db.Column('borrowerAdharCardFileName', db.String(100), nullable=False)
    borrowerAdharCardFilePath = db.Column('borrowerAdharCardFilePath', db.String(1000), nullable=False)
    borrowerAddress = db.Column('borrowerAddress', db.String(200), nullable=False)
    borrowerSocialMediaLink = db.Column('borrowerSocialMediaLink', db.String(200), nullable=False)
    borrower_LoginId = db.Column('borrower_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId), nullable=False)

    def as_dict(self):
        return {
            'borrowerId': self.borrowerId,
            'borrowerName': self.borrowerName,
            'borrowerDateOfBirth': self.borrowerDateOfBirth,
            'borrowerContact': self.borrowerContact,
            'borrower_CityId': self.borrower_CityId,
            'borrower_AreaId': self.borrower_AreaId,
            'borrowerPanCardFileName': self.borrowerPanCardFileName,
            'borrowerPanCardFilePath': self.borrowerPanCardFilePath,
            'borrowerAdharCardFileName': self.borrowerAdharCardFileName,
            'borrowerAdharCardFilePath': self.borrowerAdharCardFilePath,
            'borrowerAddress': self.borrowerAddress,
            'borrowerSocialMediaLink': self.borrowerSocialMediaLink,
            'borrower_LoginId': self.borrower_LoginId

        }


db.create_all()
