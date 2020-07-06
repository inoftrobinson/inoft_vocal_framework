class Utils:
    from boto3.dynamodb.types import TypeSerializer, TypeDeserializer
    # The serializer and deserializer can be static, even in a lambda,
    # since their classes will never change according to the user.
    _serializer = None
    _deserializer = None

    @property
    def serializer(self) -> TypeSerializer:
        if Utils._serializer is None:
            Utils._serializer = Utils.TypeSerializer()
        return Utils._serializer
    
    @property
    def deserializer(self) -> TypeDeserializer:
        if Utils._deserializer is None:
            Utils._deserializer = Utils.TypeDeserializer()
        return Utils._deserializer

    def python_to_dynamodb(self, python_object):
        dynamodb_dict = self.serializer.serialize(python_object)
        dynamodb_dict_keys = list(dynamodb_dict.keys())
        if len(dynamodb_dict_keys) == 1:
            if dynamodb_dict_keys[0] == "M":
                # With a dict, DynamoDB is not expecting the first 'M' key (stands for Map)
                return dynamodb_dict["M"]
            else:
                return dynamodb_dict
        elif len(dynamodb_dict_keys) == 0:
            return dynamodb_dict
        else:
            raise Exception(f"The number of keys of the dynamodb was superior to 1. This is NOT SUPPOSED TO HAPPEN !"
                            f"\nPlease submit an issue on the GitHub page of the framework right away (https://github.com/Robinson04/inoft_vocal_engine)."
                            f"\nThere is something really wrong on our side or on AWS side.")

    def dynamodb_to_python(self, dynamodb_object):
        if isinstance(dynamodb_object, list):
            for i, item in enumerate(dynamodb_object):
                dynamodb_object[i] = self.deserializer.deserialize(item)
        elif isinstance(dynamodb_object, dict):
            for key, item in dynamodb_object.items():
                dynamodb_object[key] = self.deserializer.deserialize(item)
            return dynamodb_object
        else:
            return self.deserializer.deserialize(dynamodb_object)
