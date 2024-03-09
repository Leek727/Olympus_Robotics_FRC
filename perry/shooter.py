import commands2
import rev


class Shooter(commands2.Subsystem):
    def __init__(self):
        super().__init__()

        # motor init
        self.shooterDrive1 = rev.CANSparkMax(24, rev.CANSparkMax.MotorType.kBrushless)
        self.shooterDrive2 = rev.CANSparkMax(23, rev.CANSparkMax.MotorType.kBrushless)
        self.feedMotor = rev.CANSparkMax(21, rev.CANSparkMax.MotorType.kBrushless)
        # shooter rotation motor
        self.rotationMotor = rev.CANSparkMax(22, rev.CANSparkMax.MotorType.kBrushless)
        self.rotationMotorContoroller = self.rotationMotor.getPIDController()

        self.shooterController1 = self.shooterDrive1.getPIDController()
        self.shooterController2 = self.shooterDrive2.getPIDController()
        self.feedController = self.feedMotor.getPIDController()

        self.shooterDriveEnc1 = self.shooterDrive1.getEncoder(rev.SparkRelativeEncoder.Type.kHallSensor, 42)
        self.shooterDriveEnc2 = self.shooterDrive2.getEncoder(rev.SparkRelativeEncoder.Type.kHallSensor, 42)
        self.feedMotorEnc = self.feedMotor.getEncoder(rev.SparkRelativeEncoder.Type.kHallSensor, 42)


        self.configShooterMotor(self.shooterController1)
        self.configShooterMotor(self.shooterController2)
        self.configFeedMotor(self.feedController)
        self.configMotor(self.rotationMotorContoroller)
        

        # shooter global variables
        self.shooterMaxVelocity = 1000
        self.homeSetpoint = 0 # home position in rotations
        self.shootSetpoint = 0 # shoot position in rotations
        self.ampSetpoint = 20 # amp position in rotations


    def configFeedMotor(self, motor: rev.SparkPIDController):
        kP = 0.5
        kI = 1e-4
        kD = 0
        kIz = 0 
        kFF = 0 
        kMaxOutput = 1 
        kMinOutput = -1

        # set PID constants
        motor.setP(kP)
        motor.setI(kI)
        motor.setD(kD)
        motor.setIZone(kIz)
        motor.setFF(kFF)
        motor.setOutputRange(kMinOutput, kMaxOutput)

    def configMotor(self, motor: rev.SparkPIDController):
        kP = 0.5
        kI = 0
        kD = 1
        kIz = 0 
        kFF = 0 
        kMaxOutput = 1 
        kMinOutput = -1

        # set PID constants
        motor.setP(kP)
        motor.setI(kI)
        motor.setD(kD)
        motor.setIZone(kIz)
        motor.setFF(kFF)
        motor.setOutputRange(kMinOutput, kMaxOutput)

    def configShooterMotor(self, motor: rev.SparkPIDController):
        # Neo PID constants
        kP = 0.1
        kI = 1e-10
        kD = 0
        kIz = 0 
        kFF = 0 
        kMaxOutput = 1 
        kMinOutput = -1

        # set PID constants
        motor.setP(kP)
        motor.setI(kI)
        motor.setD(kD)
        motor.setIZone(kIz)
        motor.setFF(kFF)
        motor.setOutputRange(kMinOutput, kMaxOutput)
    
    def targetSpeaker(self):
        self.rotationMotorContoroller.setReference(self.shootSetpoint, rev.CANSparkMax.ControlType.kPosition)
    
    def targetAmp(self):
        self.rotationMotorContoroller.setReference(self.ampSetpoint, rev.CANSparkMax.ControlType.kPosition)
    
    def goHome(self):
        self.rotationMotorContoroller.setReference(self.homeSetpoint, rev.CANSparkMax.ControlType.kPosition)

    def setAngle(self):
        self.rotationMotorContoroller.setReference(8, rev.CANSparkMax.ControlType.kPosition)


    def spinFlywheels(self) -> bool:
        #self.shooterController1.setReference(-self.shooterMaxVelocity, rev.CANSparkMax.ControlType.kVelocity)
        #self.shooterController2.setReference(self.shooterMaxVelocity, rev.CANSparkMax.ControlType.kVelocity)
        self.shooterDrive1.set(-1)
        self.shooterDrive2.set(1)
        #error1 = abs(abs(self.shooterDriveEnc1.getVelocity())-abs(self.shooterMaxVelocity))
        #error2 = abs(abs(self.shooterDriveEnc2.getVelocity())-abs(self.shooterMaxVelocity))
    
        #if (error1 + error2 > 100):
        #    return False
        
        #return True
    


    def resetFeed(self):
        self.feedMotor.set(0)
        # reset encoder
        #self.feedMotorEnc.setPosition(0)


    def pushBack(self):
        self.shooterDrive1.set(.9)
        self.shooterDrive2.set(-.9)
        

    def stopFlywheels(self):
        self.shooterDrive1.set(0)
        self.shooterDrive2.set(0)
        
    def feedNote(self):
        self.feedMotor.set(-1)
