"""to start an app"""
from healthapp import app

if __name__ == "__main__":
    app.run(debug=True, port=8080)