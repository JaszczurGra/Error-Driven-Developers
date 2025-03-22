from backend.storage import Storage


def test_backend():
    Storage.from_csv('example_data.csv')
