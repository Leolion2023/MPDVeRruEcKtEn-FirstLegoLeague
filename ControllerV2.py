import hub
import motor
import motor_pair
import color_sensor
import device

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
        # Setze das Logging-Level hier (FULL, MEDIUM, LOW oder NO)
        self.logging_level = self.FULL
        self.device = self.BOTH

        self.driveBase = DriveBase()

        logger.info("Started Program", 0)


    #############
    # Internals #
    #############

    def __button_check__(self, which: int) -> bool:
        """"""
        if which == 0:
            return bool(
                hub.button.pressed(hub.button.LEFT)
                or hub.button.pressed(hub.button.RIGHT)
            )
        elif which == 1:
            return bool(hub.button.pressed(hub.button.LEFT))
        elif which == 2:
            return bool(hub.button.pressed(hub.button.RIGHT))
        else:
            logger.exception("UNKNOWN WHICH STATE", 303)
            return False

    def __connect_addition__(self):
        self.driveBase.attach_addition(False)
        logger.info("WAITING", "START")
        time.sleep_ms(500)
        logger.info("WAITING", 10)
        while not self.__button_check__(0):
            pass
        self.driveBase.attach_addition(True)
        time.sleep(0.5)

    ##################
    # MAIN FUNCTIONS #
    ##################

    def kill(self):
        logger.info("Killed program", -1)
        self._kill_ = True

    ###############
    # RUN PROGRAM #
    ###############

    def run_program(self):
        logger.info("Run Program", 1)

        self.test_gyro_turn()
        # self.collect_items_krake()
        # self.flagge_alignment()
        # self.probe_push_up()
        # self.do_nest()
        # self.test_rotating()

    ########################
    # Tasks for Robot Game #
    ########################
    
    def collect_items_krake(self):
        db = self.driveBase
        db.run_action_duration(-200, 0)
        self.__connect_addition__()
        db.stop_motor(db.ADDITION)

        db.gyro_turn(-45, 200, 60, rotate_mode = 1)   ##
        db.gyro_drive(47, 900, 500, 0.9)
        db.gyro_drive(25, -600, -100)
        db.gyro_turn(37, 200, 60)
        db.gyro_drive(51, 600, 100, 0.8)   ## drive forward to next task
        db.gyro_turn(-87, 200, 60)  ## turn to next task
        db.gyro_drive(15, -400, -200) ## push into task
        db.gyro_drive(10, 400, 200)  ## Pull out of task
        db.gyro_turn(-10, 200, 60)
        db.gyro_drive(17, 300, 200)
        db.gyro_turn(10, 200, 60)
        db.gyro_drive(24, 300, 100)
        db.gyro_turn(30, 200, 60)
        self.flagge_alignment()

    def flagge_alignment(self):
        db = self.driveBase
        db.till_collide(400, 800, 5)
        db.gyro_drive(2, -200, -100)
        db.till_color(-400, 2, 300, 2)
        db.gyro_drive(2, -300, -80)
        db.gyro_turn(-42, 200, 60)
        db.gyro_drive(27, 300, 200)
        self.pull_probe()
    
    def pull_probe(self):
        db = self.driveBase
        db.run_action_duration(900, 0.5)
        db.gyro_drive(20, 400, 200)
        db.run_action_duration(-100, 1)
        self.collect_left_items()

    def collect_left_items(self):
        db = self.driveBase
        db.gyro_turn(-16, 200, 60)
        db.gyro_drive(35, 300, 200)
        db.gyro_turn(-30, 200, 60)
        db.gyro_drive(20, 300, 100)
        

    def probe_push_up(self):
        db = self.driveBase
        db.attach_addition(True)
        db.till_collide(-600, 700)
        db.gyro_drive(60, 600, 200)
        db.till_collide(-600, 700)
        db.gyro_turn(-30, 400, 100, rotate_mode = 1)

    def do_nest(self):
        db = self.driveBase
        db.attach_addition(True)
        db.gyro_drive(16, 400, 200)
        db.gyro_turn(30, 100, 50)
        db.gyro_drive(20, 400, 300, stop=False)
        db.gyro_turn(-6, 100, 10)
        db.gyro_drive(21, 400, 100)
        db.gyro_turn(50, 100, 50)
        db.gyro_drive(5, -200, -100)
        db.gyro_turn(10, 100, 80)
        db.gyro_drive(40, 500, 300)  # Drive into Nest
        db.gyro_drive(13, -500, -300)  # Drive out of nest
        db.gyro_turn(-40, 400, 100) # Turn first part left
        db.gyro_drive(16, -300, -200) # drive backwards to escape coralriff and align with corals
        db.gyro_turn(-38, 300, 200) # Press Corals inside
        db.gyro_drive(10, -200, -200, stop=False)
        db.gyro_turn(15, 100, 50)
        db.gyro_drive(40, -900, -900)
        db.gyro_turn(-40, -900, -100, rotate_mode = 1)
        db.till_collide(-500, 1000)

    def mini_krake(self):
        db = self.driveBase
        db.gyro_drive(40, 400, 400, stop = False)

    


    def forschungsauftrag_demo(self):
        self.__connect_addition__()
        self.driveBase.gyro_drive(100, 800, 500)


    ###########
    # TESTING #
    ###########

    def test_gyro_turn(self):
        logger.info("Run Program", 1)
        self.driveBase.gyro_turn(90)
        logger.info(self.driveBase.gyroSens.tilt_angles()[0] / 10, 2)
        time.sleep(1)
        logger.info(self.driveBase.gyroSens.tilt_angles()[0] / 10, 2)
        #nur der zweite ist korrekt!!!!

    def test_rotating(self):
        db = self.driveBase

        # db.gyro_turn(90, 300, 100, rotate_mode = 1)
        # db.gyro_turn(90, -300, -100, rotate_mode = 1)
        # db.gyro_turn(-90, 300, 100, rotate_mode = 1)
        db.gyro_turn(-90, -300, -100, rotate_mode = 1)

    def action_change_debug(self):
        motor.reset_relative_position(self.driveBase.RIGHT, 0)
        while True:
            if self.__button_check__(1):
                self.driveBase.run_motor_duration(100, 0, self.driveBase.RIGHT)
                time.sleep(0.2)
            elif self.__button_check__(2):
                self.driveBase.run_motor_duration(-100, 0, self.driveBase.RIGHT)
                time.sleep(0.2)
            else:
                self.driveBase.stop_motor(self.driveBase.RIGHT)
                time.sleep(0.5)


