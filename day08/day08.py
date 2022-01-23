from typing import NamedTuple
from typing import Iterator
from typing import Tuple
from typing import Dict
from typing import List
from collections import Counter

from numpy.lib.histograms import histogram_bin_edges


class Image(NamedTuple):
    n_layer: int
    height: int
    width: int
    numbers_iter: Iterator = None
    structure: List[List[List[int]]] = None


def parse(s: str, height=6, width=25) -> Tuple:
    numbers_list = [int(c) for c in s.strip()]
    numbers_iter = iter(numbers_list)
    n_layer = len(numbers_list) // height // width
    return n_layer, height, width, numbers_iter


def build(n_layer: int, height: int, width: int, numbers_iter: Iterator) -> Image:
    structure = []
    for layer in range(n_layer):
        structure.append([])
        for line in range(height):
            structure[layer].append([])
            for position in range(width):
                structure[layer][line].append(next(numbers_iter))
    return Image(n_layer, height, width, numbers_iter, structure)


def count_zeros(image: Image) -> Dict[int, int]:
    d = {}
    for i, layer in enumerate(image.structure):
        flat = [el for sublist in layer for el in sublist]
        d[i] = Counter(flat)[0]
    return d


def calculate_result(image: Image, d: Dict) -> int:
    min_layer = min(d, key=d.get)
    counter_target_layer = Counter(
        [el for sublist in image.structure[min_layer] for el in sublist]
    )
    return counter_target_layer[1] * counter_target_layer[2]


# 0 is black, 1 is white, and 2 is transparent.
def read_image(image: Image) -> Image:
    position_values = []
    for i in range(image.height):
        for j in range(image.width):
            values = []
            for layer in range(image.n_layer):
                val = image.structure[layer][i][j]
                values.append(val)
            position_values.append(tuple(values))
    # e.g. position_values= [(0, 1, 2, 0), (2, 1, 2, 0), (2, 2, 1, 0), (2, 2, 2, 0)]

    final_values = []
    for tpl in position_values:
        final_values.append([color for color in tpl if color != 2][0])

    merged_layers = build(1, image.height, image.width, iter(final_values))
    return merged_layers


def convert_to_string(image: Image) -> str:
    """One layered image needed here, see read_image function"""
    base = image.structure[0]
    for row in base:
        print("".join([" " if char == 0 else "*" for char in row]))
    return base


with open("day08.txt") as f:
    IMG = build(*parse("123456789012", height=2, width=3))
    assert IMG.structure == [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [0, 1, 2]]]

    inp = f.readline()
    img = build(*parse(inp))
    print("PART 1", f"{calculate_result(img, count_zeros(img))=}", sep="\n")

    IMG_2 = build(*parse("0222112222120000", height=2, width=2))
    assert read_image(IMG_2).structure == [[[0, 1], [1, 0]]]

    one_layer_img = read_image(img)
    print("PART 2")
    convert_to_string(one_layer_img)

d = {"a": one, "b": two}
