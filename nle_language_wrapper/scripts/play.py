import gym
import minihack  # pylint: disable=unused-import
import nle  # pylint: disable=unused-import

from nle_language_wrapper import NLELanguageWrapper


def main(nethack_env_name):
    """
    Play a NLE based environment using the nle-language-wrapper.
    """
    nle_env = gym.make(
        nethack_env_name,
        observation_keys=[
            "glyphs",
            "blstats",
            "tty_chars",
            "inv_letters",
            "inv_strs",
            "tty_cursor",
        ],
    )
    env = NLELanguageWrapper(nle_env)
    obsv = env.reset()
    total_reward = 0.0

    while True:
        output = ""
        output += f"Inventory:\n{obsv['text_inventory']}\n\n"
        output += f"Stats:\n{obsv['text_blstats']}\n\n"
        output += f"Cursor:{obsv['text_cursor']}\n\n"
        output += f"Observation:\n{obsv['text_glyphs']}\n\n"
        output += f"Message:\n{obsv['text_message']}\n\n"
        print(output)
        print("------")
        valid_action = False
        while not valid_action:
            action = input(" ")
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
    nle_env_names = [
        env_spec.id for env_spec in gym.envs.registry.all() if "MiniHack" in env_spec.id
    ]
    nle_env_names.append("NetHackChallenge-v0")
    for i, env_name in enumerate(nle_env_names):
        print(f"{i}: {env_name}")
    selected_name = int(
        input(f"Which base env would you like to use [0-{len(nle_env_names) - 1}]? ")
    )
    nle_env_name = nle_env_names[selected_name]
    rollout = main(nle_env_name)
    rollout["nle_env_name"] = nle_env_name
    print(sum(rollout["nle_reward"]))
