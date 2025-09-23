import pytest, math
from src.util.movement_functions import turn, move, stop_motors

class MockRaspbot:
    def __init__(self):
        self.motor_states = [0, 0, 0, 0]

    def Ctrl_Car(self, motor_id, direction, speed):
        self.motor_states[motor_id] = (direction, speed)

@pytest.fixture
def raspbot():
    return MockRaspbot()

def test_move_forward_full_speed(raspbot):
    move(0, 1, raspbot)
    assert raspbot.motor_states == [(1,255), (1,255), (1,255), (1,255)]

def test_move_forward_half_speed(raspbot):
    move(0, 0.5, raspbot)
    assert raspbot.motor_states == [(1,128), (1,128), (1,128), (1,128)]

def test_move_backward(raspbot):
    move(180, 1, raspbot)
    assert raspbot.motor_states == [(0,255), (0,255), (0,255), (0,255)]

def test_move_right(raspbot):
    move(90, 1, raspbot)
    assert raspbot.motor_states == [(1,255), (0,255), (0,255), (1,255)]

def test_move_left(raspbot):
    move(270, 1, raspbot)
    assert raspbot.motor_states == [(0,255), (1,255), (1,255), (0,255)]

def test_move_diagonally_full_speed(raspbot):
    move(45, 1, raspbot)
    assert raspbot.motor_states == [(1,255), (1,0), (1,0), (1,255)]

def test_move_diagonally_half_speed(raspbot):
    move(45, 0.5, raspbot)
    assert raspbot.motor_states == [(1,128), (1,0), (1,0), (1,128)]

def test_turn(raspbot):
    turn(0, 1, raspbot)
    assert raspbot.motor_states == [(0, 255), (0, 255), (1, 255), (1, 255)]
    turn(1, 1, raspbot)
    assert raspbot.motor_states == [(1, 255), (1, 255), (0, 255), (0, 255)]

def test_stop_motors(raspbot):
    stop_motors(raspbot)
    assert raspbot.motor_states == [(1, 0), (1, 0), (1, 0), (1, 0)]

def test_relative_movement_full_speed(raspbot):
    move(0, 1, raspbot)
    move(90, 1, raspbot,relative=True)
    # forward + right = diagonal right
    assert raspbot.motor_states == [(1,255), (1,0), (1,0), (1,255)]

def test_relative_movement_half_speed(raspbot):
    move(0, 1, raspbot)
    move(90, 0.5, raspbot,relative=True)
    # forward + right = diagonal right
    assert raspbot.motor_states == [(1,255), (1,85), (1,85), (1,255)]

if __name__ == "__main__":
    pytest.main()
