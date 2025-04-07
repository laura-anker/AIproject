from Entity import Entity

class GameState:
    def __init__(self, edibles_two_player_scene):
        self.player1_head = edibles_two_player_scene.head_1
        self.player2_head = edibles_two_player_scene.head_2
        self.player1_tail = edibles_two_player_scene.tail_1
        self.player2_tail = edibles_two_player_scene.tail_2
        self.apple = edibles_two_player_scene.apple
        self.walls = self.get_walls(edibles_two_player_scene.w, edibles_two_player_scene.h, edibles_two_player_scene.director.scale)

    def get_walls(self, width, height, scale):
        walls = []
        for i in range(0, width, 10 * scale):
            walls.append(Entity(i, 0, 10 * scale, 10 * scale, (255, 255, 255)))  # top wall
            walls.append(Entity(i, height - 10 * scale, 10 * scale, 10 * scale, (255, 255, 255)))  # bottom wall
        for i in range(0, height, 10 * scale):
            walls.append(Entity(0, i, 10 * scale, 10 * scale, (255, 255, 255)))  # left wall
            walls.append(Entity(width - 10 * scale, i, 10 * scale, 10 * scale, (255, 255, 255)))  # right wall
        return walls

    def get_player1_position(self):
        return self.player1_head.x, self.player1_head.y

    def get_player2_position(self):
        return self.player2_head.x, self.player2_head.y

    def get_apple_position(self):
        return self.apple.x, self.apple.y

    def get_player1_tail_positions(self):
        return [(segment.x, segment.y) for segment in self.player1_tail]

    def get_player2_tail_positions(self):
        return [(segment.x, segment.y) for segment in self.player2_tail]

    def get_wall_positions(self):
        return [(wall.x, wall.y) for wall in self.walls]
