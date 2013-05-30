from app import db, Beer, Bar, Price


if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    bars = ["Rivermill Map Company", "Cellar", "The London Underground", "Sharkey's", "Top Of The Stairs"]
    for bar in bars:
        b = Bar(bar)
        db.session.add(b)
    db.session.commit()
    beers = [
        ("Hoppyum", "Foothills", "IPA"),
        ("Milk Stout", "Left Hand", "Stout"),
        ("Blue Ribbon", "Pabst", "American Lager")
    ]
    for beer in beers:
        b = Beer(*beer)
        db.session.add(b)
    db.session.commit()
    beer = Beer.query.first()
    bar = Bar.query.first()
    price = Price(beer.id, bar.id, 4.0)
    db.session.add(price)
    db.session.commit()
