import pyxel
import random

class ShootingGame:
    def __init__(self):
        pyxel.init(160, 120)  # "caption" argument removed
        self.width, self.height = 160, 120
        self.player_x = self.width // 2
        self.player_y = self.height - 10
        self.player_width = 16
        self.player_height = 4
        self.player_speed = 2
        self.bullets = []
        self.bullet_speed = -4
        self.targets = []
        self.target_speed = 2
        self.target_spawn_rate = 30
        self.dummy_targets = []
        self.dummy_target_speed = 2
        self.score = 0
        self.missed_shots = 0
        self.max_missed_shots = 10
        self.frame_count = 0
        pyxel.run(self.update, self.draw)

    def spawn_target(self):
        if random.random() > 0.3:
            self.targets.append([random.randint(0, self.width - 8), 0, 8, 8])
        else:
            self.dummy_targets.append([random.randint(0, self.width - 8), 0, 8, 8])

    def update(self):
        self.frame_count += 1

        # Player movement
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x = max(0, self.player_x - self.player_speed)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x = min(self.width - self.player_width, self.player_x + self.player_speed)

        # Bullet firing
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.bullets.append([self.player_x + self.player_width // 2 - 1, self.player_y])

        # Update bullets
        for bullet in self.bullets[:]:
            bullet[1] += self.bullet_speed
            if bullet[1] < 0:
                self.bullets.remove(bullet)
                self.missed_shots += 1

        # Spawn targets
        if self.frame_count % self.target_spawn_rate == 0:
            self.spawn_target()

        # Update targets
        for target in self.targets[:]:
            target[1] += self.target_speed
            if target[1] > self.height:
                self.targets.remove(target)
            for bullet in self.bullets[:]:
                if (bullet[0] < target[0] + target[2] and
                        bullet[0] + 2 > target[0] and
                        bullet[1] < target[1] + target[3] and
                        bullet[1] + 4 > target[1]):
                    self.bullets.remove(bullet)
                    self.targets.remove(target)
                    self.score += 1

        # Update dummy targets
        for dummy_target in self.dummy_targets[:]:
            dummy_target[1] += self.dummy_target_speed
            if dummy_target[1] > self.height:
                self.dummy_targets.remove(dummy_target)
            for bullet in self.bullets[:]:
                if (bullet[0] < dummy_target[0] + dummy_target[2] and
                        bullet[0] + 2 > dummy_target[0] and
                        bullet[1] < dummy_target[1] + dummy_target[3] and
                        bullet[1] + 4 > dummy_target[1]):
                    self.bullets.remove(bullet)
                    self.dummy_targets.remove(dummy_target)
                    self.score -= 1

        # Game over
        if self.missed_shots >= self.max_missed_shots:
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)

        # Draw player
        pyxel.rect(self.player_x, self.player_y, self.player_width, self.player_height, 9)

        # Draw bullets
        for bullet in self.bullets:
            pyxel.rect(bullet[0], bullet[1], 2, 4, 10)

        # Draw targets
        for target in self.targets:
            pyxel.rect(target[0], target[1], target[2], target[3], 8)

        # Draw dummy targets
        for dummy_target in self.dummy_targets:
            pyxel.rect(dummy_target[0], dummy_target[1], dummy_target[2], dummy_target[3], 12)

        # Draw score and missed shots
        pyxel.text(5, 5, f"Score: {self.score}", 7)
        pyxel.text(5, 15, f"Missed: {self.missed_shots}/{self.max_missed_shots}", 7)

# Run the game
ShootingGame()
