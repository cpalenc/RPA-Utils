def extract_first_match(args):      
    try:
        import re
        import traceback
        args_splitted = args.split("||")
        print((args_splitted))
        regex_pattern = args_splitted[0]
        text = args_splitted[1]
        regex = re.compile(regex_pattern)
        print(f"{regex = }")
        match = regex.search(text)
        if match:
            return match.group()
        return "No se encontraron coincidencias."
    except Exception:
        return traceback.format_exc()
