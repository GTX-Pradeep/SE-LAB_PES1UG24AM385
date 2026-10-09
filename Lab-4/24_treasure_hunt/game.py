import pygame
import random

TILE = 40
COLS, ROWS = 20, 15
WALL, FLOOR, CHEST, KEY, TRAP = 0, 1, 2, 3, 4
SPEED = 3
GUARD_SPEED = 2
GUARD_SIZE = 26

def generate_world():
    grid = [[WALL]*COLS for _ in range(ROWS)]
    rooms = []
    for _ in range(8):
        w = random.randint(3,6)
        h = random.randint(3,5)
        x = random.randint(1, COLS-w-1)
        y = random.randint(1, ROWS-h-1)
        room = pygame.Rect(x, y, w, h)
        overlap = any(room.inflate(2,2).colliderect(r) for r in rooms)
        if not overlap:
            rooms.append(room)
            for ry in range(y, y+h):
                for rx in range(x, x+w):
                    grid[ry][rx] = FLOOR

    for i in range(len(rooms)-1):
        ax, ay = rooms[i].centerx, rooms[i].centery
        bx, by = rooms[i+1].centerx, rooms[i+1].centery
        cx = ax
        while cx != bx:
            grid[ay][cx] = FLOOR
            cx += 1 if bx > cx else -1
        cy = ay
        while cy != by:
            grid[cy][bx] = FLOOR
            cy += 1 if by > cy else -1

    if len(rooms) >= 2:
        cr, ck = rooms[-1], rooms[-2]
        grid[cr.centery][cr.centerx] = CHEST
        grid[ck.centery][ck.centerx] = KEY
    for room in rooms[1:-1]:
        tx, ty = room.centerx, room.centery

        if grid[ty][tx] == FLOOR:
            grid[ty][tx] = TRAP

    start = rooms[0] if rooms else None
    return grid, start

COLORS = {
    WALL: (60,50,70),
    FLOOR: (200,190,170),
    CHEST: (200,160,30),
    KEY: (220,220,60),
    TRAP: (190,50,50),
}

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 28, 28)
        self.color = (60,120,220)
        self.has_key = False

    def move(self, keys, grid, rows, cols):
        dx=dy=0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx=-SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx=SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]: dy=-SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy=SPEED
        self._try_move(dx,0,grid,rows,cols)
        self._try_move(0,dy,grid,rows,cols)

    def _try_move(self, dx, dy, grid, rows, cols):
        new = self.rect.move(dx,dy)
        for px,py in [(new.left,new.top),(new.right-1,new.top),(new.left,new.bottom-1),(new.right-1,new.bottom-1)]:
            c,r=px//TILE,py//TILE
            if not(0<=r<rows and 0<=c<cols) or grid[r][c]==WALL:
                return
        self.rect=new

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)
        if self.has_key:
            pygame.draw.circle(screen, (220,220,60), (self.rect.right-6, self.rect.top+6), 5)


class Guard:
    def __init__(self, x, y, patrol_distance=80):
        self.rect = pygame.Rect(x, y, GUARD_SIZE, GUARD_SIZE)
        self.start_x = x
        self.end_x = x + patrol_distance
        self.speed = GUARD_SPEED

    def update(self):
        self.rect.x += self.speed

        if self.rect.right >= self.end_x:
            self.rect.right = self.end_x
            self.speed = -GUARD_SPEED
        elif self.rect.left <= self.start_x:
            self.rect.left = self.start_x
            self.speed = GUARD_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 45, 55), self.rect, border_radius=6)

