def f0(
    b,
    **kwargs,
):
    """Test compatibility with comma after **kwargs."""
    pass


def f1():
    """Test compatibility with f-strings"""
    hello = 'hello'
    world = 'world'
    hello_world = f'{hello} {world}'
