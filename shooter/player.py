import pygame

import renpy.exports as renpy

from .actor import ShooterActor
from .weapon import ShooterWeapon


class ShooterPlayer(ShooterActor):
    def __init__(self, displayable=None, bullet=None, speed=(0, 0),
                 start=(0, 0), *args, **kwargs):
        super(ShooterPlayer, self).__init__(
            displayable, speed, start, *args, **kwargs)

        self.weapon = ShooterWeapon(self, bullet=bullet)
        self.enemies = []

    def check_overlap(self):
        for enemy in self.enemies:
            for bullet in self.weapon.bullets:
                if bullet.overlaps_with(enemy):
                    enemy.alive = False

            if self.overlaps_with(enemy):
                self.alive = False

    def move_player(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.speed_x = -self.max_speed_x
        elif keys[pygame.K_RIGHT]:
            self.speed_x = self.max_speed_x

        if keys[pygame.K_UP]:
            self.speed_y = -self.max_speed_y
        elif keys[pygame.K_DOWN]:
            self.speed_y = self.max_speed_y

    def render(self, width, height, st, at):
        render = renpy.Render(width, height)

        # Figure out the time elapsed since the previous frame.
        if self.old_st is None:
            self.old_st = st

        dtime = st - self.old_st
        self.old_st = st

        self.check_overlap()

        self.move_player()

        speed_x = dtime * self.speed_x
        speed_y = dtime * self.speed_y

        self.x += speed_x
        self.y += speed_y

        self.displayable_render = renpy.render(
            self.displayable,
            width,
            height,
            st,
            at
        )

        # Drawing bullets in ShooterPlayer's render so they
        # implicitly get added to the screen
        for bullet in self.weapon.bullets:
            b = renpy.render(bullet, width, height, st, at)
            render.blit(b, (0, 0))

        renpy.redraw(self, 0)
        render.blit(self.displayable_render, (self.x, self.y))

        return render

    def event(self, ev, x, y, st):
        if ev.type == pygame.KEYUP:
            self.speed_x = 0
            self.speed_y = 0

        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                self.weapon.generate_bullets()

        if not self.alive:
            return False
        else:
            raise renpy.IgnoreEvent()
