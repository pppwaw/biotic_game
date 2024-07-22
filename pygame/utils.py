import math

def is_inpoint(nball,d,ball):
    return nball.x+d>ball.x>nball.x-d and nball.y+d>ball.y>nball.y-d

def find_closest_ball(balls, current_index, direction):
    current_ball = balls[current_index]
    d=0
    while True:
        for i,ball in enumerate(balls):
            if direction=="UP" and ball.y < current_ball.y and is_inpoint(current_ball,d,ball):
                return i
            if direction=="DOWN" and ball.y > current_ball.y and is_inpoint(current_ball,d,ball):
                return i
            if direction=="LEFT" and ball.x < current_ball.x and is_inpoint(current_ball,d,ball):
                return i
            if direction=="RIGHT" and ball.x > current_ball.x and is_inpoint(current_ball,d,ball):
                return i
        d+=1
        if d>400:
            return current_index

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
