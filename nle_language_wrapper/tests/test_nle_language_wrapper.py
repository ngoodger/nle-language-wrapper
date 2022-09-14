import timeit

import gym
import numpy as np
import pytest
from gym import spaces
from nle.env import NLE
from nle.nethack import actions as nethack_actions

from nle_language_wrapper import NLELanguageWrapper
from nle_language_wrapper.scripts import play


def str_to_1d(string):
    """Convert a string to equivalent numpy array
    Args:
        string(str): string to be converted
    Returns:
        (numpy.ndarray): 1-D uint8 values for unicode string input.
    """
    output = np.array(bytearray(string.encode("utf-8")))
    return output


def strs_to_2d(strings, fill_value=0):
    """Convert a list of strings to equivalent 2d numpy array
    Args:
        strings(List[str]): string to be converted
    Returns:
        (numpy.ndarray): 2-D uint8 values for unicode strings input.
    """
    arrays = []
    max_len = 0
    for string in strings:
        arrays.append(str_to_1d(string))
        if len(string) > max_len:
            max_len = len(string)
    output = np.full((len(arrays), max_len), fill_value=fill_value, dtype=np.uint8)
    for i, array in enumerate(arrays):
        output[i, : len(array)] = array
    return output


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
    nle_env._actions = [nethack_actions.CompassDirection.N]
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
    nle_env._actions = [nethack_actions.CompassDirection.N]
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


def test_message_spell_menu(fake_nle_env):
    menu = [
        "   Choose which spell to cast                               ",
        "                                                             ",
        "   Name                 Level Category     Fail Retention   ",
        "   a - healing                1   healing        0%      100%",
        "   (end)                                                     ",
    ]
    empty_lines = [
        "                                                      ",
        "                                                      ",
    ]
    screen_map = [
        "         -----------------------------------------|           ",
        "         |               @                        |           ",
    ]
    # Fill with spaces for menu
    tty_chars = strs_to_2d(menu + empty_lines + screen_map, fill_value=32)

    fake_nle_env.reset.return_value["tty_chars"] = tty_chars
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()

    expected_menu = (
        "Choose which spell to cast\n"
        "\n"
        "Name                 Level Category     Fail Retention\n"
        "a - healing                1   healing        0%      100%\n"
        "(end)"
    )
    assert obsv["text_message"] == expected_menu


def test_message_more_end(fake_nle_env):
    things_that_are_here = [
        " Things that are here:      ",
        " a goblin corpse             ",
        " an iron skull cap           ",
        " --More--                    ",
    ]
    screen_map = [
        "         -----------------------------------------|           ",
        "         |               @                        |           ",
    ]
    # Fill with spaces for menu
    tty_chars = strs_to_2d(things_that_are_here + screen_map, fill_value=32)

    fake_nle_env.reset.return_value["tty_chars"] = tty_chars
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()

    expected_menu = (
        "Things that are here:\n"
        + "a goblin corpse\n"
        + "an iron skull cap\n"
        + "--More--"
    )
    assert obsv["text_message"] == expected_menu


def test_message_full_stop_end(fake_nle_env):
    message = [" It's a wall. ", " "]

    screen_map = [
        "         -----------------------------------------|           ",
        "         |               @                        |           ",
    ]

    # Fill with spaces for menu
    tty_chars = strs_to_2d(message + screen_map, fill_value=32)

    fake_nle_env.reset.return_value["tty_chars"] = tty_chars
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()

    expected_menu = "It's a wall."
    assert obsv["text_message"] == expected_menu


def test_message_bracket_end(fake_nle_env):
    message = [" What do you want to drop? [$a-k or ?*] ", " "]

    screen_map = [
        "         -----------------------------------------|           ",
        "         |               @                        |           ",
    ]
    # Fill with spaces for menu
    tty_chars = strs_to_2d(message + screen_map, fill_value=32)
    fake_nle_env.reset.return_value["tty_chars"] = tty_chars
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    expected_menu = "What do you want to drop? [$a-k or ?*]"
    assert obsv["text_message"] == expected_menu


