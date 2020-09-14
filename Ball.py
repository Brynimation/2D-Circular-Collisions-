import pygame as pg
class Ball:
    numBalls = 0
    def __init__(self, px, py, radius, colour):
        Ball.numBalls +=1
        self.pos = pg.math.Vector2(px, py)
        self.radius = radius
        self.colour = colour
        self.vel = pg.math.Vector2(0, 0)
        self.acc = pg.math.Vector2(0, 0)
        self.mass = 2 * self.radius
        self.selected = False
        self.id = Ball.numBalls

    def display(self, win):
        pg.draw.circle(win, self.colour, (int(self.pos.x), int(self.pos.y)), self.radius)
    
    def collisionCheck(self, vec, dist):
        if self.pos.distance_to(vec) <= dist:
            return True

    def staticCollision(self, balls, win):
        for b in balls:
            if b != self:
                if self.collisionCheck(b.pos, self.radius + b.radius):
                    disp = self.pos - b.pos
                    amountOverlapped =  disp.magnitude() - (self.radius + b.radius)
                    amountDisplaced = 0.5*amountOverlapped
                    self.pos -= amountDisplaced * disp.normalize()
                    b.pos += amountDisplaced * disp.normalize()
                    pg.draw.line(win, (0, 0, 255), b.pos, self.pos)
                    self.dynamicCollision(b, win)

    def dynamicCollision(self, b, win):
        if self.vel.magnitude() > 0 or b.vel.magnitude() > 0:
            sumMasses = self.mass + b.mass
            velDifferenceSelf = self.vel - b.vel
            velDifferenceB = b.vel - self.vel
            posDifferenceSelf = self.pos - b.pos
            posDifferenceB = b.pos - self.pos
            posDifferenceMag = posDifferenceSelf.magnitude_squared()
            dotProductSelf = velDifferenceSelf.dot(posDifferenceSelf)
            dotProductB = velDifferenceB.dot(posDifferenceB)
            self.vel -= (2*b.mass/sumMasses) * (dotProductSelf / posDifferenceMag) * posDifferenceSelf
            b.vel -= (2*self.mass/sumMasses) * (dotProductB / posDifferenceMag) * posDifferenceB


    def updatePos(self, vel, width, height, CoF):
        self.vel = vel
        self.acc = -CoF * self.vel
        self.vel +=self.acc
        self.pos +=self.vel

        if self.vel.magnitude() < 0.0001:
            self.vel = pg.math.Vector2(0, 0)
            self.acc = pg.math.Vector2(0, 0)

        if self.pos.x < 0:
            self.pos.x = width
        elif self.pos.x > width:
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = height
        elif self.pos.y > height:
            self.pos.y = 0

        





        



