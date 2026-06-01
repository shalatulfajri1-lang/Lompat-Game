from settings import SCREEN_WIDTH


class Camera:
    def __init__(self, width, height):
        self.offset_x = 0
        self.width = width
        self.height = height

    def update(self, target_x):
        target_offset = target_x - self.width // 3
        if target_offset > self.offset_x:
            self.offset_x = target_offset

    def apply(self, entity):
        if hasattr(entity, 'rect'):
            return entity.rect.x - self.offset_x, entity.rect.y
        return entity[0] - self.offset_x, entity[1]

    def reset(self):
        self.offset_x = 0
