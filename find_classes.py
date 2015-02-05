def find(base, headers, inheritance='public'):
    '''Scan header files for classes inheriting from a given base class,
    according to the specified inheritance pattern (defaults to 'public').
    Returns a sequence of class names.'''

    import re
    regex = 'class\s+([a-zA-Z_]\w+)\s*:\s*' + inheritance + '\s*' + base
    print regex
    cregex = re.compile(regex)

    class_names = []
    for header in headers:
        with open(header) as hfile: text=hfile.read()
        class_names += (match.group(1) for match in re.finditer(cregex, text))
    return class_names
