from app import app, db
from models import User, FishCapture, UserPreferences

with app.app_context():
    db.create_all()

def list_db_tables(db):
    """
    Lists tables in the current database.
    :param db: The SQLAlchemy database instance from your Flask app.
    """
    engine = db.get_engine(app)
    with engine.connect() as conn:
        inspector = db.inspect(conn)
        tables = inspector.get_table_names()
        print("Tables in the database:")
        for table in tables:
            print(table)

if __name__ == "__main__":
    list_db_tables(db)
