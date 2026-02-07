"""Core greeting logic."""


def greet(name: str = "world") -> str:
    """
    Generate a greeting message.

    Args:
        name: The name to greet. Defaults to "world".

    Returns:
        A greeting message string.
    """
    # Handle empty or whitespace-only names
    if not name or not name.strip():
        name = "world"
    return f"Hello, {name}"
