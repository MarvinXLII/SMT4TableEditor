import argparse
from pathlib import Path


def get_input_files(inputs):
    paths = []
    for x in inputs:
        p = Path(x)
        if p.is_dir():
            paths += p.glob('**/*.tbb')
        elif not p.exists():
            print(p, 'does not exist!')
        elif p.suffix == '.tbb':
            paths.append(p)
    paths.sort()
    return paths

        
def get_bin_files(inputs):
    paths = []
    for x in inputs:
        p = Path(x)
        if p.is_dir():
            paths += p.glob('**/Skill2EffectData.bin')
        elif not p.exists():
            print(p, 'does not exist!')
        elif p.name == 'Skill2EffectData.bin':
            paths.append(p)
    return paths

        
