class Image:
    def __init__(self, data, width, height):
        self.data = data
        self.width = width
        self.height = height

        self.layer_size = width * height
        self.num_layers = len(data) // self.layer_size
        self.layers = [
            self.data[i * self.layer_size : (i + 1) * self.layer_size]
            for i in range(self.num_layers)
        ]

    def layer_with_least_zeroes(self):
        min_zeroes = None
        min_layer = None
        for l in self.layers:
            zeroes = l.count(0)
            if min_zeroes is None or zeroes < min_zeroes:
                min_zeroes = zeroes
                min_layer = l
        return min_layer

    def blend(self):
        final = [-1 for _ in range(self.layer_size)]
        for l in reversed(self.layers):
            for i in range(self.layer_size):
                if l[i] in (0, 1) or final[i] == -1:
                    final[i] = l[i]
        return final

    def draw(self):
        layer = self.blend()
        for y in range(self.height):
            for x in range(self.width):
                c = " "
                if layer[y * self.width + x] == 1:
                    c = "*"
                print(c, end="")
            print()


if __name__ == "__main__":
    data = [int(p) for p in open("input.txt").read().strip()]
    image = Image(data, 25, 6)

    layer = image.layer_with_least_zeroes()
    result1 = layer.count(1) * layer.count(2)
    print(f"Part 1: {result1}")
    print("Part 2:")
    image.draw()
