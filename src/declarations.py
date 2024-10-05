WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (0, 145, 255)

ZOOM = 500
ROTATIONSPEED = 0.2
EXAMPLE = '../resources/preacher man.obj'

'''
valid examples

../resources/
airboat.obj
cessna.obj
cube.obj
dodecahedron.obj
preacher man.obj
shuttle.obj
slot_machine.obj

'''

SCREEN = (800, 600)
WIDTH = 2

'''
most computers would use camera index 0

in case you get
[ WARN:0@0.495] global cap_v4l.cpp:999 open VIDEOIO(V4L2:/dev/video0): can't open camera by index
[ERROR:0@0.614] global obsensor_uvc_stream_channel.cpp:158 getStreamChannelGroup Camera index out of range
change CAMERA_INDEX values
'''
CAMERA_INDEX = 1


FONTSIZE = 20
SHOWCVWINDOW = False
PREACHERMAN = True

CLIWINDOW = True

