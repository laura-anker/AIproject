from Entity import Entity

class GameState:
    def __init__(self, edibles_two_player_scene):
        self.head = edibles_two_player_scene.head
        self.tail = edibles_two_player_scene.tail
        self.dx = edibles_two_player_scene.dx1
        self.dy = edibles_two_player_scene.dy1
        self.apple = edibles_two_player_scene.apple
        self.walls = self.get_walls(edibles_two_player_scene.w, edibles_two_player_scene.h, edibles_two_player_scene.director.scale)
        self.scale = edibles_two_player_scene.director.scale
        self.screen = edibles_two_player_scene.director.screen

    def get_walls(self, width, height, scale):
        walls = []
        for i in range(0, width, 10 * scale):
            walls.append(Entity(i, 0, 10 * scale, 10 * scale, (255, 255, 255)))  # top wall
            walls.append(Entity(i, height - 10 * scale, 10 * scale, 10 * scale, (255, 255, 255)))  # bottom wall
        for i in range(0, height, 10 * scale):
            walls.append(Entity(0, i, 10 * scale, 10 * scale, (255, 255, 255)))  # left wall
            walls.append(Entity(width - 10 * scale, i, 10 * scale, 10 * scale, (255, 255, 255)))  # right wall
        return walls

    def get_position(self):
        return self.head.x, self.head.y

    def get_apple_position(self):
        return self.apple.x, self.apple.y

    def get_tail_positions(self):
        return [(segment.x, segment.y) for segment in self.tail]

    def get_wall_positions(self):
        return [(wall.x, wall.y) for wall in self.walls]
