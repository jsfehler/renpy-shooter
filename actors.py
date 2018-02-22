class ShooterActor(renpy.Displayable):
    """Base class for Shooter objects.
    """
    def __init__(self, colour="#ffffff", speed=(0, 0), start=(0, 0), *args, **kwargs):
        super(ActorDisplayable, self).__init__(**kwargs)

        # Stores the old value of the st value from render()
        self.old_st = None

        # Default displayable if none is provided.
        self.displayable = Solid(colour, xsize=20, ysize=20)

        self.speed_x = speed[0]
        self.speed_y = speed[1]

        self.x = start[0]
        self.y = start[1]
