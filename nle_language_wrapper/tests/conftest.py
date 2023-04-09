import gym
import numpy as np
import pytest
from gym import spaces
from nle.env import NLE
from nle.nethack import actions as nethack_actions

from nle_language_wrapper.tests.test_utils import str_to_1d
from nle_language_wrapper.tests.test_utils import strs_to_2d


@pytest.fixture
def real_nethack_env():
    """Fixture for real NLE environment"""
    nle_env = gym.make("NetHackChallenge-v0")
    return nle_env


@pytest.fixture
def fake_nle_env(mocker):
    """Fixture for fake NLE environment"""
    nle_env = mocker.MagicMock(spec=NLE)
    blstats = np.array(
        [
            66,  # player Y
            14,  # Player X
            19,  # Percentile strength
            1,  # Strength
            4,  # Dexterity
            5,  # Constitution
            6,  # Intelligence
            7,  # Wisdom
            8,  # Charisma
            123,  # Score
            11,  # HP Current
            12,  # HP Max
            9,  # Depth
            10,  # Gold
            1,  # Energy current
            13,  # Energy max
            1,  # AC
            23,  # Monster level
            7,  # Xp Current
            10,  # XP level
            5,  # Time
            4,  # Hunger
            2,  # Encumberance
            21,  # Dungeon number
            10,  # Level number
            11,  # Conditions
            -1,  # Alignment
        ],
        dtype=np.int64,
    )
    tty_cursor = np.array(
        [14 + 1, 66],  # Player X (offset by 1 for some reason)  # Player Y
        dtype=np.uint8,
    )
    tty_chars = strs_to_2d(
        ["Hello Agent, welcome to NetHack!  You are a neutral gnomish Caveman."]
    )
    inv_letters = str_to_1d("ab\x00")
    inv_strs = strs_to_2d(
        [
            "a blessed +1 quarterstaff (weapon in hands)\x00",
            "an uncursed +0 cloak of magic resistance (being worn)\x00",
        ]
    )
    glyphs = np.full((21, 79), 2359)
    glyphs[14, 66] = 333
    glyphs[20, 50] = 397  # tame dog
    glyphs[10, 65] = 2360
    glyphs[9, 64] = 2390  # fountain
    glyphs[13, 66] = 2374  # vertical closed door
    obsv = {
        "glyphs": glyphs,
        "blstats": blstats,
        "tty_chars": tty_chars,
        "inv_letters": inv_letters,
        "inv_strs": inv_strs,
        "tty_cursor": tty_cursor,
    }
    reward = 0.0
    done = False
    info = None
    nle_env.reset = mocker.MagicMock(return_value=obsv)
    nle_env.step = mocker.MagicMock(return_value=(obsv, reward, done, info))
    nle_env.actions = [nethack_actions.CompassDirection.N]
    nle_env.observation_space = spaces.Dict(
        {
            "glyphs": spaces.Space(),
            "blstats": spaces.Space(),
            "tty_cursor": spaces.Space(),
            "inv_strs": spaces.Space(),
            "inv_letters": spaces.Space(),
            "tty_chars": spaces.Space(),
        }
    )
    return nle_env


@pytest.fixture
def fake_nethack_multiple_monsters_env(mocker):
    """Fixture for fake NLE environment containing multiple monsters"""
    nle_env = mocker.MagicMock(spec=NLE)
    blstats = np.array([66, 14, 19], dtype=np.uint8)
    tty_cursor = np.array([66, 14, 19], dtype=np.uint8)
    tty_chars = strs_to_2d(
        ["Hello Agent, welcome to NetHack!  You are a neutral gnomish Caveman."]
    )
    inv_letters = str_to_1d("ab\x00")

    inv_strs = strs_to_2d(
        [
            "a blessed +1 quarterstaff (weapon in hands)\x00",
            "an uncursed +0 cloak of magic resistance (being worn)\x00",
        ]
    )
    glyphs = np.full((21, 79), 2359)
    glyphs[14, 66] = 359
    glyphs[14, 18] = 397  # tame dog 1
    glyphs[20, 50] = 397  # tame dog 2
    glyphs[20, 51] = 397  # tame dog 3
    glyphs[10, 65] = 2360
    glyphs[9, 64] = 2390  # fountain
    glyphs[9, 63] = 2390  # fountain
    glyphs[13, 66] = 2374  # vertical closed door
    obsv = {
        "glyphs": glyphs,
        "blstats": blstats,
        "tty_chars": tty_chars,
        "inv_letters": inv_letters,
        "inv_strs": inv_strs,
        "tty_cursor": tty_cursor,
    }
    reward = 0.0
    done = False
    info = None
    nle_env.reset = mocker.MagicMock(return_value=obsv)
    nle_env.step = mocker.MagicMock(return_value=(obsv, reward, done, info))
    nle_env.actions = [nethack_actions.CompassDirection.N]
    nle_env.observation_space = spaces.Dict(
        {
            "glyphs": spaces.Space(),
            "blstats": spaces.Space(),
            "tty_cursor": spaces.Space(),
            "inv_strs": spaces.Space(),
            "inv_letters": spaces.Space(),
            "tty_chars": spaces.Space(),
        }
    )
    return nle_env
