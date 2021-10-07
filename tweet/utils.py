from itertools import groupby


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
    return merged_values
