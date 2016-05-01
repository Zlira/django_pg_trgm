from django.test import TestCase

from pg_trgm.models import Food


class ManagerTestCase(TestCase):

    def test_manager(self):
        result = (Food.objects
                  .filter(name__similar='Chikcen')
                  .exists())
        # TODO some assertions
