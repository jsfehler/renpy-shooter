import pygame
import renpy.exports as renpy


class ShooterActor(renpy.Displayable):
    """Base class for Shooter objects.
    """
    solid_colour = "#ffffff"
    solid_kwargs = {
        "xsize": 20,
        "ysize": 20
    }

    def __init__(self, displayable=None, speed=(0, 0), start=(0, 0),
                 *args, **kwargs):
        super(ShooterActor, self).__init__(*args, **kwargs)

        # Stores the old value of the st value from render()
        self.old_st = None

        # Default displayable if none is provided.
        self.displayable = displayable or Solid(
            self.solid_colour, **self.solid_kwargs)

        self.speed_x = 0
        self.speed_y = 0

        self.max_speed_x = speed[0]
        self.max_speed_y = speed[1]

        self.x = start[0]
        self.y = start[1]


class ShooterPlayer(ShooterActor):
    def __init__(self, displayable=None, speed=(0, 0), start=(0, 0),
                 *args, **kwargs):
        super(ShooterPlayer, self).__init__(
            displayable, speed, start, *args, **kwargs)

        self.bullets = []
        self.max_bullets = 6

        self.enemies = []

    def check_overlap(self):
        pass

    def generate_bullets(self):
        # TODO: Don't create new bullet objects, recycle the existing ones.

        # If a bullet is dead, remove it from the list
        for item in self.bullets:
            if not item.alive:
                self.bullets.remove(item)

        # If less than the max number of bullets allowed, add a new bullet
        if len(self.bullets) < (self.max_bullets - 1):
            new_bullet = ShooterBullet(start=(self.x, self.y), speed=(0, 300))
            self.bullets.append(new_bullet)

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

        self.move_player()

        speed_x = dtime * self.speed_x
        speed_y = dtime * self.speed_y

        self.x += speed_x
        self.y += speed_y

        d = renpy.render(self.displayable, width, height, st, at)

        for bullet in self.bullets:
            b = renpy.render(bullet, width, height, st, at)
            render.blit(b, (0, 0))

        renpy.redraw(self, 0)
        render.blit(d, (self.x, self.y))

        # DEBUG
        t = Text(str(actor.x) + ':' + str(actor.y))
        debug_render = renpy.render(t, width, height, st, at)
        render.blit(debug_render, (0, 0))

        return render

    def event(self, ev, x, y, st):
        if ev.type == pygame.KEYUP:
            self.speed_x = 0
            self.speed_y = 0

        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                self.generate_bullets()


class ShooterBullet(renpy.Displayable):

    solid_colour = "#ff33ee"
    solid_kwargs = {
        "xsize": 20,
        "ysize": 20
    }

    def __init__(self, displayable=None, speed=(0, 0), start=(0, 0), *args, **kwargs):
        super(ShooterBullet, self).__init__(*args, **kwargs)

        self.alive = True

    def render(self, width, height, st, at):
        render = renpy.Render(width, height)

        # Figure out the time elapsed since the previous frame.
        if self.old_st is None:
            self.old_st = st

        dtime = st - self.old_st
        self.old_st = st

        speed_x = dtime * self.speed_x
        speed_y = dtime * self.speed_y

        self.x -= speed_x
        self.y -= speed_y

        d = renpy.render(self.displayable, width, height, st, at)

        renpy.redraw(self, 0)
        render.blit(d, (self.x, self.y))

        # Kill bullets when they leave the screen
        if self.y < 0:
            self.alive = False

        return render


class EnemyShooterActor(ShooterActor):
    def __init__(self, *args, **kwargs):
        super(EnemyShooterActor, self).__init__(**kwargs)

        self.wave = 1

    def render(self, width, height, st, at):
        render = renpy.Render(width, height)

        # Figure out the time elapsed since the previous frame.
        if self.old_st is None:
            self.old_st = st

        dtime = st - self.old_st
        self.old_st = st

        self.wave -= dtime

        if self.wave <= 1:
            #foo = renpy.random.choice([-150, 150])
            foo = 150
            #self.wave = 1
        if self.wave <= 0:
            foo = -150
        if self.wave <= -1:
            self.wave = 1
            foo = 0

        speed_x = dtime * (self.max_speed_x + foo)
        speed_y = dtime * self.max_speed_y

        self.x += speed_x
        self.y += speed_y

        d = renpy.render(self.displayable, width, height, st, at)

        renpy.redraw(self, 0)
        render.blit(d, (self.x, self.y))

        return render


class EnemyGroup(object):
    def __init__(self, start=(0, 0), enemies=None):
        for enemy in enemies:
            enemy.x += start[0]
            enemy.y += start[1]

        self.enemies = enemies
