import arcade


class Button:
    def __init__(self, image_path, hover_image_path, x, y, action, scale = 1.0):
        self.image = arcade.load_texture(image_path)
        self.hover_image = arcade.load_texture(hover_image_path)
        self.current_image = self.image
        self.x = x
        self.y = y
        self.action = action
        self.scale = scale
        self.width = self.image.width * self.scale
        self.height = self.image.height * self.scale

    def draw(self):
        # Draw the image with a tint if hovered or selected
        arcade.draw_texture_rectangle(self.x, self.y, self.width, self.height, self.current_image)

    def check_mouse_hover(self, x, y):
        if self.x - self.width / 2 < x < self.x + self.width / 2 and self.y - self.height / 2 < y < self.y + self.height / 2:
            self.current_image = self.hover_image
            return True
        else:
            self.current_image = self.image
            return False

    def select(self):
        self.current_image = self.hover_image

    def deselect(self):
        self.current_image = self.image