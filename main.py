from runner import Runner
import argparse

parser = argparse.ArgumentParser(description='Run grain type experiments.')
parser.add_argument('-i', '--input', type=str, help='Path to model grid in ASC format.', required=True)
parser.add_argument('-n', '--name', type=str, help='Experiment title', default="my_experiment", required=True)
parser.add_argument('-c', '--checkpoint', type=int, help='Number of step for checkpoints',  default=1, required=True)
parser.add_argument('-e', '--executions', type=int, help='Number of steps for experiment', required=True)

args = parser.parse_args()

assert args.executions > args.checkpoint, "A quantidade de execuções deve ser maior que checkpoints"

if __name__ == "__main__":
    grid_path = args.input
    name = args.name
    checkpoint = args.checkpoint
    executions = args.executions

    runner = Runner(grid_path, name, checkpoint)
    runner.run(executions)
