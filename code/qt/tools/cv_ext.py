import numpy as np

import cv2


def draw_arrow(image, p, q, color, arrow_magnitude=6, thickness=1, line_type=8, shift=0):
    # adapted from http://mlikihazar.blogspot.com.au/2013/02/draw-arrow-opencv.html
    # draw arrow tail
    cv2.line(image, p, q, color, thickness, line_type, shift)
    # calc angle of the arrow
    angle = np.arctan2(p[1] - q[1], p[0] - q[0])
    # starting point of first line of arrow head
    p = (int(q[0] + arrow_magnitude * np.cos(angle + np.pi / 4)),
         int(q[1] + arrow_magnitude * np.sin(angle + np.pi / 4)))
    # draw first half of arrow head
    cv2.line(image, p, q, color, thickness, line_type, shift)
    # starting point of second line of arrow head
    p = (int(q[0] + arrow_magnitude * np.cos(angle - np.pi / 4)),
         int(q[1] + arrow_magnitude * np.sin(angle - np.pi / 4)))
    # draw second half of arrow head
    cv2.line(image, p, q, color, thickness, line_type, shift)


def draw_arrowed_polyline(image, points, color, arrow_magnitude=6, thickness=1, line_type=8, shift=0):
    if len(points) >= 2:
        cv2.polylines(image, [np.array(points[:-1])], False, (0, 255, 255))
        p = (points[-2][0], points[-2][1])
        q = (points[-1][0], points[-1][1])
        draw_arrow(image, p, q, color, arrow_magnitude=arrow_magnitude, thickness=thickness, line_type=line_type, shift=shift)
