import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2
import pandas
img_path = './leaves.jpg'
img = cv2.imread(img_path)
img = half = cv2.resize(img, (720, 720), fx=0.1, fy=0.1)
# global vars that are used later on
clicked = False
r = g = b = x_pos = y_pos = 0
# reading the csv file with pandas and giving names to each
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
csv = pandas.read_csv('./colors.csv', names=index, header=None)
# function to get most matching color
# (calculate min distance from all colors)
def color(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        distance = abs(R - int(csv.loc[i, 'R'])) + abs(G - int(csv.loc[i, 'G'])) + abs(B - int(csv.loc[i, 'B']))
        if distance <= minimum:
            minimum = distance
            colorname = csv.loc[i, 'color_name']
    return colorname
# function to get coordinates of mouse click
def coordinates(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global r, g, b, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        r, g, b = img[y, x]
        r = int(r)
        g = int(g)
        b = int(b)
cv2.namedWindow('image')
cv2.setMouseCallback('image', coordinates)
while True:
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', coordinates)
    cv2.imshow('image', img)
    if clicked:
        cv2.rectangle(img, (20,20), (360,60), (r, g, b), -1)
        text = color(r, g, b)
        print("text=>",text)
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        if r+g+b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
        clicked = False
    # break loop when 'esc' pressed
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()