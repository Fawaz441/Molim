def format_serializer_errors(errors):
    l_errors = dict(errors)
    key = (list(l_errors.keys())[0])
    return key + "-" +errors[key][0]
