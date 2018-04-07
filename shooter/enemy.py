import renpy.exports as renpy

from .actor import ShooterActor


class EnemyShooterActor(ShooterActor):
    def __init__(self, *args, **kwargs):
        super(EnemyShooterActor, self).__init__(*args, **kwargs)

        self.wave = 1

    def render(self, width, height, st, at):
        render = renpy.Render(width, height)

        if self.alive:
            # Figure out the time elapsed since the previous frame.
            if self.old_st is None:
                self.old_st = st

            dtime = st - self.old_st
            self.old_st = st

            # Create number that keeps getting lower.
            # Use this value to make the enemy move in a wave motion.
            self.wave -= dtime

            if self.wave <= 1:
                skew = 150
            if self.wave <= 0:
                skew = -150
            if self.wave <= -1:
                self.wave = 1
                skew = 0

            speed_x = dtime * self.max_speed_x
            speed_y = dtime * (self.max_speed_y + skew)

            self.x += speed_x
            self.y += speed_y

            self.displayable_render = renpy.render(
                self.displayable,
                width,
                height,
                st,
                at
            )

            # Kill enemies when they leave the screen
            self.alive = self.inside_bounds()

        # Regenerate enemies at their original position
        if not self.alive:
            self.x = self.start_x
            self.y = self.start_y
            self.alive = True

        renpy.redraw(self, 0)
        render.blit(self.displayable_render, (self.x, self.y))

        return render


class EnemyGroup(object):
    def __init__(self, start=(0, 0), enemies=None):
        for enemy in enemies:
            enemy.start_x += start[0]
            enemy.start_y += start[1]

            enemy.x += start[0]
            enemy.y += start[1]

        self.enemies = enemies
