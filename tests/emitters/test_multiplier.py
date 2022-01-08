import pytest

from orchestrator.emitters.numbers.multiplier import Multiplier
from orchestrator.emitters import Value


@pytest.mark.parametrize(
    "imin, imax, omin, omax, v, expected",
    [
        (0, 10, 0, 100, 3, 30),
        (20, 40, 0, 100, 30, 50),
        (0, 10, 60, 120, 2, 72),
        (20, 40, 60, 120, 30, 90),
    ],
)
def test_multiplier(imin, imax, omin, omax, v, expected):
    assert (
        Multiplier(
            value=Value(v),
            imin=Value(imin),
            imax=Value(imax),
            omin=Value(omin),
            omax=Value(omax),
        )()
        == expected
    )
