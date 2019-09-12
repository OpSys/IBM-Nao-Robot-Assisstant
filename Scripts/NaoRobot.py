#~ This script was generated automatically by drang&drop from Position Library
class NaoRobot:
    def __init__(self, motionproxy, postureproxy):
        # For moving and positioning
        self.motionProxy = motionproxy
        self.postureProxy = postureproxy

        # For moving to a position
        self.positionErrorThresholdPos = 0.00
        self.positionErrorThresholdAng = 0.00

        # for pointing
        self.tracker = None
        self.PointX = 0.0
        self.PointY = 0.0
        self.PointZ = 0.0
        self.PointMaxSpeed = 0.0
        self.PointEffector = "Arms"
        self.PointFrame = 0  # FRAME TORSO

    def stand(self, posture):
        if(self.postureProxy != None):
            result = self.postureProxy.goToPosture(posture, 0.8)
            if(result):
                print "Yay!! It stood"
            else:
                print ("Posture StandZero is not a part of the standard posture library, robot cannot reach the posture")
        else:
            print "PostureProxy does not exist"

    def move(self, XDis, YDis, Angle, MoveArms):
        self.positionErrorThresholdPos = 0.01
        self.positionErrorThresholdAng = 0.03

        import almath
        # The command position estimation will be set to the sensor position
        # when the robot starts moving, so we use sensors first and commands later.
        initPosition = almath.Pose2D(self.motionProxy.getRobotPosition(True))
        targetDistance = almath.Pose2D(XDis,YDis,Angle * almath.PI / 180)
        expectedEndPosition = initPosition * targetDistance
        enableArms = MoveArms
        self.motionProxy.setMoveArmsEnabled(enableArms, enableArms)
        self.motionProxy.moveTo(XDis,YDis,Angle * almath.PI / 180)

        # The move is finished so output
        realEndPosition = almath.Pose2D(self.motionProxy.getRobotPosition(False))
        positionError = realEndPosition.diff(expectedEndPosition)
        positionError.theta = almath.modulo2PI(positionError.theta)
        if (abs(positionError.x) < self.positionErrorThresholdPos
                and abs(positionError.y) < self.positionErrorThresholdPos
                and abs(positionError.theta) < self.positionErrorThresholdAng):
            print "Arrived at destination"
        else:
            print "Couldn't get to destination"

    def point(self,tracker,pointx,pointy,pointz,maxspeed,pointframe="World",effector="LArm",):
        self.tracker = tracker
        self.PointX = pointx
        self.PointY = pointy
        self.PointZ = pointz
        self.PointMaxSpeed = maxspeed / 100.0
        self.PointEffector = effector
        framestring = pointframe

        if framestring == "Torso":
            self.PointFrame = 0
        elif framestring == "World":
            self.PointFrame = 1
        elif framestring == "Robot":
            self.PointFrame = 2

        point = self.tracker.pointAt(self.PointEffector,
                             [self.PointX, self.PointY, self.PointZ],
                             self.PointFrame, self.PointMaxSpeed)

    def walk(self):
        import almath as m
        import math
        self.motionProxy.setWalkArmsEnabled(True, True)

        #####################
        ## FOOT CONTACT PROTECTION
        #####################
        self.motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

        #####################
        ## get robot position before move
        #####################
        initRobotPosition = m.Pose2D(self.motionProxy.getRobotPosition(False))

        X = 0
        Y = 0
        Theta = math.pi / 2.0
        self.motionProxy.post.moveTo(X, Y, Theta)
        # wait is useful because with post moveTo is not blocking function
        self.motionProxy.waitUntilMoveIsFinished()

        #####################
        ## get robot position after move
        #####################
        endRobotPosition = m.Pose2D(self.motionProxy.getRobotPosition(False))

        #####################
        ## compute and print the robot motion
        #####################
        robotMove = m.pose2DInverse(initRobotPosition) * endRobotPosition
        print "Robot Move :", robotMove

    def walkfast(self):
        import time
        # Initialize the walk process.
        # Check the robot pose and take a right posture.
        # This is blocking called.
        self.motionProxy.moveInit()

        # TARGET VELOCITY
        X = 1.0
        Y = 0.0
        Theta = 0.0
        Frequency = 1.0

        # Default walk (MaxStepX = 0.04 m)
        self.motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
        time.sleep(3.0)
        print "walk Speed X :", self.motionProxy.getRobotVelocity()[0], " m/s"

        # Speed walk  (MaxStepX = 0.06 m)
        # Could be faster: see walk documentation
        self.motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency, [["MaxStepX", 0.06]])
        time.sleep(4.0)
        print "walk Speed X :", self.motionProxy.getRobotVelocity()[0], " m/s"

        # stop walk on the next double support
        self.motionProxy.stopMove()
