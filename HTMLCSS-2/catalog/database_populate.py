from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, Item

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create initial user -- change this to change the default user
initialUser = User(name="Richard Dunlap", email="rdunlap1125@gmail.com")
session.add(initialUser)
session.commit()

# Create categories
categoryList = ['Soccer', 'Basketball', 'Baseball', 'Frisbee', 'Snowboarding',
                'Rock Climbing', 'Foosball', 'Skating', 'Hockey']
categoryDict = {}  # Used to keep Category objects for setting up Item objects
for entry in categoryList:
    categoryEntry = Category(name=entry)
    categoryDict[entry] = categoryEntry
    session.add(categoryEntry)
session.commit()

# Create items
itemsList = [
    ('Stick', 'Hockey',
     'Play like Gretsky!'),
    ('Goggles', 'Snowboarding',
     'Keep the snow out of your face and the sun out of your eyes!'),
    ('Snowboard', 'Snowboarding',
     'Slide down the slopes with ease!'),
    ('Shinguards', 'Soccer',
     'Protect yourself from those hard tackles!'),
    ('Frisbee', 'Frisbee',
     'How ya gonna play without a disc?'),
    ('Bat', 'Baseball',
     'Swing for the fences (but not like that cheater Barry Bonds).'),
    ('Jersey', 'Soccer',
     'Keep it covered until you score a goal!'),
    ('Soccer Cleats', 'Soccer',
     'Run like Pele!'),
    ('Ice Skates', 'Skating',
     '"...If you could skate, you would be great / If you could make, a figure eight..."'),
    ('Basketball Shoes', 'Basketball',
     'Be like Mike!')
]

for entry in itemsList:
    itemCategory = categoryDict[entry[1]]
    item = Item(name=entry[0],
                description=entry[2],
                category=categoryDict[entry[1]],
                user=initialUser)
    session.add(item)
session.commit()
