from flask import Flask, jsonify, redirect, request, render_template
from models import db, connect_db, Cupcake
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecrethehe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
connect_db(app)
db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cupcakes')
def list_cupcakes():
    all_cupcakes = Cupcake.query.all()
    serialized_cupcakes = [cupcake.serialize() for cupcake in all_cupcakes]
    
    return jsonify(cupcakes=serialized_cupcakes)

@app.route('/search')
def search_cupcakes():

    search = request.args.get('search').lower() if request.args.get('search') else None

    cupcakes = Cupcake.query.filter(Cupcake.flavor.like(f"%{search}%")).all()
    print('asdfasdfdsffasdf',cupcakes)
    serialized_cupcakes = [cupcake.serialize() for cupcake in cupcakes]
    
    return jsonify(cupcakes=serialized_cupcakes)


@app.route('/cupcakes', methods=["POST"])
def add_cupcake():
    new_cupcake = request.json
    new_cupcake['image'] = new_cupcake['image'] or None
    cupcake = Cupcake(**new_cupcake)

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())


@app.route('/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def edit_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    new_info = request.json
    cupcake.flavor = new_info.get('flavor', cupcake.flavor)
    cupcake.size = new_info.get('size', cupcake.size)
    cupcake.rating = new_info.get('rating', cupcake.rating)
    cupcake.image = new_info.get('image', cupcake.image)

    db.session.commit()
    return jsonify(cupcake.serialize())

@app.route('/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize(), message='Deleted')
