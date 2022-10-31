from argparse import ArgumentParser
from experiment import load_experiment

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("exp_num", help="experiment number to run", type=int)
    return parser.parse_args()

def main(args):
    experiment = load_experiment(args.exp_num)
    experiment.run()

if __name__ == "__main__":
    args = parse_args()
    main(args)
