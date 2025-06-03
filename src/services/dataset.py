from services.bq_helper import BQHelper


def get_data(bq: BQHelper, query: str):
    return bq.get(query)
