import pytest
from game.rotation_bridge import torque_ratio, propagate_directions

def test_torque_ratio_equal():
    assert torque_ratio(1.0, 1.0) == pytest.approx(1.0)

def test_torque_ratio_2x():
    assert torque_ratio(2.0, 1.0) == pytest.approx(2.0)

def test_torque_ratio_zero_denominator():
    with pytest.raises((ValueError, ZeroDivisionError)):
        torque_ratio(1.0, 0.0)

def test_linear_chain():
    dirs = propagate_directions(3, [0,1, 1,2], 0, 1)
    assert dirs == [1, -1, 1]

def test_unpowered_stays_zero():
    dirs = propagate_directions(3, [0,1], 0, 1)
    assert dirs[2] == 0

def test_branch():
    dirs = propagate_directions(4, [0,1, 1,2, 1,3], 0, 1)
    assert dirs[0]==1 and dirs[1]==-1 and dirs[2]==1 and dirs[3]==1

def test_ccw_source():
    dirs = propagate_directions(2, [0,1], 0, -1)
    assert dirs == [-1, 1]