class Logger:
    def __init__(self, level):
        self.log_level = level

    def debug(self, message, *args):
        print("[DEBUG] {}".format(message))

    def info(self, message, code=None, *args):
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

    TYPEMOTOR = 0
    TYPECOLORSENS = 1

    MOTORR = 0
    ADDITION = 3
    MOTORL = 4
    RIGHT = 5
    COLORSENS = 2

    MOTPAIR = 0

    WHEELCIRC = 17.6

    def __init__(self):
        self.gyroSens = hub.motion_sensor
        self.stop = False

        motor_pair.pair(self.MOTPAIR, self.MOTORL, self.MOTORR)

        self.addition_state = self.get_addition_state()
        self.attach_addition(False)

    def configure(
        self,
        motor_right_port: int = 0,
        motor_left_port: int = 4,
        addition_port: int = 3,
        action_port: int = 5,
        motor_pair_id: int = 0,
        wheel_circumference: float = 17.6,
    ):
        """
        Configure the Motorports and other values

        Konfiguriere die Motorports und andere Werte

        Parameters / Parameter
        -----------------

        motor_right_port: int = 0
            The port of the right motor.
            Der Port des rechten Motors.
        motor_left_port: int = 4
            The port of the left motor.
            Der Port des linken Motors.
        addition_port: int = 3
            The port of the addition motor.
            Der Port des Zusatzmotors.
        action_right_port: int = 5
            The port of the right action motor.
            Der Port des rechten Aktionsmotors.
        motor_pair_id: int = 0
            The ID of the motorpair.
            Die ID des Motorpaares.
        wheel_circumference: float = 17.6
            The circumference of the wheels.
            Der Umfang der Räder.
        """
        self.MOTORR = motor_right_port
        self.MOTORL = motor_left_port
        self.ADDITION = addition_port
        self.RIGHT = action_port
        self.MOTPAIR = motor_pair_id
        self.WHEELCIRC = wheel_circumference

    #########################
    # Complex GyroFunctions #
    #########################

    def gyro_drive(
        self,
        distance: float = 100,
        mainspeed: int = 600,
        stopspeed: int = 300,
        brake_start: float = 0.7,
        offset: int = 0,
        avoid_collision: bool = False,
        stop: bool = True,
    ) -> bool:
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
            Ob der Roboter versuchen sollte, Kollisionen auszuweichen                                                                   WARNING NEED TO DOCUMENT
        """
        hub.motion_sensor.reset_yaw(0)
        time.sleep_ms(10)
        motor.reset_relative_position(self.MOTORL, 0)
        motor.reset_relative_position(self.MOTORR, 0)

        def get_gyro_value() -> int:
            return round(hub.motion_sensor.tilt_angles()[0] / 10)

        def get_driven():
            return (
                abs(motor.relative_position(self.MOTORL))
                + abs(motor.relative_position(self.MOTORR))
            ) / 2

        def calc_power() -> float:
            return (
                abs(motor.get_duty_cycle(self.MOTORL))
                + abs(motor.get_duty_cycle(self.MOTORR))
            ) / 2

        def full_speed(started) -> bool:
            logger.debug((int(calc_power() / 1000), mainspeed / 100))
            if not time.time() - started > 1:
                logger.debug(
                    "Time False: {} von Now: {} then {}".format(
                        time.time() - started, time.time(), started
                    )
                )
                return True
            if int(calc_power() / 1000) > mainspeed / 100:
                logger.debug(True)
                return True
            else:
                logger.debug(False)
                return False

        # Set starting speed of robot
        speed = mainspeed
        # Sets PID values

        change = 0
        old_change = 0
        integral = 0
        steering_sum = 0
        power = 0
        old_power = 0

        timestamp = 0

        invert = 1

        # Sets values based on user inputs
        loop = True

        # Calulation of degrees the motors should turn to
        # 17.6 is wheel circumference in cm. You might need to adapt it
        rotate_distance = (distance / self.WHEELCIRC) * 360
        deccelerate_distance = rotate_distance * (1 - brake_start)

        # Inversion of target rotation value for negative values
        if speed < 0:
            invert = -1

        # Calculation of braking point
        brake_start_value = brake_start * rotate_distance
        driven_distance = get_driven()

        motor_pair.move(self.MOTPAIR, 0, velocity=int(speed))
        started_time = time.time()

        power = calc_power()
        old_power = power

        while loop:

            # Calculation of driven distance and PID values
            old_driven_distance = driven_distance
            driven_distance = get_driven()
            power = calc_power()
            # if self.collided(power, old_power) and full_speed(started_time):
            #    timestamp = time.localtime()

            pids = self.get_pids(speed)
            p_regler = pids[0]
            i_regler = pids[1]
            d_regler = pids[2]
            change = (
                get_gyro_value()
            )  # yaw angle used due to orientation of the self.hub

            curren_steering = (
                change * p_regler
                + integral * i_regler
                + d_regler * (change - old_change)
            )
            # curren_steering = 0

            curren_steering = max(-100, min(curren_steering, 100))

            steering_sum += change
            integral += change - old_change
            old_change = change

            # Calculation of speed based on acceleration and braking, calculation of steering value for robot to drive perfectly straight
            if distance <= 0:
                speed = mainspeed
            else:
                speed = self.speed_calculation(
                    speed,
                    deccelerate_distance,
                    brake_start_value,
                    int(driven_distance),
                    int(old_driven_distance),
                    mainspeed=mainspeed,
                    stopspeed=stopspeed,
                )
                braking = True if driven_distance > brake_start_value else False
                curren_steering = 0 if braking else curren_steering

            if avoid_collision:
                self.around_kollision(
                    timestamp,
                    power,
                    old_power,
                    invert * int(curren_steering),
                    int(speed),
                )
            else:
                motor_pair.move(
                    self.MOTPAIR, invert * int(curren_steering), velocity=int(speed)
                )
            # old_power = power

            if distance <= 0:
                if self.stop:
                    loop = False
                    motor_pair.stop(self.MOTPAIR)
                    self.stop = False
            elif rotate_distance < driven_distance and stop:
                loop = False
                motor_pair.stop(self.MOTPAIR)
            elif rotate_distance < driven_distance:
                loop = False
            time.sleep(0.1)
        self.gyro_turn(change, 100)
        time.sleep_ms(100)
        return True

    def gyro_turn(
        self,
        angle: int = 90,
        mainspeed: int = 300,
        stopspeed: int = 200,
        brake_start: float = 0.7,
        rotate_mode: int = 0,
        avoid_collision: bool = False,
    ) -> bool:
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
        loop = True
        while loop:
            rotated_distance = self.gyroSens.tilt_angles()[0] / 10
            speed = max(math.pow(abs((abs(rotated_distance) - abs(angle))),1.6),30)
            if abs(rotated_distance) > abs(angle):
                speed *= -1
            logger.info(speed,1)
            logger.info(rotated_distance,1)
            # Checking for variants
            # Both Motors turn, robot moves on the spot
            if rotate_mode == 0:
                motor_pair.move_tank(
                    self.MOTPAIR, int(speed) * steering, -int(speed) * steering
                )

            # Only outer motor turns, robot has a wide turning radius
            elif rotate_mode == 1:

                if angle * speed > 0:
                    motor.run(self.MOTORL, int(speed))
                else:
                    motor.run(self.MOTORR, int(speed))
            self.old_rotated = rotated_distance

            if abs(abs(angle)-abs(rotated_distance)) <= 1:
                time.sleep_ms(20)
                if abs(abs(angle)-abs(self.gyroSens.tilt_angles()[0] / 10)) <= 1:
                    logger.debug(
                        (abs(angle), 0, rotated_distance, abs(rotated_distance))
                    )
                    loop = False
                    break
        motor.stop(self.MOTORL)
        motor.stop(self.MOTORR)
        return True

    
    def turn_till_color(self, direction: int = 1, speed: int = 360, color_type: int = 0, color_gate: int = 700, timeout: int = -1):
        """

            direction (either -1 or 1 idk which is which, ig -1 is left and 1 is right)
        
        """

        self.auto_detect_device(self.TYPECOLORSENS)
        if timeout > 0:
            motor_pair.move_for_time(self.MOTPAIR, timeout, direction * 100, velocity = speed)
        else:
            motor_pair.move(self.MOTPAIR, direction * 100, velocity = speed)
        
        start_time = time.ticks_ms()

        while True:
            color_val = color_sensor.rgbi(self.COLORSENS)[color_type]

            if color_val <= color_gate:
                break
            elif (time.ticks_ms() - start_time) / 1000 > timeout:
                logger.debug((time.ticks_ms() - start_time) / 1000)
                break
            else:
                time.sleep_ms(50)
        motor.stop(self.MOTPAIR)
    
    def turn_till_reflect(self, direction: int = 1, speed: int = 360, reflection_gate: int = 700, smaller_than: int = True, timeout: int = -1):
        """

            direction (either -1 or 1 idk which is which, ig -1 is left and 1 is right)

        """

        self.auto_detect_device(self.TYPECOLORSENS)
        motor_pair.move(self.MOTPAIR, direction * 100, velocity = speed)

        start_time = time.ticks_ms()

        while True:
            reflection_val = color_sensor.reflection(self.COLORSENS)

            if smaller_than and reflection_val <= reflection_gate:
                break
            elif not smaller_than and reflection_val >= reflection_gate:
                break
            elif (time.ticks_ms() - start_time) / 1000 > timeout:
                logger.debug((time.ticks_ms() - start_time) / 1000)
                break
            else:
                time.sleep_ms(50)
        print("FInish")
        motor.stop(self.MOTPAIR)

    def till_collide(self, speed, gate: int = 300, timeout: int = -1):
        def cycl() -> float:
            return (
                abs(motor.get_duty_cycle(self.MOTORL))
                + abs(motor.get_duty_cycle(self.MOTORR))
            ) / 2

        motor_pair.move(self.MOTPAIR, 0, velocity=speed)
        time.sleep(0.5)
        start_cycl = cycl()
        start_time = time.ticks_ms()
        while True:
            if self.collided(cycl(), start_cycl, gate):
                break
            elif (time.ticks_ms() - start_time) / 1000 > timeout:
                logger.debug(abs(time.ticks_diff(start_time, time.ticks_ms)) / 1000)
                break
            else:
                time.sleep_ms(50)
        motor_pair.stop(self.MOTPAIR)
        return True
    
    def till_color(self, speed: int, color_type: int = 0, color_gate: int = 700, timeout: int = -1):
        self.auto_detect_device(self.TYPECOLORSENS)
        # if timeout > 0:
        #     motor_pair.move_for_time(self.MOTPAIR, timeout, 0, velocity = speed)
        # else:
        motor_pair.move(self.MOTPAIR, 0, velocity = speed)
        
        start_time = time.ticks_ms()

        loop = True

        while loop:
            color_val = color_sensor.rgbi(self.COLORSENS)[color_type]

            if color_val <= color_gate:
                loop = False
                break
            elif (time.ticks_ms() - start_time) / 1000 > timeout:
                loop = False
                break
            else:
                time.sleep_ms(50)
            if not loop:
                print("IDK what happens")
        print("Finish")
        motor.stop(self.MOTPAIR)
        
        

    def around_kollision(self, timestamp, power, old_power, steering, speed):
        # logger.debug((timestamp, power, old_power))
        motor_pair.move(self.MOTPAIR, steering, velocity=speed)

    #######################
    # Simple Interactions #
    #######################

    def run_motor_duration(
        self, speed: int = 500, duration: float = 5, *ports: int
    ) -> bool:
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
                    motor.stop(port, stop=motor.SMART_COAST)
            return True
        except:
            logger.exception("Given unavailable port {}".format(str(ports)), 421)
            return False

    def run_motor_degree(
        self, speed: int = 500, degree: float = 90, *ports: int, tolerance: float = 5
    ) -> bool:
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
                invert = -1

            ports_list = [port for port in ports]
            if len(ports) == 0:
                logger.exception("Please give ports", 40)
                return False

            target_pos = degree

            for port in ports_list:
                start_pos = motor.relative_position(port)  # Startposition speichern
                motor.run(port, invert * speed)  # Motor starten
                # Zielposition berechnen
                target_pos = start_pos + degree

            while True:
                for port in ports_list:
                    current_pos = motor.relative_position(port)
                    if reached():
                        ports_list.remove(port)
                        motor.stop(port, stop=motor.SMART_COAST)
                if len(ports_list) == 0:
                    break
            return True
        except Exception as e:
            logger.exception(
                "Error with motor port(s) {}: {}".format(str(ports), e), 421
            )
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

    def run_to_absolute_position(
        self, position: int = 0, speed: int = 500, *ports: int
    ) -> bool:
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
            logger.exception(
                "run to absolute position had following error: {}".format(e), 12
            )
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
                    print(
                        "finish {}".format((motor.absolute_position(port) + 360) % 360)
                    )
                    motor.stop(port)
                    print(
                        "finish {}".format((motor.absolute_position(port) + 360) % 360)
                    )
                    ports_list.remove(port)
            if len(ports_list) == 0:
                break
        return True

    def run_to_relative_position(
        self, position: int = 0, speed: int = 500, *ports: int
    ) -> bool:
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
            logger.exception(
                "run to relative position had following error: {}".format(e), 12
            )
            return False
        while True:
            for port in ports_list:
                current_pos = motor.relative_position(port)
                if reached():
                    ports_list.remove(port)
                    motor.stop(port, stop=motor.SMART_COAST)
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
            motor.run_to_absolute_position(3, 95, 1000, direction=motor.SHORTEST_PATH)
            return True
        elif not attach and old_state:
            motor.run_to_absolute_position(3, 0, 1000, direction=motor.SHORTEST_PATH)
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

    def auto_detect_device(self, device_type: int) -> list[int]:
        devices = []
        for i in range(6):
            try:
                if device_type == self.TYPEMOTOR:
                    motor.relative_position(i)
                elif device_type == self.TYPECOLORSENS:
                    color_sensor.rgbi(i)
                else:
                    logger.exception("Please specify a correct device_type: 0/1", 404)
                    continue
            except:
                continue
            devices.append(i)
        if device_type == self.TYPECOLORSENS:
            self.COLORSENS = devices[0]
        return devices

    def get_addition_state(self) -> bool:
        """Return state of addition

        Return the state of the addition
        Gib den Zustand des Aufsatzes aus

        Returns / Ausgabe:
        ----------

        True: abs_pos == +-90
            Addition is connected
            Aufsatz ist verbunden
        False: abs_pos == +-0 or abs_pos == +-180
            Addition is not connected
            Aufsatz ist getrennt
        """
        if motor.absolute_position(3) in range(80, 100, 1):
            self.addition_state = True
            return True
        elif motor.absolute_position(3) in range(-10, 10, 1):
            self.addition_state = False
            return False
        elif motor.absolute_position(3) in range(170, 190, 1):
            return False
        else:
            motor.run_to_absolute_position(3, 0, 1000, direction=motor.SHORTEST_PATH)
            logger.debug(
                "State {}° inbetweeen, open completely".format(
                    motor.absolute_position(3)
                )
            )
            self.addition_state = False
            return False

    def speed_calculation(
        self,
        speed: int,
        deccelerate_distance: float,
        brake_start_value: float,
        driven: int,
        old_driven: int,
        mode: int = 0,
        rotate_mode: int = 0,
        mainspeed: int = 300,
        stopspeed: int = 300,
    ):
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

            subtraction = (
                abs(driven) - abs(old_driven)
                if abs(driven) - abs(old_driven) >= 1
                else 1
            ) * sub_speed_per_degree

            if abs(driven) > abs(brake_start_value):

                if abs(speed) > abs(stopspeed):
                    speed = int(speed - subtraction)

            return speed
        else:
            deccelerate_distance = max(deccelerate_distance, 1)
            sub_speed_per_degree = (mainspeed - stopspeed) / deccelerate_distance

            subtraction = (
                abs(driven) - abs(old_driven)
                if abs(driven) - abs(old_driven) >= 1
                else 1
            ) * sub_speed_per_degree

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

    def collided(self, cycl, start_cycl, gate: int = 300):
        diff = cycl - start_cycl
        if diff > gate:
            return True
        else:
            return False

    def convert_abs(self, abs_pos: int = 0) -> int:
        return (abs_pos + 360) % 360


def convert_abs(abs_pos: int = 0) -> int:
    return (abs_pos + 360) % 360


logger = Logger(FULL)

ctrl = Controller()


def main():
    ctrl.run_program()
    ctrl.kill()


# Start the main async function
if __name__ == "__main__":
    main()
    raise Exception("Program Ended")
