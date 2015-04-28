from path import Path

def asset(filename):
    path = Path(__file__).dirname().realpath().joinpath('assets', filename)
    return path
