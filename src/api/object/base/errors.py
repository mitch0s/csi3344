# User errors
class SessionNotFound(Exception):
    def __init__(self, *args):
        super().__init__(*args)

# User errors
class UserNotFoundError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

# Account errors
class AccountNotFoundError(Exception):
    def __init__(self, *args):
        super().__init__(*args)