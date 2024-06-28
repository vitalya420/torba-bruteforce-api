from sanic import json


def convert_named_tuple_to_dict(instance):
    if isinstance(instance, tuple) and hasattr(instance, '_fields'):
        return {field: convert_named_tuple_to_dict(getattr(instance, field)) for field in instance._fields}
    elif isinstance(instance, list):
        return [convert_named_tuple_to_dict(item) for item in instance]
    else:
        return instance


def named_tuple_serializer(instance, status):
    as_dict = convert_named_tuple_to_dict(instance)
    return json(as_dict, status=status)


def many_named_tuple_serializer(instances, status):
    as_list = [convert_named_tuple_to_dict(instance) for instance in instances]
    return json(as_list, status=status)
