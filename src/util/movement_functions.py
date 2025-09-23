import math

def turn(turn_direction, speed, raspbot):
    """Turn the car at a given speed.
    - turn_direction: 0 or 1
    - speed: speed, float, [0,1]
    TODO: maybe add relative here as well
    """

    # normalize turn direction
    turn_direction = turn_direction*2-1

    # calculate speeds
    front_left_speed = turn_direction * 255 * speed 
    front_right_speed = turn_direction * 255 * speed
    rear_left_speed = -turn_direction * 255 * speed
    rear_right_speed = -turn_direction * 255 * speed

    # normalize speeds to max 255
    speeds = normalize_speeds_to_255(front_left_speed, front_right_speed, rear_left_speed, rear_right_speed)

    # Control the motors with the calculated speeds
    raspbot.Ctrl_Car(0, 1 if speeds[0] >= 0 else 0, abs(speeds[0]))  # Front Left
    raspbot.Ctrl_Car(1, 1 if speeds[1] >= 0 else 0, abs(speeds[1]))  # Front Right
    raspbot.Ctrl_Car(2, 1 if speeds[2] >= 0 else 0, abs(speeds[2]))  # Rear Left
    raspbot.Ctrl_Car(3, 1 if speeds[3] >= 0 else 0, abs(speeds[3]))  # Rear Right

def stop_motors(raspbot):
    """Stop all motors."""
    raspbot.Ctrl_Car(0, 1, 0)  # Front Left
    raspbot.Ctrl_Car(1, 1, 0)  # Front Right
    raspbot.Ctrl_Car(2, 1, 0)  # Rear Left
    raspbot.Ctrl_Car(3, 1, 0)  # Rear Right

def move(direction_angle, speed, raspbot, relative=False):
    """Move the car in a specified direction.
    - direction_angle: direction in which to move, int, [0,360)
    - speed: speed at which to do this, float, [0,1]
    - raspbot: raspbot object
    - relative: whether to add this movement on top of the current movement state (True) or to stop the current movement and replace it (False)
    """
    if relative:
        front_left_speed = raspbot.motor_states[0][1] if raspbot.motor_states[0][0]==1 else -raspbot.motor_states[0][1] 
        front_right_speed = raspbot.motor_states[1][1] if raspbot.motor_states[1][0]==1 else -raspbot.motor_states[1][1] 
        rear_left_speed = raspbot.motor_states[2][1] if raspbot.motor_states[2][0]==1 else -raspbot.motor_states[2][1] 
        rear_right_speed = raspbot.motor_states[3][1] if raspbot.motor_states[3][0]==1 else -raspbot.motor_states[3][1] 
    else:
        front_left_speed = 0
        front_right_speed = 0
        rear_left_speed = 0
        rear_right_speed = 0
        
    # Convert angle to radians for trigonometric functions
    rad_angle = math.radians(direction_angle)

    # Calculate the speed for each wheel based on the mecanum wheel configuration
    normalization_factor = abs((math.sin(rad_angle) + math.cos(rad_angle))) if (math.sin(rad_angle) + math.cos(rad_angle)) != 0 else 1
    front_left_speed += (math.sin(rad_angle) + math.cos(rad_angle)) / normalization_factor * speed * 255
    front_right_speed += (math.cos(rad_angle) - math.sin(rad_angle)) / normalization_factor * speed * 255
    rear_left_speed += (math.cos(rad_angle) - math.sin(rad_angle)) / normalization_factor * speed * 255
    rear_right_speed += (math.sin(rad_angle) + math.cos(rad_angle)) / normalization_factor * speed * 255

    # normalize speeds to max 255
    speeds = normalize_speeds_to_255(front_left_speed, front_right_speed, rear_left_speed, rear_right_speed)

    # Control the motors with the calculated speeds
    raspbot.Ctrl_Car(0, 1 if speeds[0] >= 0 else 0, abs(speeds[0]))  # Front Left
    raspbot.Ctrl_Car(1, 1 if speeds[1] >= 0 else 0, abs(speeds[1]))  # Front Right
    raspbot.Ctrl_Car(2, 1 if speeds[2] >= 0 else 0, abs(speeds[2]))  # Rear Left
    raspbot.Ctrl_Car(3, 1 if speeds[3] >= 0 else 0, abs(speeds[3]))  # Rear Right

def normalize_speeds_to_255(front_left_speed, front_right_speed, rear_left_speed, rear_right_speed):
    # Normalize speeds to be within the range of 0 to 255
    speeds = [front_left_speed, front_right_speed, rear_left_speed, rear_right_speed]
    max_speed = max(abs(speed) for speed in speeds)
    if max_speed > 255:
        speeds = [speed * (255 / max_speed) for speed in speeds]

    # round to int
    speeds = [round(speed) for speed in speeds]
    
    return speeds