from functools import lru_cache

import gym
import numpy as np
import torch
from sample_factory.envs.env_registry import global_env_registry
from transformers import RobertaTokenizerFast

from nle_language_wrapper import NLELanguageWrapper


class SampleFactoryNLELanguageEnv(gym.Env):
    LRU_CACHE_SIZE = 1000

    def __init__(self, cfg):
        self.cfg = cfg
        self.observation_space = gym.spaces.Dict()
        self.observation_space.spaces["obs"] = gym.spaces.Box(
            0, 1000000, shape=(1,), dtype=np.int32
        )
        self.observation_space.spaces["input_ids"] = gym.spaces.Box(
            0, 1000000, shape=(self.cfg["max_token_length"],), dtype=np.int32
        )
        self.observation_space.spaces["attention_mask"] = gym.spaces.Box(
            0, 1, shape=(self.cfg["max_token_length"],), dtype=np.int32
        )
        self.nle_env = gym.make(self.cfg["nle_env_name"])
        self.env = NLELanguageWrapper(self.nle_env, use_language_action=False)
        self.action_space = self.env.action_space
        self.tokenizer = RobertaTokenizerFast.from_pretrained(
            "distilroberta-base", truncation_side="left"
        )

    # We use caching to avoid re-tokenizing observations that are already seen.
    @lru_cache(maxsize=LRU_CACHE_SIZE)
    def _tokenize(self, str_obsv):
        tokens = self.tokenizer(
            str_obsv,
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=self.cfg["max_token_length"],
        )
        # Sample factory insists on normalizing obs key.
        tokens.data["obs"] = torch.zeros(1)
        return tokens.data

    def _convert_obsv_to_str(self, obsv):
        text_obsv = ""
        text_obsv += f"Inventory:\n{obsv['text_inventory']}\n\n"
        text_obsv += f"Stats:\n{obsv['text_blstats']}\n\n"
        text_obsv += f"Cursor:\n{obsv['text_cursor']}\n\n"
        text_obsv += f"Stats:\n{obsv['text_glyphs']}\n\n"
        text_obsv += f"Message:\n{obsv['text_message']}"
        return text_obsv

    def reset(self, **kwargs):
        return self._tokenize(self._convert_obsv_to_str(self.env.reset(**kwargs)))

    def step(self, action):
        obsv, reward, done, info = self.env.step(action)
        tokenized_obsv = self._tokenize(self._convert_obsv_to_str(obsv))
        return tokenized_obsv, reward, done, info

    def seed(self, *args):  # pylint: disable=['unused-argument']
        # Nethack does not allow seeding
        return

    def render(self, *args, **kwargs):  # pylint: disable=['unused-argument']
        self.env.render()


def make_custom_env_func(
    full_env_name, cfg=None, env_config=None
):  # pylint: disable=['unused-argument']
    env = SampleFactoryNLELanguageEnv(cfg)
    return env


global_env_registry().register_env(
    env_name_prefix="nle_language_env",
    make_env_func=make_custom_env_func,
)
