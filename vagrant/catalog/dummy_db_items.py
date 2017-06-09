import datetime
from shutil import copyfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Dealers, Cars

engine = create_engine('sqlite:///cars4sale.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy dealer
Dealer1 = Dealers(name="Car seller", email="example@gmail.com")
session.add(Dealer1)
session.commit()

# cars of dummy dealer
newList = [True, False]
typeList = ["suv","sedan"]
makeList = ["honda", "ford"]
modelList = ["model1", "model2"]
trimList = ["lx", "sx"]
yearList = [1999, 2015]
mileageList = [10000, 20000]
priceList = [5000, 15000]

pic = 1
for new in newList:
    for type in typeList:
        for make in makeList:
            for model in modelList:
                for trim in trimList:
                    for year in yearList:
                        for mileage in mileageList:
                            for price in priceList:
                                car = Cars(newCar=new,
                                            created=datetime.datetime.utcnow(),
                                            type=type,
                                            make=make,
                                            model=model,
                                            trim=trim,
                                            year=year,
                                            mileage=mileage,
                                            price=price,
                                            description='car_' + str(pic),
                                            picture= 'uploaded/' + str(pic) + '.jpg',
                                            dealer_id = 1)
                                session.add(car)
                                session.commit()
                                car.picture = 'uploaded/' + str(car.id) + '.jpg'
                                session.commit()
                                srcPic = '/vagrant/tempPic4Upload/' + str(1+pic%6) + '.jpg'
                                dstPic = '/vagrant/catalog/static/uploaded/' + str(car.id) + '.jpg' 
                                copyfile(srcPic, dstPic)
                                pic = pic + 1
