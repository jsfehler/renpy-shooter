import renpy.exports as renpy


class ShooterActor(renpy.Displayable):
    """Base class for Shooter objects.
    """
    def __init__(self, displayable, speed=(0, 0), start=(0, 0),
                 *args, **kwargs):
        super(ShooterActor, self).__init__(*args, **kwargs)

        self.displayable = displayable

        self.speed_x = 0
        self.speed_y = 0

        self.max_speed_x = speed[0]
        self.max_speed_y = speed[1]

        self.x = start[0]
        self.y = start[1]

        # Stores the old value of the st value from render()
        self.old_st = None

        self.alive = True

        self.displayable_render = None

    @property
    def width(self):
        try:
            return self.displayable_render.get_size()[0]
        except AttributeError:
            return 0

    @property
    def height(self):
        try:
            return self.displayable_render.get_size()[1]
        except AttributeError:
            return 0

    def overlaps_with(self, other):
        """Check if this object's rectangle overlaps with another one."""

        left = self.x
        right = self.x + self.width
        top = self.y
        bottom = self.y + self.height

        other_left = other.x
        other_right = other.x + other.width
        other_top = other.y
        other_bottom = other.y + other.height

        horizontal_hit = False
        vertical_hit = False

        # Left side of self hits other
        if (left >= other_left) and (left <= other_right):
            horizontal_hit = True

        # Right side of self hits other
        if (right >= other_left) and (right <= other_right):
            horizontal_hit = True

        # Top side of self hits other
        if (top >= other_top) and (top <= other_bottom):
            vertical_hit = True

        # Bottom side of self hits other
        if (bottom >= other_top) and (bottom <= other_bottom):
            vertical_hit = True

        if horizontal_hit and vertical_hit:
            return True
        return False

    def inside_bounds(self):
        """Check if Actor is in the screen bounds."""
        if (self.x < 0) or (self.x > config.screen_width):
            return False
        elif (self.y < 0) or (self.y > config.screen_height):
            return False

        return True