def test_message_parenthesis_end(fake_nle_env):
    message = [" Where do you want to travel to?  (For instructions type a '?') ", " "]

    screen_map = [
        "         -----------------------------------------|           ",
        "         |               @                        |           ",
    ]
    # Fill with spaces for menu
    tty_chars = strs_to_2d(message + screen_map, fill_value=32)
    fake_nle_env.reset.return_value["tty_chars"] = tty_chars
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    expected_message = "Where do you want to travel to?  (For instructions type a '?')"
    assert obsv["text_message"] == expected_message


def test_message_multipage(fake_nle_env):
    message = [
        " Extended Commands List    ",
        "                               ",
        " a - Hide commands that don't autocomplete (those not marked with [A])   ",
        " : - Search extended commands      ",
        " ",
        " Extended commands                     ",
        " #                  perform an extended command  ",
        " ?              [A] list all extended commands  ",
        " adjust         [A] adjust inventory letters   ",
        " annotate       [A] name current level  ",
        " (1 of 5) ",
    ]

    tty_chars = strs_to_2d(message, fill_value=32)
    fake_nle_env.reset.return_value["tty_chars"] = tty_chars
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    expected_message = (
        "Extended Commands List\n"
        "\n"
        "a - Hide commands that don't autocomplete (those not marked with [A])\n"
        ": - Search extended commands\n"
        "\n"
        "Extended commands\n"
        "#                  perform an extended command\n"
        "?              [A] list all extended commands\n"
        "adjust         [A] adjust inventory letters\n"
        "annotate       [A] name current level\n"
        "(1 of 5)"
    )
    assert obsv["text_message"] == expected_message


def test_message_takeoffall(fake_nle_env):
    message = [
        " What type of things do you want to take off?    ",
        " ",
        "  a - All worn types                             ",
        " b - Weapons ",
        " c - Armor ",
        " U - Items known to be Uncursed ",
        " (end) ",
    ]
    screen_map = [
        "         -----------------------------------------|           ",
        "         |               @                        |           ",
    ]
    # Fill with spaces for menu
    tty_chars = strs_to_2d(message + screen_map, fill_value=32)
    fake_nle_env.reset.return_value["tty_chars"] = tty_chars
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    expected_message = (
        "What type of things do you want to take off?\n"
        "\n"
        "a - All worn types\n"
        "b - Weapons\n"
        "c - Armor\n"
        "U - Items known to be Uncursed\n"
        "(end)"
    )
    assert obsv["text_message"] == expected_message


def test_filter_map_from_conduct(fake_nle_env):
    message = [
        "                          Voluntary challenges:                  ",
        "                           You have gone without food.              ",
        "                           You have been an atheist.                ",
        "              -----        You have never hit with a wielded weapon.",
        "             #+....######  You have been a pacifist.                ",
        "             #+....######  --More--                ",
    ]
    tty_chars = strs_to_2d(message, fill_value=32)
    fake_nle_env.reset.return_value["tty_chars"] = tty_chars
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    expected_message = (
        "Voluntary challenges:\n"
        "You have gone without food.\n"
        "You have been an atheist.\n"
        "You have never hit with a wielded weapon.\n"
        "You have been a pacifist.\n"
        "--More--"
    )
    assert obsv["text_message"] == expected_message


def test_filter_map_from_name(fake_nle_env):
    message = [
        "                              What do you want to name? ",
        "                                                        ",
        "---------                     m - a monster ",
        "|........                     i - a particular object in inventory ",
        "|.......|                     o - the type of an object in inventory  ",
        "|....@.%|                     f - the type of an object upon the floor  ",
        "|!...df.|                     d - the type of an object on discoveries list ",
        "|.......+                     a - record an annotation for the current level ",
        "--+------                     (end)",
    ]
    tty_chars = strs_to_2d(message, fill_value=32)
    fake_nle_env.reset.return_value["tty_chars"] = tty_chars
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    expected_message = (
        "What do you want to name?\n"
        "\n"
        "m - a monster\n"
        "i - a particular object in inventory\n"
        "o - the type of an object in inventory\n"
        "f - the type of an object upon the floor\n"
        "d - the type of an object on discoveries list\n"
        "a - record an annotation for the current level\n"
        "(end)"
    )
    assert obsv["text_message"] == expected_message


