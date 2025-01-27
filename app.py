from flask import Flask, request, jsonify, render_template
from extensions import db, ma
from models import QuestModel
from schema import quest_schema, quests_schema

app = Flask(__name__, template_folder='Resources\\Web')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quests.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)


@app.route('/quests/generate', methods=['POST'])
def create_random_quests():
    """
    Generate and save a set of random quests.
    """
    try:
        quests = QuestModel.generate_random_quests(5)
        db.session.add_all(quests)
        db.session.commit()
        return quests_schema.jsonify(quests), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route('/quest', methods=['POST'])
def create_quest():
    data = request.json
    try:
        quest = QuestModel(**data)
        quest.validate()
        db.session.add(quest)
        db.session.commit()
        return quest_schema.jsonify(quest), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route('/quest/<quest_id>', methods=['GET'])
def get_quest(quest_id):
    quest = QuestModel.query.get(quest_id)
    if not quest:
        return jsonify({"error": "Quest not found"}), 404
    return quest_schema.jsonify(quest)


@app.route('/', methods=['GET'])
def homepage():
    quests = QuestModel.query.all()
    return render_template('index.html', quests=quests)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
