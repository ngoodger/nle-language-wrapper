import gym
import minihack  # pylint: disable=unused-import
import nle  # pylint: disable=unused-import

from nle_language_wrapper import NLELanguageWrapper


def main(nethack_env_name):
    """
    Play a NLE based environment using the nle-language-wrapper.
    """
    env = NLELanguageWrapper(
        gym.make(
            nethack_env_name,
            observation_keys=[
                "glyphs",
                "blstats",
                "tty_chars",
                "inv_letters",
                "inv_strs",
                "tty_cursor",
                "tty_colors",
            ],
        )
    )
    obsv = env.reset()
    total_reward = 0.0
    shown_help = False

    while True:
        output = ""
        output += f"Inventory:\n{obsv['text_inventory']}\n\n"
        output += f"Stats:\n{obsv['text_blstats']}\n\n"
        output += f"Cursor:{obsv['text_cursor']}\n\n"
        output += f"Observation:\n{obsv['text_glyphs']}\n\n"
        output += f"Message:\n{obsv['text_message']}"
        if output[-1] != "\n":
            output += "\n"
        print(output)
        print("------")
        valid_action = False
        while not valid_action:
            if not shown_help:
                print(
                    'Type "instructions" anytime to see '
                    "the instructions on how to play"
                )
                print(
                    'Type "actions" anytime to see valid actions '
                    "for the current environment"
                )
                print('Type "render" anytime to render the nle environment')
                shown_help = True
            action = input("Action: ")
            if action == "actions":
                print("")
                print("Actions")
                max_key_len = max(
                    len(repr(k)) for k, _ in env.action_str_enum_map.items()
                )
                for action_str, nle_action_enum in env.action_str_enum_map.items():
                    key_str = f"{repr(action_str)}"
                    print(
                        key_str
                        + (max_key_len - len(key_str)) * " "
                        + f":{str(nle_action_enum)}"
                    )
                print("")
                continue
            if action == "instructions":
                print("")
                print("Instructions")
                print(
                    "To play, write a text action at the prompt, "
                    'e.g "north" will move you north.'
                )
                print(
                    "For the complete list of actions supported "
                    'in the current environment type "actions"'
                )
                print('To render the current display type "render"')
                print("")
                continue
            if action == ("render"):
                env.render()
                continue
            try:
                (
                    obsv,
                    reward,
                    done,
                    _,
                ) = env.step(action)
                total_reward += reward
                if done:
                    return total_reward
                valid_action = True
            except ValueError as exception:
                print(exception)
    return total_reward


if __name__ == "__main__":
    while True:
        nle_env_names = [
            env_spec.id
            for env_spec in gym.envs.registry.all()
            if "MiniHack" in env_spec.id
        ]
        nle_env_names.append("NetHackChallenge-v0")
        for i, env_name in enumerate(nle_env_names):
            print(f"{i}: {env_name}")
        selected_name = int(
            input(
                f"Which base env would you like to use [0-{len(nle_env_names) - 1}]? "
            )
        )
        nle_env_name = nle_env_names[selected_name]
        total_reward = main(nle_env_name)
        print("Done!")
        print(f"Total Reward: {total_reward}")
        if input("Play again? [y,n]:") != "y":
            break
