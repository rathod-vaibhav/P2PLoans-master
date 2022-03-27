from project import db
from project.com.vo.LoginVO import LoginVO


class ScrapingVO(db.Model):
    __tablename__ = 'scrapingmaster'
    scrapingId = db.Column('scrapingId', db.Integer, primary_key=True, autoincrement=True)
    scrapingSocialId = db.Column('scrapingSocialId', db.String(100))
    scrapingPostTime = db.Column('scrapingPostTime', db.String(100))
    scrapingLike = db.Column('scrapingLike', db.Integer)
    scrapingComment = db.Column('scrapingComment', db.Integer)
    scrapingMedia = db.Column('scrapingMedia', db.String(1000))
    scrapingVideo = db.Column('scrapingVideo', db.BOOLEAN)
    scrapingFrom_LoginId = db.Column('scrapingFrom_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    # scrapingStatus = db.Column('scrapingStatus', db.String(1000))

    def as_dict(self):
        return {
            'scrapingId': self.scrapingId,
            'scrapingSocialId': self.scrapingSocialId,
            'scrapingPostTime': self.scrapingPostTime,
            'scrapingLike': self.scrapingLike,
            'scrapingComment': self.scrapingComment,
            'scrapingMedia': self.scrapingMedia,
            'scrapingVideo': self.scrapingVideo,
            'scrapingFrom_LoginId': self.scrapingFrom_LoginId
            # 'scrapingStatus': self.scrapingStatus
        }


db.create_all()
