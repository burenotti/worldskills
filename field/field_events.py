from .fieldnode import FieldNode


class AnyType:

    def __eq__(self, other):
        return True

    def __and__(self, other):
        return True

    def __or__(self, other):
        return True

    def __contains__(self, item):
        return True


class Conflict:
    def __init__(self, conflict_type: str):
        self.type = conflict_type


class MoveConflict(Conflict):
    def __init__(self, field, first_node: FieldNode, second_node: FieldNode):
        super().__init__("move_conflict")
        self.field = field
        self.first_node = first_node
        self.second_node = second_node


class Rule:
    def __init__(self, rule, checker):
        self.rule = rule
        self.checker = checker

    def __call__(self, conflict) -> bool:
        if self.checker(conflict):
            self.rule(conflict)
            return True
        return False
