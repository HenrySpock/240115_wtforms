from flask import Flask, render_template, jsonify, request, session, url_for, redirect, abort, flash 
from flask_debugtoolbar import DebugToolbarExtension
from dotenv import load_dotenv 
from forms import AddPetForm, EditPetForm
from models import db, Pet
# ---
from flask_sqlalchemy import SQLAlchemy

load_dotenv('.flaskenv')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adoptdb'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = "sesh_secr" 

toolbar = DebugToolbarExtension(app)
 
db.init_app(app)

with app.app_context():
    db.create_all() 

@app.route('/')
def home():
    return redirect(url_for('list_pets'))

@app.route('/add_pet', methods=['GET', 'POST'])
def add_pet():
    form = AddPetForm()

    # if form.validate_on_submit():
    if form.validate():  
        # Create a new pet based on the form data
        new_pet = Pet(
            name=form.name.data,
            species=form.species.data,
            photo_url=form.photo_url.data,
            age=form.age.data,
            notes=form.notes.data
        )
        db.session.add(new_pet)
        db.session.commit()
        flash(f"Added {new_pet.name} to the database!")
        return redirect(url_for('list_pets'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field.title()} {error}") 
    return render_template('add_pet.html', form=form)

@app.route('/list_pets')
def list_pets():
    pets = Pet.query.all()
    return render_template('list_pets.html', pets=pets)

@app.route('/edit_pet/<int:pet_id>', methods=['GET', 'POST'])
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        form.populate_obj(pet)
        db.session.commit()
        flash(f"Updated {pet.name}!")
        return redirect(url_for('list_pets'))

    return render_template('edit_pet.html', form=form, pet=pet)
