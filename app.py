"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.route('/')
def homepage():
    """ Show  form where new cupcakes can be added """
    cupcakes = Cupcake.query.all()
    return render_template("homepage.html", cupcakes=cupcakes)

@app.route('/api/cupcakes')
def list_cupcakes():
    """ Get data about all cupcakes. Return JSON {'cupcakes': [{id, flavor, size, rating, image}, ...]}"""
    serialized = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """ Get data about a single cupcake. Return JSON {'cupcakes': {id, flavor, size, rating, image}}"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods = ["POST"])
def create_cupcake():
    """ Create a cupcake with flavor, size, rating and image data from the body of the request. """
    cupcake_data=request.json
    flavor=cupcake_data['flavor']
    size=cupcake_data['size']
    rating=cupcake_data['rating']
    image=cupcake_data['image']
    new_cupcake=Cupcake(flavor=flavor, size=size, rating=rating, image=image or None)
    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=new_cupcake.serialize())
    return (response_json, 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
    """ Update a cupcake. Raise a 404 if the cupcake cannot be found. Respond with JSON of the newly-updated cupcake, 
    like this: {cupcake: {id, flavor, size, rating, image}}. """
    cupcake=Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor=request.json.get("flavor", cupcake.flavor)
    cupcake.size=request.json.get("size", cupcake.size)
    cupcake.rating=request.json.get("rating", cupcake.rating)
    cupcake.image=request.json.get("image", cupcake.image)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())    

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """ Raise a 404 if the cupcake cannot be found. Delete cupcake with the id passed in the URL.
    Respond with JSON like {message: "Deleted"}."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()     
    return jsonify(message="deleted")
