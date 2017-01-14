import re
from orderedset import OrderedSet
from lib.py3rumcajs.exceptions.exceptions import SampleValidationException

headers = ['# TEXT EXPORT', 'X Unit:', 'point']


def validate_file(file):
    if validate_extension(file) and validate_by_1stline(file):
        return True
    raise SampleValidationException('file is not valid')


def validate_extension(file):
    filename = file.filename
    if '.' in filename:
        return filename.split('.')[-1] in ['txt', 'dat', 'data']
    else:
        return True


def validate_by_1stline(file):
    content = repr(file.read())
    file.seek(0, 0)
    for header in headers:
        for shift in [0, 1, 2]:
            if content.startswith(header, shift):
                return True
    return False


def parse_to_dict(filename):
    with open(filename, 'r') as f:
        content = f.read()
        num_start = re.search(r'^\d.*', content, re.M)
        content_numbers = [line.strip() for line in
                           content[num_start.start():].split('\n')
                           if line.strip()]
        content_header = content[:num_start.start()].split('\n')

        numbers_len = len(content_numbers[0].split())
        data = []
        for line in content_numbers:
            try:
                numbers = [float(num) for num in line.split()]
                if numbers_len == 4:
                    numbers = (numbers[1], numbers[3])
                elif numbers_len == 2:
                    numbers = tuple(numbers)
                elif numbers_len == 6:
                    numbers = (numbers[2], numbers[1])
                else:
                    raise Exception()  # TODO
                data.append(numbers)
            except:
                print(line, '<<<<<,')
                break
                content_header.append(line)
        data = list(OrderedSet(data))
        data = [{'x': _[0], 'y': _[1]} for _ in data]
        data = cut_half_if_need(data)

    for line in content_header:
        match = re.search('X\s+Unit:\s+([\w\?]+)', line)
        if match:
            x_prefix = match.group(1)
        match = re.search('Y\s+Unit:\s+([\w\?]+)', line)
        if match:
            y_prefix = match.group(1)
        match = re.search('\s+(.m)\s+.m\s+(.N)', line)
        if match:
            x_prefix = match.group(1)
            y_prefix = match.group(2)
        match = re.search('units:\s.\s(.)\s(.)\s.\s.\s.', line)
        if match:
            x_prefix = match.group(2)
            y_prefix = match.group(1)

    data = rescale_data(data, x_prefix, y_prefix)

    return {'name': filename.split('/')[-1],
            'x_prefix': 'Meter',
            'y_prefix': 'Newton',
            'data': data}


def get_prefix(prefix):
    if prefix == 'N' or prefix == 'm':
        return 1
    elif prefix.lower().startswith('mili'):
        return 10**-3
    elif prefix.lower().startswith('micro') or \
            prefix.lower().startswith('mikro'):
        return 10**-6
    elif prefix.lower().startswith('nano'):
        return 10**-9
    elif prefix.lower().startswith('piko'):
        return 10**-12
    elif prefix.lower().startswith('?'):  # TODO mikro ??
        return 10**-6
    elif prefix.lower().startswith('n'):
        return 10**-9

    raise Exception('can\'t determine how to rescale - prefix: {}'
                    .format(prefix))


def rescale_data(data, prefix_x, prefix_y):
    x_scale = get_prefix(prefix_x)
    y_scale = get_prefix(prefix_y)
    return [{'x': _['x'] * x_scale, 'y': _['y'] * y_scale} for _ in data]


def cut_half_if_need(data):
    middle_point = data[int(len(data)/2)]
    begin_point = data[0]
    end_point = data[-1]
    if end_point['y'] < middle_point['y'] > begin_point['y']:
        return data[:int(len(data)/2)]
    else:
        return data

