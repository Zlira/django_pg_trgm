from django.db.models.expressions import F
from django.db.models.expressions import Value
from django.test import TestCase

from pg_trgm.models import Food
from pg_trgm.functions import Similarity


# TODO rename - not a manager test
class ManagerTestCase(TestCase):

    def test_manager(self):
        result = (Food.objects
                  .filter(name__similar='Chikcen')
                  .exists())
        # TODO some assertions

    def test_similarity_func(self):
        blue_cheese = "Cheese, blue"
        res = (Food.objects
               .annotate(similarity_to_cheese=Similarity(
                   F('name'), Value(blue_cheese)
               ))
               .get(name=blue_cheese))
        self.assertEqual(res.similarity_to_cheese, 1)
