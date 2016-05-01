from django.db.models.expressions import F
from django.db.models.expressions import Value
from django.test import TestCase

from pg_trgm.models import Food
from pg_trgm.functions import Similarity
from pg_trgm.functions import Distance
from pg_trgm.functions import Threegrams


# TODO rename - not a manager test
class ManagerTestCase(TestCase):

    def test_similar_lookup(self):
        result = (Food.objects
                  .filter(name__similar='Chikcen')
                  .exists())
        # TODO some assertions

    def test_similar_with_changed_limit(self):
        blue_cheese = "Cheese, blue"
        result = (Food.objects
                  .with_threegram_limit(1)
                  .filter(name__similar=blue_cheese))
        self.assertEqual(result.count(), 1)

    def test_similarity_func(self):
        blue_cheese = "Cheese, blue"
        res = (Food.objects
               .annotate(similarity_to_cheese=Similarity(
                   F('name'), Value(blue_cheese)
               ))
               .get(name=blue_cheese))
        self.assertEqual(res.similarity_to_cheese, 1)

    def test_distance_func(self):
        blue_cheese = "Cheese, blue"
        res = (Food.objects
               .annotate(distance_from_cheese=Distance(
                   F('name'), Value(blue_cheese)
               ))
               .get(name=blue_cheese))
        self.assertEqual(res.distance_from_cheese, 0)

    def test_threegrams_func(self):
        res = (Food.objects
               .annotate(name_threegrams=Threegrams(F('name')))
               .first())
        self.assertIsInstance(res.name_threegrams, list)
