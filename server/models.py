from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import relationship, validates

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)


class Episode(db.Model):
    __tablename__ = 'episodes'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    number = db.Column(db.Integer, nullable=False)

    appearances = db.relationship("Appearance", back_populates="episode", cascade="all, delete")
    guests = db.relationship("Guest", secondary="appearances", back_populates="episodes")

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.strftime('%-m/%-d/%y'),
            "number": self.number
        }

    def to_dict_with_appearances(self):
        return {
            "id": self.id,
            "date": self.date.strftime('%-m/%-d/%y'),
            "number": self.number,
            "appearances": [appearance.to_dict_with_guest() for appearance in self.appearances]
        }

    def __repr__(self):
        return f"<Episode {self.number}, {self.date}>"


class Guest(db.Model):
    __tablename__ = 'guests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=False)

    appearances = db.relationship("Appearance", back_populates="guest", cascade="all, delete")
    episodes = db.relationship("Episode", secondary="appearances", back_populates="guests")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "occupation": self.occupation
        }

    def __repr__(self):
        return f"<Guest {self.name}, {self.occupation}>"


class Appearance(db.Model):
    __tablename__ = 'appearances'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=True)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)

    episode = db.relationship("Episode", back_populates="appearances")
    guest = db.relationship("Guest", back_populates="appearances")

    @validates("rating")
    def validate_rating(self, key, value):
        if value is None:
            raise ValueError("Rating cannot be None")
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5")
        return value

    def to_dict_with_guest(self):
        return {
            "id": self.id,
            "rating": self.rating,
            "guest_id": self.guest_id,
            "episode_id": self.episode_id,
            "guest": self.guest.to_dict()
        }

    def to_full_dict(self):
        return {
            "id": self.id,
            "rating": self.rating,
            "guest_id": self.guest_id,
            "episode_id": self.episode_id,
            "guest": self.guest.to_dict(),
            "episode": self.episode.to_dict()
        }

    def __repr__(self):
        return f"<Appearance Guest {self.guest.name} in Episode {self.episode.number}>"

