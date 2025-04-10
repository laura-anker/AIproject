import random

class Snake:
    def __init__(self, game_state):
        self.game_state = game_state
        self.head = game_state.head
        self.tail = game_state.tail
        self.dx = game_state.dx
        self.dy = game_state.dy
        self.scale = game_state.scale
        self.apple = game_state.apple
        self.screen = game_state.screen

    def will_hit_wall(self, dx, dy):
        next_x = self.head.x + dx
        next_y = self.head.y + dy
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        return next_x < 0 or next_x >= screen_width or next_y < 0 or next_y >= screen_height

    def will_hit_self(self, dx, dy):
        next_x = self.head.x + dx
        next_y = self.head.y + dy
        return any(segment.x == next_x and segment.y == next_y for segment in self.tail)

    def possible_moves(self):
        moves = []
        directions = [
            ("up", 0, -10 * self.scale),
            ("down", 0, 10 * self.scale),
            ("left", -10 * self.scale, 0),
            ("right", 10 * self.scale, 0)
        ]
        for name, dx, dy in directions:
            if not self.will_hit_wall(dx, dy) and not self.will_hit_self(dx, dy):
                # Prevent reversing into yourself
                if (self.dx == 0 and dx != 0) or (self.dy == 0 and dy != 0):
                    moves.append((name, dx, dy))
        if not self.will_hit_wall(self.dx, self.dy):
            moves.append(("none", self.dx, self.dy))
        return moves

    def choose_random_move(self):
        moves = self.possible_moves()
        if moves:
            move = random.choice(moves)
            self.dx, self.dy = move[1], move[2]

    def choose_move_toward_apple(self):
        moves = []

        dx_to_apple = self.apple.x - self.head.x
        dy_to_apple = self.apple.y - self.head.y

        if dx_to_apple > 0 and not self.will_hit_wall(10 * self.scale, 0) and not self.will_hit_self(10 * self.scale, 0):
            moves.append(('right', 10 * self.scale, 0))
        elif dx_to_apple < 0 and not self.will_hit_wall(-10 * self.scale, 0) and not self.will_hit_self(-10 * self.scale, 0):
            moves.append(('left', -10 * self.scale, 0))

        if dy_to_apple > 0 and not self.will_hit_wall(0, 10 * self.scale) and not self.will_hit_self(0, 10 * self.scale):
            moves.append(('down', 0, 10 * self.scale))
        elif dy_to_apple < 0 and not self.will_hit_wall(0, -10 * self.scale) and not self.will_hit_self(0, -10 * self.scale):
            moves.append(('up', 0, -10 * self.scale))

        if not moves:
            moves = self.possible_moves()

        if moves:
            move = random.choice(moves)
            self.dx, self.dy = move[1], move[2]
