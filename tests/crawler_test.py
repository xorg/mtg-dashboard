import os
from mtg_dashboard import crawler
from mtg_dashboard.models import Collection


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


