def extract_features(speed, rpm, throttle, prev_speed, prev_throttle, interval):
    acceleration = (speed - prev_speed) / interval
    delta_throttle = throttle - prev_throttle
    return [speed, rpm, throttle, acceleration, delta_throttle]


def rule_based_label(features):
    speed, rpm, throttle, acc, d_throttle = features

    # Idle
    if rpm < 1000:
        return "Smooth"

    # Rash conditions
    if abs(acc) > 12:
        return "Rash"

    if d_throttle > 20:
        return "Rash"

    # Aggressive
    if rpm > 3000:
        return "Aggressive"

    if throttle > 70:
        return "Aggressive"

    return "Normal"
