"""Testing line-up utilities."""
from ..line_up import (
    LU343, LU433, LU352, LU442, LU532, LU451, LU541
)


def test_line_up_initialization():
    """Testing the initialization of the line-ups."""
    for line_up_type in [LU343, LU433, LU352, LU442, LU532, LU451, LU541]:
        _ = line_up_type()
