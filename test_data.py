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

def f6(
    *,
    d
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

a = ['x',  # S100
     'y']  # S101

a = [
    'x'  # S101
]

a = [
    'x',
    'y',
]

a = [x  # S100
     for x in range(1)]

a = [
    x
    for x in range(1)
]

a = {'x',  # S100
     'y'}  # S101

a = {
    'x',
    'y',
}

a = {x  # S100
     for x in range(1)}

a = {
    x
    for x in range(1)
}

a = {'x': 1,  # S100
     'y': 2}  # S101

a = {
    'x': 1,
    'y': 2,
}

a = {x: x  # S100
     for x in range(1)}

a = {
    x: x
    for x in range(1)
}


f3([
    '11',
    '22',
])

f3({
    '11',
    '22',
})

f3({
    '11': 11,
    '22': 22,
})

f3([
    x
    for x in range(1)
])

f3({
    x
    for x in range(1)
})

f3({
    x: x
    for x in range(1)
})


kwargs = {}

f5('-o',  # S100
   some_keyword_argument='./')  # S101

f5(
    b='something',
)

(
    ''.
    format())

f4(
    3,
    *[1, 2]
)

f5(
    3,
    **{
        'a': 3,
    }
)


@f2(3,  # S100
    4)  # S101
def f7():
    pass


from typing import (
    Any,
    Optional,
)


from typing import (Any,  # S100
    Optional  # S101
)
