import copy

import renpy.exports as renpy

from .actor import ShooterActor


class ShooterWeapon(object):
    def __init__(self, player, bullet=None, *args, **kwargs):
        self.player = player
        self.bullet = bullet

        self.bullets = []
        self.max_bullets = 6

    def generate_bullets(self):
        # TODO: Don't create new bullet objects, recycle the existing ones.

        # If a bullet is dead, remove it from the list
        for item in self.bullets:
            if not item.alive:
                self.bullets.remove(item)

        # If less than the max number of bullets allowed, add a new bullet
        if len(self.bullets) < (self.max_bullets - 1):
            self.bullet.x = self.player.x
            self.bullet.y = self.player.y
            self.bullets.append(copy.deepcopy(self.bullet))


class ShooterBullet(ShooterActor):
    def __init__(self, displayable=None, speed=(0, 0), *args, **kwargs):
        super(ShooterBullet, self).__init__(
            displayable, speed, *args, **kwargs)

        self.alive = True

    def render(self, width, height, st, at):
        render = renpy.Render(width, height)

        # Figure out the time elapsed since the previous frame.
        if self.old_st is None:
            self.old_st = st

        dtime = st - self.old_st
        self.old_st = st

        speed_x = dtime * self.max_speed_x
        speed_y = dtime * self.max_speed_y

        self.x += speed_x
        self.y -= speed_y

        self.displayable_render = renpy.render(
            self.displayable,
            width,
            height,
            st,
            at
        )

        renpy.redraw(self, 0)
        render.blit(self.displayable_render, (self.x, self.y))

        # Kill bullets when they leave the screen
        self.alive = self.inside_bounds()

        return render
