from backend.storage import BStorage


def test_backend():

    storage = BStorage.from_csv('example_data.csv')
    storage
