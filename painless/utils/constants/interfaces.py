from __future__ import annotations
from abc import ABC, abstractmethod


class IMessage(ABC):

    @abstractmethod
    def get_content(self, message: str) -> AbstractContent:
        """
        Return attribute value
        """
        raise NotImplementedError("Subclasses should implement this!")

