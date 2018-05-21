def english_full_name(first=None, last=None, middle=None,
                      prefix=None, suffix=None):
    fullname = None

    if first is None or last is None:
        raise ValueError("first and last must be specified")

    if middle:
        fullname = first + " " + middle + " " + last
    else:
        fullname = "{} {}".format(first, last)

    if prefix:
        fullname = prefix + " " + fullname

    if suffix:
        fullname = fullname + " " + suffix

    return fullname
