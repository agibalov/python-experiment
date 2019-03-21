class MessageGenerator:
    def __init__(self, message: str) -> None:
        self._message = message

    def make_message(self) -> str:
        return self._message


def get_message(message_generator: MessageGenerator):
    return {
        'message': message_generator.make_message()
    }
