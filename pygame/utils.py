import math

def find_closest_ball(balls, current_index, direction):
    current_ball = balls[current_index]
    min_distance = float('inf')
    closest_index = current_index

    for i, ball in enumerate(balls):
        if i == current_index:
            continue

        if direction == "UP" and ball.y < current_ball.y:
            distance = current_ball.y - ball.y
            if distance < min_distance:
                min_distance = distance
                closest_index = i
        elif direction == "DOWN" and ball.y > current_ball.y:
            distance = ball.y - current_ball.y
            if distance < min_distance:
                min_distance = distance
                closest_index = i
        elif direction == "LEFT" and ball.x < current_ball.x:
            distance = current_ball.x - ball.x
            if distance < min_distance:
                min_distance = distance
                closest_index = i
        elif direction == "RIGHT" and ball.x > current_ball.x:
            distance = ball.x - current_ball.x
            if distance < min_distance:
                min_distance = distance
                closest_index = i

    return closest_index