WIDTH = COLS * TILE
HEIGHT = ROWS * TILE + 50
FPS = 60

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Treasure Hunt")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 24)
        self.big_font = pygame.font.SysFont("monospace", 40, bold=True)
        self.reset()

    def reset(self):
        self.grid, start = generate_world()
        if start:
            sx = start.x * TILE + 6
            sy = start.y * TILE + 6
        else:
            sx, sy = TILE+6, TILE+6
        self.player = Player(sx, sy)
        
        self.start_position = (sx, sy)

        chest_pos = next(
            (
                (c, r)
                for r in range(ROWS)
                for c in range(COLS)
                if self.grid[r][c] == CHEST
            ),
            None
        )

        if chest_pos:
            cx, cy = chest_pos
            guard_x = cx * TILE
            guard_y = cy * TILE + (TILE - GUARD_SIZE) // 2
            self.guard = Guard(guard_x, guard_y)
        else:
            self.guard = None

        self.won = False
        self.status = "Find the KEY, then the CHEST!"
    def reset_player(self):
        self.player.rect.topleft = self.start_position
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r: self.reset()
        return True

    def update(self):
        if self.won:
            return
        if self.guard:
            self.guard.update()
        keys = pygame.key.get_pressed()
        self.player.move(keys, self.grid, ROWS, COLS)
        
        if self.guard and self.player.rect.colliderect(self.guard.rect):
            self.reset_player()
            self.status = "Guard caught you! Back to start!"
            return

        pr = self.player.rect.centery // TILE
        pc = self.player.rect.centerx // TILE
        
        if 0 <= pr < ROWS and 0 <= pc < COLS:
          cell = self.grid[pr][pc]

          if cell == TRAP:
           self.reset_player()
           self.status = "Trap triggered! Back to start!"

          elif cell == KEY:
           self.player.has_key = True
           self.grid[pr][pc] = FLOOR
           self.status = "Got the key! Find the CHEST!"

          elif cell == CHEST and self.player.has_key:
           self.won = True
           self.status = "Treasure found!"
    
    def draw_minimap(self):
        map_tile = 5
        margin = 10
        map_width = COLS * map_tile
        map_height = ROWS * map_tile

        x0 = WIDTH - map_width - margin
        y0 = margin

        pygame.draw.rect(
            self.screen, (15, 15, 25),
            (x0 - 3, y0 - 3, map_width + 6, map_height + 6)
        )

        for r in range(ROWS):
            for c in range(COLS):
                color = (65, 60, 75) if self.grid[r][c] == WALL else (205, 195, 175)
                pygame.draw.rect(
                    self.screen, color,
                    (x0 + c * map_tile, y0 + r * map_tile, map_tile, map_tile)
                )

        px = x0 + (self.player.rect.centerx // TILE) * map_tile
        py = y0 + (self.player.rect.centery // TILE) * map_tile
        pygame.draw.rect(self.screen, (50, 130, 255), (px, py, map_tile, map_tile))

    def draw(self):
        self.screen.fill((30,25,40))
        for r in range(ROWS):
            for c in range(COLS):
                cell = self.grid[r][c]
                rect = pygame.Rect(c*TILE, r*TILE, TILE, TILE)
                pygame.draw.rect(self.screen, COLORS[cell], rect)
                
                if cell == KEY:
                   pygame.draw.circle(
                       self.screen, (255,240,60),
                          (c*TILE+TILE//2, r*TILE+TILE//2), 10
                    )
                elif cell == CHEST:
                    pygame.draw.rect(
                       self.screen,(180,120,20),
                             rect.inflate(-12,-12), border_radius=4
                    )
                elif cell == TRAP:
                    pygame.draw.polygon(
                        self.screen, (130,20,20),
                        [
                        (c*TILE+TILE//2, r*TILE+7),
                        (c*TILE+TILE-7, r*TILE+TILE-7),
                        (c*TILE+7, r*TILE+TILE-7)
                        ]
                    )

        self.player.draw(self.screen)
        self.draw_minimap()
        if self.guard:
         self.guard.draw(self.screen)
        
        hud = pygame.Rect(0, ROWS*TILE, WIDTH, 50)
        pygame.draw.rect(self.screen, (20,20,35), hud)

        st = self.font.render(self.status + "  |  R=Restart", True, (200,200,200))
        self.screen.blit(st, (8, ROWS*TILE + 13))

        # Inventory slot
        slot_rect = pygame.Rect(WIDTH - 55, ROWS*TILE + 5, 40, 40)
        pygame.draw.rect(self.screen, (100,100,115), slot_rect, 2)

        if self.player.has_key:
            key_x = slot_rect.centerx
            key_y = slot_rect.centery
            pygame.draw.circle(self.screen, (255,220,50), (key_x - 5, key_y - 5), 7, 3)
            pygame.draw.line(
                self.screen, (255,220,50),
                (key_x, key_y), (key_x + 10, key_y + 10), 3
            )
            pygame.draw.line(
                self.screen, (255,220,50),
                (key_x + 6, key_y + 6), (key_x + 10, key_y + 6), 3
            )

        if self.won:
            ov=pygame.Surface((WIDTH,ROWS*TILE),pygame.SRCALPHA)
            ov.fill((0,0,0,140))
            self.screen.blit(ov,(0,0))
            msg=self.big_font.render("TREASURE FOUND!", True,(220,180,30))
            sub=self.font.render("Press R to Play Again",True,(180,180,180))
            self.screen.blit(msg,(WIDTH//2-msg.get_width()//2,ROWS*TILE//2-30))
            self.screen.blit(sub,(WIDTH//2-sub.get_width()//2,ROWS*TILE//2+20))
        pygame.display.flip()

    def run(self):
        running=True
        while running:
            running=self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

if __name__ == "__main__":
    engine = GameEngine()
    engine.run()
