import os
from mtg_dashboard import crawler
from mtg_dashboard.models import Collection, Price


def test_parse_collection_filename(app):
    with app.app_context():
        # test with only filename given
        filename = "collection_name.txt"
        col = crawler.parse_collection(filename, None)
        query = Collection.query.all()
        assert len(query) == 3
        assert col == query[2]

        # test with collection object already in db
        col_2 = crawler.parse_collection(filename, col.name)
        query = Collection.query.all()

        # there should be only the additional collection from above in db
        assert len(query) == 3
        assert col_2.id == query[2].id

        # test with new collection name not in db
        col_2 = crawler.parse_collection(filename, "new_collection")
        query = Collection.query.all()

        # there should be two additional collections now
        assert len(query) == 4
        assert query[3].name == col_2.name


def test_import_file(app):
    with app.app_context():
        path = os.path.join(os.path.dirname(__file__), "fixtures", "test_import_data.txt")
        c = crawler.parse_collection("test_import_data.txt", "Collection 2")
        assert type(c) == Collection
        cards = crawler.parse_txt(path, c)
        assert type(cards) == list

        prices = crawler.fetch_prices(cards)
        assert type(prices) == list
        assert type(prices[0]) == Price
