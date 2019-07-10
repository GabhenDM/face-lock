import RPi.GPIO as GPIO
import sys
import time


channel = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.out)


def motor_on(pin):
    GPIO.output(pin, GPIO.HIGH)


def motor_off(pin):
    GPIO.output(pin, GPIO.LOW)


if __name__ == '__main__':
    if sys.argv[1] == "on":
        print("[+] Ligando Rele")
        motor_on(channel)
        # time.sleep(5)
        # motor_off(channel)
        # GPIO.cleanup()
    elif sys.argv[1] == "off":
        print("[+] Desligando Rele")
        motor_off(channel)
        # time.sleep(5)
        # motor_off(channel)
        # GPIO.cleanup()
