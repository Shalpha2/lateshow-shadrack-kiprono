from datetime import datetime
from app import app  
from models import db, Episode, Guest, Appearance

with app.app_context():
    

    print("Deleting data..")
    Episode.query.delete()
    Guest.query.delete()
    Appearance.query.delete()

    # Create sample Episodes

    episode1 = Episode(date=datetime(2024, 5, 1), number=1)
    episode2 = Episode(date=datetime(2024, 5, 8), number=2)
    episode3 = Episode(date=datetime(2024, 5, 15), number=3)
    

    # Create sample Guests
    guest1 = Guest(name="John Doe", occupation="Comedian")
    guest2 = Guest(name="Jane Smith", occupation="Actor")
    guest3 = Guest(name="Dr. Alex Ray", occupation="Scientist")
    guest4 = Guest(name="Emily Johnson", occupation="Author")
    guest5 = Guest(name="Michael Brown", occupation="Musician")

    # Create sample Appearances (ratings between 1 and 5)
    appearance1 = Appearance(rating=5, episode=episode1, guest=guest1)
    appearance2 = Appearance(rating=4, episode=episode1, guest=guest2)
    appearance3 = Appearance(rating=3, episode=episode2, guest=guest3)
    appearance4 = Appearance(rating=2, episode=episode2, guest=guest1)
    appearance5 = Appearance(rating=1, episode=episode3, guest=guest4)
    appearance6 = Appearance(rating=5, episode=episode3, guest=guest5)

    # Add to session and commit
    db.session.add_all([
        episode1, episode2, episode3,
        guest1, guest2, guest3, guest4, guest5,
        appearance1, appearance2, appearance3, appearance4, appearance5, appearance6
    ])
    db.session.commit()

    print("✅ Database seeded successfully!")
