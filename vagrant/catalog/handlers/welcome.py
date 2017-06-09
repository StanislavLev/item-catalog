from flask import Flask, render_template, request, redirect, url_for, jsonify
from project import app
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Dealers, Cars
from flask import session as login_session

engine = create_engine('sqlite:///cars4sale.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/', methods=['GET', 'POST'])
def welcome():
    if 'username' not in login_session:
        user = "guest"
    else:
        user = login_session['username']
    # These values will be used in drop-down lists in html
    carsStrDict = {'condition': ["All conditions", "New", "Pre-owned"],
                   'type': ["All types"],
                   'make': ["All makes"],
                   'model': ["All models"],
                   'trim': ["All trims"]}
    # These values will be selected items in drop-down lists in html
    carsSelectedDict = {'condition': "All conditions",
                        'type': "All types",
                        'make': "All makes",
                        'model': "All models",
                        'trim': "All trims"}
    carsIntDict = {'year': ["1900", "2017"],
                   'price': ["0", "1000000"],
                   'mileage': ["0", "1000000"]}
    # In the next for loops "make/typeVal" are tuples,
    # (''.join(value)) is used to convert them to string
    # otherwise it seems as unicode in html page
    for makeVal in session.query(Cars.make).distinct():
            carsStrDict['make'].append(''.join(makeVal))
    for typeVal in session.query(Cars.type).distinct():
            carsStrDict['type'].append(''.join(typeVal))
    allCars = ()
    allCarsQuery = "allCars = session.query(Cars)"
    carsPerPage = 10
    myCars = "Show my cars"
    if request.method == 'POST':
        prevPageDisabled = ""
        nextPageDisabled = ""
        # if user didn't login he doesn`t see "show my/all cars" button
        # and can't filter by dealer_id
        if 'username' in login_session:
            # myCars indicates if all cars or dealer's cars will be displayed
            myCars = request.form['myCarsPrev']
            # if "show my/all cars" button wasn't pressed,
            # request.form['myCars'] will cause exception
            try:
                myCars = request.form['myCars']
                if myCars == "Show my cars":
                    dealer = session.query(Dealers).filter_by(name=user).one()
                    allCarsQuery = (allCarsQuery +
                                    ".filter(Cars.dealer_id==dealer.id)")
                    myCars = "Show all cars"
                else:
                    myCars = "Show my cars"
            except:
                if myCars == "Show all cars":
                    dealer = session.query(Dealers).filter_by(name=user).one()
                    allCarsQuery = (allCarsQuery +
                                    ".filter(Cars.dealer_id==dealer.id)")
        conditionReq = request.form['condition']
        makeReq = request.form['make']
        modelReq = request.form['model']
        trimReq = request.form['trim']
        typeReq = request.form['type']
        yearFromReq = request.form['yearFrom']
        yearToReq = request.form['yearTo']
        priceFromReq = request.form['priceFrom']
        priceToReq = request.form['priceTo']
        mileageFromReq = request.form['mileageFrom']
        mileageToReq = request.form['mileageTo']
        pageNum = int(request.form['pageNum'])
        if conditionReq == carsStrDict['condition'][1]:
            # Updating query for user car list if "New" condition was selected.
            allCarsQuery = allCarsQuery + ".filter(Cars.newCar==True)"
        elif conditionReq == carsStrDict['condition'][2]:
            # Updating query for user car list
            # if "condition" was selected "Pre-owned".
            allCarsQuery = allCarsQuery + ".filter(Cars.newCar==False)"
        # Updating "condition" field that will be selectet
        # when page will be loaded.
        carsSelectedDict['condition'] = conditionReq
        if makeReq != carsStrDict['make'][0]:
            # Updating query for user car list if "make" was selected.
            allCarsQuery = allCarsQuery + ".filter(Cars.make==makeReq)"
            # Updating "make" field that will be selected
            # when page will be loaded.
            carsSelectedDict['make'] = makeReq
            # Updating possible "model" and "type" options,
            # if "make" was selected.
            for modelVal in (session.query(Cars.model)
                             .filter(Cars.make == makeReq)
                             .distinct()):
                carsStrDict['model'].append(''.join(modelVal))
            carsStrDict['type'] = ["All types"]
            for typeVal in (session.query(Cars.type)
                            .filter(Cars.make == makeReq)
                            .distinct()):
                carsStrDict['type'].append(''.join(typeVal))
            # "modelReq in carsStrDict['model']" should be checked
            # otherwise if user chooses "make"->"model" and change "make"
            # wrong results will be displayed
            if (modelReq != carsStrDict['model'][0] and
                    modelReq in carsStrDict['model']):
                # Updating query for user car list if "model" was selected.
                allCarsQuery = allCarsQuery + ".filter(Cars.model==modelReq)"
                # Updating "model" field that will be selectet
                # when page will be loaded.
                carsSelectedDict['model'] = modelReq
                # Updating possible "trim" options
                # if "make" and "model" options were selected.
                for trimVal in (session.query(Cars.trim)
                                .filter(Cars.make == makeReq)
                                .filter(Cars.model == modelReq)
                                .distinct()):
                    carsStrDict['trim'].append(''.join(trimVal))
                # If "model" was selected, "type" isn`t useful any more.
                carsStrDict['type'] = ["All types"]
                # "trimReq in carsStrDict['trim']" should be checked
                # otherwise if user chooses "make"->"model"->"trim"
                # and change "make" or "model"
                # wrong results will be displayed
                if (trimReq != carsStrDict['trim'][0] and
                        trimReq in carsStrDict['trim']):
                    # Updating query for user car list if "trim" was selected.
                    allCarsQuery = allCarsQuery + ".filter(Cars.trim==trimReq)"
                    # Updating "trim" field that will be selectet
                    # when page will be loaded.
                    carsSelectedDict['trim'] = trimReq
        # If "make" but not "model" were selected,
        # "type" can be useful in search.
        # "modelReq in carsStrDict['model']" should be checked
        # otherwise if user chooses "make"->"model" and change "make"
        # wrong results will be displayed
        if (typeReq != carsStrDict['type'][0] and
                modelReq == carsStrDict['model'][0] and
                typeReq in carsStrDict['type']):
            # Updating query for user car list if "type" was selected.
            allCarsQuery = allCarsQuery + ".filter(Cars.type==typeReq)"
            # Updating "type" field that will be selectet
            # when page will be loaded.
            carsSelectedDict['type'] = typeReq
        # Adding "year" filters and update default values
        # with search requirements.
        allCarsQuery = (allCarsQuery +
                        ".filter(Cars.year>=yearFromReq)" +
                        ".filter(Cars.year<=yearToReq)")
        carsIntDict['year'][0] = yearFromReq
        carsIntDict['year'][1] = yearToReq
        # Adding "price" filters and update default values
        # with search requirements.
        allCarsQuery = (allCarsQuery +
                        ".filter(Cars.price>=priceFromReq)" +
                        ".filter(Cars.price<=priceToReq)")
        carsIntDict['price'][0] = priceFromReq
        carsIntDict['price'][1] = priceToReq
        # Adding "mileage" filters and update default values
        # with search requirements.
        allCarsQuery = (allCarsQuery +
                        ".filter(Cars.mileage>=mileageFromReq)" +
                        ".filter(Cars.mileage<=mileageToReq)")
        carsIntDict['mileage'][0] = mileageFromReq
        carsIntDict['mileage'][1] = mileageToReq
        allCarsQuery = allCarsQuery + ".order_by(desc(Cars.created))"
        try:
            nextPage = request.form['nextPage']
            pageNum = pageNum + 1
        except:
            try:
                prevPage = request.form['prevPage']
                pageNum = pageNum - 1
            except:
                pass
        # When user enter too small number it is changed to allowed minimum
        if pageNum <= 1:
            pageNum = 1
            prevPageDisabled = "disabled"
        exec(allCarsQuery)
        # Calculation of maximum allowed page number
        if (allCars.count() % carsPerPage > 0 or allCars.count() == 0):
            maxPage = allCars.count()/carsPerPage + 1
        else:
            maxPage = allCars.count()/carsPerPage
        # When user enter too large number it is changed to allowed maximum
        if pageNum >= maxPage:
            pageNum = maxPage
            nextPageDisabled = "disabled"
        allCars = allCars.limit(carsPerPage).offset((pageNum-1)*carsPerPage)
        return render_template(
            'welcome.html',
            user=user,
            myCars=myCars,
            carsStrDict=carsStrDict,
            carsIntDict=carsIntDict,
            sortedStrKeys=sorted(carsStrDict),
            sortedIntKeys=reversed(sorted(carsIntDict)),
            carsSelectedDict=carsSelectedDict,
            pageNum=pageNum,
            prevPageDisabled=prevPageDisabled,
            nextPageDisabled=nextPageDisabled,
            allCars=allCars)
    else:
        allCarsQuery = allCarsQuery + ".order_by(desc(Cars.created))"
        pageNum = 1
        exec(allCarsQuery)
        if allCars.count() <= carsPerPage:
            nextPageDisabled = "disabled"
        else:
            nextPageDisabled = ""
        exec(allCarsQuery + ".limit(carsPerPage)")
        return render_template(
            'welcome.html',
            user=user,
            myCars=myCars,
            carsStrDict=carsStrDict,
            carsIntDict=carsIntDict,
            sortedStrKeys=sorted(carsStrDict),
            sortedIntKeys=reversed(sorted(carsIntDict)),
            carsSelectedDict=carsSelectedDict,
            pageNum=pageNum,
            prevPageDisabled="disabled",
            nextPageDisabled=nextPageDisabled,
            allCars=allCars)
