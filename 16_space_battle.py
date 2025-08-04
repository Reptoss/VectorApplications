from lib.window_arena import *
from lib.winobj_ship import *
from typing import List

# update ship (this is where your code goes)

def updateShip1(ship: Ship, powerUps: List[PowerUp], targets: List[Target]):
    #ThrustLeft/Right takes a degree to move
    #Thrust takes a constant (distance)
    ship.setPlayerName("Neev")
    
    #turnSpeed = 180 # can turn 180 degrees per second (fully rotate in 2 seconds)
    closestTarget = targets[0]
    tDst = ((ship.pos[0]-closestTarget.pos[0])**2+(ship.pos[1]-closestTarget.pos[1])**2)**0.5
    for t in targets:
        dst = ((ship.pos[0]-t.pos[0])**2+(ship.pos[1]-t.pos[1])**2)**0.5
        if dst < tDst:
            closestTarget = t
            tDst = dst

    if ship.ammo > 0 and tDst < ship.ammoMaxRange:
        # Estimate time to impact
        shootSpeed = 8
        dist = length(closestTarget.pos - ship.pos)
        timeToImpact = dist / shootSpeed #+ closestTarget.vel
        u = ship.dir
        v = closestTarget.pos-ship.pos
        uMag = ( u[0]**2 + u[1]**2 )**0.5
        vMag = ( v[0]**2 + v[1]**2 )**0.5
        r = dot(u, v) / (uMag * vMag)
        if r < -1: r = -1
        elif r > 1: r = 1
        theta = acosDeg(r)
        newPos = closestTarget.pos + (theta / ship.shipTurnSpeed) * closestTarget.vel
        
        # Predict future position of the target
        predPos = newPos + closestTarget.vel * timeToImpact

        tDir = predPos-ship.pos
        if (((ship.pos[0]-predPos[0])**2+(ship.pos[1]-predPos[1])**2)**0.5 <= ship.ammoMaxRange):
            ship.queueCommand(ShipCmd_Shoot(tDir))


    else:
        closestPowerUp = powerUps[0]
        dist = ((ship.pos[0]-closestPowerUp.pos[0])**2+(ship.pos[1]-closestPowerUp.pos[1])**2)**0.5
        for p in powerUps:
            dst = ((ship.pos[0]-p.pos[0])**2+(ship.pos[1]-p.pos[1])**2)**0.5
            # if p.type == "R" and ship.ammoMaxRange > 15:
            #     dst = 99
            if dst < dist:
                closestPowerUp = p
                dist = dst
        u = ship.dir
        v = closestPowerUp.pos-ship.pos
        uMag = ( u[0]**2 + u[1]**2 )**0.5
        vMag = ( v[0]**2 + v[1]**2 )**0.5
        r = dot(u, v) / (uMag * vMag)
        if r < -1: r = -1
        elif r > 1: r = 1
        theta = acosDeg(r)
        # Use 2D cross product to determine turn direction
        cross = u[0]*v[1] - u[1]*v[0]
        if cross > 0:
            ship.queueCommand(ShipCmd_ThrustRight(theta))
        else:
            ship.queueCommand(ShipCmd_ThrustLeft(theta))
        ship.queueCommand(ShipCmd_Thrust(dist))
    print(ship.ammoMaxRange,ship.activeCommand,ship.shipMoveSpeed,ship.shipTurnSpeed,ship.ammo)

def multiPlayer(ship: Ship, powerUps: List[PowerUp], targets: List[Target]):
    #ThrustLeft/Right takes a degree to move
    #Thrust takes a constant (distance)
    ship.setPlayerName("Jeev")
    
    #turnSpeed = 180 # can turn 180 degrees per second (fully rotate in 2 seconds)
    # closestTarget = targets[0]
    # tDst = ((ship.pos[0]-closestTarget.pos[0])**2+(ship.pos[1]-closestTarget.pos[1])**2)**0.5
    # for t in targets:
    #     dst = ((ship.pos[0]-t.pos[0])**2+(ship.pos[1]-t.pos[1])**2)**0.5
    #     if dst < tDst:
    #         closestTarget = t
    #         tDst = dst
    otherShip = ship.getOther()
    shipDistance = ((ship.pos[0]-otherShip.pos[0])**2+(ship.pos[1]-otherShip.pos[1])**2)**0.5
    if ship.ammo > 0 and shipDistance < ship.ammoMaxRange:
        # Estimate time to impact
        shootSpeed = 8
        dist = length(otherShip.pos - ship.pos)
        timeToImpact = dist / shootSpeed #+ closestTarget.vel
        u = ship.dir
        v = otherShip.pos-ship.pos
        uMag = ( u[0]**2 + u[1]**2 )**0.5
        vMag = ( v[0]**2 + v[1]**2 )**0.5
        r = dot(u, v) / (uMag * vMag)
        if r < -1: r = -1
        elif r > 1: r = 1
        theta = acosDeg(r)
        newPos = otherShip.pos + (theta / ship.shipTurnSpeed) * otherShip.vel
        
        # Predict future position of the target
        predPos = newPos + otherShip.vel * timeToImpact

        targetDirection = predPos-ship.pos
        if (((ship.pos[0]-predPos[0])**2+(ship.pos[1]-predPos[1])**2)**0.5 <= ship.ammoMaxRange):
            ship.queueCommand(ShipCmd_Shoot(targetDirection))
    

    else:
        closestPowerUp = powerUps[0]
        dist = ((ship.pos[0]-closestPowerUp.pos[0])**2+(ship.pos[1]-closestPowerUp.pos[1])**2)**0.5
        for p in powerUps:
            dst = ((ship.pos[0]-p.pos[0])**2+(ship.pos[1]-p.pos[1])**2)**0.5
            if p.type == "R" and ship.ammoMaxRange > 15:
                dst = 99
            if dst < dist:
                closestPowerUp = p
                dist = dst
        u = ship.dir
        v = closestPowerUp.pos-ship.pos
        uMag = ( u[0]**2 + u[1]**2 )**0.5
        vMag = ( v[0]**2 + v[1]**2 )**0.5
        r = dot(u, v) / (uMag * vMag)
        if r < -1: r = -1
        elif r > 1: r = 1
        theta = acosDeg(r)
        # Use 2D cross product to determine turn direction
        cross = u[0]*v[1] - u[1]*v[0]
        if cross > 0:
            ship.queueCommand(ShipCmd_ThrustRight(theta))
        else:
            ship.queueCommand(ShipCmd_ThrustLeft(theta))
        ship.queueCommand(ShipCmd_Thrust(dist))
    print(ship.ammoMaxRange,ship.activeCommand,ship.shipMoveSpeed,ship.shipTurnSpeed,ship.ammo)


####################################################################################################
############################## DO NOT MODIFY  METHODS BELOW THIS LINE ##############################
########################## EXCEPT TO REMOVE TUTORIAL GAME CONFIG ARGUMENT  #########################
####################################################################################################
WindowArena(userCode1 = updateShip1,
            gameConfig = WindowArenaConfig.SPACE_BATTLE,
            windowTitle = "Lab 16: Space Battle!").runGameLoop()
