import re

regex1 = r'([-+]?\d+\.?\d*?[Ee]?[-+]?\d*?[\s]){2,}'
pattern1 = re.compile(regex1, re.M)


def validate_file(file):
    filename = file.filename
    return validate_extension(filename) and validate_by_regex(file)


def validate_extension(filename):
    if '.' in filename:
        return filename.rsplit('.', 1)[1] in ['txt', 'dat', 'data']
    else:
        return True


def validate_by_regex(file):
    content = repr(file.read())
    file.seek(0, 0)
    return pattern1.search(content)


def remove_duplicates(filename):
    with open(filename, 'r') as f:
        content = f.read()
    match = pattern1.search(content)
    if match:
        lines = match.group()
        columns_num = lines.split()
        print(match, columns_num, lines, "<<<<")
        #for id, line in enumerate(lines[:-1]):
        #    if columns_num ==2:
        #        if lines[id] == lines[id+1]:
        #            print(line)

