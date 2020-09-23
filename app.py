from flask import Flask, render_template, url_for, redirect, request, make_response, jsonify
from sqlalchemy import MetaData, Table, Column, Integer, String, Sequence, create_engine, select, text, exc
import yaml
from datetime import datetime

# Create the Flask App
app = Flask(__name__)

# Configure the Database and connect
db_config = yaml.load(open('config.yaml'))
db_url = db_config["url"]
engine = create_engine(db_url, pool_size=20, echo=True)
metadata = MetaData(bind=engine)

# Route for the request (simple GET)
@app.route('/')
def index():

    # prepare the query from the file
    with open("bsg_db.sql", mode="r") as file:
        query = text(file.read())
        response_string = ""

    # create the engine and run the query
    with engine.connect() as eng:
        eng.execute(query)

        # update the metadata so we can run a select query, run it
        metadata.reflect()
        bsg_people = Table("bsg_people", metadata)
        select_query = select([bsg_people])
        result = eng.execute(select_query).fetchall()

        # gather our data
        data = {}
        index = 0
        for row in result:
            data[index] = {}
            for key, value in row.items():
                data[index]["{}".format(key)] = "{}".format(value)
            index += 1

        # get the current date and time
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        date = now.strftime("%m-%d-%Y")

        # create information to populate the rest of the web app
        information = {}
        information['title'] = "Assignment 0: Access and Use the CS340 Database"
        information['author'] = "George Kochera"
        information['date'] = date
        information['time'] = time
        information['email'] = "kocherag@oregonstate.edu"
        information['class'] = "CS 340"
    

    return render_template("content.jinja2", content=data, info=information)

if __name__ == '__main__':
    app.run(port=5001)