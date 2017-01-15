import lib.rust.formulas.libformulas as formulas


def compute_elasticity(data, settings):
    hertz, sneddon = [], []
    for point in data['calibration_deltas']:
        force = point['x']
        delta = point['y']
        hertz.append({'x': force, 'y': formulas.hertz(force, settings.r, delta)})
        sneddon.append({'x': force, 'y': formulas.sneddon(force, settings.mi_k,
                                        settings.alpha, delta)})
    data['hertz'] = hertz
    data['sneddon'] = sneddon

