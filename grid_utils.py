import os

import landlab
import matplotlib.pyplot as plt
from landlab.io import read_esri_ascii
from landlab.io.esri_ascii import write_esri_ascii
from matplotlib.colors import LinearSegmentedColormap
import time

OUTPUT_FOLDER = "./output"


def register_custom_pallet():
    colors = [
        (0, 170 / 255, 255 / 255),
        (123 / 255, 239 / 255, 91 / 255),
        (246 / 255, 247 / 255, 188 / 255),
        (255 / 255, 255 / 255, 0 / 255),
        (244 / 255, 212 / 255, 116 / 255),
        (255 / 255, 128 / 255, 0 / 255),
        (165 / 255, 81 / 255, 22 / 255)]  # R -> G -> B
    n_bins = 7  # Discretizes the interpolation into bins
    cmap_name = 'mcmap'
    cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)
    plt.register_cmap(cmap=cm)


def read_dem(path):
    (mg, z) = read_esri_ascii(path, name="topographic__elevation")
    return mg


def create_base_folder(name):
    path = os.path.join(OUTPUT_FOLDER, name)
    create_folder(path)


def create_folder(path):
    if not os.path.exists(path):
        os.mkdir(path)


def write_dem(name, output, model_grid):
    path = os.path.join(OUTPUT_FOLDER, name + "/" + str(output))
    create_folder(path)

    landlab.plot.imshow.imshow_grid_at_node(model_grid, 'grain_type', cmap='mcmap', output=path + "/grain_type.jpg")
    landlab.plot.imshow.imshow_grid_at_node(model_grid, "drainage_area", output=path + "/drainage_area.jpg")
    landlab.plot.imshow.imshow_grid_at_node(model_grid, 'shear_stress_discrete', cmap='Dark2', output=path + "/shear_stress_discrete.jpg")
    landlab.plot.imshow.imshow_grid_at_node(model_grid, 'topographic__elevation', cmap='terrain', output=path + "/topographic__elevation.jpg")

    return write_esri_ascii(path + "/" + str(output) + ".asc", model_grid)


def benchmark(fn):
    def _timing(*a, **kw):
        st = time.perf_counter()
        r = fn(*a, **kw)
        print(f"{fn.__name__} execution: {time.perf_counter() - st} seconds")
        return r

    return _timing