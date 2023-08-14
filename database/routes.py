from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from app import app, db
from models import User, FishCapture, UserPreferences
from forms import LoginForm, RegistrationForm, FishCaptureForm

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    fish_captures = user.fish_captures.order_by(FishCapture.timestamp.desc())
    return render_template('user.html', user=user, fish_captures=fish_captures)

@app.route('/add_fish_capture', methods=['GET', 'POST'])
@login_required
def add_fish_capture():
    form = FishCaptureForm()
    if form.validate_on_submit():
        fish_capture = FishCapture(user_id=current_user.id, GPS_location=form.GPS_location.data, fishing_spot_tag=form.fishing_spot_tag.data, tide_state=form.tide_state.data, weather_conditions=form.weather_conditions.data, daylight_state=form.daylight_state.data, fish_type=form.fish_type.data, lure_bait_type=form.lure_bait_type.data)
        db.session.add(fish_capture)
        db.session.commit()
        flash('Your fish capture has been added!')
        return redirect(url_for('index'))
    return render_template('add_fish_capture.html', title='Add Fish Capture', form=form)

@app.route('/edit_fish_capture/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_fish_capture(id):
    fish_capture = FishCapture.query.get_or_404(id)
    if current_user.id != fish_capture.user_id:
        abort(403)
    form = FishCaptureForm()
    if form.validate_on_submit():
        fish_capture.GPS_location = form.GPS_location.data
        fish_capture.fishing_spot_tag = form.fishing_spot_tag.data
        fish_capture.tide_state = form.tide_state.data
        fish_capture.weather_conditions = form.weather_conditions.data
        fish_capture.daylight_state = form.daylight_state.data
        fish_capture.fish_type = form.fish_type.data
        fish_capture.lure_bait_type = form.lure_bait_type.data
        db.session.commit()
        flash('Your fish capture has been updated!')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.GPS_location.data = fish_capture.GPS_location
        form.fishing_spot_tag.data = fish_capture.fishing_spot_tag
        form.tide_state.data = fish_capture.tide_state
        form.weather_conditions.data = fish_capture.weather_conditions
        form.daylight_state.data = fish_capture.daylight_state
        form.fish_type.data = fish_capture.fish_type
        form.lure_bait_type.data = fish_capture.lure_bait_type
    return render_template('edit_fish_capture.html', title='Edit Fish Capture', form=form)

@app.route('/delete_fish_capture/<int:id>', methods=['POST'])
@login_required
def delete_fish_capture(id):
    fish_capture = FishCapture.query.get_or_404(id)
    if current_user.id != fish_capture.user_id:
        abort(403)
    db.session.delete(fish_capture)
    db.session.commit()
    flash('Your fish capture has been deleted!')
    return redirect(url_for('user', username=current_user.username))
