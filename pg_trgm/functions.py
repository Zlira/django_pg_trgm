from django.contrib.postgres.fields import ArrayField
from django.db.models.expressions import CombinedExpression
from django.db.models.expressions import Func
from django.db.models.fields import CharField


class Similarity(Func):
    function = 'similarity'

    def __init__(self, first, second, **extra):
        # TODO add validations for fields
        super(Similarity, self).__init__(first, second, **extra)


class Distance(CombinedExpression):
    connector = '<->'

    def __init__(self, lhs, rhs, output_field=None):
        super(CombinedExpression, self).__init__(output_field=output_field)
        # TODO add validations for fields
        self.lhs = lhs
        self.rhs = rhs


class Threegrams(Func):
    function = 'show_trgm'

    def __init__(self, text, **extra):
        output_field = extra.get('output_field') or ArrayField(CharField())
        return super(Threegrams, self).__init__(
            text, output_field=output_field, **extra
        )
