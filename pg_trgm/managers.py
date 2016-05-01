from django.db.models import QuerySet
from django.db import connection


class ThreegramQuerySet(QuerySet):

    def with_threegram_limit(self, limit):
        with connection.cursor() as cursor:
            cursor.execute(
                "select set_limit(%s);", [limit]
            )
        return self


ThreegramManager = ThreegramQuerySet.as_manager()
