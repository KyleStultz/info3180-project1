"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, send_from_directory, session, abort
from app.models import UserProfile, PropertyInfo
from app.forms import LoginForm, PropertyForm
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import os
from flask_login import login_user, logout_user, current_user, login_required

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

### 
# project1
###
@app.route('/properties/create', methods=['POST', 'GET'])
def create_property ():
    form = PropertyForm()
    if request.method== "POST":

     if form.validate_on_submit:
            propertytitle=form.propertytitle.data
            numberofbedrooms = form.numberofbedrooms.data
            numberofbathrooms = form.numberofbathrooms.data
            propertylocation = form.propertylocation.data
            price = form.price.data
            propertytype = form.propertytype.data
            propertydescription = form.propertydescription.data
            photo = form.photo.data

            #adding the pictures
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            #adding property info to db    
            ppty = PropertyInfo(request.form['propertytitle'], request.form['propertydescription'], request.form['numberofbedrooms'], 
                                       request.form['numberofbathrooms'], request.form['price'], request.form['propertytype'], 
                                       request.form['propertylocation'], filename)

            db.session.add(ppty)
            db.session.commit()
            
            #ppty = PropertyInfo(propertytitle,propertylocation,price,propertytype,propertydescription,numberofbedrooms,
                                       #numberofbathrooms,filename)
            #db.session.add(ppty)
            #db.session.commit()

            

            flash('Property Added', 'success')
            return redirect(url_for('properties'))

    return render_template("addproperty.html,form=form")


@app.route('/uploads/<filename>')
def get_image(filename):
    #root_dir = os.getcwd()
    return send_from_directory(os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER']), filename)
##@app.route('/uploads/<filename>')
##def get_image(filename):
    ##return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/properties/')
def properties():
    all_properties = db.session.execute(db.select(PropertyInfo)).scalars()
    if all_properties is not None:
        return render_template('properties.html', all_properties=all_properties)
    flash('Property not available or showing', 'error')
    return redirect(url_for('addproperty'))

@app.route('/properties/<propertyid>')
def get_property(propertyid):
    current_property = db.session.execute(db.select(PropertyInfo).filter_by(propertyid=propertyid)).scalar_one()
    if current_property is not None:
        return render_template('full_property.html', current_property=current_property)
    flash('This property seems to be missing', 'error')
    return redirect(url_for('properties'))


#####
@app.route('/login', methods=['POST', 'GET'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('properties'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = db.session.execute(db.select(UserProfile).filter_by(username=username)).scalar()
        if user is not None and check_password_hash(user.password, password):

        # Gets user id, load into session
            login_user(user)
            flash(f'User {username} has successfully logged in!!!')
            return redirect(url_for("properties"))
        else:
            flash(f'User {username} was not logged in !!')
            return redirect(url_for('home'))
    return render_template("login.html", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are successfully logged out')
    return redirect(url_for('home'))

@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(UserProfile).filter_by(id=id)).scalar()







###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
