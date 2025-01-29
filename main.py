import pygame
import random
from pygame.math import Vector2

# Configuración
WIDTH, HEIGHT = 800, 600
PARTICLE_COUNT = 150  # Reducido para mejor rendimiento
GRAVITY_STRENGTH = 1200
BASE_GRAVITY = Vector2(0, 0.5)
DAMPING = 0.98
BOUNCE = -0.8
PARTICLE_SIZE = 3
MIN_DISTANCE = 2 * PARTICLE_SIZE  # Distancia mínima entre partículas

class Particle:
    def __init__(self):
        self.pos = Vector2(random.randrange(WIDTH), random.randrange(HEIGHT))
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)
        self.color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )

    def apply_force(self, force):
        self.acc += force

    def update(self):
        self.vel += self.acc
        self.vel *= DAMPING
        self.pos += self.vel
        self.acc *= 0  # Resetear aceleración

        # Límites de la pantalla
        if self.pos.x < 0:
            self.pos.x = 0
            self.vel.x *= BOUNCE
        elif self.pos.x > WIDTH:
            self.pos.x = WIDTH
            self.vel.x *= BOUNCE
        if self.pos.y < 0:
            self.pos.y = 0
            self.vel.y *= BOUNCE
        elif self.pos.y > HEIGHT:
            self.pos.y = HEIGHT
            self.vel.y *= BOUNCE

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), PARTICLE_SIZE)

def handle_collisions(particles):
    for i in range(len(particles)):
        for j in range(i+1, len(particles)):
            p1 = particles[i]
            p2 = particles[j]
            
            # Vector y distancia entre partículas
            distance_vec = p2.pos - p1.pos
            distance_sq = distance_vec.length_squared()
            
            # Distancia mínima al cuadrado
            min_distance_sq = MIN_DISTANCE ** 2
            
            if 0 < distance_sq < min_distance_sq:
                distance = distance_vec.length()
                normal = distance_vec / distance
                overlap = (MIN_DISTANCE - distance) / 2
                
                # Corregir posición
                p1.pos -= normal * overlap
                p2.pos += normal * overlap
                
                # Transferencia de velocidad (masas iguales)
                v1n = p1.vel.dot(normal)
                v2n = p2.vel.dot(normal)
                
                p1.vel += (v2n - v1n) * normal
                p2.vel += (v1n - v2n) * normal

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Particle Collision System")
    clock = pygame.time.Clock()

    particles = [Particle() for _ in range(PARTICLE_COUNT)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mouse_pos = Vector2(pygame.mouse.get_pos())
        
        # Aplicar fuerzas
        for particle in particles:
            to_mouse = mouse_pos - particle.pos
            distance_sq = to_mouse.length_squared()
            
            if distance_sq > 0:
                force = to_mouse.normalize() * (GRAVITY_STRENGTH / (distance_sq + 1))
                particle.apply_force(force)
            
            particle.apply_force(BASE_GRAVITY)
            particle.update()
        
        # Manejar colisiones
        handle_collisions(particles)
        
        # Dibujar
        screen.fill((0, 0, 0))
        for particle in particles:
            particle.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
