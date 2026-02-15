def explain(features):
    speed, rpm, throttle, acc, d_throttle = features
    reasons = []

    if abs(acc) > 10:
        reasons.append("Sudden acceleration or braking")

    if rpm > 3500:
        reasons.append("High RPM usage")

    if d_throttle > 15:
        reasons.append("Rapid throttle input")

    if throttle > 70:
        reasons.append("High throttle usage")

    if not reasons:
        reasons.append("Stable driving parameters")

    return reasons
