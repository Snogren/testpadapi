def handle_error(message, exception=None):
    """
    Logs an error message and optionally an exception.
    """
    print(f"ERROR: {message}")
    if exception:
        print(exception)
