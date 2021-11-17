from typing import Dict
from typing import List
from collections import Counter
import copy

Image = List[List[List[int]]]


def parse_image(raw: str, width: int, height: int) -> Image:
    pixels = [int(c) for c in raw]

    num_layers = len(pixels) // width // height

    image = [
        [[None for _ in range(width)] for _ in range(height)] for _ in range(num_layers)
    ]

    layer = i = j = 0
    for pixel in pixels:
        image[layer][i][j] = pixel

        j += 1
        if j == width:
            j = 0
            i += 1

        if i == height:
            i = 0
            layer += 1

    return image


def count_colors_by_layer(image: Image) -> List[Dict[int, int]]:
    # l = []
    # for layer in image:
    #     c = Counter()
    #     for row in layer:
    #         c.update(row)
    #     l.append(c)
    return [Counter(pixel for row in layer for pixel in row) for layer in image]


def one_times_two(image: Image) -> int:
    color_counts = count_colors_by_layer(image)
    min_layer_counter = min(color_counts, key=lambda cc: cc[0])
    return min_layer_counter[1] * min_layer_counter[2]


def show(image: Image) -> None:
    consolidated = copy.deepcopy(image[0])
    num_layers = len(image)
    height = len(image[0])
    width = len(image[0][0])

    for i in range(height):
        for j in range(width):
            for layer in range(num_layers):
                color = image[layer][i][j]
                if color == 0:
                    consolidated[i][j] = " "
                    break
                if color == 1:
                    consolidated[i][j] = "*"
                    break
    for row in consolidated:
        print("".join(row))


RAW = "123456789012"
IMAGE = parse_image(RAW, 3, 2)
assert IMAGE == [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [0, 1, 2]]]
assert one_times_two(IMAGE) == 1

RAW_2 = "0222112222120000"
IMAGE_2 = parse_image(RAW_2, 2, 2)
show(IMAGE_2)

with open("day08.txt") as f:
    inp = f.readline().strip()
    image = parse_image(inp, 25, 6)
    print(f"{one_times_two(image)=}")
    show(image)
