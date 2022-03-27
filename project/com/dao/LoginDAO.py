from project import db
from project.com.vo.LoginVO import LoginVO


class LoginDAO:
    def insertLogin(self, loginVO):
        db.session.add(loginVO)
        db.session.commit()

    def validateLogin(self, loginVO):
        loginList = LoginVO.query.filter_by(loginUserName=loginVO.loginUserName, loginPassword=loginVO.loginPassword,
                                            loginStatus=LoginVO.loginStatus)
        return loginList

    def viewLogin(self):
        loginList = LoginVO.query.all()
        return loginList

    # def adminUpdateLoginStatus(self, loginVO):
    #     db.session.merge(loginVO)
    #     db.session.commit()

    def validateLoginUserName(self, loginVO):
        loginList = LoginVO.query.filter_by(loginUserName=loginVO.loginUserName).all()
        return loginList

    # def loginUpdatePassword(self, loginVO):
    #     db.session.merge(loginVO)
    #     db.session.commit()

    def updateLogin(self, loginVO):
        db.session.merge(loginVO)
        db.session.commit()
