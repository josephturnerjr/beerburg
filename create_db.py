from app import db, Beer, Bar, Price


if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    bars = ["Rivermill Map Company",
            "Cellar",
            "The London Underground",
            "Sharkey's",
            "Top Of The Stairs",
            "Champs", "Big Al's Upstairs",
            "Hokie House", "PKs"]
    for bar in bars:
        b = Bar(bar)
        db.session.add(b)
    db.session.commit()
    beers = [
        ("Bud Light", "Budweiser", "American Lager"),
        ("Traditional Lager", "Yuengling", "American Lager"),
        ("Hoppyum", "Foothills", "IPA"),
        ("Milk Stout", "Left Hand", "Stout"),
        ("Blue Ribbon", "Pabst", "American Lager"),
        ("Vienna Lager", "Devil's Backbone", "Lager"),
        ("In-Heat Wheat", "Flying Dog", "American Wheat"),
        ("Stout", "Guinness", "Irish Stout"),
        ("Ale", "Bass", "English Ale"),
        ("Irish Cream Ale", "Kilkenny", "Irish Ale"),
        ("Oatmeal Porter", "Highland", "Porter"),
        ("Cider", "Angry Orchard", "Cider"),
        ("Milk Stout", "Duck Rabbit", "Stout"),
    ]
    for beer in beers:
        b = Beer(*beer)
        db.session.add(b)
    db.session.commit()
    beer = Beer.query.first()
    bar = Bar.query.first()
    price = Price(beer.id, bar.id, 4.0)
    price = Price(beer.id, bar.id, 2.0, 3, 15, 18)
    db.session.add(price)
    db.session.commit()
