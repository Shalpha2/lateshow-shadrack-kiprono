## Late Show API
A Flask RESTful API for managing podcast episodes, guests, and their appearances on a fictional talk show.

## Repository Structure

lateshow-firstname-lastname/
│
├── server/
│   ├── app.py              # Main Flask app and routes
│   ├── models.py           # SQLAlchemy models
│   ├── seed.py             # Script to seed database with initial data
│   ├── migrations/         # Auto-generated database migrations
│   └── app.db              # SQLite database (after migration & seed)
├── README.md               # Project documentation (this file)
└── challenge-4-lateshow.postman_collection.json # Postman collection

##  Technologies Used
Python 3.x

Flask

Flask-RESTful

Flask-Migrate

SQLAlchemy

SQLite (for development)

Postman (for API testing)

##  Setup Instructions
1. Clone the Repository

git clone https://github.com/Shalpha2/lateshow-shadrack-kiprono
cd lateshow-firstname-lastname/server
2. Create and Activate Virtual Environment

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies

pip install -r requirements.txt

4. Run Database Migrations

flask db init        # Only run once
flask db revision --autogenerate -m "Initial migration"
flask db upgrade
5. Seed the Database

python seed.py
6. Start the Server

flask run
The API will be running on: http://127.0.0.1:5555

## API Endpoints

 GET /episodes
Returns all episodes:


[
  {
    "id": 1,
    "date": "5/1/24",
    "number": 1
  }
]
 GET /episodes/:id
Returns one episode with its appearances:


{
  "id": 1,
  "date": "5/1/24",
  "number": 1,
  "appearances": [
    {
      "id": 1,
      "rating": 5,
      "guest_id": 1,
      "episode_id": 1,
      "guest": {
        "id": 1,
        "name": "John Doe",
        "occupation": "Comedian"
      }
    }
  ]
}
If not found:


{
  "error": "Episode not found"
}

 DELETE /episodes/:id
Deletes an episode and its appearances:

Response status: 204 No Content

If not found:


{
  "error": "Episode not found"
}

 GET /guests
Returns a list of all guests:


[
  {
    "id": 1,
    "name": "John Doe",
    "occupation": "Comedian"
  }
]

 POST /appearances
Creates a new guest appearance:

Request body:

json
{
  "rating": 4,
  "episode_id": 1,
  "guest_id": 2
}
Success response:

json

{
  "id": 7,
  "rating": 4,
  "guest_id": 2,
  "episode_id": 1,
  "guest": {
    "id": 2,
    "name": "Jane Smith",
    "occupation": "Actor"
  },
  "episode": {
    "id": 1,
    "date": "5/1/24",
    "number": 1
  }
}
Error response (validation fails):

json

{
  "errors": ["Rating must be between 1 and 5"]
}
## Testing the API
You can import the provided Postman collection:

Open Postman

Import challenge-4-lateshow.postman_collection.json

Run requests for:

GET all episodes

GET one episode

DELETE episode

GET guests

POST appearance

## Validations
rating must be an integer between 1 and 5.

Appearances are linked to both an Episode and a Guest.

## Additional Notes
Cascading deletes are configured for Appearance records.

The API avoids infinite nesting via custom to_dict() methods.

##L icense
This project is licensed under the MIT License.