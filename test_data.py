def f1(a,  # S100
       b):  # S101
    pass


def f2(
    a,
    b  # S101
):
    pass


def f3(
    a,
    b,
):
    pass


# trailing comma after *args or **kwargs is a syntax error therefore
# we don't want to enforce it such situations


def f4(
    a,
    *args
):
    pass


def f5(
    b,
    **kwargs
):
    pass


f3(1,  # S100
   2)  # S101

f3(
    1,
    2)  # S101

f3(
    1,
    2  # S101
)

f3(
    1,
    2,
)

kwargs = {}

