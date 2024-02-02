def format_num(num: int, decimal_places=1) -> str:
    """Formats numbers into simplistic number representations.

    ``format_num(200)`` returns "200". ``format_num(2000)`` returns "2k". ``format_num(2000000)`` returns "2M".

    :param num: number to be converted.
    :param decimal_places: number of decimal places for the large numbers. Set to ``None`` if no decimal places desired.
    """
    if num < 1000:
        return str(num)
    elif num < 1000000:
        return str(round(num / 1000.0, decimal_places)) + "k"
    return str(round(num / 1000000.0, decimal_places)) + "M"
