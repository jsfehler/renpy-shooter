default actor = ShooterPlayer(start=(400, 400), speed=(300, 300))

default enemy1 = EnemyShooterActor(speed=(0, 150), start=(0, 0))
default enemy2 = EnemyShooterActor(speed=(0, 150), start=(0, -50))

default enemy_group = EnemyGroup(start=(400, 0), enemies=[enemy1, enemy2])
    
screen shooter():    
    add actor
    
    for enemy in enemy_group.enemies:
        add enemy
    
label start:
    
    call screen shooter
