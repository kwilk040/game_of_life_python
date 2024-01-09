from abc import ABC
from cell import CellState
from enum import Enum

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


class Ruleset(ABC):
    def __init__(self, birth_survival: _BirthSurvival):
        self.birth = birth_survival[0]
        self.survival = birth_survival[1]

    def apply(self, cell_state: CellState, neighbours: int) -> CellState:
        return (
            self.__apply_ruleset_for_alive_cell(neighbours)
            if cell_state == CellState.ALIVE
            else self.__apply_ruleset_for_dead_cell(neighbours)
        )

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


class ConwaysRuleset(Ruleset):
    def __init__(self):
        super().__init__(_Utils.convert_rulestring_to_birth_survival("B3/S23"))


class DayAndNightRuleset(Ruleset):
    def __init__(self):
        super().__init__(_Utils.convert_rulestring_to_birth_survival("B3678/S34678"))


class MazeRuleset(Ruleset):
    def __init__(self):
        super().__init__(_Utils.convert_rulestring_to_birth_survival("B3/S12345"))


class IceballsRuleset(Ruleset):
    def __init__(self):
        super().__init__(_Utils.convert_rulestring_to_birth_survival("B25678/S5678"))


class LifeWithoutDeathRuleset(Ruleset):
    def __init__(self):
        super().__init__(_Utils.convert_rulestring_to_birth_survival("B3/S012345678"))


class SeedsRuleset(Ruleset):
    def __init__(self):
        super().__init__(_Utils.convert_rulestring_to_birth_survival("B2/S"))


class HTreesRuleset(Ruleset):
    def __init__(self):
        super().__init__(_Utils.convert_rulestring_to_birth_survival("B1/S012345678"))


class ServiettesRuleset(Ruleset):
    def __init__(self):
        super().__init__(_Utils.convert_rulestring_to_birth_survival("B234/S"))


class BacteriaRuleset(Ruleset):
    def __init__(self):
        super().__init__(_Utils.convert_rulestring_to_birth_survival("B34/S456"))


class PedestrianLifeRuleset(Ruleset):
    def __init__(self):
        super().__init__(_Utils.convert_rulestring_to_birth_survival("B38/S23"))


class PulsarLifeRuleset(Ruleset):
    def __init__(self):
        super().__init__(_Utils.convert_rulestring_to_birth_survival("B3/S238"))


class CustomRuleset(Ruleset):
    def __init__(self, rulestring: str):
        super().__init__(_Utils.convert_rulestring_to_birth_survival(rulestring))


class RulesetFactory:
    @staticmethod
    def get_ruleset(rule: Rule) -> Ruleset:

        match rule:
            case Rule.CONWAYS_LIFE:
                return ConwaysRuleset()
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
    @staticmethod
    def __remove_alpha(param: str) -> str:
        return ''.join(filter(str.isdigit, param))

    @staticmethod
    def __map_list_of_strings_to_list_of_ints(string_list: list[str]) -> list[int]:
        return list(map(int, string_list))

    @staticmethod
    def convert_rulestring_to_birth_survival(rulestring: str) -> _BirthSurvival:
        parsed_rulestring: list[str] = list(map(_Utils.__remove_alpha, rulestring.split("/")))
        return _Utils.__map_list_of_strings_to_list_of_ints(
            list(parsed_rulestring[0])), _Utils.__map_list_of_strings_to_list_of_ints(list(parsed_rulestring[1]))
