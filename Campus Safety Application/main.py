from website import app_create, db

# gets the app from init file
app = app_create()

# application context creates the database
with app.app_context():
    db.create_all()
       
       
# run the app
if __name__ == '__main__':

    app.run(debug=True)
    

