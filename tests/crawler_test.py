from mtg_dashboard import crawler
from mtg_dashboard.models import Collection


def test_parse_collection(app):
    with app.app_context():
        # test with only filename given
        filename = "collection_name.txt"
        col = crawler.parse_collection(filename, None)
        query = Collection.query.all()
        assert len(query) == 1
        assert col == query[0]

        # test with collection object already in db
        col_2 = crawler.parse_collection(filename, col.name)
        query = Collection.query.all()
        # there still should be only the collection from above in db
        assert len(query) == 1
        assert col_2.id == query[0].id

        # test with new collection name not in db
        col_2 = crawler.parse_collection(filename, "new_collection")
        query = Collection.query.all()
        # there should be two collections now
        assert len(query) == 2
        assert query[1].name == col_2.name





