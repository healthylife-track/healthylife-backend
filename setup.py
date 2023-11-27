"""to start an app"""
from healthapp import app, scheduler
from healthapp.routes import check_due_reminders

if __name__ == "__main__":
    # scheduler.start()
    app.run(debug=True)
    # app.run()
    