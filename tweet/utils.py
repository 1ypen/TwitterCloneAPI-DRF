from itertools import groupby
from django.core.exceptions import ObjectDoesNotExist


def merge_values(values):
    """

    Combines all the values of the many to many field into one
    taken from https://stackoverflow.com/questions/12139923/all-the-values-of-the-many-to-many-field-django
    """
    grouped_results = groupby(values, key=lambda value: value['id'])
    merged_values = []
    for k, g in grouped_results:
        groups = list(g)
        merged_value = {}
        for group in groups:
            for key, val in group.items():
                if not merged_value.get(key):
                    merged_value[key] = val
                elif val != merged_value[key]:
                    if isinstance(merged_value[key], list):
                        if val not in merged_value[key]:
                            merged_value[key].append(val)
                    else:
                        old_val = merged_value[key]
                        merged_value[key] = [old_val, val]
        merged_values.append(merged_value)

    return merged_values[0] if len(merged_values) == 1 else merged_values


def get_object_or_none(model, **kwargs):
    try:
        object = model.objects.get(**kwargs)
    except model.DoesNotExist:
        object = None
    return object
