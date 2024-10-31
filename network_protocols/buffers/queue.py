from typing import Optional

from network_protocols.buffers.messages import Message
from network_protocols.buffers.base import BaseBuffer


class Queue(BaseBuffer):
    def __init__(self):
        self.head: Optional[Message] = None
        self.tail: Optional[Message] = None

    def put(self, data: Message) -> None:
        if self.head is None:
            self.head = data
            self.tail = data
        else:
            self.tail.next = data
            self.tail = data

    def pop(self) -> Optional[Message]:
        if self.head is None:
            return None

        data = self.head
        self.head = self.head.next

        data.next = None

        return data

    def clear(self) -> None:
        """Clears the buffer"""
        self.head = None
        self.tail = None

    @property
    def length(self) -> int:
        if self.head is None:
            return 0

        length = 1
        current = self.head

        while current.next is not None:
            length += 1
            current = current.next

        return length
