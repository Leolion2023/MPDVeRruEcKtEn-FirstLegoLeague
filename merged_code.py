import hub
import motor
import motor_pair

import time
import math



"""

Our Personal Main Code

Here you can also find our specific exercises and also some examples.

Those are the ports we used for the specific tasks:
MotorPorts:
    A = 0: MotorRight
    B = 1: Unused
    C = 2: Unused
    D = 3: Addition
    E = 4: MotorLeft
    F = 5: AbilityRight

"""

# Logging-Level Konstanten innerhalb der Klasse
FULL = 2
LOW = 1
NO = 0

# Device Konstanten
BOTH = 0
LED = 1
CLI = 2


class Controller:
    PORTS = ["A", "B", "C", "D", "E", "F"]
    CONN_MOTOR = [0, 1]
    colorSensor = 4

    # Logging-Level Konstanten innerhalb der Klasse
    FULL = 2
    LOW = 1
    NO = 0

    # Device Konstanten
    BOTH = 0
    LED = 1
    CLI = 2

    def __init__(self):
        self._kill_ = False
        self.logging_level = self.FULL # Setze das Logging-Level hier (FULL, MEDIUM, LOW oder NO)
        self.device = self.BOTH

        self.driveBase = DriveBase()


        logger.info("Started Program", 0)

    def __button_check__(self, which: int) -> bool:
        """"""
        if which == 0:
            return bool(hub.button.pressed(hub.button.LEFT) or
                hub.button.pressed(hub.button.RIGHT))
        elif which == 1:
            return bool(hub.button.pressed(hub.button.LEFT))
        elif which == 2:
            return bool(hub.button.pressed(hub.button.RIGHT))
        else:
            logger.exception("UNKNOWN WHICH STATE", 303)
            return False


    def kill(self):
        logger.info("Killed program", -1)
        self._kill_ = True




    def run_program(self):
        logger.info("Run Program", 1)
        # self.forschungsauftrag_demo()

        # self.krake()        #0
        # self.taucherin_riff() #1
        # self.get_shark()    #2
        # self.dreizack()    #3
        # self.deploy_koralle() #4

    def connect_addition(self):
        self.driveBase.attach_addition(False)
        logger.info("WAITING", "START")
        time.sleep_ms(500)
        logger.info("WAITING", 10)
        while not self.__button_check__(0):pass
        self.driveBase.attach_addition(True)
        time.sleep(0.5)

    def reset_addition_riff(self):
        motor.run_for_degrees(self.driveBase.RIGHT, 10, 100000)
        time.sleep(0.5)
        self.driveBase.reset_null(self.driveBase.RIGHT)
        time.sleep(0.2)
        # motor.run_for_degrees(self.driveBase.RIGHT, -800, 500)
        self.driveBase.run_motor_degree(self.driveBase.RIGHT, 800, -710, tolerance = 10)
        time.sleep(0.1)
        self.driveBase.reset_null(self.driveBase.RIGHT)

    def forschungsauftrag_demo(self):
        self.connect_addition()
        self.driveBase.gyro_drive(100, 800, 500)



    def collide_testing(self):
        self.driveBase.gyro_drive(80, 200, 200, avoid_collision = True)
        logger.info("Finished", 23)

    def gyro_backwards(self):
        # self.driveBase.gyro_drive(70, -900, -500)
        self.driveBase.gyro_drive(70, 300, 200)

    def drive_to_me(self, direction: int):
        self.driveBase.gyro_drive(60, direction * 800, direction * 600)

    def dreizack(self):
        self.driveBase.attach_addition(False)
        self.driveBase.run_motor_duration(20, -1, self.driveBase.RIGHT)
        motor.run_to_absolute_position(5,45,1000,direction=motor.SHORTEST_PATH)
        while not self.__button_check__(0):pass
        self.driveBase.attach_addition(True)
        time.sleep(0.2)
        motor.run_to_absolute_position(5,5,1000,direction=motor.SHORTEST_PATH)
        time.sleep(0.2)
        motor.run_to_absolute_position(5,5,1000,direction=motor.SHORTEST_PATH)
        time.sleep(0.2)
        self.driveBase.run_motor_duration(300, 0.3, self.driveBase.RIGHT)
        motor.stop(5,stop = motor.BRAKE)
        while not self.__button_check__(0):pass
        self.driveBase.gyro_drive(30, 500, 100)
        self.driveBase.gyro_turn(90, 100, 100)
        self.driveBase.gyro_drive(60, 500, 100)
        self.driveBase.gyro_turn(-90, 200, 100)
        self.driveBase.run_motor_duration(-100, 1, self.driveBase.RIGHT) #deploy hai
        self.driveBase.reset_null(self.driveBase.RIGHT)
        #self.driveBase.run_motor_duration(1,-300,0.3)
        motor.run_to_relative_position(self.driveBase.RIGHT, 80, 100)
        self.driveBase.gyro_turn(-90, 200, 100)
        self.driveBase.gyro_drive(6, 500, 100)
        self.driveBase.gyro_turn(90, 200, 100)
        self.driveBase.gyro_drive(10, 100, 100)
        motor.run_to_relative_position(self.driveBase.RIGHT, 100, 200)#take dreizack
        #self.driveBase.run_motor_duration(1,-300,0.2)
        self.driveBase.gyro_drive(10, -500, -100)
        self.driveBase.gyro_turn(-110, 300, 100)
        self.driveBase.gyro_drive(80, 800, 100)
        self.driveBase.run_motor_duration(300, 0.1, self.driveBase.RIGHT)
        #homebase
        while not self.__button_check__(0):pass
        self.driveBase.gyro_drive(20, 100, 100)
        self.driveBase.run_motor_duration(-300, 0.3, self.driveBase.RIGHT)
        motor.run_to_relative_position(self.driveBase.RIGHT , 90,-300)
        time.sleep(0.5)
        self.driveBase.gyro_drive(30,-900, -100)
        self.driveBase.attach_addition(False)
        time.sleep(0.2)
        self.driveBase.run_motor_duration(500, 2, self.driveBase.RIGHT)

    def deploy_koralle(self):
        self.driveBase.attach_addition(False)
        self.driveBase.run_motor_duration(20, -1, self.driveBase.RIGHT)
        motor.run_to_absolute_position(5,45,1000,direction=motor.SHORTEST_PATH)
        while not self.__button_check__(0):pass
        self.driveBase.attach_addition(True)
        time.sleep(0.2)
        motor.run_to_absolute_position(5,5,1000,direction=motor.SHORTEST_PATH)
        time.sleep(0.2)
        motor.run_to_absolute_position(5,5,1000,direction=motor.SHORTEST_PATH)
        time.sleep(0.2)
        self.driveBase.run_motor_duration(300, 0.3, self.driveBase.RIGHT)
        motor.stop(5,stop = motor.BRAKE)
        while not self.__button_check__(0):pass
        self.driveBase.gyro_drive(20, 100, 100)
        self.driveBase.run_motor_duration(-300, 0.3, self.driveBase.RIGHT)
        motor.run_to_relative_position(self.driveBase.RIGHT,motor.relative_position(self.driveBase.RIGHT) + 90,-300)
        time.sleep(0.5)
        self.driveBase.gyro_drive(30,-900, -100)
        self.driveBase.attach_addition(False)
        time.sleep(0.2)
        self.driveBase.run_motor_duration(500, 2, self.driveBase.RIGHT)

    def get_shark(self):
        self.driveBase.attach_addition(False)
        self.driveBase.run_motor_duration(100, -1, self.driveBase.RIGHT)
        self.driveBase.run_motor_duration(5,100,-1)
        while not self.__button_check__(0):pass
        self.driveBase.attach_addition(True)
        self.driveBase.run_motor_duration(1000, -1, self.driveBase.RIGHT)
        self.driveBase.gyro_drive(20, 500, 100)
        self.driveBase.run_motor_duration(-1000, -1, self.driveBase.RIGHT)
        self.driveBase.gyro_drive(45, 500, 100)
        motor.stop(self.driveBase.RIGHT,stop = motor.BRAKE)
        self.driveBase.gyro_turn(-90, 100, 100)
        self.driveBase.run_motor_duration(1000, -1, self.driveBase.RIGHT)
        self.driveBase.gyro_drive(20, 900, 500)#press korallenriff
        self.driveBase.gyro_drive(14, -500, -100)
        motor.stop(self.driveBase.RIGHT,stop = motor.BRAKE)
        self.driveBase.gyro_turn(45, 100, 100)
        self.driveBase.run_motor_duration(-1000, -1, self.driveBase.RIGHT)
        self.driveBase.gyro_drive(35, 900, 100)#press Hai
        self.driveBase.run_motor_duration(1000, -1, self.driveBase.RIGHT)
        self.driveBase.gyro_drive(30, -500, 100)
        self.driveBase.gyro_turn(-110, 300, 100)
        self.driveBase.attach_addition(False)
        self.driveBase.gyro_drive(80, 800, 100)

    def krake(self):
        self.driveBase.attach_addition(False)
        motor.run_to_absolute_position(5,45,1000,direction=motor.SHORTEST_PATH)
        logger.info("WAITING", "START")
        while not self.__button_check__(0):pass
        # runloop.until(self.button_check)
        self.driveBase.attach_addition(True)
        motor.stop(5,stop = motor.BRAKE)
        self.driveBase.gyro_drive(2, 500, 100)
        self.driveBase.gyro_turn(-47, 100, 100)
        self.driveBase.gyro_drive(50, 500, 1000)#get kraken
        self.driveBase.gyro_drive(20, -500, -100) #rückwärts??
        self.driveBase.gyro_turn(-23, 100, 100)
        self.driveBase.gyro_drive(45, 500, 100)
        self.driveBase.gyro_turn(32, 100, 100)
        self.driveBase.gyro_drive(20, 500, 100)
        self.driveBase.run_motor_duration(68, 1.5, self.driveBase.RIGHT)# release kraken
        self.driveBase.run_motor_duration(-600, 0.5, self.driveBase.RIGHT)
        #self.driveBase.gyro_drive(5, 500, 100)
        self.driveBase.gyro_turn(-23, 500, 500)#fisch einklappen
        self.driveBase.gyro_drive(24, 500, 100)#einsammeln item 1
        self.driveBase.gyro_turn(-30, 500, 500)
        self.driveBase.gyro_turn(5, 200, 200)
        self.driveBase.gyro_drive(25, 500, 100)
        self.driveBase.gyro_turn(-20, 100, 100)
        self.driveBase.gyro_drive(10, 500, 100)#einsammeln koralle 1
        self.driveBase.gyro_turn(-20, 100, 100)
        self.driveBase.gyro_turn(-30, 20, 20)#verschieben koralle 2
        self.driveBase.gyro_turn(10, 100, 20)
        self.driveBase.attach_addition(False)
        self.driveBase.gyro_drive(80, 1000, 100)

    def taucherin_riff(self):

        motor.run_to_absolute_position(self.driveBase.RIGHT, 0, 600, direction = motor.SHORTEST_PATH)
        self.connect_addition()
        self.reset_addition_riff()
        logger.debug("Resetted addition riff")

        self.driveBase.reset_null(self.driveBase.RIGHT)
        pin = self.driveBase.RIGHT
        self.driveBase.gyro_drive(78.5, 600, 400)
        self.driveBase.gyro_turn(90, 200, 100, rotate_mode = 1)
        motor.run_to_relative_position(pin, 285, 800)
        time.sleep(0.4)
        self.driveBase.gyro_drive(20, 200, 60)
        motor.run_to_relative_position(pin, 380, 800)
        self.driveBase.gyro_drive(26.5, -300, -200)
        self.driveBase.gyro_turn(90, -200, -100, rotate_mode = 1)
        motor.run_to_relative_position(pin, 370, 800)
        time.sleep_ms(200)
        self.driveBase.gyro_drive(7, 300, 300)
        time.sleep_ms(300)
        self.driveBase.gyro_turn(10, 200, 100)
        time.sleep_ms(300)
        motor.run_to_relative_position(pin, 230, 800)
        time.sleep_ms(300)
        self.driveBase.gyro_drive(8, -400, -400)
        motor.run_to_relative_position(pin, 200, 800)
        time.sleep_ms(200)
        self.driveBase.gyro_turn(-13, 200, 100) # Turn before push korallen down
        self.driveBase.gyro_drive(9, 400, 300)
        motor.run_to_relative_position(pin, 0, 900)
        time.sleep_ms(900)
        motor.run_to_relative_position(pin, 200, 900)
        time.sleep_ms(900)
        self.driveBase.gyro_drive(14, -400, -300)
        self.driveBase.gyro_turn(90, 200, 100)
        self.driveBase.gyro_drive(15, -400, -300)
        time.sleep_ms(500)
        motor.run_to_relative_position(pin, 0, 900)
        time.sleep_ms(300)
        self.driveBase.gyro_turn(5, 100, 100)
        self.driveBase.gyro_drive(15, 600, 300)
        self.nest_auf()
        time.sleep_ms(300)

    def nest_auf(self):

        motor_pair.move(self.driveBase.MOTPAIR, 0, velocity = 200)
        motor.run_for_degrees(self.driveBase.RIGHT, 300, 1000)
        time.sleep(2)
        motor.set_duty_cycle(self.driveBase.RIGHT, 0)
        motor_pair.stop(self.driveBase.MOTPAIR)
        self.driveBase.gyro_turn(5, 300, 200)
        motor.run_for_degrees(self.driveBase.RIGHT, 70, 300)
        self.driveBase.run_pair(-300, 1)
        motor.run_to_relative_position(self.driveBase.RIGHT, 100, 600)
        time.sleep_ms(200)
        self.driveBase.gyro_drive(10, -300, -100)
        motor.run_to_relative_position(self.driveBase.RIGHT, 780, 600)
        time.sleep_ms(600)
        self.driveBase.gyro_turn(100, 400, 300)
        self.driveBase.attach_addition(False)
        self.driveBase.gyro_drive(80, 800, 800)


    def action_change_debug(self):
        motor.reset_relative_position(self.driveBase.RIGHT, 0)
        while True:
            if self.button_check(1):
                self.driveBase.run_motor_duration(self.driveBase.RIGHT, 100, duration = 0)
                time.sleep(0.2)
            elif self.button_check(2):
                self.driveBase.run_motor_duration(self.driveBase.RIGHT, -100, duration = 0)
                time.sleep(0.2)
            else:
                self.driveBase.stop_motor(self.driveBase.RIGHT)
                time.sleep(0.5)


