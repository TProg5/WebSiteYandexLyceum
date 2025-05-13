from sqlalchemy import insert, select
from sqlalchemy.engine import Result

from database.models.cars_model import Models, Brands, Cars

from database.sync_engine import sync_session


def get_models_by_brand(brand_id: int):
    with sync_session as session:
        result: Result = session.execute(
            select(Models)
            .where(Models.brand_id == brand_id)
        ).scalars().all()

        return result


def get_cars_by_model(model_id: int):
    with sync_session as session:
        result: Result = session.execute(
            select(Cars).where(Cars.model_id == model_id)
        )
        
        return result.scalars().all()