def test_filter_map_travel(fake_nle_env):
    message = ["doorway      ", "", "      ------------ ", "      |..........| "]
    tty_chars = strs_to_2d(message, fill_value=32)
    fake_nle_env.reset.return_value["tty_chars"] = tty_chars
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    expected_message = "doorway"
    assert obsv["text_message"] == expected_message


def test_create_env_real(real_nethack_env):
    dut = NLELanguageWrapper(real_nethack_env)
    dut.reset()


def test_env_language_action_space(real_nethack_env):
    dut = NLELanguageWrapper(real_nethack_env, use_language_action=True)
    assert isinstance(dut.action_space, gym.spaces.Space)


def test_env_discrete_action_space(real_nethack_env):
    dut = NLELanguageWrapper(real_nethack_env, use_language_action=False)
    assert isinstance(dut.action_space, gym.spaces.Discrete)


def test_env_obsv_space(real_nethack_env):
    dut = NLELanguageWrapper(real_nethack_env)
    expected_observation_space_keys = [
        "text_glyphs",
        "text_message",
        "text_blstats",
        "text_inventory",
        "text_cursor",
    ]
    assert isinstance(dut.observation_space, gym.spaces.Dict)
    for key in expected_observation_space_keys:
        assert key in dut.observation_space.spaces
    for _, value in dut.observation_space.spaces.items():
        assert isinstance(value, gym.spaces.Space)


def test_step_real(real_nethack_env):
    dut = NLELanguageWrapper(
        real_nethack_env,
    )
    dut.reset()
    dut.step("northwest")


def test_step_invalid_action(real_nethack_env):
    dut = NLELanguageWrapper(real_nethack_env)
    dut.reset()
    with pytest.raises(
        ValueError, match="is not recognized or not supported for this environment"
    ):
        dut.step("invalid action")


def test_action_actions_maps_reflect_valid_actions(fake_nle_env):
    fake_nle_env._actions = [nethack_actions.CompassDirection.N]
    dut = NLELanguageWrapper(fake_nle_env)
    assert dut.action_enum_index_map == {nethack_actions.CompassDirection.N: 0}
    assert dut.action_str_enum_map == {
        "north": nethack_actions.CompassDirection.N,
        "k": nethack_actions.CompassDirection.N,
    }


def test_step_valid_action_not_supported(real_nethack_env):
    real_nethack_env._actions = [
        action
        for action in list(real_nethack_env._actions)
        if action != nethack_actions.Command.TRAVEL
    ]

    dut = NLELanguageWrapper(real_nethack_env)
    dut.reset()
    dut.env._actions = list(dut.env._actions)
    with pytest.raises(ValueError):
        dut.step("travel")


def test_obsv_fake(fake_nle_env):
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    expected_cursor = "Yourself a monk"
    expected_inventory = (
        "a: a blessed +1 quarterstaff (weapon in hands)\n"
        "b: an uncursed +0 cloak of magic resistance (being worn)"
    )
    expected_message = (
        "Hello Agent, welcome to NetHack!  You are a neutral gnomish Caveman."
    )
    expected_obsv = (
        "tame little dog far westsouthwest\n"
        "fountain near northnorthwest\n"
        "dark area very near north\n"
        "vertical closed door adjacent north\n"
        "dark area adjacent northeast, east, southeast, "
        "south, southwest, west, and northwest"
    )
    expected_text_blstats = (
        "Strength: 1/19\n"
        "Dexterity: 4\n"
        "Constitution: 5\n"
        "Intelligence: 6\n"
        "Wisdom: 7\n"
        "Charisma: 8\n"
        "Depth: 9\n"
        "Gold: 10\n"
        "HP: 11/12\n"
        "Energy: 1/13\n"
        "AC: 1\n"
        "XP: 7/10\n"
        "Time: 5\n"
        "Position: 66|14\n"
        "Hunger: Fainting\n"
        "Monster Level: 23\n"
        "Encumbrance: Stressed\n"
        "Dungeon Number: 21\n"
        "Level Number: 10\n"
        "Score: 123\n"
        "Alignment: Chaotic\n"
        "Condition: Stoned Slimed Food Poisoning"
    )

    assert obsv["text_glyphs"] == expected_obsv
    assert obsv["text_message"] == expected_message
    assert obsv["text_inventory"] == expected_inventory
    assert obsv["text_blstats"] == expected_text_blstats
    assert obsv["text_cursor"] == expected_cursor


