def html_formation(string: str) -> str:

    symbols = {
        "<": "&lt;",
        ">": "&gt;",
        "&": "&amp;"
    }

    result = ""
    for char in string:
        if char in symbols:
            result += symbols[char]
        else:
            result += char

    return result