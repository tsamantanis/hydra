"""Import initialized app from main package."""
from hydra import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
