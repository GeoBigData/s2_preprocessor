
def convert_type(var, f, expected_type):

    # try to convert the inputs to correct types
    if var is None:
        return None

    try:
        var = f(var)
    except ValueError as e:
        err = "Inputs {var} cannot be converted to type {expected_type}".format(var=var,
                                                                                expected_type=expected_type)
        raise ValueError(err)

    return var