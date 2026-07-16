from datetime import datetime
from app.chat.message import Message
import uuid

from app.chat.context_manager import ContextManager


class ChatSession:

    def __init__(self, title="New Chat"):

        self.id = str(uuid.uuid4())

        self.title = title

        self.created_at = datetime.now()

        self.updated_at = datetime.now()

        self.messages = []

        self.context = ContextManager()

    @property
    def history(self):

        return self.messages

    def add_message(self, role, content):

        self.messages.append(
            Message(
                role=role,
                content=content
            )
        )

        self.updated_at = datetime.now()

    def add_user_message(self, content):

        self.add_message("user", content)

    def add_assistant_message(self, content):

        self.add_message("assistant", content)

    def last_message(self):

        if not self.messages:
            return None

        return self.messages[-1]

    def has_messages(self):

        return bool(self.messages)

    def has_context(self):

        return self.context.has_context()

    def clear(self):

        self.messages.clear()

        self.context.clear()

        self.updated_at = datetime.now()