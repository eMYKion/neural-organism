from argparse import ArgumentParser
import config as cfg
from simulation import Simulation
from population import Population
from datetime import datetime
import csv
import logging
import json
import sys

def save_csv(filename, header, rows):
        try:
            with open(filename, "a", newline='') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow(header)
                
                for stat_dict in rows:
                    row = [stat_dict[stat] if stat in stat_dict else None for stat in header]
                    writer.writerow(row)

        except Exception as e:
            # NOTE: logging should be known/structured key-val pairs,
            # followed by optional, unstructured string/text (with or without quotes)
            logging.error("error={} Problem writing to {}".format(filename, json.dumps(e)))

def main(args):
    
    config = cfg.load_file(args.config)

    logging_handlers = {}
    if args.verbose:
        logging_handlers["STDOUT"] = logging.StreamHandler(sys.stdout)
    if args.save_logs is not None:
        logging_handlers["FILE"] = logging.FileHandler(args.save_logs)

    if len(logging_handlers) == 0:
        logging.disable(logging.CRITICAL)
    else:
        logging.basicConfig(
            level=logging.INFO, 
            format="%(asctime)s [%(levelname)s, %(name)s, %(funcName)s] %(message)s",
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=list(logging_handlers.values())
        )

    logging.info("logging_handlers={}".format(
        json.dumps(list(logging_handlers.keys()))
    ))

    

    # TODO input/output sizes fixed for now
    population = Population(**config.population)

    simulation = Simulation(config.simulation, population, verbose=args.verbose, display=args.display)

    stat_list = simulation.run()

    if args.save_stats is not None:
        save_csv(args.save_stats, header=config.simulation.statistics, rows=stat_list)

if __name__ == "__main__":

    parser = ArgumentParser()

    dtstamp = datetime.now().strftime("%Y%m%d%H%M%S")

    parser.add_argument('config', help="experiment configuration file (.yaml) to run")
    
    parser.add_argument('-v', '--verbose', action='store_true', 
        help='print logs to stdout')
    
    parser.add_argument('-d', '--display', action='store_true', 
        help='display a histogram of the population fitness every 5 generations of the simulation')
    
    parser.add_argument('-l', '--save_logs', required=False,
        nargs='?', 
        const=dtstamp + ".log",
        help='save logs to file')
    
    parser.add_argument('-s', '--save_stats', required=False,
        nargs='?', 
        const="stats-" + dtstamp + ".csv",
        help='whether to save simulation run statistics as a CSV file')

    args = parser.parse_args()

    main(args)