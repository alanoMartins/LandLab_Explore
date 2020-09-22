import os
from landlab.components import FlowAccumulator, SedDepEroder,FastscapeEroder,LinearDiffuser, ErosionDeposition, DepressionFinderAndRouter
from landlab import RasterModelGrid
import landlab
import numpy as np
import statistics
from pylab import show, figure
from landlab.io import read_esri_ascii
from landlab import Component
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from landlab.io.esri_ascii import write_esri_ascii
from shear_component import Shear_Stress


def create_folder(name):
    parent_folder = "../testes_dispersao"
    path = os.path.join(parent_folder, name)
    if not os.path.exists(path):
        os.mkdir(path)

test_name = 'asc_crop_ed_time_step_100_alano'
create_folder(test_name)

(mg, z) = read_esri_ascii("../save_asc/testes/ascii_cropadotest.asc", name="topographic__elevation")
mg.at_node.keys()#lista os grids contidos no DEM

mg.BC_LINK_IS_FIXED
#mg.set_fixed_value_boundaries_at_grid_edges(right, top, left, bottom)
mg.set_fixed_value_boundaries_at_grid_edges(True, True, True, True)

#fda = FlowAccumulator(mg, 'topographic__elevation') #cria o componente flow accumulator
css = Shear_Stress(mg) #cria o componente shear stress
fr = FlowAccumulator(mg, flow_director='D8')
df = DepressionFinderAndRouter(mg)
sp = FastscapeEroder(mg, K_sp=0.001, m_sp=0.5, n_sp=1.0, threshold_sp= 0.0) #k eh erodibilidade, usar 0.0004
#FastscapeEroder(grid, K_sp=0.001, m_sp=0.5, n_sp=1.0, threshold_sp=0.0, discharge_field='drainage_area', erode_flooded_nodes=True)
ed = ErosionDeposition(
     mg,
     K=0.0004, # Erodibility for substrate (units vary)valor anterior = 0.00001
     v_s=0.001, # Effective settling velocity for chosen grain size metric [L/T].
     m_sp=0.5, # Discharge exponent (units vary) usar valores do fast scape (valor anterior = 0.5)
     n_sp = 1.0, #Slope exponent (units vary) usar valores do fast scape
     sp_crit=0) #Critical stream power to erode substrate [E/(TL^2)] usar valores do fast scape
lin_diffuse = LinearDiffuser (mg, linear_diffusivity = 0.01)

uplift_rate = 0.001
time_step = 1000
fr.run_one_step()
sp.run_one_step(time_step)
for i in range(101):
    print(i)
    fr.run_one_step()
    df.map_depressions()
    flooded = np.where(df.flood_status==3)[0] # ver pra que serve
    ed.run_one_step(time_step)
    mg.at_node['topographic__elevation'] += time_step * uplift_rate
    #no artigo ele usa em anos mas esta de acordo com todos os outros parametros em anos tbm
    #lin_diffuse.run_one_step(time_step)
    css.run_one_step()
    if i == 1  or i == 10 or i ==20 or i == 40 or i == 60 or i == 80 or i == 100:
        files = write_esri_ascii("../testes_dispersao/"+test_name+"/"+str(i)+".asc", mg)
