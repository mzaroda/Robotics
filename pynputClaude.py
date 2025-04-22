from pynput import keyboard
import RPi.GPIO as GPIO
import time

# L298N Motor Controller Pins
# Motor A - Left Motor
ENA = 17  # PWM pin for controlling speed of motor A
IN1 = 27  # Direction control 1 for motor A
IN2 = 22  # Direction control 2 for motor A

# Motor B - Right Motor
ENB = 18  # PWM pin for controlling speed of motor B
IN3 = 23  # Direction control 1 for motor B
IN4 = 24  # Direction control 2 for motor B

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup all pins as outputs
motor_pins = [ENA, IN1, IN2, ENB, IN3, IN4]
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

# Setup PWM for motor speed control
left_motor_pwm = GPIO.PWM(ENA, 100)
right_motor_pwm = GPIO.PWM(ENB, 100)

# Start PWM with 0% duty cycle (stopped)
left_motor_pwm.start(0)
right_motor_pwm.start(0)

# Motor speed (0-100)
SPEED = 70

def stop():
    """Stop both motors"""
    left_motor_pwm.ChangeDutyCycle(0)
    right_motor_pwm.ChangeDutyCycle(0)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    print("Stopped")

def forward():
    """Move robot forward"""
    left_motor_pwm.ChangeDutyCycle(SPEED)
    right_motor_pwm.ChangeDutyCycle(SPEED)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    print("Moving Forward")

def backward():
    """Move robot backward"""
    left_motor_pwm.ChangeDutyCycle(SPEED)
    right_motor_pwm.ChangeDutyCycle(SPEED)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    print("Moving Backward")

def turn_left():
    """Turn robot left"""
    left_motor_pwm.ChangeDutyCycle(SPEED)
    right_motor_pwm.ChangeDutyCycle(SPEED)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    print("Turning Left")

def turn_right():
    """Turn robot right"""
    left_motor_pwm.ChangeDutyCycle(SPEED)
    right_motor_pwm.ChangeDutyCycle(SPEED)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    print("Turning Right")

# Initialize by stopping motors
stop()

# Define key press and release functions
currently_pressed_keys = set()

def on_press(key):
    """Handle key press events"""
    try:
        # Get the character the key represents
        key_char = key.char.lower()

        # Add key to currently pressed set
        currently_pressed_keys.add(key_char)

        # Control the robot based on the key
        if key_char == 'w':
            forward()
        elif key_char == 'x':
            backward()
        elif key_char == 'a':
            turn_left()
        elif key_char == 'd':
            turn_right()
        elif key_char == 'q':
            return False  # Stop listener

    except AttributeError:
        # Handle special keys
        if key == keyboard.Key.esc:
            # Stop on ESC key
            print("Exiting program...")
            return False  # Stop listener

def on_release(key):
    """Handle key release events"""
    try:
        # Remove from currently pressed set
        key_char = key.char.lower()
        if key_char in currently_pressed_keys:
            currently_pressed_keys.remove(key_char)

        # If no control keys are pressed, stop the robot
        if not any(k in currently_pressed_keys for k in ['w', 'a', 's', 'd', 'x']):
            stop()

    except AttributeError:
        # Special key released
        pass

# Set up the keyboard listener
def main():
    print("Robot Control with Keyboard")
    print("---------------------------")
    print("w: Forward")
    print("a: Turn Left")
    print("d: Turn Right")
    print("x: Backward")
    print("q or ESC: Quit")
    print("---------------------------")

    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

    # Clean up GPIO pins
    left_motor_pwm.stop()
    right_motor_pwm.stop()
    GPIO.cleanup()
    print("GPIO cleaned up. Program ended.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Handle Ctrl+C
        stop()
        left_motor_pwm.stop()
        right_motor_pwm.stop()
        GPIO.cleanup()
        print("\nProgram stopped by user")# Write your code here :-)
