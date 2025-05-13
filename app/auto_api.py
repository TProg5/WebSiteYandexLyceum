from flask import Blueprint
from flask import jsonify, abort, request
from flask import render_template

from app.database.models.cars_model import Cars, Brands, Models
from app.database.sync_engine import sync_session
from sqlalchemy.orm import selectinload

auto = Blueprint(
    'auto', 
    __name__, 
    url_prefix='/auto',
    template_folder='templates'
)


@auto.route('/get-models')
def get_models():
    brand_name = request.args.get('brand')
    session = sync_session()

    try:
        brand = session.query(Brands).filter_by(name=brand_name).first()

        if not brand:
            return jsonify([])

        models = [model.name for model in brand.models]
        return jsonify(models)

    finally:
        session.close()


@auto.route('/<brand>/<model>', methods=['GET', 'POST'])
def get_auto_detail(brand, model):
    session = sync_session()
    try:
        car = session.query(Cars).join(Models).filter(Models.name == model.lower()).first()
        if not car:
            abort(404, description="Автомобиль не найден")

        return render_template("one_car.html", car=car)
    
    finally:
        session.close()


@auto.route("/album")
def car_album():
    session = sync_session()
    try:
        cars = (
            session.query(Cars)
            .join(Cars.model)
            .join(Models.brand)
            .options(selectinload(Cars.model).selectinload(Models.brand))
            .all()
        )


        car_data = [
            {
                "brand": car.model.brand.name,
                "model": car.model.name,
                "title": f"{car.model.brand.name} {car.model.name}",
                "description": f"Год: {car.year}, Двигатель: {car.engine_size}, Коробка: {car.transmission}",
                "img": f"/static/images/cars/{car.model.brand.name.lower()}/{car.model.brand.name.lower()}_{car.model.name.lower()}.jpg",
            }
            for car in cars
        ]

        return render_template("car_album.html", cars=car_data)
    finally:
        session.close()


@auto.route("/album/<brand>")
def one_car_album(brand):
    session = sync_session()
    try:
        cars = (
            session.query(Cars)
            .join(Cars.model)
            .join(Models.brand)
            .options(selectinload(Cars.model).selectinload(Models.brand))
            .filter(Brands.name.ilike(brand))  # фильтруем по бренду
            .all()
        )

        car_data = [
            {
                "brand": car.model.brand.name,
                "model": car.model.name,
                "title": f"{car.model.brand.name} {car.model.name}",
                "description": f"Год: {car.year}, Двигатель: {car.engine_size}, Коробка: {car.transmission}",
                "img": f"/static/images/cars/{car.model.brand.name.lower()}/{car.model.brand.name.lower()}_{car.model.name.lower()}.jpg",
            }
            for car in cars
        ]

        return render_template("car_album.html", cars=car_data, brand=brand)
    finally:
        session.close()