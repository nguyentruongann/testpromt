class APIError(Exception):
    def __init__(self, status_code, message):
        super().__init__(f"[{status_code}] {message}")
