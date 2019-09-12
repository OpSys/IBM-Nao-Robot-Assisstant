from naoqi import ALProxy
import MSTT
import STTS
import NaoRobot
import time

print "================ Choregraphe's Initialization ================"
naoIP = '127.0.0.1'
# Go to Choregraphe, click on edit->Preferences->Virtual bot tab.
# Your bot's port is at the bottom of the window in green text.
# The port number changes for a new virtual bot connection.
naoPort = 57449

# create all proxies
motionProxy = ALProxy("ALMotion", naoIP, naoPort)
postureProxy = ALProxy("ALRobotPosture", naoIP, naoPort)
trackerProxy = ALProxy("ALTracker", naoIP, naoPort)


def main():
    MSTT.start_listening()


if __name__ == "__main__":
    main()


# Create the Robot
Neo = NaoRobot.NaoRobot(motionProxy, postureProxy)

# Do something

# Stand up
posture = 'Stand'
Neo.stand(posture)
time.sleep(2.0)
Neo.point(trackerProxy, -1.9750, 4.9000, 0.8550, 50, pointframe="Robot")  # first rack

