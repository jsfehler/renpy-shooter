class ShooterActor(renpy.Displayable):
    """Base class for Shooter objects.
    """
    def __init__(self, displayable, speed=(0, 0), start=(0, 0), *args, **kwargs):
        super(ShooterActor, self).__init__(**kwargs)

        # Stores the old value of the st value from render()
        self.old_st = None

        # Default displayable if none is provided.
        self.displayable = displayable or Solid("#ffffff", xsize=20, ysize=20)

        self.speed_x = speed[0]
        self.speed_y = speed[1]

        self.x = start[0]
        self.y = start[1]


class ShooterPlayer(ShooterActor):
    def __init__(self, displayable, speed=(0, 0), start=(0, 0), *args, **kwargs):
        super(ShooterPlayer, self).__init__(**kwargs)    

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

        # If there are less than the max number of bullets allowed, add a new bullet
        if len(self.bullets) < 5:
            self.bullets.append(ShooterBullet(start=(self.x, self.y)))

    def move_player(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.speed_x = -self.max_speed
        elif keys[pygame.K_RIGHT]:
            self.speed_x = self.max_speed

        if keys[pygame.K_UP]:
            self.speed_y = -self.max_speed
        elif keys[pygame.K_DOWN]:
            self.speed_y = self.max_speed

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

        old_x = self.x          
        old_y = self.y

        self.x += speed_x
        self.y += speed_y

        d = renpy.render(self.displayable, width, height, st, at)

        for bullet in self.bullets:
            b = renpy.render(item, width, height, st, at)
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