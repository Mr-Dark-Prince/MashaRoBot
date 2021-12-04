async def json_object_prettify(objecc):
    dicc = objecc.__dict__
    output = ""
    for key, value in dicc.items():
        if key in ["pinned_message", "photo", "_", "_client"]:
            continue
        output += f"**{key}:** `{value}`\n"
    return output


async def json_prettify(data):
    output = ""
    try:
        for key, value in data.items():
            output += f"**{str(key).capitalize()}:** `{value}`\n"
    except Exception:
        for datas in data:
            for key, value in datas.items():
                output += f"**{str(key).capitalize()}:** `{value}`\n"
            output += "------------------------\n"
    return output
