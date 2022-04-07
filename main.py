from argparse import ArgumentParser
from app import SolverApp
from constants import NUMBER_TO_BEAT

parser = ArgumentParser(description="Beats {}".format(NUMBER_TO_BEAT))

parser.add_argument("-d", "--debug", action="store_true", help="debug output")
parser.add_argument("-f", "--file_path", default="cache/cache.json", help="the file path")
parser.add_argument("-t", "--num_threads", default=8, help="number of threads")
parser.add_argument("-w", "--what_to_beat", action="store_true", help="just give me the number to beat")
parser.add_argument("-n", "--number", default=NUMBER_TO_BEAT, help="the number to beat")

args = parser.parse_args()

if args.what_to_beat:
    print(NUMBER_TO_BEAT)
    exit()

SolverApp().run(
    number=args.number,
    debug=args.debug,
    num_threads=int(args.num_threads),
    file_path=args.file_path
)
