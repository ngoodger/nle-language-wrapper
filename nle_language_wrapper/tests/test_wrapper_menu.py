from nle_language_wrapper import NLELanguageWrapper
from nle_language_wrapper.tests.test_utils import strs_to_2d


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
        "a - Hide commands that don't autocomplete (those not marked with [A])\n"
        ": - Search extended commands\n"
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


def test_empty_tty_chars_returns_empty_message(fake_nle_env):
    message = [" "]
    tty_chars = strs_to_2d(message, fill_value=32)
    fake_nle_env.reset.return_value["tty_chars"] = tty_chars
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_message"] == ""


def test_death_message(fake_nle_env):
    message = [
        "" + "No  Points     Name                 Hp [max] \n"
        "\n"
        "0  Agent-Cav-Hum-Mal-Law died in The Dungeons of Doom on            \n"
        "\n"
        "level 1.  Burned by molten lava.                        -  [16]"
    ]
    tty_chars = strs_to_2d(message, fill_value=32)
    fake_nle_env.reset.return_value["tty_chars"] = tty_chars
    dut = NLELanguageWrapper(fake_nle_env)
    obsv = dut.reset()
    assert obsv["text_message"] == (
        "No  Points     Name                 Hp [max] \n\n"
        "0  Agent-Cav-Hum-Mal-Law died in The Dungeons of Doom on            \n\n"
        "level 1.  Burned by molten lava.                        -  [16]"
    )


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
