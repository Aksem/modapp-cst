from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar, Union

if TYPE_CHECKING:
    from .cst import CstNode


CstNodeT = TypeVar('CstNodeT')


class Visitor:
    def on_visit(self, node: CstNode) -> bool:
        visit_func = getattr(self, f"visit_{type(node).__name__}", None)
        if visit_func is not None:
            retval = visit_func(node)
        else:
            retval = True
        # Don't visit children IFF the visit function returned False.
        return False if retval is False else True

    def on_leave(self, original_node: CstNode) -> CstNode:
        leave_func = getattr(self, f"leave_{type(original_node).__name__}", None)
        if leave_func is not None:
            leave_func(original_node)
        return original_node

    # TODO: on_visit_attribute
    # TODO: on_leave_attribute


class Transformer(Generic[CstNodeT]):
    def on_visit(self, node: CstNodeT) -> bool:
        visit_func = getattr(self, f"visit_{type(node).__name__}", None)
        if visit_func is not None:
            retval = visit_func(node)
        else:
            retval = True
        # Don't visit children IFF the visit function returned False.
        return False if retval is False else True
    
    def on_leave(
        self, original_node: CstNodeT, updated_node: CstNodeT
    ) -> CstNodeT:
        """
        Called every time we leave a node, after we've visited its children. If
        the :func:`~libcst.CSTTransformer.on_visit` function for this node returns
        ``False``, this function will still be called on that node.

        ``original_node`` is guaranteed to be the same node as is passed to
        :func:`~libcst.CSTTransformer.on_visit`, so it is safe to do state-based
        checks using the ``is`` operator. Modifications should always be performed
        on the ``updated_node`` so as to not overwrite changes made by child
        visits.

        Returning :attr:`RemovalSentinel.REMOVE` indicates that the node should be
        removed from its parent. This is not always possible, and may raise an
        exception if this node is required. As a convenience, you can use
        :func:`RemoveFromParent` as an alias to :attr:`RemovalSentinel.REMOVE`.
        """
        leave_func = getattr(self, f"leave_{type(original_node).__name__}", None)
        if leave_func is not None:
            updated_node = leave_func(original_node, updated_node)

        return updated_node


CSTVisitorT = Union[Visitor, Transformer]
