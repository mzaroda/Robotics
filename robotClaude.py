#!/usr/bin/env python3
import RPi.GPIO as GPIO
import curses
import time

# GPIO pin setup for L298N motor controller
# Motor A - Left side
ENA = 17  # Enable pin for motor A
IN1 = 27  # Input 1 for motor A
IN2 = 22  # Input 2 for motor A

# Motor B - Right side
ENB = 18  # Enable pin for motor B
IN3 = 23  # Input 3 for motor B
IN4 = 24  # Input 4 for motor B

# Setup GPIO
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Setup motor A pins
    GPIO.setup(ENA, GPIO.OUT)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)

    # Setup motor B pins
    GPIO.setup(ENB, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)

    # Setup PWM for speed control
    pwm_a = GPIO.PWM(ENA, 100)  # 100 Hz frequency
    pwm_b = GPIO.PWM(ENB, 100)

    # Start PWM with 0% duty cycle
    pwm_a.start(0)
    pwm_b.start(0)

    return pwm_a, pwm_b

# Motor control functions
def forward(pwm_a, pwm_b, speed=50):
    # Set motor A direction
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)

    # Set motor B direction
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

    # Set speed
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)

def backward(pwm_a, pwm_b, speed=50):
    # Set motor A direction
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)

    # Set motor B direction
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

    # Set speed
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)

def left(pwm_a, pwm_b, speed=50):
    # Set motor A direction (backward)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)

    # Set motor B direction (forward)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

    # Set speed
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)

def right(pwm_a, pwm_b, speed=50):
    # Set motor A direction (forward)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)

    # Set motor B direction (backward)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

    # Set speed
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)

def stop(pwm_a, pwm_b):
    # Set motor A stop
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)

    # Set motor B stop
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

    # Set speed to 0
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)

def main():
    try:
        # Setup GPIO and get PWM objects
        pwm_a, pwm_b = setup_gpio()

        # Initialize curses for keyboard control
        screen = curses.initscr()
        curses.noecho()  # Turn off automatic echoing of keys
        curses.cbreak()  # React to keys instantly without Enter key
        screen.keypad(True)  # Enable special keys

        # Display control instructions
        screen.addstr(0, 0, "Robot Control with Keyboard")
        screen.addstr(1, 0, "-----------------------")
        screen.addstr(2, 0, "W: Forward")
        screen.addstr(3, 0, "A: Left")
        screen.addstr(4, 0, "D: Right")
        screen.addstr(5, 0, "X: Backward")
        screen.addstr(6, 0, "S: Stop")
        screen.addstr(7, 0, "Q: Quit")
        screen.addstr(9, 0, "Current State: Stopped")
        screen.refresh()

        current_state = "Stopped"

        while True:
            # Wait for key press
            key = screen.getch()

            # Update status based on key press
            if key == ord('w') or key == ord('W'):
                forward(pwm_a, pwm_b)
                current_state = "Moving Forward"
            elif key == ord('a') or key == ord('A'):
                left(pwm_a, pwm_b)
                current_state = "Turning Left"
            elif key == ord('d') or key == ord('D'):
                right(pwm_a, pwm_b)
                current_state = "Turning Right"
            elif key == ord('x') or key == ord('X'):
                backward(pwm_a, pwm_b)
                current_state = "Moving Backward"
            elif key == ord('s') or key == ord('S'):
                stop(pwm_a, pwm_b)
                current_state = "Stopped"
            elif key == ord('q') or key == ord('Q'):
                break

            # Update status display
            screen.addstr(9, 0, f"Current State: {current_state}      ")
            screen.refresh()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up
        curses.nocbreak()
        screen.keypad(False)
        curses.echo()
        curses.endwin()

        # Stop motors
        if 'pwm_a' in locals() and 'pwm_b' in locals():
            stop(pwm_a, pwm_b)
            pwm_a.stop()
            pwm_b.stop()

        GPIO.cleanup()

if __name__ == "__main__":
    main()# Write your code here :-)
