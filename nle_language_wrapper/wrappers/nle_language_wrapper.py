from gym import Wrapper
from gym import spaces
from nle.env import NLE
from nle.nethack import actions as nethack_actions

from nle_language_wrapper.nle_language_obsv import NLELanguageObsv


class NLELanguageWrapper(Wrapper):
    @property
    def spec(self):
        return self.env.spec

    all_nle_action_map = {
        nethack_actions.UnsafeActions.HELP: ["help", "?"],
        nethack_actions.UnsafeActions.PREVMSG: ["previous message", "^p"],
        nethack_actions.CompassDirection.N: ["north", "k"],
        nethack_actions.CompassDirection.E: ["east", "l"],
        nethack_actions.CompassDirection.S: ["south", "j"],
        nethack_actions.CompassDirection.W: ["west", "h"],
        nethack_actions.CompassIntercardinalDirection.NE: ["northeast", "u"],
        nethack_actions.CompassIntercardinalDirection.SE: ["southeast", "n"],
        nethack_actions.CompassIntercardinalDirection.SW: ["southwest", "b"],
        nethack_actions.CompassIntercardinalDirection.NW: ["northwest", "y"],
        nethack_actions.CompassCardinalDirectionLonger.N: ["far north", "K"],
        nethack_actions.CompassCardinalDirectionLonger.E: ["far east", "L"],
        nethack_actions.CompassCardinalDirectionLonger.S: ["far south", "J"],
        nethack_actions.CompassCardinalDirectionLonger.W: ["far west", "H"],
        nethack_actions.CompassIntercardinalDirectionLonger.NE: ["far northeast", "U"],
        nethack_actions.CompassIntercardinalDirectionLonger.SE: ["far southeast", "N"],
        nethack_actions.CompassIntercardinalDirectionLonger.SW: ["far southwest", "B"],
        nethack_actions.CompassIntercardinalDirectionLonger.NW: ["far northwest", "Y"],
        nethack_actions.MiscDirection.UP: ["up", "<"],
        nethack_actions.MiscDirection.DOWN: ["down", ">"],
        nethack_actions.MiscDirection.WAIT: ["wait", "."],
        nethack_actions.MiscAction.MORE: ["more", "\r", r"\r"],
        nethack_actions.Command.EXTCMD: ["extcmd", "#"],
        nethack_actions.Command.EXTLIST: ["extlist", "M-?"],
        nethack_actions.Command.ADJUST: ["adjust", "M-a"],
        nethack_actions.Command.ANNOTATE: ["annotate", "M-A"],
        nethack_actions.Command.APPLY: ["apply", "a"],
        nethack_actions.Command.ATTRIBUTES: ["attributes", "^x"],
        nethack_actions.Command.AUTOPICKUP: ["autopickup", "@"],
        nethack_actions.Command.CALL: ["call", "C"],
        nethack_actions.Command.CAST: ["cast", "Z"],
        nethack_actions.Command.CHAT: ["chat", "M-c"],
        nethack_actions.Command.CLOSE: ["close", "c"],
        nethack_actions.Command.CONDUCT: ["conduct", "M-C"],
        nethack_actions.Command.DIP: ["dip", "M-d"],
        nethack_actions.Command.DROP: ["drop", "d"],
        nethack_actions.Command.DROPTYPE: ["droptype", "D"],
        nethack_actions.Command.EAT: ["eat", "e"],
        nethack_actions.Command.ESC: ["esc", "^["],
        nethack_actions.Command.ENGRAVE: ["engrave", "E"],
        nethack_actions.Command.ENHANCE: ["enhance", "M-e"],
        nethack_actions.Command.FIRE: ["fire", "f"],
        nethack_actions.Command.FIGHT: ["fight", "F"],
        nethack_actions.Command.FORCE: ["force", "M-f"],
        nethack_actions.Command.GLANCE: ["glance", ";"],
        nethack_actions.Command.HISTORY: ["history", "V"],
        nethack_actions.Command.INVENTORY: ["inventory", "i"],
        nethack_actions.Command.INVENTTYPE: ["inventtype", "I"],
        nethack_actions.Command.INVOKE: ["invoke", "M-i"],
        nethack_actions.Command.JUMP: ["jump", "M-j"],
        nethack_actions.Command.KICK: ["kick", "^d"],
        nethack_actions.Command.KNOWN: ["known", "\\"],
        nethack_actions.Command.KNOWNCLASS: ["knownclass", "`"],
        nethack_actions.Command.LOOK: ["look", ":"],
        nethack_actions.Command.LOOT: ["loot", "M-l"],
        nethack_actions.Command.MONSTER: ["monster", "M-m"],
        nethack_actions.Command.MOVE: ["move", "m"],
        nethack_actions.Command.MOVEFAR: ["movefar", "M"],
        nethack_actions.Command.OFFER: ["offer", "M-o"],
        nethack_actions.Command.OPEN: ["open", "o"],
        nethack_actions.Command.OPTIONS: ["options", "O"],
        nethack_actions.Command.OVERVIEW: ["overview", "^o"],
        nethack_actions.Command.PAY: ["pay", "p"],
        nethack_actions.Command.PICKUP: ["pickup", ","],
        nethack_actions.Command.PRAY: ["pray", "M-p"],
        nethack_actions.Command.PUTON: ["puton", "P"],
        nethack_actions.Command.QUAFF: ["quaff", "q"],
        nethack_actions.Command.QUIT: ["quit", "M-q"],
        nethack_actions.Command.QUIVER: ["quiver", "Q"],
        nethack_actions.Command.READ: ["read", "r"],
        nethack_actions.Command.REDRAW: ["redraw", "^r"],
        nethack_actions.Command.REMOVE: ["remove", "R"],
        nethack_actions.Command.RIDE: ["ride", "M-R"],
        nethack_actions.Command.RUB: ["rub", "M-r"],
        nethack_actions.Command.RUSH: ["rush", "g"],
        nethack_actions.Command.RUSH2: ["rush2", "G"],
        nethack_actions.Command.SAVE: ["save", "S"],
        nethack_actions.Command.SEARCH: ["search", "s"],
        nethack_actions.Command.SEEALL: ["seeall", "*"],
        nethack_actions.Command.SEEAMULET: ["seeamulet", '"'],
        nethack_actions.Command.SEEARMOR: ["seearmor", "["],
        nethack_actions.Command.SEEGOLD: ["seegold", "dollar", "$"],
        nethack_actions.Command.SEERINGS: ["seerings", "="],
        nethack_actions.Command.SEESPELLS: ["seespells", "plus", "+"],
        nethack_actions.Command.SEETOOLS: ["seetools", "("],
        nethack_actions.Command.SEETRAP: ["seetrap", "^"],
        nethack_actions.Command.SEEWEAPON: ["seeweapon", ")"],
        nethack_actions.Command.SHELL: ["shell", "!"],
        nethack_actions.Command.SIT: ["sit", "M-s"],
        nethack_actions.Command.SWAP: ["swap", "x"],
        nethack_actions.Command.TAKEOFF: ["takeoff", "T"],
        nethack_actions.Command.TAKEOFFALL: ["takeoffall", "A"],
        nethack_actions.Command.TELEPORT: ["teleport", "^t"],
        nethack_actions.Command.THROW: ["throw", "t"],
        nethack_actions.Command.TIP: ["tip", "M-T"],
        nethack_actions.Command.TRAVEL: ["travel", "_"],
        nethack_actions.Command.TURN: ["turnundead", "M-t"],
        nethack_actions.Command.TWOWEAPON: ["twoweapon", "X"],
        nethack_actions.Command.UNTRAP: ["untrap", "M-u"],
        nethack_actions.Command.VERSION: ["version", "M-v"],
        nethack_actions.Command.VERSIONSHORT: ["versionshort", "v"],
        nethack_actions.Command.WEAR: ["wear", "W"],
        nethack_actions.Command.WHATDOES: ["whatdoes", "&"],
        nethack_actions.Command.WHATIS: ["whatis", "/"],
        nethack_actions.Command.WIELD: ["wield", "w"],
        nethack_actions.Command.WIPE: ["wipe", "M-w"],
        nethack_actions.Command.ZAP: ["zap", "z"],
        nethack_actions.TextCharacters.MINUS: ["minus", "-"],
        nethack_actions.TextCharacters.SPACE: ["space", " "],
        nethack_actions.TextCharacters.APOS: ["apos", "'"],
        nethack_actions.TextCharacters.NUM_0: ["zero", "0"],
        nethack_actions.TextCharacters.NUM_1: ["one", "1"],
        nethack_actions.TextCharacters.NUM_2: ["two", "2"],
        nethack_actions.TextCharacters.NUM_3: ["three", "3"],
        nethack_actions.TextCharacters.NUM_4: ["four", "4"],
        nethack_actions.TextCharacters.NUM_5: ["five", "5"],
        nethack_actions.TextCharacters.NUM_6: ["six", "6"],
        nethack_actions.TextCharacters.NUM_7: ["seven", "7"],
        nethack_actions.TextCharacters.NUM_8: ["eight", "8"],
        nethack_actions.TextCharacters.NUM_9: ["nine", "9"],
        nethack_actions.WizardCommand.WIZDETECT: ["wizard detect", "^e"],
        nethack_actions.WizardCommand.WIZGENESIS: ["wizard genesis", "^g"],
        nethack_actions.WizardCommand.WIZIDENTIFY: ["wizard identify", "^i"],
        nethack_actions.WizardCommand.WIZLEVELPORT: ["wizard teleport", "^v"],
        nethack_actions.WizardCommand.WIZMAP: ["wizard map", "^f"],
        nethack_actions.WizardCommand.WIZWHERE: ["wizard where", "^o"],
        nethack_actions.WizardCommand.WIZWISH: ["wizard wish", "^w"],
    }

    REQUIRED_NLE_OBSV_KEYS = {
        "glyphs",
        "blstats",
        "tty_cursor",
        "inv_strs",
        "inv_letters",
        "tty_chars",
    }

    def step(self, action):
        if self.use_language_action:
            action = self.pre_step(action)
        nle_obsv, reward, done, info = self.env.step(action)
        return self.post_step(nle_obsv), reward, done, info

    def pre_step(self, action: str):
        """Translate language action to nle action.
        Args:
            action (str): language/text action
        Returns:
            (Enum): nle action
        """
        if action not in self.action_str_enum_map:
            raise ValueError(
                f"Action {repr(action)} is not recognized "
                "or not supported for this environment"
            )
        nle_action_enum = self.action_str_enum_map[action]
        nle_action_idx = self.action_enum_index_map[nle_action_enum]
        return nle_action_idx

    def nle_obsv_to_language(self, nle_obsv):
        """Translate NLE Observation into a language observation.
        Args:
            nle_obsv (dict): NLE observation from the base environment
        Returns:
            (dict): language observation
        """
        glyphs = nle_obsv["glyphs"]
        blstats = nle_obsv["blstats"]
        tty_cursor = nle_obsv["tty_cursor"]
        inv_strs = nle_obsv["inv_strs"]
        inv_letters = nle_obsv["inv_letters"]
        tty_chars = nle_obsv["tty_chars"]
        return {
            "text_glyphs": self.nle_language.text_glyphs(glyphs, blstats).decode(
                "latin-1"
            ),
            "text_message": self.nle_language.text_message(tty_chars).decode("latin-1"),
            "text_blstats": self.nle_language.text_blstats(blstats).decode("latin-1"),
            "text_inventory": self.nle_language.text_inventory(
                inv_strs, inv_letters
            ).decode("latin-1"),
            "text_cursor": self.nle_language.text_cursor(
                glyphs, blstats, tty_cursor
            ).decode("latin-1"),
        }

    def post_step(self, nle_obsv):
        """Post step operations. Used for translating the observation
        Args:
            nle_obsv (dict): nle observation from base environment
        Returns:
            (dict): language observation
        """
        return self.nle_obsv_to_language(nle_obsv)

    def reset(self, **kwargs):
        self.pre_reset()
        obsv = self.env.reset(**kwargs)
        return self.post_reset(obsv)

    def pre_reset(self):
        """Pre reset operations."""

    def post_reset(self, obsv):
        """Post reset operations.  Translate the NLE observation into language version
        Args:
            nle_obsv (dict): nle observation from base environment
        Returns:
            (dict): language observation
        """
        return self.nle_obsv_to_language(obsv)

    def __init__(self, env, use_language_action=True):
        """Initialize the wrapper
        Args:
            env (nle.env.NLE): NLE based environment to be wrapped
            use_language_action(bool): Use language action or discrete integer actions
        """
        super().__init__(env)
        assert isinstance(env, NLE), "Only NLE environments are supported"
        missing_obsv_keys = self.REQUIRED_NLE_OBSV_KEYS.difference(
            env.observation_space.spaces.keys()
        )
        assert (
            len(missing_obsv_keys) == 0
        ), f"NLE environment missing required obsv key(s): {missing_obsv_keys}"
        # assert observations are included
        self.use_language_action = use_language_action
        self.nle_language = NLELanguageObsv()

        # Build map for action string to NLE Action Enum
        self.action_str_enum_map = {}
        for nle_action_enum, action_strs in self.all_nle_action_map.items():
            if nle_action_enum in self.env._actions:
                for action_str in action_strs:
                    self.action_str_enum_map[action_str] = nle_action_enum

        # Build map for NLE Action Enum to NLE action index
        self.action_enum_index_map = {}
        for nle_action_enum, _ in self.all_nle_action_map.items():
            if nle_action_enum in self.env._actions:
                self.action_enum_index_map[nle_action_enum] = self.env._actions.index(
                    nle_action_enum
                )

        if self.use_language_action:
            self.action_space = spaces.Space()
        self.observation_space = spaces.Dict(
            {
                "text_glyphs": spaces.Space(),
                "text_message": spaces.Space(),
                "text_blstats": spaces.Space(),
                "text_inventory": spaces.Space(),
                "text_cursor": spaces.Space(),
            }
        )
