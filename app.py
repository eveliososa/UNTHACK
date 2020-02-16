from flask import Flask, render_template, redirect, g, url_for, flash
from flask_login import LoginManager, login_user, login_required, current_user
from flask_bcrypt import check_password_hash
import forms
import models
import data

app = Flask(__name__)
app.secret_key = 'smadknsajdnqasdnaskjdnsad'

# LOGIN
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    # connect to the database before each request
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    # close the database connection after each request
    g.db.close()
    return response


# SIGN UP PAGE
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = forms.SignUpForm()
    if form.validate_on_submit():
        flash("Yay, you registered!", "success")
        models.User.create_user(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
        )
        return redirect(url_for('account'))
    return render_template('signup.html', form=form)


# LOG IN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LogInForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.username == form.username.data)
        except models.DoesNotExist:
            flash("Your username or password doesn't match", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You have been logged in!", "success")
                return redirect(url_for('account'))
            else:
                flash("Your email or password doesn't match", "error")
    return render_template('login.html', form=form)


# MAIN PAGE
@app.route('/')
def index():
    return render_template('main.html')


# BOOKING PAGE
@app.route('/book', methods=['GET', 'POST'])
def book():
    form = forms.FlightSearchForm()

    if form.validate_on_submit():
        date = form.date.data.replace('/', '')
        return redirect(url_for(
            'flights',
            date=date,
            origin=form.origin.data,
            destination=form.destination.data
        ))

    return render_template(
        'book.html',
        form=form,
        symbol_list=data.symbol_list,
        airport_list=data.airport_list,
        num_of_airports=data.num_of_airports
    )


# FLIGHTS PAGE
@app.route('/<date>/<origin>/<destination>', methods=['GET', 'POST'])
def flights(date, origin, destination):
    temp = str(date[0:2]) + '-' + str(date[2:4]) + '-' + str(date[4:8])
    date = str(date[4:8]) + '-' + str(date[0:2]) + '-' + str(date[2:4])
    flight_data = data.flights_search(date, origin, destination)

    return render_template(
        'flights.html',
        flight_data=flight_data,
        date=temp
    )


# ADD FLIGHT
@app.route('/<flight>/<date>/<origin>/<destination>/<arrival>/<departure>/<model>', methods=['GET', 'POST'])
@login_required
def add_flight(flight, date, origin, destination, arrival, departure, model):
    seat = '21F'
    models.Flight.create(
        user=g.user.id,
        origin=origin,
        destination=destination,
        date=date,
        arrival_time=arrival,
        departure_time=departure,
        flight_number=flight,
        airplane_model=model,
        seat_number=seat
    )
    return redirect(url_for('my_flights'))


# REMOVE FLIGHT
@app.route('/remove/<flight>', methods=['GET', 'POST'])
@login_required
def remove_flight(flight):
    # find symbol in users watchlist but expect it not to be found
    try:
        models.Flight.get(
            flight_number=flight
        ).delete_instance()
    except models.IntegrityError:
        pass
    return redirect(url_for('my_flights'))


# ACCOUNT PAGE
@app.route('/account')
@login_required
def account():
    return render_template(
        'account.html',
        first_name=g.user.first_name,
        last_name=g.user.last_name,
        username=g.user.username,
        miles=g.user.miles
    )


# MY FLIGHTS PAGE
@app.route('/myflights')
@login_required
def my_flights():
    stream = current_user.get_flights()
    return render_template(
        'myflights.html',
        stream=stream
    )


# SEAT PAGE
@app.route('/flight/seats/<flight>/<seat_number>')
@login_required
def seats(flight, seat_number):
    form = forms.UpdateSeatForm()
    if form.validate_on_submit():
        try:
            models.Flight.get(
                flight_number=flight
            ).delete_instance()
        except models.IntegrityError:
            pass
        return redirect(url_for(
            'my_flights'
        ))
    return render_template(
        'seats738.html',
        flight_number=flight,
        seat_number=seat_number,
        form=form
    )


# RUN PROGRAM
if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            first_name="Evelio",
            last_name="Sosa",
            email="eveliososa123@gmail.com",
            username="evsosa",
            password="password",
        )
    except ValueError:
        pass
    app.run(debug=True)
