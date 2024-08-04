from argparse import ArgumentParser
import config as cfg
from simulation import Simulation
from population import Population
import datetime
import csv

def main(args):
    
    config = cfg.load_file(args.config)

    # TODO input/output sizes fixed for now
    population = Population(**config.population)

    simulation = Simulation(config.simulation, population)

    stat_list = simulation.run(verbose=args.verbose)


    if args.save_stat:
        # TODO save stats
        now = datetime.datetime.now()
        filename = now.strftime("stats--%Y-%m-%d--%H-%M-%S.csv")

        try:
            with open(filename, "a", newline='') as file:
                writer = csv.writer(file, delimiter=',')
                header = config.simulation.statistics
                writer.writerow(header)
                
                for stat_dict in stat_list:
                    row = [stat_dict[stat] if stat in stat_dict else None for stat in header]
                    writer.writerow(row)

        except Exception as e:
            print("[WARN] Problem writing to {}:\n{}".format(filename, e))

if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument('config', help="experiment configuration file (.yaml) to run")

    parser.add_argument('-s', '--save_stat', action='store_true', 
        help='whether to save generation statistics')
    
    parser.add_argument('-v', '--verbose', action='store_true', 
        help='printing verbosity')

    args = parser.parse_args()

    main(args)