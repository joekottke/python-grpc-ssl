def english_full_name(first=None, last=None, middle=None,
                      prefix=None, suffix=None):
    if first is None or last is None:
        raise ValueError("first and last must be specified")

    parts = []
    if prefix:
        parts.append(prefix)
    parts.append(first)
    if middle:
        parts.append(middle)
    parts.append(last)
    if suffix:
        parts.append(suffix)

    return " ".join(parts)
