from flask_marshmallow import Marshmallow
from config import app

ma = Marshmallow(app)


class NFLShareSchema(ma.Schema):
    class Meta:
        fields = ('id', "date", "score", "teams")


class NBAShareSchema(ma.Schema):
    class Meta:
        fields = ('id', "date", "score", "teams")


class MLBShareSchema(ma.Schema):
    class Meta:
        fields = ('id', "date", "score", "teams")


class UFCShareSchema(ma.Schema):
    class Meta:
        fields = ('id', "date", "result", "fighters", "winner")
