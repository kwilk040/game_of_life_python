import re
from abc import ABC
from enum import Enum

from cell import CellState

type _BirthSurvival = tuple[list[int], list[int]]


class Rule(Enum):
    CONWAYS_LIFE = 0
    DAY_AND_NIGHT = 1
    MAZE = 2
    ICEBALLS = 3
    LIFE_WITHOUT_DEATH = 4
    SEEDS = 5
    H_TREES = 6
    SERVIETTES = 7
    BACTERIA = 8
    PEDESTRIAN_LIFE = 9
    PULSAR_LIFE = 10
    CUSTOM = 11

    def next(self):
        next_value: int = self.value + 1
        if next_value > 10:
            next_value = 0
        return Rule(next_value)

    def previous(self):
        previous_value: int = self.value - 1
        if previous_value < 0:
            previous_value = 10
        return Rule(previous_value)


class Ruleset(ABC):
    def __init__(self, birth_survival: _BirthSurvival, rulestring: str, rule: Rule):
        self.birth = birth_survival[0]
        self.survival = birth_survival[1]
        self.rulestring = rulestring
        self.rule = rule

    def apply(self, cell_state: CellState, neighbours: int) -> CellState:
        return (
            self.__apply_ruleset_for_alive_cell(neighbours)
            if cell_state == CellState.ALIVE
            else self.__apply_ruleset_for_dead_cell(neighbours)
        )

    def get_rule(self):
        return self.rule

    def get_name(self):
        return self.__class__.__name__.replace("Ruleset", "")

    def get_rulestring(self):
        return self.rulestring

    def __apply_ruleset_for_alive_cell(self, neighbours: int) -> CellState:
        return (
            CellState.ALIVE
            if self.survival.__contains__(neighbours)
            else CellState.DEAD
        )

    def __apply_ruleset_for_dead_cell(self, neighbours: int) -> CellState:
        return (
            CellState.ALIVE if self.birth.__contains__(neighbours) else CellState.DEAD
        )


class ConwaysLifeRuleset(Ruleset):
    def __init__(self):
        rulestring: str = "B3/S23"
        super().__init__(_Utils.convert_rulestring_to_birth_survival(rulestring), rulestring, Rule.CONWAYS_LIFE)


class DayAndNightRuleset(Ruleset):
    def __init__(self):
        rulestring: str = "B3678/S34678"
        super().__init__(_Utils.convert_rulestring_to_birth_survival(rulestring), rulestring,
                         Rule.DAY_AND_NIGHT)


class MazeRuleset(Ruleset):
    def __init__(self):
        rulestring: str = "B3/S12345"
        super().__init__(_Utils.convert_rulestring_to_birth_survival(rulestring), rulestring, Rule.MAZE)


class IceballsRuleset(Ruleset):
    def __init__(self):
        rulestring: str = "B25678/S5678"
        super().__init__(_Utils.convert_rulestring_to_birth_survival(rulestring), rulestring, Rule.ICEBALLS)


class LifeWithoutDeathRuleset(Ruleset):
    def __init__(self):
        rulestring: str = "B3/S012345678"
        super().__init__(_Utils.convert_rulestring_to_birth_survival(rulestring), rulestring, Rule.LIFE_WITHOUT_DEATH)


class SeedsRuleset(Ruleset):
    def __init__(self):
        rulestring: str = "B2/S"
        super().__init__(_Utils.convert_rulestring_to_birth_survival(rulestring), rulestring, Rule.SEEDS)


class HTreesRuleset(Ruleset):
    def __init__(self):
        rulestring: str = "B1/S012345678"
        super().__init__(_Utils.convert_rulestring_to_birth_survival(rulestring), rulestring, Rule.H_TREES)


class ServiettesRuleset(Ruleset):
    def __init__(self):
        rulestring: str = "B234/S"
        super().__init__(_Utils.convert_rulestring_to_birth_survival(rulestring), rulestring, Rule.SERVIETTES)


class BacteriaRuleset(Ruleset):
    def __init__(self):
        rulestring: str = "B34/S456"
        super().__init__(_Utils.convert_rulestring_to_birth_survival(rulestring), rulestring, Rule.BACTERIA)


class PedestrianLifeRuleset(Ruleset):
    def __init__(self):
        rulestring: str = "B38/S23"
        super().__init__(_Utils.convert_rulestring_to_birth_survival(rulestring), rulestring, Rule.PEDESTRIAN_LIFE)


class PulsarLifeRuleset(Ruleset):
    def __init__(self):
        rulestring: str = "B3/S238"
        super().__init__(_Utils.convert_rulestring_to_birth_survival(rulestring), rulestring, Rule.PULSAR_LIFE)


class CustomRuleset(Ruleset):
    def __init__(self, rulestring: str):
        super().__init__(_Utils.convert_rulestring_to_birth_survival(rulestring), rulestring, Rule.CUSTOM)


class RulesetFactory:
    @staticmethod
    def get_ruleset(rule: Rule) -> Ruleset:

        match rule:
            case Rule.CONWAYS_LIFE:
                return ConwaysLifeRuleset()
            case Rule.DAY_AND_NIGHT:
                return DayAndNightRuleset()
            case Rule.MAZE:
                return MazeRuleset()
            case Rule.ICEBALLS:
                return IceballsRuleset()
            case Rule.LIFE_WITHOUT_DEATH:
                return LifeWithoutDeathRuleset()
            case Rule.SEEDS:
                return SeedsRuleset()
            case Rule.H_TREES:
                return HTreesRuleset()
            case Rule.SERVIETTES:
                return ServiettesRuleset()
            case Rule.BACTERIA:
                return BacteriaRuleset()
            case Rule.PEDESTRIAN_LIFE:
                return PedestrianLifeRuleset()
            case Rule.PULSAR_LIFE:
                return PulsarLifeRuleset()
            case _:
                raise ValueError("Invalid rule.")

    @staticmethod
    def get_custom_ruleset(rulestring: str) -> Ruleset:
        return CustomRuleset(rulestring)


class _Utils:
    birth_survival_notation_regex: re.Pattern = re.compile(r'^B[0-8]{0,9}/S[0-8]{0,9}$')

    @staticmethod
    def __remove_alpha(param: str) -> str:
        return ''.join(filter(str.isdigit, param))

    @staticmethod
    def __map_list_of_strings_to_list_of_ints(string_list: list[str]) -> list[int]:
        return list(map(int, string_list))

    @staticmethod
    def convert_rulestring_to_birth_survival(rulestring: str) -> _BirthSurvival:
        match: re.Match = _Utils.birth_survival_notation_regex.match(rulestring)
        if not match:
            raise ValueError("Invalid rulestring.")
        parsed_rulestring: list[str] = list(map(_Utils.__remove_alpha, rulestring.split("/")))
        return _Utils.__map_list_of_strings_to_list_of_ints(
            list(parsed_rulestring[0])), _Utils.__map_list_of_strings_to_list_of_ints(list(parsed_rulestring[1]))
