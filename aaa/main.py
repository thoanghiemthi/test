from typing import List, Optional
from pydantic import BaseModel
from core.domain import model


class Foo(BaseModel):
    count: int
    size: Optional[float]


class Bar(BaseModel):
    apple = 'x'
    banana = 'y'


class Spam(BaseModel):
    foo: Foo
    bars: List[Bar]


m = Spam(foo={'count': 4}, bars=[{'apple': 'x1'}])
print(m)
#> foo=Foo(count=4, size=None) bars=[Bar(apple='x1', banana='y'),
#> Bar(apple='x2', banana='y')]
print(m.dict())
a = {}
print(a.get('a',{}))