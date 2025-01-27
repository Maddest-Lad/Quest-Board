from extensions import ma
from models import QuestModel

class QuestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = QuestModel
        include_fk = True

quest_schema = QuestSchema()
quests_schema = QuestSchema(many=True)
