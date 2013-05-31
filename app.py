from flask import Flask, request, abort, render_template, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


@app.template_filter('currency')
def format_currency(value):
    return "${:,.2f}".format(value)


class Beer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    brewery = db.Column(db.String(80))
    beer_type = db.Column(db.String(120))
    __table_args__ = (UniqueConstraint("name", "brewery"),)

    def __init__(self, name, brewery, beer_type):
        self.name = name
        self.brewery = brewery
        self.beer_type = beer_type

    def __repr__(self):
        return '<Beer %r>' % self.name

    def current_price(self):
        today = datetime.datetime.today()
        day = today.weekday()
        hour = today.hour
        price_dict = {}
        always_prices = self.prices.filter(Price.day == None).all()
        for price in always_prices:
            price_dict[price.bar] = price.price
        current_prices = self.prices.filter(Price.day == day,
                                            Price.start_hour <= hour,
                                            Price.end_hour >= hour).all()
        for price in current_prices:
            price_dict[price.bar] = price.price
        return price_dict

    def normal_price(self):
        always_prices = self.prices.filter(Price.day == None).all()
        return min(price.price for price in always_prices)

    def current_lowest_price(self):
        prices = self.current_price()
        if prices.values():
            lowest = min(prices.values())
            return (lowest, [bar for bar in prices if prices[bar] == lowest])
        else:
            return (None, [])


class Bar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __init__(self, name):
        self.name = name

    def beers(self):
        today = datetime.datetime.today()
        day = today.weekday()
        hour = today.hour
        price_dict = {}
        always_prices = self.prices.filter(Price.day == None).all()
        for price in always_prices:
            price_dict[price.beer] = price.price
        current_prices = self.prices.filter(Price.day == day,
                                            Price.start_hour <= hour,
                                            Price.end_hour >= hour).all()
        for price in current_prices:
            price_dict[price.beer] = price.price
        return sorted(price_dict.iteritems(), key=lambda x: (x[1], x[0].name))

    def __repr__(self):
        return '<Bar %r>' % self.name


class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    beer_id = db.Column(db.Integer, db.ForeignKey('beer.id'))
    beer = db.relationship('Beer',
        backref=db.backref('prices', lazy='dynamic'))
    bar_id = db.Column(db.Integer, db.ForeignKey('bar.id'))
    bar = db.relationship('Bar',
        backref=db.backref('prices', lazy='dynamic'))
    price = db.Column(db.Float)
    day = db.Column(db.Integer, nullable=True)
    start_hour = db.Column(db.Integer, nullable=True)
    end_hour = db.Column(db.Integer, nullable=True)

    def __init__(self, beer_id, bar_id, price,
                 day=None, start_hour=None, end_hour=None):
        self.beer_id = beer_id
        self.bar_id = bar_id
        self.price = price
        self.day = day
        self.start_hour = start_hour
        self.end_hour = end_hour

    def __repr__(self):
        return '<Price %s %s %s>' % (self.beer, self.bar, self.price)


@app.route('/')
def bar_list():
    beers = Beer.query.all()
    bars = Bar.query.all()
    prices = Price.query.all()
    return render_template('index.html', beers=beers, bars=bars, prices=prices)


@app.route('/bars/')
def hello_world():
    bars = Bar.query.all()
    return render_template('bars.html', bars=bars)


@app.route('/add_beer', methods=['GET'])
def add_beer_form():
    return render_template('add_beer.html')


@app.route('/add_beer', methods=['POST'])
def add_beer():
    name = request.form.get('name')
    beer_type = request.form.get('beer_type')
    brewery = request.form.get('brewery')
    if not all([name, beer_type, brewery]):
        abort(400)
    b = Beer(name, brewery, beer_type)
    db.session.add(b)
    db.session.commit()
    return redirect('/add_beer')


@app.route('/add_price', methods=['GET'])
def add_price_form():
    beers = Beer.query.all()
    bars = Bar.query.all()
    return render_template('add_price.html', beers=beers, bars=bars)


@app.route('/add_special', methods=['GET'])
def add_special_form():
    beers = Beer.query.all()
    bars = Bar.query.all()
    return render_template('add_special.html', beers=beers, bars=bars)


@app.route('/add_price', methods=['POST'])
def add_price():
    beer = request.form.get('beer_id')
    bar = request.form.get('bar_id')
    price = request.form.get('price')
    day = request.form.get('day')
    start = request.form.get('start')
    end = request.form.get('end')
    if not all([beer, bar, price]):
        abort(400)
    # if it's a speshy, need them all, otherwise, none
    if day or start or end:
        if not all([day, start, end]):
            abort(400)
    p = Price(beer, bar, price, day, start, end)
    db.session.add(p)
    db.session.commit()
    return redirect('/add_price')


@app.route('/add_bar', methods=['GET'])
def add_bar_form():
    return render_template('add_bar.html')


@app.route('/add_bar', methods=['POST'])
def add_bar():
    name = request.form.get('name')
    if not all([name]):
        abort(400)
    b = Bar(name)
    db.session.add(b)
    db.session.commit()
    return redirect('/add_bar')


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
