import sys

from sample_factory.algorithms.appo.enjoy_appo import enjoy

import nle_language_wrapper.agents.sample_factory.env  # pylint: disable=['unused-import']
import nle_language_wrapper.agents.sample_factory.language_encoder  # pylint: disable=['unused-import']
from nle_language_wrapper.agents.sample_factory.common import custom_parse_args


def main():
    cfg = custom_parse_args(evaluation=True)
    status = enjoy(cfg)
    return status


if __name__ == "__main__":
    sys.exit(main())
