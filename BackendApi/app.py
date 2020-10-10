"""Import initialized app from main package."""
from hydra import app

if __name__ == "__main__":
    app.run(debug=True)