def test_blstats_condition_none(fake_nle_env):

    # Set condition to None.
    fake_nle_env.reset.return_value["blstats"][25] = 0

    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()

    expected_condition = "Condition: None"

    assert expected_condition in obsv["text_blstats"]


def test_blstats_condition_flying(fake_nle_env):

    # Set condition to Flying.
    fake_nle_env.reset.return_value["blstats"][25] = 2048

    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()

    expected_condition = "Condition: Flying"

    assert expected_condition in obsv["text_blstats"]


def test_multiple_obsv_fake(fake_nethack_multiple_monsters_env):
    dut = NLELanguageWrapper(fake_nethack_multiple_monsters_env)
    obsv = dut.reset()
    expected_inventory = (
        "a: a blessed +1 quarterstaff (weapon in hands)\n"
        "b: an uncursed +0 cloak of magic resistance (being worn)"
    )
    expected_message = (
        "Hello Agent, welcome to NetHack!  You are a neutral gnomish Caveman."
    )
    expected_obsv = (
        "tame little dog very far west\n"
        "tame little dogs far westsouthwest\n"
        "fountains near northnorthwest\n"
        "dark area very near north\n"
        "vertical closed door adjacent north\n"
        "dark area adjacent northeast, east, "
        "southeast, south, southwest, west, and northwest"
    )
    assert obsv["text_glyphs"] == expected_obsv
    assert obsv["text_message"] == expected_message
    assert obsv["text_inventory"] == expected_inventory


def test_step_fake(fake_nle_env):
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    expected_inventory = (
        "a: a blessed +1 quarterstaff (weapon in hands)\n"
        "b: an uncursed +0 cloak of magic resistance (being worn)"
    )
    expected_message = (
        "Hello Agent, welcome to NetHack!  You are a neutral gnomish Caveman."
    )
    expected_obsv = (
        "tame little dog far westsouthwest\n"
        "fountain near northnorthwest\n"
        "dark area very near north\n"
        "vertical closed door adjacent north\n"
        "dark area adjacent northeast, east, "
        "southeast, south, southwest, west, and northwest"
    )
    obsv, reward, done, info = dut.step("north")
    assert obsv["text_glyphs"] == expected_obsv
    assert obsv["text_message"] == expected_message
    assert obsv["text_inventory"] == expected_inventory
    assert reward == 0.0
    assert not done
    assert info is None


