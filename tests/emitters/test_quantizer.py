import pytest

from orchestrator.emitters.numbers.quantizer import Quantizer, extend_list
from orchestrator.emitters import Value


@pytest.mark.parametrize(
    "v, to, filter_in, extend, expected",
    [
        (0, [0, 1, 2], False, False, 0),
        (2, [0, 1, 2], False, False, 2),
        (9, [0, 10], False, False, 10),
        (9, [0, 20], False, False, 0),
        (9, [0, 20], True, False, None),
        (None, [0, 20], False, False, None),
    ],
)
def test_multiplier(v, to, filter_in, extend, expected):
    assert (
        Quantizer(
            value=Value(v),
            to=Value(to),
            filter_in=Value(filter_in),
            extend=Value(extend),
        )()
        == expected
    )


@pytest.mark.parametrize(
    "in_list, expected",
    [
        (
            [3, 5, 37],
            [
                1,
                3,
                5,
                13,
                15,
                17,
                25,
                27,
                29,
                37,
                39,
                41,
                49,
                51,
                53,
                61,
                63,
                65,
                73,
                75,
                77,
                85,
                87,
                89,
                97,
                99,
                101,
                109,
                111,
                113,
                121,
                123,
                125,
            ],
        )
    ],
)
def test_extend_list(in_list, expected):
    assert extend_list(in_list) == expected
