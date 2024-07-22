from typing import Generator, Sequence, Tuple, List

import cv2
import numpy as np
import pygame
import random

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)


class Box:
    def __init__(self, x, y, w, h, color=GRAY):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

    def draw(self, screen):
        # 只画边框
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h), 2)

    def distance(self, box):
        return abs(self.x - box.x) + abs(self.y - box.y)

    def colliderect(self, other):
        return self.x < other.x + other.w and self.x + self.w > other.x and self.y < other.y + other.h and self.y + self.h > other.y

    def __str__(self):
        return f'Box({self.x}, {self.y}, {self.w}, {self.h})'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.w == other.w and self.h == other.h


class CV:
    def __init__(self, video_path, width, height):
        self.cap = cv2.VideoCapture(video_path)
        self.width = width
        self.height = height
        self.tracker = None
        self.box = None

    def _get_image(self):
        ret, frame = self.cap.read()
        if not ret:
            print('Cannot read image')
            self.cap.release()
            quit()
        frame = cv2.resize(frame, (self.width, self.height))
        return frame

    def _find_circle_contours(self, image) -> Generator:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3, 3), 1)
        fan = cv2.bitwise_not(blurred)
        edges = cv2.Canny(fan, 40, 60)
        kernel = np.ones((3, 3), np.uint8)
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=1)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 30:
                continue
            perimeter = cv2.arcLength(contour, True)
            if perimeter == 0:
                continue
            circularity = 4 * np.pi * (area / (perimeter * perimeter))
            if 0.5 < circularity < 1.2:
                yield contour

    def update_tracker(self, image, boxes) -> List[Box]:
        if not self.tracker and boxes:
            selected_box = random.choice(boxes)
            tracker = cv2.TrackerCSRT_create()
            tracker.init(image, (selected_box.x, selected_box.y, selected_box.w, selected_box.h))
            self.tracker = tracker
            self.box = selected_box
        else:
            success, box = self.tracker.update(image)
            if success:
                self.box = Box(*box)
            else:
                selected_box = random.choice(boxes)
                tracker = cv2.TrackerCSRT_create()
                tracker.init(image, (selected_box.x, selected_box.y, selected_box.w, selected_box.h))
                self.tracker = tracker
                self.box = selected_box
        if self.tracker:

            distances = [(i, self.box.distance(box)) for i, box in enumerate(boxes)]
            distances.sort(key=lambda x: x[1])
            # debug_image = image.copy()
            # for i in range(1, min(11, len(distances))):
            #     index = distances[i][0]
            #     box = boxes[index]
            #     cv2.rectangle(debug_image, (box.x, box.y), (box.x + box.w, box.y + box.h), (0, 255, 0), 2)
            # for i in self.boxes:
            #     cv2.rectangle(debug_image, (i.x, i.y), (i.x + i.w, i.y + i.h), (0, 0, 255), 2)
            # assert 1 == 1
            # cv2.imshow('debug', debug_image)
            for i in range(1, min(11, len(distances))):
                boxes[distances[i][0]].color = BLUE
            return boxes

    def get_image_and_boxes(self) -> Tuple[np.ndarray, Box]:
        # 先获取图像，然后得到所有圆形轮廓，然后更新tracker，最后为轮廓染色并返回
        image = self._get_image()
        contours = list(self._find_circle_contours(image))
        boxes = [Box(*cv2.boundingRect(contour)) for contour in contours]
        boxes = self.update_tracker(image, boxes)
        # 将存在self.boxes的标记为蓝色，是selected的标记为红色
        if self.box and self.box in boxes:
            boxes[boxes.index(self.box)].color = RED
        elif self.box:
            boxes.append(self.box)
            boxes[-1].color = RED
        # print(len(boxes), len([box for box in boxes if box.color == RED]),
        #       len([box for box in boxes if box.color == BLUE]))
        return image, boxes

    def select_up(self, boxes, image):
        # 将selected_index转为在自己上面离自己最近的
        selected_box = self.box
        distances = [(i, abs(selected_box.x - box.x) + abs(selected_box.y - box.y)) for i, box in enumerate(boxes)
                     if box.y < selected_box.y]
        distances.sort(key=lambda x: x[1])
        if distances:
            self.box = boxes[distances[0][0]]
            self.tracker = cv2.TrackerCSRT_create()
            self.tracker.init(image, (self.box.x, self.box.y, self.box.w, self.box.h))

    def select_down(self, boxes, image):
        # 将selected_index转为在自己下面离自己最近的
        selected_box = self.box
        distances = [(i, abs(selected_box.x - box.x) + abs(selected_box.y - box.y)) for i, box in enumerate(boxes)
                     if box.y > selected_box.y]
        distances.sort(key=lambda x: x[1])
        if distances:
            self.box = boxes[distances[0][0]]
            self.tracker = cv2.TrackerCSRT_create()
            self.tracker.init(image, (self.box.x, self.box.y, self.box.w, self.box.h))

    def select_right(self, boxes, image):
        # 将selected_index转为在自己右边离自己最近的
        selected_box = self.box
        distances = [(i, abs(selected_box.x - box.x) + abs(selected_box.y - box.y)) for i, box in enumerate(boxes)
                     if box.x > selected_box.x]
        distances.sort(key=lambda x: x[1])
        if distances:
            self.box = boxes[distances[0][0]]
            self.tracker = cv2.TrackerCSRT_create()
            self.tracker.init(image, (self.box.x, self.box.y, self.box.w, self.box.h))

    def select_left(self, boxes, image):
        # 将selected_index转为在自己左边离自己最近的
        selected_box = self.box
        distances = [(i, abs(selected_box.x - box.x) + abs(selected_box.y - box.y)) for i, box in enumerate(boxes)
                     if box.x < selected_box.x]
        distances.sort(key=lambda x: x[1])
        if distances:
            self.box = boxes[distances[0][0]]
            self.tracker = cv2.TrackerCSRT_create()
            self.tracker.init(image, (self.box.x, self.box.y, self.box.w, self.box.h))
