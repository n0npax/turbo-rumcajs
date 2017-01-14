import scipy.signal
import numpy
import copy

from scipy.spatial import distance
from scipy.stats import linregress


def smooth(data, window=17, key='data', dest_key='data'):
    if dest_key not in data:
        data[dest_key] = copy.deepcopy(data[key])
    y_vals = [point['y'] for point in data[key]]
    y_vals = scipy.signal.savgol_filter(y_vals, window, 3)
    for i, y in enumerate(y_vals):
        data[dest_key][i]['y'] = y


def calibrate(data):
    # TODO split to 2-3 separate functions
    remove_edge_duplicated_points(data)
    smooth(data, dest_key='smooth_data')
    derivative(data)

    # AXIS_{smooth,derivative}VALS
    y_vals = [point['y'] for point in data['data']]
    x_vals = [point['x'] for point in data['data']]
    y_dvals = [point['y'] for point in data['derivative']]
    x_dvals = [point['x'] for point in data['derivative']]
    y_svals = [point['y'] for point in data['smooth_data']]
    x_svals = [point['x'] for point in data['smooth_data']]

    xs_max_index = x_svals.index(max(x_vals))
    yd_min_index = y_dvals.index(min(y_dvals))
    index = yd_min_index

    def get_step(xs_max_index, yd_min_index):
        if xs_max_index > yd_min_index:
            return 1
        else:
            return -1

    step = get_step(xs_max_index, yd_min_index)

    # 1st c_point
    while True:
        if y_svals[index] - y_dvals[index] < 0:
            break
        index += step

    # 2ns c_point
    while True:
        slope_shift_y = y_svals[index-10*step:index] or \
            y_svals[index:index-10*step]
        no_slope_shift_x = x_svals[index+100*step:index] or \
            x_svals[index:index+100*step]
        no_slope_shift_y = y_svals[index+100*step:index] or \
            y_svals[index:index+100*step]

        slope, intercept, r_value, p_value, std_err = \
            linregress(no_slope_shift_x, no_slope_shift_y)

        if slope * x_svals[index] + intercept + std_err < y_svals[index] or \
                slope * x_svals[index] + intercept - std_err > y_svals[index]:
            print('REG_BREAK')
            break

        if slope_shift_y == sorted(slope_shift_y):
                break

        index -= step

    # 3rd c_point
    #for i in range(-30, 30):
    #    pass
    #    Fir by linreg

    # save c_point
    data['c_point'] = [{'x': x_vals[index], 'y': y_vals[index]},
                       {'x': x_vals[index], 'y': min(y_vals)},
                       {'x': x_vals[index], 'y': max(y_vals)}]
    data['c_point_index'] = index

    shift_data_to_00(data)
    cut_to_c_point(data, 'smooth_data', 'calibrated')

    return data


def cut_to_c_point(data, key, dest_key):
    if data[key][0]['y'] > data[key][-1]['y']:
        data[dest_key] = data[key][:data['c_point_index']]
    else:
        data[dest_key] = data[key][data['c_point_index']:]


def shift_data_to_00(data):
    dx = data['c_point'][0]['x']
    dy = data['c_point'][0]['y']
    for key, values in data.items():
        if type(values) != list:
            continue
        for point in values:
            point['x'] -= dx
            point['y'] -= dy


def remove_edge_duplicated_points(data):
    beg_index, end_index = 0, -1
    y_vals = [point['y'] for point in data['data']]
    for i in range(len(y_vals)):
        if y_vals[i] == y_vals[i+1]:
            continue
        beg_index = i
        break
    for i in reversed(range(len(y_vals))):
        if y_vals[i] == y_vals[i-1]:
            continue
        end_index = i
        break
    data['data'] = data['data'][beg_index:end_index]


def derivative(data):

    data['derivative'] = []
    y_vals = [point['y'] for point in data['smooth_data']]
    x_vals = [point['x'] for point in data['smooth_data']]
    for i in range(len(data['data'])):
        if i > 0 and i < len(data['data']) - 1:
            indexes = [i-1, i, i+1]
        elif i == 0:
            indexes = [i, i+1]
        elif i == len(data['data']) - 1:
            indexes = [i-1, i]
        else:
            raise Exception('shouldnt happen {}'.format(i))
        x = [x_vals[j] for j in indexes]
        y = [y_vals[j] for j in indexes]
        slope, intercept, _, _, _ = linregress(x, y)
        data['derivative'] += [{'x': x_vals[i], 'y': slope}]
    smooth(data, key='derivative', dest_key='derivative')


def compute_deltas(d_data, c_data):
    d_y_vals = [point['y'] for point in d_data['calibrated']]
    c_y_vals = [point['y'] for point in c_data['calibrated']]

    max_y_lvl = max(max(d_y_vals), max(c_y_vals))

    if max(c_y_vals) == max_y_lvl:
        data1 = d_data  # data1 shorter data set
        data2 = c_data  # data2 longer data set
    else:
        data1 = c_data
        data2 = d_data
    numpy_points2 = numpy.array([[point['x'], point['y']]
                                for point in data2['calibrated']])

    dict_points1 = data1['calibrated']
    dict_points2 = data2['calibrated']

    deltas = []
    for i, point_dict in enumerate(dict_points1):
        point = (point_dict['x'], point_dict['y'])
        n = get_nearest_point(point, numpy_points2)
        n_index = dict_points2.index({'x':n[0],'y':n[1]})
        try:
            # TODO FIX
            d_p = dict_points2[n_index-1:n_index+1]
            x ,y = [ _['x'] for _ in d_p],[_['y'] for _ in d_p]
            slope, intercept, _, _, _ = linregress(x,y)
            y = slope * point_dict['x'] + intercept
            delta = abs(point_dict['y'] - y)
            deltas.append({'x' : point_dict['y'], 'y': delta})
        except Exception as e:
            print(e,x,y)
    d_data['calibration_deltas'] = deltas


def get_nearest_point(point, points):
    return points[distance.cdist([point], points).argmin()]

