from django.db.migrations.operations.base import Operation


class CreatedThreegramIndex(Operation):
    index_name_suffix = '_trgm'

    def __init__(self, model_name, field_name, index_type='GIN'):
        assert index_type in ('GiST', 'GIN'), ''
        self.index_type = index_type
        self.model_name = model_name
        self.field_name = field_name

    def state_forwards(self, app_label, state):
        # TODO maybe indexes should be represented in state?
        pass

    def _get_index_name(self, schema_editor, model, field):
        return schema_editor._create_index_name(
            model, [field.name], suffix=self.index_name_suffix
        )

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        index_ops = self.index_type.lower() + '_trgm_ops'
        from_model = from_state.apps.get_model(app_label, self.model_name)
        field = from_model._meta.get_field(self.field_name)
        index_name = self._get_index_name(schema_editor, from_model, field)
        sql_create_index = (
            "CREATE INDEX %(name)s ON %(table)s "
            "USING %(index_type)s (%(column)s %(index_ops)s)%(extra)s"
        )

        # TODO check tablespace functionality
        if field.db_tablespace:
            tablespace_sql = schema_editor.connection.ops.tablespace_sql(
                field.db_tablespace
            )
        elif from_model._meta.db_tablespace:
            tablespace_sql = schema_editor.connection.ops.tablespace_sql(
                from_model._meta.db_tablespace
            )
        else:
            tablespace_sql = ""
        if tablespace_sql:
            tablespace_sql = " " + tablespace_sql

        sql = sql_create_index % {
            "table": schema_editor.quote_name(from_model._meta.db_table),
            "name": schema_editor.quote_name(index_name),
            "column": schema_editor.quote_name(field.name),
            "index_type": self.index_type,
            "index_ops": index_ops,
            "extra": tablespace_sql,
        }
        schema_editor.execute(sql)

    def database_backwards(self, app_label, schema_editor,
                           from_state, to_state):
        to_model = to_state.apps.get_model(app_label, self.model_name)
        field = to_model._meta.get_field(self.field_name)
        index_name = self._get_index_name(schema_editor, to_model, field)
        schema_editor.execute(
            schema_editor.sql_delete_index % {
                'name': schema_editor.quote_name(index_name)
            }
        )

    def describe(self):
        return (
            'Create threegram {index_type} index for field "{field_name}" '
            'of model "{model_name}".'
        ).format(vars(self))

