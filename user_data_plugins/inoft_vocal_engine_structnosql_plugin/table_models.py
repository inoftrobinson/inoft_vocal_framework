from StructNoSQL import TableDataModel, BaseField


class BaseUserTableDataModel(TableDataModel):
    accountProjectTableKeyId = BaseField(field_type=str, required=True)
    thenState = BaseField(field_type=str, required=False)
    lastIntentHandler = BaseField(field_type=str, required=False)
