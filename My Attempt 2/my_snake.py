import numpy as np
import pygame

pygame.init()

class Snake:
    def __init__(self, useUI=True, grid_width=32, grid_height=20, block_size=20, game_speed=40):
        self.ui = useUI

        self.width = grid_width
        self.height = grid_height
        self.size = block_size

        if useUI:
            self.clock = pygame.time.Clock()
            self.display = pygame.display.set_mode((grid_width * block_size, grid_height * block_size))
            pygame.display.set_caption('Snake')
            self.boardUI = pygame.image.load('board.png').convert()
            self.snakeUI = pygame.image.load('snake_piece.png').convert()
            self.fruitUI = pygame.image.load('fruit2.png').convert_alpha()
            self.font = pygame.font.Font('arial.ttf', 25)
            self.fontColor = (0, 0, 0)
            self.speed = game_speed
        else:
            pygame.quit()

        self.reset()
    
    def reset(self):
        self.pieces = [[self.width // 2, self.height // 2],
                        [self.width // 2 - 1, self.height // 2],
                        [self.width // 2 - 2, self.height // 2]]
        self.direction = 1
        self.fruit = self.pieces[0]
        self.moveFruit()
        self.frame = 0
        self.score = 0



    def step(self, action, draw=True):
        self.frame += 1

        # Check user input
        if self.ui:
            # Check for window close
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        # Use input to rotate
        if np.array_equal(action, [1, 0, 0]):
            # Turn left by subtracting 1 (0 goes to 3)
            # self.direction = (self.direction + 3) % 4
            pass
        elif np.array_equal(action, [0, 1, 0]):
            # Straight - no change
            self.direction = (self.direction + 1) % 4 # right
            pass
        else: #[0, 0, 1]
            # Turn right by adding 1 (3 goes to 0)
            # self.direction = (self.direction + 1) % 4
            self.direction = (self.direction + 3) % 4 # left

        # Move snake
        headPiece = [self.pieces[-1][0], self.pieces[-1][1]]
        if self.direction == 0: # Up
            headPiece[1] -= 1
        elif self.direction == 1: # Right
            headPiece[0] += 1
        elif self.direction == 2: # Down
            headPiece[1] += 1
        elif self.direction == 3: # Left
            headPiece[0] -= 1

        # Check for game over
        game_over = False
        reward = 0
        if self.dangerAt(headPiece) or self.frame > 100 * len(self.pieces):
            reward = -10
            game_over = True
            return reward, game_over, self.score

        self.pieces.append(headPiece)

        # Collect fruit
        if self.fruit in self.pieces:
            self.score += 1
            reward = 10
            self.moveFruit()
        else:
            del self.pieces[0]
            pass


        # Update UI
        if self.ui and draw:
            self.update_ui()
            self.clock.tick(self.speed)

        # Return status
        return reward, game_over, self.score


    def dangerAt(self, location):
        return location in self.pieces or location[0] < 0 or location[0] >= self.width or location[1] < 0 or location[1] >= self.height

    def moveFruit(self):
        while self.fruit in self.pieces:
            self.fruit = [np.random.randint(0, self.width), np.random.randint(0, self.height)]

    def update_ui(self):
        # Background image
        self.display.blit(self.boardUI, (0, 0))
        
        # Snake pieces
        for piece in self.pieces:
            self.display.blit(self.snakeUI, (piece[0] * self.size, piece[1] * self.size))
        
        # Fruit
        self.display.blit(self.fruitUI, (self.fruit[0] * self.size, self.fruit[1] * self.size))
        
        # Score
        text = self.font.render("Score: " + str(self.score), True, self.fontColor)
        self.display.blit(text, [0, 0])
        
        # Update display image
        pygame.display.flip()

    def get_state(self):
        
        headPiece = self.pieces[-1]

        point_l = [headPiece[0] - 1, headPiece[1]]
        point_r = [headPiece[0] + 1, headPiece[1]]
        point_u = [headPiece[0], headPiece[1] - 1]
        point_d = [headPiece[0], headPiece[1] + 1]

        dir_l = self.direction == 3
        dir_r = self.direction == 1
        dir_u = self.direction == 0
        dir_d = self.direction == 2

        state = [
            #Danger straight
            (dir_r and self.dangerAt(point_r)) or
            (dir_l and self.dangerAt(point_l)) or
            (dir_u and self.dangerAt(point_u)) or
            (dir_d and self.dangerAt(point_d)),
            
            #Danger right
            (dir_u and self.dangerAt(point_r)) or
            (dir_d and self.dangerAt(point_l)) or
            (dir_l and self.dangerAt(point_u)) or
            (dir_r and self.dangerAt(point_d)),

            #Danger left
            (dir_d and self.dangerAt(point_r)) or
            (dir_u and self.dangerAt(point_l)) or
            (dir_r and self.dangerAt(point_u)) or
            (dir_l and self.dangerAt(point_d)),

            #Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            #Food location
            self.fruit[0] < self.pieces[-1][0], #food left
            self.fruit[0] > self.pieces[-1][0], #food right
            self.fruit[1] < self.pieces[-1][1], #food up
            self.fruit[1] > self.pieces[-1][1] #food down
        ]

        return np.array(state, dtype=int)
