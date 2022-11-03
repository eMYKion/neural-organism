from argparse import ArgumentParser
from configs.config import get_cfg_defaults
from experiment import load_experiment

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("exp_cfg", help="experiment configuration file (.yaml) to run", type=str)
    return parser.parse_args()

def main(args):
    cfg = get_cfg_defaults()
    cfg.merge_from_file(args.exp_cfg)
    cfg.freeze()
    print(cfg)
    
    experiment = load_experiment(cfg)
    experiment.run()

if __name__ == "__main__":
    args = parse_args()
    main(args)
