from landlab.components import FlowAccumulator, SedDepEroder
from landlab import RasterModelGrid
import landlab
import numpy as np
from pylab import show, figure
from landlab.io import read_esri_ascii


(mg, z) = read_esri_ascii("bacia_piratini_90m.asc", name="topographic__elevation")

fda = FlowAccumulator(mg, 'topographic__elevation')
sde1 = SedDepEroder(mg, Qc="MPM")

fda.run_one_step()
sde1.run_one_step(dt=30) #dt em anos

print(sde1.characteristic_grainsize)