def test_statue(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 5653  # kobold statue
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "kobold statue adjacent east"


def test_warning(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 5593  # unknown creature causing you alarm adjacent east
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "unknown creature causing you alarm adjacent east"


def test_swallow(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 5332  # swallow
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "swallow bottom right adjacent east"


def test_zap_beam(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 2528  # right slant beam
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "right slant zap beam adjacent east"


def test_explosion(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 2460  # explosion middle right
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "explosion middle right adjacent east"


def test_illegal_object(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 1906  # strange object
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "strange object adjacent east"


def test_weapon(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 1917  # elven spear
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "elven spear adjacent east"


def test_armour(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 1988  # gray dragon scale mail
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "gray dragon scale mail adjacent east"


def test_ring(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 2068  # sapphire ring
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "sapphire ring adjacent east"


def test_amulet(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 2091  # hexagonal amulet
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "hexagonal amulet adjacent east"


def test_tool(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 2123  # magic marker
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "magic marker adjacent east"


def test_food(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 2163  # carrot
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "carrot adjacent east"


def test_potion(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 2187  # magenta potion
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "magenta potion adjacent east"


def test_scroll(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 2206  # scroll labeled NR 9
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "scroll labeled NR 9 adjacent east"


def test_spellbook(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 2250  # mottled spellbook
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "mottled spellbook adjacent east"


def test_wand(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 2291  # crystal wand
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "crystal wand adjacent east"


def test_coin(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 2316  # gold piece
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "gold piece adjacent east"


def test_gem(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 2333  # violet amethyst
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "violet amethyst adjacent east"


def test_rock(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 2353  # boulder
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "boulder adjacent east"


def test_ball(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 2355  # heavy iron ball
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "heavy iron ball adjacent east"


def test_chain(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 2356  # iron chain
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "iron chain adjacent east"


def test_venom(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 2358  # splash of acid venom
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "splash of acid venom adjacent east"


def test_ridden(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 1611  # ridden mastodon
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "ridden mastodon adjacent east"


def test_corpse(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 1226  # leocrotta corpse
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "leocrotta corpse adjacent east"


def test_invisible(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 762  # invisible creature
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "invisible creature adjacent east"


def test_detected(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 917  # detected water elemental
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "detected water elemental adjacent east"


def test_tame(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 613  # tame yeti
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "tame yeti adjacent east"


def test_monster(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 67] = 255  # iron golem
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "iron golem adjacent east"


def test_plural_end_ey(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 72] = 229  # monkey 1'
    glyphs[14, 73] = 229  # monkey 2
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "monkeys far east"


def test_plural_end_y(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 72] = 99  # pony 1'
    glyphs[14, 73] = 99  # pony 2
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "ponies far east"


def test_plural_default(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 72] = 341  # wizard 1'
    glyphs[14, 73] = 341  # wizard 2
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "wizards far east"


def test_plural_end_s(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 72] = 335  # priestess 1'
    glyphs[14, 73] = 335  # priestess 2
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "priestesses far east"


def test_plural_end_f(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 72] = 260  # elf 1'
    glyphs[14, 73] = 260  # elf 2
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "elves far east"


def test_plural_end_ff(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 72] = 1967  # quarterstaff 1'
    glyphs[14, 73] = 1967  # quarterstaff 2
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "quarterstaves far east"


def test_plural_lava(fake_nle_env):
    glyphs = np.full((21, 79), 2378)  # Room floor
    glyphs[14, 72] = 2393  # lava 1
    glyphs[14, 73] = 2393  # lava 2
    fake_nle_env.reset.return_value["glyphs"] = glyphs
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_glyphs"] == "area of lava far east"


def test_wrapper_only_works_with_nle_envs():
    with pytest.raises(AssertionError, match=r"Only NLE environments are supported"):
        NLELanguageWrapper(gym.make("CartPole-v0"))


def test_wrapper_requires_all_keys(real_nethack_env):
    real_nethack_env.observation_space.spaces.pop("glyphs")
    with pytest.raises(
        AssertionError,
        match=r"NLE environment missing required obsv key\(s\): {'glyphs'}",
    ):
        NLELanguageWrapper(real_nethack_env)


def test_play(mocker):
    with mocker.patch("builtins.input", return_value="north"):
        play.main("NetHackChallenge-v0")


def test_time_reset(real_nethack_env):
    dut = NLELanguageWrapper(real_nethack_env)
    baseline_runtime = min(timeit.repeat(real_nethack_env.reset, number=100, repeat=10))
    runtime = min(timeit.repeat(dut.reset, number=100, repeat=10))
    relative_slowdown = runtime / baseline_runtime
    # Resetting takes a lot more time than stepping so the overhead is a lot less.
    assert relative_slowdown < 1.2


def test_time_step(real_nethack_env):
    wait_action = 18
    dut = NLELanguageWrapper(real_nethack_env)
    dut.reset()
    baseline_runtime = min(
        timeit.repeat(lambda: real_nethack_env.step(wait_action), number=100, repeat=10)
    )
    runtime = min(timeit.repeat(lambda: dut.step("wait"), number=100, repeat=10))
    relative_slowdown = runtime / baseline_runtime
    assert relative_slowdown < 3.2
