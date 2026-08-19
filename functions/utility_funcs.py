import os

def check_folders():
    # If folders are not there, make them
    os.makedirs("audio", exist_ok=True)
    os.makedirs("graphs", exist_ok=True)


def seconds_to_samples(sample_rate, seconds):
    return int(seconds * sample_rate)