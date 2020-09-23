from flask import Flask, render_template, url_for, redirect, request, make_response, jsonify
from sqlalchemy import MetaData, Table, Column, Integer, String, Sequence, create_engine, select, text, exc
import yaml

# Create the Flask App
app = Flask(__name__)

# Configure the Database and connect
db_config = yaml.load(open('config.yaml'))
db_url = db_config["url"]
engine = create_engine(db_url, pool_size=20, echo=True)
metadata = MetaData(bind=engine)

@app.route('/')
def index():
    with open("bsg_db.sql", mode="r") as file:
        query = text(file.read())
        response_string = ""
    with engine.connect() as eng:
        eng.execute(query)
        metadata.reflect()
        bsg_people = Table("bsg_people", metadata)
        select_query = select([bsg_people])
        result = eng.execute(select_query).fetchall()
        data = {}
        index = 0
        for row in result:
            data[index] = {}
            for key, value in row.items():
                data[index]["{}".format(key)] = "{}".format(value)
            index += 1
        print(type(data))
    

    return render_template("content.jinja2", content=data)

if __name__ == '__main__':
    app.run(port=5001)