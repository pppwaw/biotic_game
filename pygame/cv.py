from typing import Tuple, List

import cv2
import numpy as np
import pygame


class Box:

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __str__(self):
        return f'x: {self.x}, y: {self.y}, w: {self.w}, h: {self.h}'

    def draw(self, screen):
        color = (0, 0, 255)
        pygame.draw.rect(screen, color, (self.x, self.y, self.w, self.h), 2)

    def colliderect(self, rect):
        return pygame.Rect(self.x, self.y, self.w, self.h).colliderect(rect)


class CV:
    def __init__(self, input_, width, height):
        self.cam = cv2.VideoCapture(input_)
        self.width = width
        self.height = height
        self.previous_contours = []

    def read_image(self):
        ret, frame = self.cam.read()
        if not ret:
            print('Cannot read image')
            self.cam.release()
            self.end()
        frame = cv2.resize(frame, (self.width, self.height))
        return frame

    def detect_init(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 1)
        edges = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        kernel = np.ones((3, 3), np.uint8)
        closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)

        dist_transform = cv2.distanceTransform(closing, cv2.DIST_L2, 5)
        ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
        sure_fg = np.uint8(sure_fg)

        sure_bg = cv2.dilate(closing, kernel, iterations=3)
        unknown = cv2.subtract(sure_bg, sure_fg)

        ret, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown == 255] = 0

        markers = cv2.watershed(image, markers)
        image[markers == -1] = [255, 0, 0]

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def detect_circular_contours(self, image, prev_contours=None):
        contours = self.detect_init(image)
        valid_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 30:
                continue
            perimeter = cv2.arcLength(contour, True)
            if perimeter == 0:
                continue
            circularity = 4 * np.pi * (area / (perimeter * perimeter))
            if 0.6 < circularity < 1.2:
                valid_contours.append(contour)

        if prev_contours is not None:
            final_contours = []
            for contour in valid_contours:
                if any(cv2.matchShapes(contour, prev, cv2.CONTOURS_MATCH_I2, 0) < 0.1 for prev in prev_contours):
                    final_contours.append(contour)
            valid_contours = final_contours if final_contours else valid_contours

        # for contour in valid_contours:
        #     cv2.drawContours(image, [contour], -1, (255, 0, 0), 2)

        return image, valid_contours

    def refresh(self) -> Tuple[List[Box], np.ndarray]:
        frame = self.read_image()
        frame, current_contours = self.detect_circular_contours(frame)
        coords = [Box(*cv2.boundingRect(contour)) for contour in current_contours]
        return coords, frame

    def end(self):
        cv2.destroyAllWindows()
        quit()
