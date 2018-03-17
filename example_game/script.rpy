default standard_bullet = ShooterBullet(Image("bullet.png"), speed=(300, 0))
default actor = ShooterPlayer(Image("actor.png"), bullet=standard_bullet, start=(400, 400), speed=(300, 300))

default enemy1 = EnemyShooterActor(Image("actor.png"), speed=(0, 150), start=(0, 0))
default enemy2 = EnemyShooterActor(Image("actor.png"), speed=(0, 150), start=(0, 50))

default enemy_group = EnemyGroup(start=(400, 0), enemies=[enemy1, enemy2])

screen shooter_main():
    add actor

    for enemy in enemy_group.enemies:
        add enemy

label start:
    $ actor.enemies = [enemy1, enemy2]
    call screen shooter_main