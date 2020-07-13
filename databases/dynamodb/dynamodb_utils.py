from decimal import Context, Rounded


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

    def float_serializer(self, python_object):
        if isinstance(python_object, float):
            # Okay, this is a weird one. The decimal module will crash if it is passed a float
            # with less than two decimal numbers, like float(0.5) which has only one. The decimal
            # module is used when using the Utils.TypeSerializer accessible via the serializer property.
            # Yet, the module has no issues with number with more than 20 decimals, and we want to keep
            # this infos, so we will not round the object. Instead, with the "%.f" % python_object we will
            # get the number of decimal numbers on the float (returned in the form of a string, for real,
            # and if this number is under two, we will turn the float into a float with two decimal numbers by
            # using "%.2f" % python_object, which will then be able to be passed to the Decimal modules without errors.
            # PS : Obviously, instead of doing this, a number like 0.5 cannot be converted to an int ;)
            if ("%.f" % python_object) < "2":
                python_object = "%.2f" % python_object

            from decimal import Decimal
            return Decimal(python_object)
        elif isinstance(python_object, list):
            for i, item in enumerate(python_object):
                python_object[i] = self.float_serializer(python_object=item)
            return python_object
        elif isinstance(python_object, dict):
            for key, value in python_object.items():
                python_object[key] = self.float_serializer(python_object=value)
            return python_object
        else:
            return python_object

    def decimal_deserializer(self, python_object):
        from decimal import Decimal
        if isinstance(python_object, Decimal):
            if ("%.f" % python_object) > "0":
                python_object = float(python_object)
            else:
                python_object = int(python_object)
            return python_object
        elif isinstance(python_object, list):
            for i, item in enumerate(python_object):
                python_object[i] = self.decimal_deserializer(python_object=item)
            return python_object
        elif isinstance(python_object, dict):
            for key, value in python_object.items():
                python_object[key] = self.decimal_deserializer(python_object=value)
            return python_object
        else:
            return python_object

    def python_to_dynamodb(self, python_object):
        self.float_serializer(python_object=python_object)
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