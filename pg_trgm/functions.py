from django.db.models.expressions import Func


class Similarity(Func):
    function = 'similarity'

    def __init__(self, *expressions, **extra):
        if len(expressions) != 2:
            raise ValueError(
                'Similarity takes exactly two expressions'
            )
        return super(Similarity, self).__init__(
            *expressions, **extra
        )
