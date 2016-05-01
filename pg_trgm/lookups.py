from django.db.models import Lookup


class Similar(Lookup):
    lookup_name = 'similar'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        operator = '%%'
        return '%s %s %s' % (lhs, operator, rhs), params
