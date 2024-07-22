import math


def find_closest_boxes(boxes, current_index, direction):
    current_ball = boxes[current_index]
    min_distance = float('inf')
    closest_index = current_index
    for i, ball in enumerate(boxes):
        if i == current_index:
            continue
        distance = math.sqrt((ball.x - current_ball.x) ** 2 + (ball.y - current_ball.y) ** 2)
        if direction == "UP" and ball.y < current_ball.y and distance < min_distance:
            min_distance = distance
            closest_index = i
        if direction == "DOWN" and ball.y > current_ball.y and distance < min_distance:
            min_distance = distance
            closest_index = i
        if direction == "LEFT" and ball.x < current_ball.x and distance < min_distance:
            min_distance = distance
            closest_index = i
        if direction == "RIGHT" and ball.x > current_ball.x and distance < min_distance:
            min_distance = distance
            closest_index = i
    return closest_index
