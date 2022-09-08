[![PyPI](https://img.shields.io/pypi/v/nle-language-wrapper.svg)](https://pypi.org/project/nle-language-wrapper)
[![codecov](https://codecov.io/gh/ngoodger/nle-language-wrapper/branch/main/graph/badge.svg)](https://codecov.io/gh/ngoodger/nle-language-wrapper)
[![Downloads](https://static.pepy.tech/personalized-badge/nle-language-wrapper?period=total&units=abbreviation&left_color=grey&right_color=green&left_text=Downloads%20Total)](https://pepy.tech/project/nle-language-wrapper)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)


# Nethack Learning Environment Language Wrapper 

Language Wrapper for the [Nethack Learning Environment (NLE)](https://github.com/facebookresearch/nle) and [MiniHack](https://github.com/facebookresearch/minihack)

![Diagram](media/diagram.png?raw=true)

## Description
This wrapper inherits from the [Gym Wrapper](https://github.com/openai/gym/blob/9e66399b4ef04c1534c003641802e2ac1363e8a6/gym/core.py#L286-L421) Class and translates the non-language observations from [NLE](https://github.com/facebookresearch/nle) tasks into similar language representations.  Actions can also be optionally provided in text form which are converted to the Discrete actions of the NLE.

```
Inventory:
a: a blessed +1 mace (weapon in hand)
b: a +0 robe (being worn)
c: a blessed +0 small shield (being worn)
d: 4 potions of holy water
e: a clove of garlic
f: a sprig of wolfsbane
g: a spellbook of stone to flesh
h: a spellbook of identify

Stats:
Strength:15/15
Dexterity:10
Constitution:12
Intelligence:12
Wisdom:18
Charisma:9
Depth:1
Gold:0
HP:14/14
Energy:6/6
AC:7
XP:1/0
Time:1
Position:46|14
Hunger:Not Hungry
Monster Level:0
Encumbrance:Unemcumbered
Dungeon Number:0
Level Number:1
Score:0
Alignment:Neutral
Condition:None

Cursor:Yourself a priestess

Observation:
vertical closed door far westnorthwest
horizontal wall near north and northwest
vertical wall very near northeast and east
vertical closed door very near eastnortheast
southeast corner very near southeast
horizontal wall very near south and southwest
tame kitten adjacent northeast

Message:
Hello Agent, welcome to NetHack!  You are a neutral human Priestess.
```

### Observations
The environment converts the NLE observations: `glyphs`, `blstats`, `tty_chars`, `inv_letters`, `inv_strs` and `tty_cursor` to text equivalents.

- `text_glyphs`: A compressed textual representation of the surroundings.
```
dark area far west
vertical wall near east and southeast
horizontal wall near south and southwest
horizontal closed door near southsouthwest
black onyx ring near westsouthwest
doorway near west
egg very near east
horizontal wall adjacent north, northeast, and northwest
tame little dog adjacent southwest
```
Corresponding to the following visual display
```
---------
.....@.%|
|...d...|
|.......|
|=......|
----+----
```
- `text_message`: Current message.  Same as `message` from NLE however also includes menus when present.
```
Aloha Agent, welcome to NetHack!  You are a neutral female human Tourist.
```
- `text_blstats`: Text version of the bottom-line stats and auxiliary stats include with NLE.
```
Strength:11/11
Dexterity:12
Constitution:14
Intelligence:16
Wisdom:9
Charisma:14
Depth:1
Gold:241
HP:10/10
Energy:2/2
AC:10
XP:1/0
Time:1
Position:48|2
Hunger:Not Hungry
Monster Level:0
Encumbrance:Unemcumbered
Dungeon Number:0
Level Number:1
Score:0
Alignment:Neutral
Condition:None
```
- `text_inventory`: Current inventory with letters.
```
$: 241 gold pieces
a: 22 +2 darts (at the ready)
b: 6 uncursed food rations
c: 3 uncursed tripe rations
d: an uncursed egg
e: 2 uncursed fortune cookies
f: 2 uncursed potions of extra healing
g: 2 uncursed scrolls of magic mapping
h: 2 blessed scrolls of magic mapping
i: an uncursed +0 Hawaiian shirt (being worn)
j: an expensive camera (0:68)
k: an uncursed credit card
```
- `text_cursor`: Description of glyph currently under cursor.
```
Yourself a tourist
```

### Actions
Actions are by default text actions like `wait`, `apply`, `north` ect.  The corresponding key-presses are supported as well, e.g. `west` is the same as `h` and `kick` is the same as `^d`. Alternatively the standard discrete action space from NLE can be used by passing `use_language_action=False` to the wrapper.

## Getting Started

### Supported platforms
The wrapper is tested on macOS 12.5 and Ubuntu 20.04.

### Requirements 

Requires `python>=3.7` and `cmake>=3.15`.

 To install 

 CMake can be installed on macos using homebrew
 ```
 brew install cmake
 ```
 Alternatively, and for other platforms follow the instructions at https://cmake.org/install/

On Ubuntu you may also require additional dependencies, follow the steps at https://github.com/facebookresearch/nle#installation.

### Installation

To use the environment you can install it directly from PyPI.
```
pip install nle-language-wrapper
```

### Google Colab
The wrapper can be installed in Google Colab after installing the following dependencies
```
!sudo apt-get install -y build-essential autoconf libtool pkg-config \
    python3-dev python3-pip python3-numpy git libncurses5-dev \
    libzmq3-dev flex bison
!git clone https://github.com/google/flatbuffers.git
!cd flatbuffers && cmake -G "Unix Makefiles" && make -j2 && sudo make install
!pip install cmake==3.15.3
```

For an example Google Colab notebook, see [NLE-Language-Wrapper-Example.ipynb](https://colab.research.google.com/drive/1xwjPu9UbCCHNM6ezLw86kjw67KXswt_O#scrollTo=WJYfMxSeADnB)

### Development

For development on the wrapper clone the repository and install it in development mode.
```
git clone https://github.com/ngoodger/nle-language-wrapper --recursive
pip install -e ".[dev]"
```
To update the library with changes to the C++ code recompile by running
```
python -m setup develop
```

## Usage

The wrapper can be used simply by instantiating a base environment from [NLE](https://github.com/facebookresearch/nle) or [MiniHack](https://github.com/facebookresearch/minihack) and passing it to the wrapper constructor.
```
import gym
import nle
from nle_language_wrapper import NLELanguageWrapper
env = NLELanguageWrapper(gym.make("NetHackChallenge-v0"))
obsv = env.reset()
obsv, reward, done, info = env.step("wait")
```

Alternatively to utilize the discrete actions rather than language actions specify `use-text-action=True`.
```
env = NLELanguageWrapper(gym.make("NetHackChallenge-v0"),  use_language_action=text)
obsv = env.reset()
wait_action = 17
obsv, reward, done, info = env.step(wait_action)
```

## Manual play
A script is provided select an NLE or MiniHack task and directly interact with an environment.
```
python -m nle_language_wrapper.scripts.play
```

## Agent

An included [Sample Factory](https://github.com/alex-petrenko/sample-factory) based agent achieves 730 reward after 700M frames.  This agent uses a small transformer model to encode the language observations for the policy and value function models.  The algorithm used is Asynchronous Proximal Policy Optimization (APPO) described in [Sample Factory: Egocentric 3D Control from Pixels at 100000 FPS with Asynchronous Reinforcement Learning](https://arxiv.org/abs/2006.11751v2).

![Reward Curves](media/reward_curves.png?raw=true)

### Hardware Requirements
The default configuration was tested on an Nvidia 3090 with 24Gbyte RAM and a Ryzen 1700 CPU. Training runs at approximately 4k/FPS.  To train on a GPU with less RAM a smaller model could be configured, or a smaller max token length, or batch size could be used.  These parameters can be passed when running the training script `nle_language_wrapper/agents/sample_factory/train.py`, e.g.
```
    --transformer_hidden_size 64
    --transformer_hidden_layers 2
    --transformer_attention_heads 2
    --max_token_length 256
    --batch_size 1024
```

### Running the agent
The pre-trained agent checkpoints are included in the `train_dir`.  Clone the repository and run the following script to test it.
```
python nle_language_wrapper/agents/sample_factory/enjoy.py \
--env nle_language_env \
--encoder_custom nle_language_transformer_encoder \
--experiment nle_language_agent \
--algo APPO \
--fps 1
```

### Training the agent
To train a new agent simply run the following script and the set the experiment name to the desired value.
```
python nle_language_wrapper/agents/sample_factory/train.py \
--env nle_language_env \
--encoder_custom nle_language_transformer_encoder \
--experiment nle_language_agent_1 \
--algo APPO \
--batch_size 2048 \
--num_envs_per_worker 24 \
--num_workers 8 \
--reward_scale 0.1
```

## Licence
MIT License

