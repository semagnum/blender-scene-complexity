def format_num(num: int) -> str:
    """Formats numbers into simplistic number representations.

    ``format_num(200)`` returns "200". ``format_num(2000)`` returns "2k". ``format_num(2000000)`` returns "2M".

    :param num: number to be converted.
    """
    if num < 1000:
        return str(num)
    elif num < 1000000:
        return str(round(num / 1000.0, 1)) + "k"
    return str(round(num / 1000000.0, 1)) + "M"
