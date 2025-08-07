#utils.py
import time

def bits_to_mbps(bits_per_sec):
    """Convert bits per second to Megabits per second (Mbps)."""
    return round(bits_per_sec / 1_000_000, 2)

def map_value(value, in_min, in_max, out_min, out_max):
    """Linearly maps a value from one range to another."""
    """ Usage example:
    # Convert 500 Mbps (in range 0-1000) to an angle (e.g. -120° to 120°)
        angle = map_value(500, 0, 1000, -120, 120)
    """
    value = max(min(value, in_max), in_min)  # clamp
    return out_min + (float(value - in_min) / (in_max - in_min)) * (out_max - out_min)

def smooth_update(callback, start, end, duration=1.5, steps=30):
    """Smoothly update a value from start to end over 'duration' seconds."""
    step_time = duration / steps
    delta = (end - start) / steps

    value = start
    for _ in range(steps):
        value += delta
        callback(value)
        time.sleep(step_time)