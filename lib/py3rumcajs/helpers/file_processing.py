import re
from orderedset import OrderedSet

headers = ['# TEXT EXPORT', 'X Unit:', 'point']


def validate_file(file):
    return validate_extension(file) and validate_by_1stline(file)


def validate_extension(file):
    filename = file.filename
    if '.' in filename:
        return filename.rsplit('.', 1)[1] in ['txt', 'dat', 'data']
    else:
        return True


def validate_by_1stline(file):
    content = repr(file.read())
    file.seek(0, 0)
    for header in headers:
        if content.startswith(header, 1):
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

    return {'name': filename.split('/')[-1],
            'x_prefix': x_prefix,
            'y_prefix': y_prefix,
            'data': data}


def rescale_data(data, prefix):
    # TODO
    return data


def cut_half_if_need(data):
    middle_point = data[int(len(data)/2)]
    begin_point = data[0]
    end_point = data[-1]
    if end_point['y'] < middle_point['y'] > begin_point['y']:
        return data[:int(len(data)/2)]
    else:
        return data

