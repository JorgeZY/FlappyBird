#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import random
import pygame
from pygame.locals import *


WIDTH = 400
HEIGHT = 720
TUBE_WIDTH = 100
GAP = 150
MAX_TUBE_LEN = 400
MIN_TUBE_LEN = 100
BIRD_START_POS_X = 30
BIRD_START_POS_Y = 300
JUMP_DISTANCE = 70
TILT_ANGLE = 20
SCORE = 0


pygame.init()
pygame.display.set_caption('Flappy Bird')
pygame.display.set_icon(pygame.image.load('resources/icon.png'))
screen = pygame.display.set_mode([WIDTH, HEIGHT])
font = pygame.font.SysFont('freemono', 30, bold=1)


def generate_tube_len():
    bottom = random.randint(MIN_TUBE_LEN, MAX_TUBE_LEN)
    top = HEIGHT - bottom - 60 - GAP
    return top, bottom


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.smoothscale(pygame.image.load('resources/bird.png'), (51, 36))
        self.image_rect = self.image.get_rect()
        self.image_rect.y = BIRD_START_POS_Y
        self.image_rect.x = BIRD_START_POS_X

        self.rect = self.image_rect
        self.rotation = TILT_ANGLE

    def update(self):
        pygame.time.delay(20)
        self.image_rect.y += 4
        rotating_img = pygame.transform.rotate(self.image, self.rotation)
        self.rotation -= 1 if self.rotation >= -TILT_ANGLE else 0
        screen.blit(rotating_img, self.image_rect)


class Background:
    def __init__(self):
        self.background_img = pygame.transform.smoothscale(pygame.image.load('resources/background.png'), [1280, 720])

    def update(self):
        score_text = font.render(f'Score:{int(SCORE)}', False, (255, 255, 255))
        screen.blit(self.background_img, [0, 0])
        screen.blit(score_text, [WIDTH//2+40, 0])


class BottomPipe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pipe_img = pygame.image.load('resources/pipe.png')
        self.pipe_img_rect = self.pipe_img.get_rect()

        self.state = False
        self.pipes_list = []
        self.rect = self.pipe_img_rect

    def create_pipes(self, posy, tube_len):
        bottom_pipe = pygame.transform.smoothscale(self.pipe_img, [TUBE_WIDTH, tube_len])
        bottom_rect = bottom_pipe.get_rect()
        bottom_rect.x = posy
        bottom_rect.y = HEIGHT-60-tube_len

        self.pipes_list = [bottom_pipe, bottom_rect]

        return self.pipes_list

    def update(self, tube_len):
        global SCORE
        if not self.state:
            self.create_pipes(WIDTH, tube_len)
            self.state = True

        elif self.state:
            if self.pipes_list[1].x < -TUBE_WIDTH:
                SCORE += 0.5
                self.state = False
            else:
                self.pipes_list[1].x -= 5

        self.rect = self.pipes_list[1]
        screen.blit(self.pipes_list[0], self.pipes_list[1])


class TopPipe(BottomPipe):
    def __init__(self):
        super().__init__()
        self.state = False
        self.pipes_list = []

    def create_pipes(self, posy, tube_len):
        top_pipe = pygame.transform.smoothscale(self.pipe_img, [TUBE_WIDTH, tube_len])
        top_rect = top_pipe.get_rect()
        top_rect.x = posy
        top_rect.y = 0
        top_pipe = pygame.transform.rotate(top_pipe, 180)

        self.pipes_list = [top_pipe, top_rect]

        return self.pipes_list


def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and 120 < event.pos[0] < 284 and 360 < event.pos[1] < 450:
                    waiting = False


def show_start_screen():
    screen.fill([1, 134, 149])
    screen.blit(pygame.transform.smoothscale(pygame.image.load('resources/start_screen.jpg'), [400, 266]), [0, 100])
    button_img = pygame.transform.smoothscale(pygame.image.load('resources/start_button.png'), [164, 90])
    screen.blit(button_img, [120, HEIGHT / 2])
    pygame.display.update()
    wait_for_key()


def show_stop_screen():
    screen.blit(pygame.transform.smoothscale(pygame.image.load('resources/game_over.png'), [350, 80]), [25, HEIGHT / 4])
    button_img = pygame.transform.smoothscale(pygame.image.load('resources/start_button.png'), [164, 90])
    screen.blit(button_img, [120, HEIGHT/2])
    pygame.display.update()
    wait_for_key()


def check_collision(bird, top_pipe, bottom_pipe):
    global SCORE
    group = pygame.sprite.Group()
    group.add(top_pipe)
    group.add(bottom_pipe)
    result = pygame.sprite.spritecollideany(bird, group)
    if result or bird.rect.y >= 660 or bird.rect.y <= 0:
        show_stop_screen()
        top_pipe.state = False
        bottom_pipe.state = False
        bird.image_rect.x = BIRD_START_POS_X
        bird.image_rect.y = BIRD_START_POS_Y
        SCORE = 0


def handle_event(bird):
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.image_rect.y -= JUMP_DISTANCE
                bird.rotation = TILT_ANGLE


def main():
    show_start_screen()
    bird = Bird()
    background = Background()
    bottom_pipe = BottomPipe()
    top_pipe = TopPipe()
    while True:
        handle_event(bird)

        background.update()
        bird.update()
        top, bot = generate_tube_len()
        top_pipe.update(top)
        bottom_pipe.update(bot)

        check_collision(bird, top_pipe, bottom_pipe)

        pygame.display.update()


if __name__ == "__main__":
    main()