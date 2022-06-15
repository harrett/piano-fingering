import sys; sys.path.insert(0, './modules')
from parse import midi2notes
from ga import notes2fingering

params = {
    "n_genes": 30,
    "n_children": 20,
    "mutation": 0.02,
    "n_generation": 100,
    "n_choices": 5,
}

def midi2fingering(path):
    notes = midi2notes(path)
    fingering = notes2fingering(notes, **params)
    return fingering