import os

from app import routes
from app.routes import tap

tap.config["SECRET_KEY"] = os.urandom(24)

if __name__ == "__main__":
    tap.run(debug=True)

