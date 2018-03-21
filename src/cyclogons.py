
import math
import matplotlib.pyplot as plt
import matplotlib.patches as ptch
from matplotlib.widgets import Slider, RadioButtons

from shapely.geometry import LineString
from shapely.geometry import Point


###############################################
#             POINTS OF THE LINE             #
###############################################

x1 = -9
y1 = -7
x2 = 9
y2 = 7


###############################################
#             SECONDARY FUNCTIONS             #
###############################################

def find_second_point_on_line (x, y, length):
    p = Point(x, y)
    c = p.buffer(length).boundary
    l = LineString(lineShapely)
    i = c.intersection(l)

    return i.coords[0]


def find_rotated_vertex(support_rib, length, rotate_angle, up):
    base = length * math.sqrt(2) * math.sqrt(1 - math.cos(rotate_angle))

    p1 = Point(support_rib[0][0], support_rib[0][1])
    c1 = p1.buffer(base).boundary
    p2 = Point(support_rib[1][0], support_rib[1][1])
    c2 = p2.buffer(length).boundary

    i = c1.intersection(c2)

    if(y1 == y2):
        if(i.geoms[0].coords[0][1] > y2):
            return i.geoms[0].coords[0]
        else:
            return i.geoms[1].coords[0]

    if(up == True):
        return i.geoms[0].coords[0]
    else:
        return i.geoms[1].coords[0]


def calc_vertex_coord(support_rib, vertex_num, exterior_angle):
    points = [support_rib[0], support_rib[1]]

    a1 = [support_rib[0][0], support_rib[0][1]]
    a2 = [support_rib[1][0], support_rib[1][1]]

    for i in range(1, vertex_num-1):
        nextX = (a2[0] - a1[0]) * math.cos(exterior_angle) + (a2[1] - a1[1]) * (-math.sin(exterior_angle)) + a2[0]
        nextY = (a2[0] - a1[0]) * math.sin(exterior_angle) + (a2[1] - a1[1]) * math.cos(exterior_angle) + a2[1]

        points.append((nextX, nextY))


        a1[0] = a2[0]
        a1[1] = a2[1]
        a2[0] = nextX
        a2[1] = nextY

    return points


def draw_cyclogon(points):
    cyclogon.xy = points



###############################################
#                 MAIN PART                   #
###############################################
global SIDE_LENGTH

# coordinate plane setting
plt.axis('equal')
fig = plt.figure()
fig.canvas.set_window_title('Cyclogon')
global ax
ax = fig.add_subplot(111)

# Adjust the subplots region to leave some space for the sliders and buttons
fig.subplots_adjust(left=0.25, bottom=0.3)

# graph limits
ax.set_xlim([-10, 10])
ax.set_ylim([-10, 10])

up = True
if (y2 <= y1):
    up = False


# SOURCE DATA
# oblique line
global line
global lineShapely
lineShapely = [(x1, y1), (x2, y2)]
plt.plot([x1, x2], [y1, y2])

# characteristics of a regular polygon
VERTEX_NUM = 3
SIDE_LENGTH = 2
EXTERIOR_ANGLE = math.pi / 180.0 * (360 / VERTEX_NUM)

# auxiliary characteristics
global ANGULAR_SCALE
global supportRib

ANGULAR_SCALE = EXTERIOR_ANGLE / SIDE_LENGTH
supportRib = [(x1, y1), find_second_point_on_line(x1, y1, SIDE_LENGTH)]


global cyclogon
cyclogon = ptch.Polygon(calc_vertex_coord(supportRib, VERTEX_NUM, EXTERIOR_ANGLE))
cyclogon.set_linewidth(2)
cyclogon.set_linestyle('solid')
cyclogon.set_color('white')
cyclogon.set_edgecolor('red')
ax.add_patch(cyclogon)

# add sliders for tweaking the cyclogon position
axis_color = 'lightgoldenrodyellow'
radius_slider_ax  = fig.add_axes([0.25, 0.15, 0.65, 0.03], axisbg=axis_color)
len = math.sqrt( (x2-x1)*(x2-x1) + (y2-y1)*(y2-y1) )
radius_slider = Slider(radius_slider_ax, '', 0, len-SIDE_LENGTH, valinit=0)

# add a set of radio buttons for changing vertex number
vertex_radios_ax = fig.add_axes([0.025, 0.3, 0.12, 0.35], axisbg=axis_color)
vertex_radios = RadioButtons(vertex_radios_ax, (3, 4, 5, 6, 7, 8, 9, 10, 11, 12), active=0)


###############################################
#       SLIDERS AND SWITCHES CALLBACKS        #
###############################################

# Define an action for modifying the line when any slider's value changes
def slider_on_changed(val):
    VERTEX_NUM = int(vertex_radios.value_selected)
    EXTERIOR_ANGLE = math.pi / 180.0 * (360 / VERTEX_NUM)
    ANGULAR_SCALE = EXTERIOR_ANGLE / SIDE_LENGTH

    roundVal = (math.floor(val) // SIDE_LENGTH) * SIDE_LENGTH

    if roundVal == 0:
        roundVal = 0.001

    lyingFirstPoint = find_second_point_on_line(x1, y1, roundVal)
    lyingSecondPoint = find_second_point_on_line(x1, y1, roundVal + SIDE_LENGTH)

    lyingSupportRib = [lyingFirstPoint, lyingSecondPoint]
    rotateAngle = ANGULAR_SCALE * (val - roundVal)

    rotateVertex = find_rotated_vertex(lyingSupportRib, SIDE_LENGTH, rotateAngle, up)
    supportRib = [rotateVertex, find_second_point_on_line(x1, y1, roundVal + SIDE_LENGTH)]

    draw_cyclogon(calc_vertex_coord(supportRib, VERTEX_NUM, EXTERIOR_ANGLE))
    fig.canvas.draw_idle()

# SET CALLBACK
radius_slider.on_changed(slider_on_changed)


def vertex_radios_on_clicked(num):
    radius_slider.set_val(0)
    fig.canvas.draw_idle()

# SET CALLBACK
vertex_radios.on_clicked(vertex_radios_on_clicked)

plt.show()
