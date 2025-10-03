from abc import ABC, abstractmethod
from typing import Dict, Any


class Notifier(ABC):

    @abstractmethod
    def notify(self, user: str, subject: str, body: str) -> None:
        pass


class ConsoleNotifier(Notifier):

    def notify(self, user: str, subject: str, body: str) -> None:

        print(f"[EMAIL SIMULATION] To: {user} | Subject: {subject} | Body: {body}")
