from project import db
from project.com.vo.LoginVO import LoginVO
from project.com.vo.ScrapingVO import ScrapingVO


class ScrapingDAO:
    def insertScraping(self, scrapingVO):
        db.session.merge(scrapingVO)
        db.session.commit()

    def viewScraping(self, scrapingVO):
        scrapingList = db.session.query(ScrapingVO, LoginVO). \
            join(LoginVO, ScrapingVO.scrapingFrom_LoginId == LoginVO.loginId). \
            filter(ScrapingVO.scrapingFrom_LoginId == scrapingVO.scrapingFrom_LoginId).all()
        return scrapingList

    def validationScraping(self, scrapingVO):
        scrapingValidationList = ScrapingVO.query.filter_by(scrapingSocialId=scrapingVO.scrapingSocialId).all()
        return scrapingValidationList
