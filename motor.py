import RPi.GPIO as GPIO
import time

# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define motor control pins
motor1_pwm = 17  # Example GPIO pin for Motor 1 PWM
motor1_in1 = 18  # Example GPIO pin for Motor 1 IN1
motor1_in2 = 19  # Example GPIO pin for Motor 1 IN2

motor2_pwm = 27  # Example GPIO pin for Motor 2 PWM
motor2_in1 = 20  # Example GPIO pin for Motor 2 IN1
motor2_in2 = 21  # Example GPIO pin for Motor 2 IN2

# Set up pins as output
GPIO.setup(motor1_pwm, GPIO.OUT)
GPIO.setup(motor1_in1, GPIO.OUT)
GPIO.setup(motor1_in2, GPIO.OUT)

GPIO.setup(motor2_pwm, GPIO.OUT)
GPIO.setup(motor2_in1, GPIO.OUT)
GPIO.setup(motor2_in2, GPIO.OUT)

# Set up PWM
motor1_pwm_obj = GPIO.PWM(motor1_pwm, 1000)  # Frequency: 1000 Hz
motor2_pwm_obj = GPIO.PWM(motor2_pwm, 1000)

# Start PWM with 0% duty cycle (motors off)
motor1_pwm_obj.start(0)
motor2_pwm_obj.start(0)

# Function to control motor throttle
def set_motor_speed(pwm_obj, in1, in2, speed):
    if speed >= 0:
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
    else:
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
    pwm_obj.ChangeDutyCycle(abs(speed))

try:
    while True:
        throttle_motor1 = float(input("Enter throttle for Motor 1 (-100 to 100): "))
        throttle_motor2 = float(input("Enter throttle for Motor 2 (-100 to 100): "))
        
        set_motor_speed(motor1_pwm_obj, motor1_in1, motor1_in2, throttle_motor1)
        set_motor_speed(motor2_pwm_obj, motor2_in1, motor2_in2, throttle_motor2)
        
except KeyboardInterrupt:
    pass

# Stop PWM and cleanup
motor1_pwm_obj.stop()
motor2_pwm_obj.stop()
GPIO.cleanup()