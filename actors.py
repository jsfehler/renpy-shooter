import copy
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

        self.width = self.solid_kwargs["xsize"]
        self.height = self.solid_kwargs["ysize"]

        self.speed_x = 0
        self.speed_y = 0

        self.max_speed_x = speed[0]
        self.max_speed_y = speed[1]

        self.x = start[0]
        self.y = start[1]

    def overlaps_with(self, other):
        """Check if this object overlaps with another one."""
        left = other.x
        right = other.x + other.width
        top = other.y
        bottom = other.y + other.height

        horizontal_hit = False
        vertical_hit = False

        if (self.x >= left) and (self.x <= right):
            horizontal_hit = True
        if (self.y >= top) and (self.y <= bottom):
            vertical_hit = True

        if horizontal_hit and vertical_hit:
            return True
        return False


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
                    enemy.kill()

            if self.overlaps_with(enemy):
                pass

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

        d = renpy.render(self.displayable, width, height, st, at)

        # Drawing bullets in ShooterPlayer's render so they
        # implicitly get added to the screen
        for bullet in self.weapon.bullets:
            b = renpy.render(bullet, width, height, st, at)
            render.blit(b, (0, 0))

        renpy.redraw(self, 0)
        render.blit(d, (self.x, self.y))

        return render

    def event(self, ev, x, y, st):
        if ev.type == pygame.KEYUP:
            self.speed_x = 0
            self.speed_y = 0

        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                self.weapon.generate_bullets()


class ShooterWeapon(store.object):
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
    solid_colour = "#ff33ee"
    solid_kwargs = {
        "xsize": 10,
        "ysize": 10
    }

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
        self.alive = True

    def kill(self):
        self.alive = False

    def render(self, width, height, st, at):
        render = renpy.Render(width, height)

        if self.alive:
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
