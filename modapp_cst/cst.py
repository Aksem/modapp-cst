from __future__ import annotations
from abc import ABC
from typing import Sequence

from .visitor import Visitor, CSTVisitorT


class CstNode(ABC):
    def visit(self, visitor: CSTVisitorT) -> CstNode:
        # visit self
        should_visit_children = visitor.on_visit(self)

        if should_visit_children:
            for child in self.children:
                child.visit(visitor)

        if isinstance(visitor, Visitor):
            leave_result = visitor.on_leave(self)
        else:
            leave_result = visitor.on_leave(self, self)
        # TODO: validate return type
        return leave_result

    @property
    def children(self) -> Sequence[CstNode]:
        return []
