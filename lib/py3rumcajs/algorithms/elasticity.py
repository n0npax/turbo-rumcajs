import lib.rust.formulas.libformulas as formulas


def compute_elasticity(data, settings):
    hertz, sneddon = [], []
    for point in data['calibration_deltas']:
        force = point['x']
        delta = point['y']
        hertz.append({'x': force, 'y': formulas.hertz(force, settings.r,
                                                      delta)})
        sneddon.append({'x': force, 'y': formulas.sneddon(force, settings.mi_k,
                       settings.alpha, delta)})

    # the higest of all. usefull with graph plotting
    highest_elasticity = [max(hertz, key=lambda x: x['y']),
                          max(sneddon, key=lambda x: x['y']),
                          ]

    highest_elasticity = max(highest_elasticity, key=lambda x: x['y'])
    data['highest_elasticity'] = highest_elasticity

    data['hertz'] = hertz
    data['sneddon'] = sneddon
