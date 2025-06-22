from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Episode, Guest, Appearance

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

@app.route('/')
def index():
    return make_response({"message": "Welcome to the Podcast API"}, 200)


class Episodes(Resource):
    def get(self):
        episodes = [episode.to_dict() for episode in Episode.query.all()]
        return make_response(episodes, 200)
    
    

api.add_resource(Episodes, '/episodes')


class EpisodeById(Resource):
    def get(self, episode_id):
        episode = db.session.get(Episode, episode_id)
        if not episode:
            return make_response({"error": "Episode not found"}, 404)
        return make_response(episode.to_dict_with_appearances(), 200)
    
    def delete(self, episode_id):
        episode = db.session.get(Episode, episode_id)
        if not episode:
            return make_response({"error": "Episode not found"}, 404)
        db.session.delete(episode)
        db.session.commit()
        return make_response({"message": "Episode deleted successfully"}, 204)

api.add_resource(EpisodeById, '/episodes/<int:episode_id>')


class Guests(Resource):
    def get(self):
        guests = [guest.to_dict() for guest in Guest.query.all()]
        return make_response(guests, 200)

api.add_resource(Guests, '/guests')


class Appearances(Resource):
    def post(self):
        data = request.get_json()
        try:
            appearance = Appearance(
                rating=data["rating"],
                episode_id=data["episode_id"],
                guest_id=data["guest_id"]
            )
            db.session.add(appearance)
            db.session.commit()
            return make_response(appearance.to_full_dict(), 201)
        except Exception as e:
            db.session.rollback()
            return make_response({"errors": [str(e)]}, 400)

api.add_resource(Appearances, '/appearances')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

   