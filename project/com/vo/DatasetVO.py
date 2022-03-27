from project import db


class DatasetVO(db.Model):
    __tablename__ = 'datasetmaster'
    datasetId = db.Column('datasetId', db.Integer, primary_key=True, autoincrement=True)
    datasetFileName = db.Column('datasetFileName', db.String(1000), nullable=False)
    datasetFilePath = db.Column('datasetFilePath', db.String(1000), nullable=False)
    datasetUploadDate = db.Column('datasetUploadDate', db.DATE)
    datasetUploadTime = db.Column('datasetUploadTime', db.String(100))

    def as_dict(self):
        return {
            'datasetId': self.datasetId,
            'datasetFileName': self.datasetFileName,
            'datasetFilePath': self.datasetFilePath,
            'datasetUploadDate': self.datasetUploadDate,
            'datasetUploadTime': self.datasetUploadTime
        }


db.create_all()
