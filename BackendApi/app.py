"""Import initialized app from main package."""
from hydra import app

if __name__ == "__main__":
    app.run(
        debug=True
    )  # Leaving available for testing, to be removed in prod.
    # socketio.run(app, cors_allowed_origins="*")
