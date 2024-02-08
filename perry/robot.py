import wpilib
import wpilib.drive
from wpimath import controller
import math
from pathplannerlib.auto import AutoBuilder, ReplanningConfig, PathPlannerPath
from pathplannerlib.config import HolonomicPathFollowerConfig, ReplanningConfig, PIDConstants
from wpimath.kinematics import ChassisSpeeds
from wpimath.geometry import Rotation2d
import wpilib.drive
from wpilib import DriverStation
import drivetrain
import commands2
from wpimath import trajectory
import random
import rev
import math
import commands2
from pathplannerlib.path import PathPlannerPath
from pathplannerlib.auto import AutoBuilder
from pathplannerlib.config import HolonomicPathFollowerConfig, ReplanningConfig, PIDConstants
from wpimath import controller
from wpimath.kinematics import SwerveDrive4Kinematics, SwerveModuleState, ChassisSpeeds, SwerveDrive4Odometry, SwerveModulePosition
from wpimath.geometry import Translation2d, Rotation2d, Pose2d
import phoenix6 as ctre
from wpilib import DriverStation
from wpilib import SmartDashboard, Field2d

class MyRobot(commands2.TimedCommandRobot):

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self.drivetrain = drivetrain.DriveTrain()
        self.time = 0.0
        #self.configure_auto()

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        #self.command = self.getAutoCommand()

        #if self.command:
        #    self.command.schedule()
            # self.drivetrain.resetMotors()
        self.drivetrain.gyro.set_yaw(0)
        self.time = 0.0
        config = trajectory.TrajectoryConfig(
            10,
            10
        )
        
        self.HoloController = controller.HolonomicDriveController(
            controller.PIDController(1,0,0), controller.PIDController(-1,0,0),
            controller.ProfiledPIDControllerRadians(1,0,0, trajectory.TrapezoidProfileRadians.Constraints(6.28, 3.14))
        )


        self.myTrajectory = trajectory.TrajectoryGenerator.generateTrajectory(
            Pose2d(0,0,Rotation2d(0)),
            [],
            Pose2d(4,0,Rotation2d(0)),
            config
        )
        

    def configure_auto(self):
        AutoBuilder.configureHolonomic(
            self.drivetrain.getPose, # Robot pose supplier
            self.drivetrain.resetPose, # Method to reset odometry (will be called if your auto has a starting pose)
            self.drivetrain.getChassisSpeed, # ChassisSpeeds supplier. MUST BE ROBOT RELATIVE
            self.drivetrain.driveFromChassisSpeeds, # Method that will drive the robot given ROBOT RELATIVE ChassisSpeeds
            HolonomicPathFollowerConfig( # HolonomicPathFollowerConfig, this should likely live in your Constants class
                PIDConstants(.5, 0.0, 0.0), # Translation PID constants
                PIDConstants(0.5, 0.0, 0.0), # Rotation PID constants
                .4, # Max module speed, in m/s
                0.4, # Drive base radius in meters. Distance from robot center to furthest module.
                ReplanningConfig(False) # Default path replanning config. See the API for the options here
            ),
            self.drivetrain.shouldFlipPath, # Supplier to control path flipping based on alliance color
            self.drivetrain# Reference to this subsystem to set requirements
        )


    
    def getAutoCommand(self):
        # Load the path you want to follow using its name in the GUI
        #path = PathPlannerPath.fromPathFile('test') 

        # Create a path following command using AutoBuilder. This will also trigger event markers.
        #   return AutoBuilder.followPath(path)
        pass
 

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        """pathfindingCommand = AutoBuilder.pathfindToPose(
        targetPose,
        constraints,
        goal_end_vel=0.0, # Goal end velocity in meters/sec
        rotation_delay_distance=0.0 # Rotation delay distance in meters. This is how far the robot should travel before attempting to rotate.
        )"""

        
        if self.myTrajectory.totalTime() >= self.time:
            goal = self.myTrajectory.sample(self.time)
            adjSpeeds = self.HoloController.calculate(
                self.drivetrain.odometry.getPose(),
                goal,
                Rotation2d.fromDegrees(0.0)
            )
            self.drivetrain.driveFromChassisSpeeds(adjSpeeds)
            self.time += 0.02
            self.drivetrain.updateOdometry()
        else:
            self.drivetrain.resetMotors()



    def teleopInit(self):
        """This function is called once each time the robot enters teleoperated mode."""

        
        self.drivetrain.gyro.set_yaw(0)        

        
        """self.backLeftRotation.set(-self.BleftPID.calculate(self.BleftEnc.get_absolute_position()._value, 5.0))
        self.frontLeftRotation.set(-self.FleftPID.calculate(self.FleftEnc.get_absolute_position()._value, 5.0))
        self.backRightRotation.set(-self.BrightPID.calculate(self.BrightEnc.get_absolute_position()._value, 5.0))
        self.frontRightRotation.set(-self.FrightPID.calculate(self.FrightEnc.get_absolute_position()._value, 5.0))"""
    
        
 

    def teleopPeriodic(self):
        """This function is called periodically during teleoperated mode."""
        #self.fuckyouhenry.set (1.0)

        self.joystick = wpilib.Joystick(0)

        xspeed = self.joystick.getX()
        yspeed = self.joystick.getY()
        tspeed = self.joystick.getTwist()

        yaw = -self.drivetrain.gyro.get_yaw().value_as_double
        


        h = yaw % 360
        if h < 0:
            h += 360

        h2 = h / 360

        heading = h2 * (math.pi*2)
        
        if abs(xspeed) <.10:
            xspeed=0
        if abs(yspeed) <.10:
            yspeed=0
        if abs(tspeed) <.10:
            tspeed=0


        if False:#xspeed == 0 and yspeed == 0 and tspeed == 0:
            self.backLeftDrive.set(0)
            self.backRightDrive.set(0)
            self.frontLeftDrive.set(0)
            self.frontRightDrive.set(0)

            self.backLeftRotation.set(0)
            self.backRightRotation.set(0)
            self.frontLeftRotation.set(0)
            self.frontRightRotation.set(0)            
        else:
            speeds = ChassisSpeeds.fromFieldRelativeSpeeds(xspeed, yspeed, -tspeed, Rotation2d(heading))
            self.drivetrain.driveFromChassisSpeeds(speeds)

    # Convert to module states
            
            """print("HENRY HELP ME")
            print(f"{backLeftOptimized.angle.radians()}, {backLeftOptimized.speed}")
            print(f"{backRightOptimized.angle.radians()}, {backRightOptimized.speed}")
            print(f"{frontLeftOptimized.angle.radians()}, {frontLeftOptimized.speed}")
            print(f"{frontRightOptimized.angle.radians()}, {-frontRightOptimized.speed}")"""

            


if __name__ == "__main__":
    wpilib.run(MyRobot)
