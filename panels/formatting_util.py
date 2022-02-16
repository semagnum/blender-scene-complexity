def format_num(num):
    if num < 1000:
        return str(num)
    elif num < 1000000:
        return str(round(num / 1000.0, 1)) + "k"
    return str(round(num / 1000000.0, 1)) + "M"
