import sys

from sample_factory.algorithms.utils.arguments import arg_parser
from sample_factory.algorithms.utils.arguments import parse_args
from sample_factory.run_algorithm import run_algorithm

# Needs to be imported to register models and envs
import nle_language_wrapper.agents.sample_factory.env  # pylint: disable=['unused-import']
import nle_language_wrapper.agents.sample_factory.language_encoder  # pylint: disable=['unused-import']
from nle_language_wrapper.agents.sample_factory.common import custom_parse_args


def parse_all_args(argv=None, evaluation=False):
    parser = arg_parser(argv, evaluation=evaluation)
    cfg = parse_args(argv=argv, evaluation=evaluation, parser=parser)
    return cfg


def main():
    cfg = custom_parse_args()
    status = run_algorithm(cfg)
    return status


if __name__ == "__main__":
    sys.exit(main())