class Logger:
    def __init__(self, level):
        self.log_level = level

    def debug(self, message, *args):
        print("[DEBUG] {}".format(message))

    def info(self, message, code = None, *args):
        if code != None:
            hub.light_matrix.write(str(code))
        print("[INFO] {}".format(message))

    def exception(self, message, code: int, *args):
        hub.light_matrix.write(str(code))
        print("[ERROR] {}".format(message))



class DriveBase:
    """

        Alle Funktionen mit denen Wir unseren Roboter steuern!

        Diese Klasse in den Code hinzufügen und benutzen.

    """

    MOTORR = 0
    ADDITION = 3
    MOTORL = 4
    RIGHT = 5

    MOTPAIR = 0

    WHEELCIRC = 17.6

    def __init__(self):
        self.gyroSens = hub.motion_sensor
        self.stop = False

        motor_pair.pair(self.MOTPAIR, self.MOTORL, self.MOTORR)

        self.addition_state = self.get_addition_state()
        self.attach_addition(False)

    #########################
    # Complex GyroFunctions #
    #########################

    def gyro_drive(self, distance: float = 100, mainspeed: int = 600, stopspeed: int = 300, brake_start: float = 0.7, offset: int = 0, avoid_collision: bool = False) -> bool:
        """Drive for specified distance

            Drive the robot for a given distance, it uses the GyroSensor and PID calculations to drive perfectly straight.
            The robot can also deccelerate when a distance is reached.

            Fahre den Roboter eine bestimmte Distanz. Die Funktion benutzt den GyroSensor und PID Berechnungen um perfekt geradeaus zu fahren.
            Der Roboter kann auch abbremsen sobald eine bestimmte Distanz ist erreicht.

            Parameters / Parameter
            ----------------------
            distance : int = 100
                The distance that the robot is supposed to drive.
                Die Distanz die der Roboter fahren soll.
            mainspeed: int = 600
                The maximum speed the robot reaches.
                Die maximale Geschwindigkeit, die der Roboter erreicht.
            stopspeed : float = 300
                The target speed while braking; the minimum speed at the end of the program.
                Die minimale Geschwindigkeit am Ende des Programms.
            brake_start : int = 0.7
                Percentage of the driven distance after which the robot starts braking.
                Prozentsatz der zurückgelegten Strecke, nach der der Roboter mit dem Bremsen beginnt.
            offset : int = 0    ---> UNUSED
                The offset of the gyrovalues.
                Der Offset von den Gyrowerten.
            avoid_collision : bool = False    ---> UNUSED
                If the robot should try to avoid every collision
                Ob der Roboter versuchen sollte, Kollisionen auszuweichen
        """
        hub.motion_sensor.reset_yaw(0)
        time.sleep_ms(10)
        motor.reset_relative_position(self.MOTORL, 0)
        motor.reset_relative_position(self.MOTORR, 0)

        def get_gyro_value() -> int:
            return round(hub.motion_sensor.tilt_angles()[0]/ 10)

        def get_driven():
            return (
                abs(motor.relative_position(self.MOTORL)) +
                abs(motor.relative_position(self.MOTORR))) / 2

        def calc_power() -> float:
            return (
                abs(motor.get_duty_cycle(self.MOTORL)) +
                abs(motor.get_duty_cycle(self.MOTORR))) / 2

        def full_speed(started) -> bool:
            logger.debug((int(calc_power() / 1000), mainspeed / 100))
            if not time.time() - started > 1:
                logger.debug("Time False: {} von Now: {} then {}".format(time.time() - started, time.time(), started))
                return True
            if int(calc_power() / 1000) > mainspeed / 100:
                logger.debug(True)
                return True
            else:
                logger.debug(False)
                return False

        #Set starting speed of robot
        speed = mainspeed
        #Sets PID values

        change = 0
        old_change = 0
        integral = 0
        steering_sum = 0
        power = 0
        old_power = 0

        timestamp = 0


        invert = 1

        #Sets values based on user inputs
        loop = True

        #Calulation of degrees the motors should turn to
        #17.6 is wheel circumference in cm. You might need to adapt it
        rotate_distance = (distance / self.WHEELCIRC) * 360
        deccelerate_distance = rotate_distance * (1 - brake_start)

        #Inversion of target rotation value for negative values
        if speed < 0:
            invert = -1

        #Calculation of braking point
        brake_start_value = brake_start * rotate_distance
        driven_distance = get_driven()

        motor_pair.move(self.MOTPAIR, 0, velocity = int(speed))
        started_time = time.time()

        power = calc_power()
        old_power = power

        while loop:

            #Calculation of driven distance and PID values
            old_driven_distance = driven_distance
            driven_distance = get_driven()
            power = calc_power()
            # if self.collided(power, old_power) and full_speed(started_time):
            #    timestamp = time.localtime()

            pids = self.get_pids(speed)
            p_regler = pids[0]
            i_regler = pids[1]
            d_regler = pids[2]
            change = get_gyro_value() #yaw angle used due to orientation of the self.hub


            curren_steering = (change * p_regler + integral * i_regler + d_regler * (change - old_change))
            # curren_steering = 0

            curren_steering = max(-100, min(curren_steering, 100))

            steering_sum += change
            integral += change - old_change
            old_change = change


            #Calculation of speed based on acceleration and braking, calculation of steering value for robot to drive perfectly straight
            if distance <= 0:
                speed = mainspeed
            else:
                speed = self.speed_calculation(speed, deccelerate_distance, brake_start_value, int(driven_distance), int(old_driven_distance), mainspeed = mainspeed, stopspeed = stopspeed)
                braking = True if driven_distance > brake_start_value else False
                curren_steering = 0 if braking else curren_steering

            if avoid_collision:
                self.around_kollision(timestamp, power, old_power, invert * int(curren_steering), int(speed))
            else:
                motor_pair.move(self.MOTPAIR, invert * int(curren_steering), velocity = int(speed))
            # old_power = power

            if distance <= 0:
                if self.stop:
                    loop = False
                    motor_pair.stop(self.MOTPAIR)
                    self.stop = False
            elif rotate_distance < driven_distance:
                    loop = False
                    motor_pair.stop(self.MOTPAIR)
            time.sleep(0.1)

        return True


    def gyro_turn(self, angle: int = 90, mainspeed: int = 300, stopspeed: int = 200, brake_start: float = 0.7, rotate_mode: int = 0, avoid_collision: bool = False) -> bool:
        """Rotate Robot to Angle using Gyrosensor

            Turn the Robot to a given Angle, use Gyro-Sensor to check if angle is reached. Gyro is used for better stopping

            Drehe Roboter um eine gegebene Gradzahl, benutze den GyroSensor um die genaue Gradzahl zu überprüfen.
            Kann durch den GyroSensor abbremsen.

            Parameters / Parameter
            ----------------------
            angle : int = 90
                The angle the robot should turn for.
                Die Gradzahl um die sich der Roboter drehen soll
            mainspeed: int = 300
                The maximum speed the robot reaches.
                Die maximale Geschwindigkeit, die der Roboter erreicht.
            stopspeed : float = 200
                The target speed while braking; the minimum speed at the end of the program.
                Die Zielgeschwindigkeit beim Bremsen; die minimale Geschwindigkeit am Ende des Programms.
            brake_start : int = 0.7
                Percentage of the driven distance after which the robot starts braking.
                Prozentsatz der zurückgelegten Strecke, nach dem der Roboter mit dem Bremsen beginnt.
            rotate_mode : int = 0
                The turning mode: normal_turn[0] or tank_turn[1].
                Der Drehmodus: normal_turn[0] oder tank_turn[1].
            avoid_collision : bool = False
                If the robot should try to avoid every collision
                Ob der Roboter versuchen sollte, Kollisionen auszuweichen
        """

        self.gyroSens.reset_yaw(0)
        time.sleep_ms(10)

        self.old_rotated = 0

        if rotate_mode == 0:
            mainspeed = abs(mainspeed)
            stopspeed = abs(stopspeed)
        # else:
        #    angle = int(angle)

        speed = mainspeed

        rotated_distance = 0
        steering = 1

        deccelerate_distance = abs(angle * (1 - brake_start))


        loop = True
        brake_start_value = (angle + 0) * brake_start

        if angle < 0:
            steering = -1

        while loop:
            rotated_distance = self.gyroSens.tilt_angles()[0] / 10
            speed = self.speed_calculation(speed, int(deccelerate_distance), brake_start_value, int(rotated_distance), int(self.old_rotated), mainspeed = mainspeed, stopspeed = stopspeed)

            # Checking for variants
            # Both Motors turn, robot moves on the spot
            if rotate_mode == 0:
                motor_pair.move_tank(self.MOTPAIR, int(speed) * steering, -int(speed) * steering)

            # Only outer motor turns, robot has a wide turning radius
            elif rotate_mode == 1:

                if angle * speed > 0:
                    motor.run(self.MOTORL, int(speed))
                else:
                    motor.run(self.MOTORR, int(speed))
            self.old_rotated = rotated_distance

            if abs(angle) <= abs(rotated_distance - 0):
                logger.debug((abs(angle), 0, rotated_distance, abs(rotated_distance - 0)))
                loop = False
                break
        motor.stop(self.MOTORL)
        motor.stop(self.MOTORR)
        return True



    def till_colide(self, speed):
        def cycl() -> float:
            return (
                abs(motor.get_duty_cycle(self.MOTORL)) +
                abs(motor.get_duty_cycle(self.MOTORR))) / 2

        motor_pair.move(self.MOTPAIR, 0, velocity=speed)
        time.sleep(0.5)
        start_cycl = cycl()
        while not self.collided(cycl(), start_cycl):
            time.sleep(0.1)
        motor_pair.stop(self.MOTPAIR)
        return True

    def around_kollision(self, timestamp, power, old_power, steering, speed):
        # logger.debug((timestamp, power, old_power))
        motor_pair.move(self.MOTPAIR, steering, velocity = speed)


    #######################
    # Simple Interactions #
    #######################

    def run_motor_duration(self, speed: int = 500, duration: float = 5, *ports: int) -> bool:
        """Run the given Motor

            Start the given ports for a specified time duration.
            If the duration is <= 0 do not stop.

            Starte die gegebenen ports für eine angegebene Zeit.
            Wenn die Zeit <= 0 ist, stoppt der Motor nicht.

            Parameters / Parameter
            -----------------

            speed: int = 500
                How fast the motor should turn
                Wie schnell sich der Motor drehen soll
            duration: float = 5
                How long the motor should run, if <= 0 no stopping
                Wie lange der Motor sich drehen soll, wenn <= 0 stoppt er nicht
            ports: int
                The ports which will be controlled, needs to be specified, otherwise throws Error
                Die Ports die gesteuert werden sollen, muss angegeben sein, sonst kommt ein Fehler
        """
        if len(ports) == 0:
                logger.exception("Please give ports", 40)
                return False
        ports_list = list(ports)
        print(ports_list)

        try:
            for port in ports_list:
                motor.run(port, speed)
            if duration > 0:
                time.sleep(duration)
                for port in ports_list:
                    motor.stop(port, stop = motor.SMART_COAST)
            return True
        except:
            logger.exception("Given unavailable port {}".format(str(ports)), 421)
            return False

    def run_motor_degree(self, speed: int = 500, degree: float = 90, *ports: int, tolerance: float = 5) -> bool:
        """Run the given Motor

            Start the given ports for a specified angle.

            Starte die gegebenen ports für eine angegeben Gradzahl.

            Parameters / Parameter
            -----------------

            speed: int = 500 [degree/second]
                How fast the motor should turn
                Wie schnell sich der Motor drehen soll
            angle: float = 5 [degree]
                How much the motor should turn
                Wie viel sich der Motor drehen soll
            ports: int
                The ports which will be controlled, needs to be specified, otherwise throws Error
                Die Ports die gesteuert werden sollen, muss angegeben sein, sonst kommt ein Fehler
            tolerance: float = 5
                The tolerance the motor checks for between the given and measured angle.
                Die Toleranz der Motor überprüft zwischen der gegebenen und gemessenen Gradzahl
        """
        def reached() -> bool:
            if abs(current_pos - target_pos) <= tolerance:
                return True
            else:
                return False

        try:
            if degree > 0:
                invert = 1
            else:
                invert =-1

            ports_list = [port for port in ports]
            if len(ports) == 0:
                logger.exception("Please give ports", 40)
                return False

            target_pos = degree

            for port in ports_list:
                start_pos = motor.relative_position(port)# Startposition speichern
                motor.run(port, invert * speed)# Motor starten
                # Zielposition berechnen
                target_pos = start_pos + degree

            while True:
                for port in ports_list:
                    current_pos = motor.relative_position(port)
                    if reached():
                        ports_list.remove(port)
                        motor.stop(port, stop = motor.SMART_COAST)
                if len(ports_list) == 0:
                    break
            return True
        except Exception as e:
            logger.exception("Error with motor port(s) {}: {}".format(str(ports), e), 421)
            return False

    def run_action_duration(self, speed: int = 360, duration: float = 5) -> bool:
        """Run the right action/ability motor for time.

        Run the right action motor with given speed, for the given time.

        Drehe den Motor mit dem gegebenen Speed, die gegebene Zeit.

        Parameters / Parameter
        --------------

        speed: float = 700
            The given speed, with which the motor turns, given in degree/s
            Der gegebene Speed mit dem der Motor sich dreht, angegeben in Grad/s
        time: float = 5
            The given time, for which the motor should turn
            Die gegebene Zeit, die sich der Motor drehen soll
        """
        return self.run_motor_duration(speed, duration, self.RIGHT)

    def run_action_degree(self, speed: int = 700, degree: float = 90) -> bool:
        """Run the right action/ability motor for degree

        Run the right action motor until it has turned the given degree. (not a turn to-, but a turn for-action)

        Drehe den Motor mit dem gegebenen Speed bis er sich um die gegebene Gradzahl dreht. (Kein drehen bis auf Position, aber ein drehen um Grad)

        Parameters / Parameter
        --------------

        speed: int = 700
            The given speed, with which the motor turns, given in degree/s
            Der gegebene Speed mit dem der Motor sich dreht, angegeben in Grad/s
        degree: float = 90
            The given degree, for which the motor should turn
            Die gegebene Gradzahl, um die sich der Motor drehen soll
        """
        return self.run_motor_degree(speed, degree, self.RIGHT)

    def run_to_absolute_position(self, position: int = 0, speed: int = 500, *ports: int) -> bool:
        """Run motor(s) to given absolute position

            Run the given motors to the position, waits until position is reached

            Drehe die Motoren auf die Position, wartet bis die Position erreicht ist

            Parameters / Parameter
            ------------

            position: int = 0
                Where the robot should turn to
                Auf welchen Wert sich der Roboter drehen soll
            speed: int = 500
                With which speed the robot should turn
                Mit welcher Geschwindigkeit der Roboter sich drehen soll
            ports: tuple[int, ...]
                Which port should be used
                Welche Ports angesteuert werden sollen

        """

        def reached(port: int) -> bool:
            """
                Return whether the distance is reached
            """
            pos = (motor.absolute_position(port) + 360) % 360
            # print(pos, position)
            if position < 0 and pos <= position:
                motor.stop(port)
                return True
            elif position > 0 and pos >= position:
                motor.stop(port)
                return True
            elif position == 0 and abs(pos) >= 340:
                motor.stop(port)
                return True
            else:
                return False

        def invert(port: int) -> int:
            """
                Return whether the speed should be inverted for this port
            """
            current_pos = self.convert_abs(motor.absolute_position(port))
            if (position - current_pos) > 0:
                logger.debug(-1)
                return -1
            else:
                logger.debug(1)
                return 1

        ports_list = [port for port in ports]
        if len(ports) == 0:
            logger.exception("Please give ports", 40)
            return False
        try:
            for port in ports_list:
                motor.run(port, invert(port) * speed)
        except Exception as e:
            logger.exception("run to absolute position had following error: {}".format(e), 12)
            return False
        while True:
            for port in ports_list:
                pos = (motor.absolute_position(port) + 360) % 360
                if position < 0 and pos <= position:
                    motor.stop(port)
                    ports_list.remove(port)
                elif position > 0 and pos >= position:
                    motor.stop(port)
                    ports_list.remove(port)
                elif position == 0 and pos in range(position, position + 5):
                    print("finish {}".format((motor.absolute_position(port) + 360) % 360))
                    motor.stop(port)
                    print("finish {}".format((motor.absolute_position(port) + 360) % 360))
                    ports_list.remove(port)
            if len(ports_list) == 0:
                break
        return True

    def run_to_relative_position(self, position: int = 0, speed: int = 500, *ports: int) -> bool:
        """Run motor(s) to given relative position

            Run the given motors to the position, waits until position is reached

            Drehe die Motoren auf die Position, wartet bis die Position erreicht ist

            Parameters / Parameter
            ------------

            position: int = 0
                Where the robot should turn to
                Auf welchen Wert sich der Roboter drehen soll
            speed: int = 500
                With which speed the robot should turn
                Mit welcher Geschwindigkeit der Roboter sich drehen soll
            ports: tuple[int, ...]
                Which port should be used
                Welche Ports angesteuert werden sollen

        """

        def reached() -> bool:
            """
                Return whether the distance is reached
            """
            if position > 0 and current_pos >= position:
                return True
            elif position < 0 and current_pos <= position:
                return True
            else:
                return False

        def invert(port) -> int:
            """
                Return whether the speed should be inverted for this port
            """
            current_pos = motor.relative_position(port)
            if (position - current_pos) > 0:
                return -1
            else:
                return 1

        ports_list = [port for port in ports]
        if len(ports) == 0:
            logger.exception("Please give ports", 40)
            return False
        try:
            for port in ports_list:
                motor.run(port, invert(port) * speed)
                pass
        except Exception as e:
            logger.exception("run to relative position had following error: {}".format(e), 12)
            return False
        while True:
            for port in ports_list:
                current_pos = motor.relative_position(port)
                if reached():
                    ports_list.remove(port)
                    motor.stop(port, stop = motor.SMART_COAST)
            if len(ports_list) == 0:
                break
        return True

    def attach_addition(self, attach: bool = True) -> bool:
        """Attach/Detach the addition.

            Attach or detach the addition of the robot.

            Befestige oder Löse Aufsatz vom Roboter.

            Parameters/Parameter
            --------
            attach: bool
                In which state the addition should be set
                In welchen Zustand der Aufsatz gesetzt werden soll
        """
        old_state = self.get_addition_state()
        if attach and not old_state:
            motor.run_to_absolute_position(3, 95, 1000, direction = motor.CLOCKWISE)
            return True
        elif not attach and old_state:
            motor.run_to_absolute_position(3, 0, 1000, direction = motor.COUNTERCLOCKWISE)
            return True
        else:
            return False


    def reset_null(self, *ports: int):
        """Reset given motor to zero

            Reset the position of a given motor to absolute position zero.

            Setze die Position von einem gegebenen Motor auf die absolute Position Null.

            Parameters
            ------

            ports: list[int]

        """
        for port in ports:
            motor.reset_relative_position(port, 0)
            while True:
                current_pos = motor.relative_position(port)
                if abs(current_pos) == 0:
                    break

    def stop_motor(self, *ports) -> bool:
        """Stop given motor

            Stop the motor(s) with given port(s)

            ports: tuple[int]
                The given port(s)
                Die gegebenen Port(s)
        """
        try:
            for port in ports:
                motor.stop(port)
            return True
        except OSError:
            logger.exception("Given unavailable port(s) {}".format(str(ports)), 621)
            return False



    #########################
    # Calculating Functions #
    #########################

    def get_addition_state(self) -> bool:
        """Return state of addition

            Return the state of the addition
            Gib den Zustand des Aufsatzes aus

            Returns / Ausgabe:
            ----------

            True: abs_pos == +-90
                Addition is connected
                Aufsatz ist verbunden
            False: abs_pos == +-0
                Addition is not connected
                Aufsatz ist getrennt
        """
        if motor.absolute_position(3) in range(80, 100, 1):
            self.addition_state = True
            return True
        elif motor.absolute_position(3) in range(-10, 10, 1):
            self.addition_state = False
            return False
        else:
            motor.run_to_absolute_position(3, 0, 1000, direction = motor.COUNTERCLOCKWISE)
            logger.debug("State {}° inbetweeen, open completely".format(motor.absolute_position(3)))
            self.addition_state = False
            return False

    def speed_calculation(self, speed: int, deccelerate_distance: float, brake_start_value: float, driven: int, old_driven: int, mode: int = 0, rotate_mode: int = 0, mainspeed: int = 300, stopspeed: int = 300):
        """Calculating the speed depending on all given parameters

            Used to calculate all the speeds in our programs.
            Executed separately to reduce redundancy.

            Wird verwendet, um alle Geschwindigkeiten in unseren Programmen zu berechnen.
            Wird separat ausgeführt, um Redundanz zu reduzieren.

            Parameters / Parameter
            ----------------------
            speed : int
                The current speed of the robot.
                Die aktuelle Geschwindigkeit des Roboters.
            deccelerate_distance: float
                The distance at which the robot starts to deccelerate.
                Die Distanz, ab welcher der Roboter anfängt zu bremsen.
            brakeStartValue : float
                Percentage of the driven distance after which the robot starts braking.
                Prozentsatz der zurückgelegten Strecke, nach dem der Roboter mit dem Bremsen beginnt.
            driven : int
                Distance the robot has currently traveled.
                Strecke, die der Roboter aktuell zurückgelegt hat.
            old_driven : int
                Distance the robot traveled during the last function call.
                Strecke, die der Roboter beim letzten Aufruf zurückgelegt hat.
            mode : int = 0
                The mode the robot operates in: turn[0] or drive[1].
                Der Modus, in dem der Roboter arbeitet: turn[0] oder drive[1].
            rotate_mode : int = 0
                The turning mode: normal_turn[0] or tank_turn[1].
                Der Drehmodus: normal_turn[0] oder tank_turn[1].
            mainspeed : int = 300
                The maximum speed the robot reaches.
                Die maximale Geschwindigkeit, die der Roboter erreicht.
            stopspeed : int = 300
                The target speed while braking; the minimum speed at the end of the program.
                Die Zielgeschwindigkeit beim Bremsen; die minimale Geschwindigkeit am Ende des Programms.
        """


        if rotate_mode == 1:
            if mainspeed in range(-300, 300):
                return mainspeed
            else:
                return int(math.copysign(1, mainspeed)) * 300


        if mode == 0:
            deccelerate_distance = max(deccelerate_distance, 1)
            sub_speed_per_degree = (mainspeed - stopspeed) / deccelerate_distance


            subtraction = (abs(driven) - abs(old_driven) if abs(driven) - abs(old_driven) >= 1 else 1) * sub_speed_per_degree

            if abs(driven) > abs(brake_start_value):

                if abs(speed) > abs(stopspeed):
                    speed = int(speed - subtraction)

            return speed
        else:
            deccelerate_distance = max(deccelerate_distance, 1)
            sub_speed_per_degree = (mainspeed - stopspeed) / deccelerate_distance

            subtraction = (abs(driven) - abs(old_driven) if abs(driven) - abs(old_driven) >= 1 else 1) * sub_speed_per_degree

            if abs(driven) > abs(brake_start_value):
                if abs(speed) > abs(stopspeed):
                    speed = int(speed - subtraction)
            return speed

    def get_pids(self, speed: float) -> tuple[float, float, float]:
        """Calculation of PID Values.

            Return the PID Values depending on the given speed.

            Gib die PID-Werte aus, abhängig davon, wie schnell der Roboter fährt

            Returns / Ausgabe
            -----
            (pRegler, iRegler, dRegler=1)

        """

        speed = abs(speed)
        def pRegler():
            return (
                14.59
                - 0.177132762 * speed
                + 0.000920045989 * speed**2
                - 2.34879006e-6 * speed**3
                + 3.15365919e-9 * speed**4
                - 2.15176282e-12 * speed**5
                + 5.90277778e-16 * speed**6
            )

        def iRegler():
            return (
                4.30433333
                - 0.0374442063 * speed
                + 0.00018870942 * speed**2
                - 5.52917468e-7 * speed**3
                + 8.790625e-10 * speed**4
                - 6.96201923e-13 * speed**5
                + 2.14583333e-16 * speed**6
            )


        if speed > 0:
            pids = (pRegler(), iRegler(), 1)
        else:
            pids = (pRegler(), iRegler(), 1)

        return pids

    def collided(self, cycl, start_cycl):
        diff = cycl - start_cycl
        if diff > 300:
            return True
        else:
            return False

    def convert_abs(self, abs_pos: int = 0) -> int:
        return (abs_pos + 360) % 360

def convert_abs(abs_pos: int = 0) -> int:
        return (abs_pos + 360) % 360

logger = Logger(FULL)

# ctrl = Controller()

db = DriveBase()


# def main():
#    ctrl.run()
#    ctrl.kill()

def testing():
    db.reset_null(5, 4, 0)
    # db.run_motor_duration(500, 5, 5)
    # db.run_motor_degree(500, 90, 5)
    # db.run_action_duration()
    # db.run_action_degree()
    print("Now to abs: {}".format(convert_abs(-170)))

    motor.run_to_absolute_position(5, 0, 300, direction = motor.CLOCKWISE)
    # time.sleep(1)
    db.run_to_absolute_position(0, 500, 5)
    print(convert_abs(motor.absolute_position(5)))
    # print("Now to rel: {}".format(motor.relative_position(5)))
    # db.run_to_relative_position(200, 500, 5)
    db.attach_addition(True)
    db.attach_addition(False)

# Start the main async function
if __name__ == "__main__":
    testing()
    # raise Exception("Program Ended")