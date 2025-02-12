"""

    def reset_addition_riff(self):
        motor.run_for_degrees(self.driveBase.RIGHT, 10, 100000)
        time.sleep(0.5)
        self.driveBase.reset_null(self.driveBase.RIGHT)
        time.sleep(0.2)
        # motor.run_for_degrees(self.driveBase.RIGHT, -800, 500)
        self.driveBase.run_motor_degree(self.driveBase.RIGHT, 800, -710, tolerance=10)
        time.sleep(0.1)
        self.driveBase.reset_null(self.driveBase.RIGHT)

    def collect_all(self):
        db = self.driveBase
        db.till_colide(500)
        db.till_color(-300, 2, 600)
    def drive_testing(self, speed):
        self.driveBase.gyro_drive(100, speed, speed - 100)
        self.driveBase.gyro_drive(50, -speed, -speed - 100)
        self.driveBase.gyro_turn(90, speed, speed - 100)
        self.driveBase.gyro_drive(50, speed, speed - 100)
        self.driveBase.gyro_drive(50, -speed, -speed - 100)
        self.driveBase.gyro_turn(90, speed, speed - 100)
        self.driveBase.gyro_drive(50, speed, speed - 100)
        self.driveBase.gyro_drive(50, -speed, -speed - 100)
        self.driveBase.gyro_turn(90, speed, speed - 100)
        self.driveBase.gyro_drive(50, speed, speed - 100)
        self.driveBase.gyro_drive(50, -speed, -speed - 100)
        self.driveBase.gyro_turn(90, speed, speed - 100)
        self.driveBase.gyro_drive(50, speed, speed - 100)
        self.driveBase.gyro_drive(50, -speed, -speed - 100)
        self.driveBase.gyro_drive(50, -speed, -speed - 100)

    def krake(self):
        db = self.driveBase
        db.attach_addition(False)
        motor.run_to_absolute_position(5, 45, 1000, direction=motor.SHORTEST_PATH)
        logger.info("WAITING", "START")
        while not self.__button_check__(0):
            pass
        db.attach_addition(True)
        motor.stop(5, stop=motor.BRAKE)
        db.gyro_drive(2, 500, 100)
        db.gyro_turn(-47, 100, 100)
        db.gyro_drive(50, 500, 1000) # get kraken
        db.gyro_drive(20, -500, -100) # rückwärts??
        db.gyro_turn(-23, 100, 100)
        db.gyro_drive(45, 500, 100)
        db.gyro_turn(32, 100, 100)
        db.gyro_drive(20, 500, 100)
        db.run_motor_duration(68, 1.5, db.RIGHT)# release kraken | open gate
        db.run_motor_duration(-600, 0.5, db.RIGHT) # close gate
        # db.gyro_drive(5, 500, 100)
        # db.gyro_turn(-23, 500, 500) # fisch einklappen| will be done later on
        db.gyro_turn(-10, 300, 200)
        db.gyro_drive(24, 500, 100) # einsammeln item 1
        db.gyro_turn(-30, 500, 500)
        db.gyro_turn(5, 200, 200)
        db.gyro_drive(25, 500, 100)
        db.gyro_turn(-20, 100, 100)
        db.gyro_drive(10, 500, 100)# einsammeln koralle 1
        db.gyro_turn(-20, 100, 100)
        db.gyro_turn(-30, 20, 20)# verschieben koralle 2
        db.gyro_turn(10, 100, 20)
        db.attach_addition(False)
        db.gyro_drive(80, 1000, 100)


    def collide_testing(self):
        self.driveBase.gyro_drive(80, 200, 200, avoid_collision=True)
        logger.info("Finished", 23)

    def gyro_backwards(self):
        # self.driveBase.gyro_drive(70, -900, -500)
        self.driveBase.gyro_drive(70, 300, 200)

    def drive_to_me(self, direction: int):
        self.driveBase.gyro_drive(60, direction * 800, direction * 600)

    def dreizack(self):
        self.driveBase.attach_addition(False)
        self.driveBase.run_motor_duration(20, -1, self.driveBase.RIGHT)
        motor.run_to_absolute_position(
            5, 45, 1000, direction=motor.SHORTEST_PATH)
        while not self.__button_check__(0):
            pass
        self.driveBase.attach_addition(True)
        time.sleep(0.2)
        motor.run_to_absolute_position(
            5, 5, 1000, direction=motor.SHORTEST_PATH)
        time.sleep(0.2)
        motor.run_to_absolute_position(
            5, 5, 1000, direction=motor.SHORTEST_PATH)
        time.sleep(0.2)
        self.driveBase.run_motor_duration(300, 0.3, self.driveBase.RIGHT)
        motor.stop(5, stop=motor.BRAKE)
        while not self.__button_check__(0):
            pass
        self.driveBase.gyro_drive(30, 500, 100)
        self.driveBase.gyro_turn(90, 100, 100)
        self.driveBase.gyro_drive(60, 500, 100)
        self.driveBase.gyro_turn(-90, 200, 100)
        # deploy hai
        self.driveBase.run_motor_duration(-100, 1, self.driveBase.RIGHT)
        self.driveBase.reset_null(self.driveBase.RIGHT)
        # self.driveBase.run_motor_duration(1,-300,0.3)
        motor.run_to_relative_position(self.driveBase.RIGHT, 80, 100)
        self.driveBase.gyro_turn(-90, 200, 100)
        self.driveBase.gyro_drive(6, 500, 100)
        self.driveBase.gyro_turn(90, 200, 100)
        self.driveBase.gyro_drive(10, 100, 100)
        motor.run_to_relative_position(
            self.driveBase.RIGHT, 100, 200)# take dreizack
        # self.driveBase.run_motor_duration(1,-300,0.2)
        self.driveBase.gyro_drive(10, -500, -100)
        self.driveBase.gyro_turn(-110, 300, 100)
        self.driveBase.gyro_drive(80, 800, 100)
        self.driveBase.run_motor_duration(300, 0.1, self.driveBase.RIGHT)
        # homebase
        while not self.__button_check__(0):
            pass
        self.driveBase.gyro_drive(20, 100, 100)
        self.driveBase.run_motor_duration(-300, 0.3, self.driveBase.RIGHT)
        motor.run_to_relative_position(self.driveBase.RIGHT, 90, -300)
        time.sleep(0.5)
        self.driveBase.gyro_drive(30, -900, -100)
        self.driveBase.attach_addition(False)
        time.sleep(0.2)
        self.driveBase.run_motor_duration(500, 2, self.driveBase.RIGHT)

    def deploy_koralle(self):
        self.driveBase.attach_addition(False)
        self.driveBase.run_motor_duration(20, -1, self.driveBase.RIGHT)
        motor.run_to_absolute_position(
            5, 45, 1000, direction=motor.SHORTEST_PATH)
        while not self.__button_check__(0):
            pass
        self.driveBase.attach_addition(True)
        time.sleep(0.2)
        motor.run_to_absolute_position(
            5, 5, 1000, direction=motor.SHORTEST_PATH)
        time.sleep(0.2)
        motor.run_to_absolute_position(
            5, 5, 1000, direction=motor.SHORTEST_PATH)
        time.sleep(0.2)
        self.driveBase.run_motor_duration(300, 0.3, self.driveBase.RIGHT)
        motor.stop(5, stop=motor.BRAKE)
        while not self.__button_check__(0):
            pass
        self.driveBase.gyro_drive(20, 100, 100)
        self.driveBase.run_motor_duration(-300, 0.3, self.driveBase.RIGHT)
        motor.run_to_relative_position(
            self.driveBase.RIGHT, motor.relative_position(self.driveBase.RIGHT) + 90, -300)
        time.sleep(0.5)
        self.driveBase.gyro_drive(30, -900, -100)
        self.driveBase.attach_addition(False)
        time.sleep(0.2)
        self.driveBase.run_motor_duration(500, 2, self.driveBase.RIGHT)

    def get_shark(self):
        self.driveBase.attach_addition(False)
        self.driveBase.run_motor_duration(100, -1, self.driveBase.RIGHT)
        self.driveBase.run_motor_duration(5, 100, -1)
        while not self.__button_check__(0):
            pass
        self.driveBase.attach_addition(True)
        self.driveBase.run_motor_duration(1000, -1, self.driveBase.RIGHT)
        self.driveBase.gyro_drive(20, 500, 100)
        self.driveBase.run_motor_duration(-1000, -1, self.driveBase.RIGHT)
        self.driveBase.gyro_drive(45, 500, 100)
        motor.stop(self.driveBase.RIGHT, stop=motor.BRAKE)
        self.driveBase.gyro_turn(-90, 100, 100)
        self.driveBase.run_motor_duration(1000, -1, self.driveBase.RIGHT)
        self.driveBase.gyro_drive(20, 900, 500)# press korallenriff
        self.driveBase.gyro_drive(14, -500, -100)
        motor.stop(self.driveBase.RIGHT, stop=motor.BRAKE)
        self.driveBase.gyro_turn(45, 100, 100)
        self.driveBase.run_motor_duration(-1000, -1, self.driveBase.RIGHT)
        self.driveBase.gyro_drive(35, 900, 100)# press Hai
        self.driveBase.run_motor_duration(1000, -1, self.driveBase.RIGHT)
        self.driveBase.gyro_drive(30, -500, 100)
        self.driveBase.gyro_turn(-110, 300, 100)
        self.driveBase.attach_addition(False)
        self.driveBase.gyro_drive(80, 800, 100)

    

    def taucherin_riff(self):

        motor.run_to_absolute_position(
            self.driveBase.RIGHT, 0, 600, direction=motor.SHORTEST_PATH)
        self.connect_addition()
        self.reset_addition_riff()
        logger.debug("Resetted addition riff")

        self.driveBase.reset_null(self.driveBase.RIGHT)
        pin = self.driveBase.RIGHT
        self.driveBase.gyro_drive(78.5, 600, 400)
        self.driveBase.gyro_turn(90, 200, 100, rotate_mode=1)
        motor.run_to_relative_position(pin, 285, 800)
        time.sleep(0.4)
        self.driveBase.gyro_drive(20, 200, 60)
        motor.run_to_relative_position(pin, 380, 800)
        self.driveBase.gyro_drive(26.5, -300, -200)
        self.driveBase.gyro_turn(90, -200, -100, rotate_mode=1)
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
        # Turn before push korallen down
        self.driveBase.gyro_turn(-13, 200, 100)
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

        motor_pair.move(self.driveBase.MOTPAIR, 0, velocity=200)
        motor.run_for_degrees(self.driveBase.RIGHT, 300, 1000)
        time.sleep(2)
        motor.set_duty_cycle(self.driveBase.RIGHT, 0)
        motor_pair.stop(self.driveBase.MOTPAIR)
        self.driveBase.gyro_turn(5, 300, 200)
        motor.run_for_degrees(self.driveBase.RIGHT, 70, 300)
        self.driveBase.gyro_drive(1, -300, -200)
        motor.run_to_relative_position(self.driveBase.RIGHT, 100, 600)
        time.sleep_ms(200)
        self.driveBase.gyro_drive(10, -300, -100)
        motor.run_to_relative_position(self.driveBase.RIGHT, 780, 600)
        time.sleep_ms(600)
        self.driveBase.gyro_turn(100, 400, 300)
        self.driveBase.attach_addition(False)
        self.driveBase.gyro_drive(80, 800, 800)



"""