from sample_factory.algorithms.utils.arguments import arg_parser
from sample_factory.algorithms.utils.arguments import parse_args


def custom_parse_args(argv=None, evaluation=False):
    parser = arg_parser(argv, evaluation=evaluation)

    # add custom args here
    parser.add_argument(
        "--nle_env_name", type=str, default="NetHackChallenge-v0", help=""
    )
    parser.add_argument(
        "--transformer_hidden_size",
        type=int,
        default=64,
        help="size of transformer hidden layers",
    )
    parser.add_argument(
        "--transformer_hidden_layers",
        type=int,
        default=2,
        help="number of transformer hidden layers",
    )
    parser.add_argument(
        "--transformer_attention_heads",
        type=int,
        default=2,
        help="number of transformer attention heads",
    )
    parser.add_argument(
        "--max_token_length",
        type=int,
        default=256,
        help="Maximum token input length before truncation",
    )

    cfg = parse_args(argv=argv, evaluation=evaluation, parser=parser)
    return cfg
