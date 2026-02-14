#!/usr/bin/env python3

from app import create_app, db
from app.db_helpers import init_db, create_user, get_user_by_username

# Create the Flask app
app = create_app()

if __name__ == "__main__":
    with app.app_context():
        
        init_db(app, seed_sample_data=True)

    print("TaskManager API is running!")
    app.run(port=8000)