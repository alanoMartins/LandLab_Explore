import numpy as np
from landlab.components import FlowAccumulator, DepressionFinderAndRouter

from grid_utils import read_dem, write_dem, create_base_folder, register_custom_pallet, benchmark
from shear_stress import ShearStress


class Runner:

    def __init__(self, model_grid_path, name, checkpoint):
        self.model_grid = read_dem(model_grid_path)
        self.shear_stress = ShearStress(self.model_grid)
        self.flow_accumulator = FlowAccumulator(self.model_grid, flow_director='D8')
        self.finder_router = DepressionFinderAndRouter(self.model_grid)
        self.time_step = 1
        self.uplift_rate = 0
        self.name = name
        self.checkpoint = checkpoint

        create_base_folder(name)
        register_custom_pallet()

    def run(self, executions):
        self.flow_accumulator.run_one_step()
        for i in range(executions):
            print(f"Start interation: {i}")
            self.run_step()
            if i % self.checkpoint == 0:
                self.save_dem(i)

    @benchmark
    def run_step(self):
        #    fr.run_one_step()
        self.finder_router.map_depressions()
        flooded = np.where(self.finder_router.flood_status == 3)[0]  # ver pra que serve
        #    ed.run_one_step(time_step)
        self.model_grid.at_node['topographic__elevation'][
            self.model_grid.status_at_node == self.model_grid.BC_NODE_IS_CORE] += self.time_step * self.uplift_rate
        # no artigo ele usa em anos mas esta de acordo com todos os outros parametros em anos tbm
        #    lin_diffuse.run_one_step(time_step)
        self.shear_stress.run_one_step()

    @benchmark
    def save_dem(self, i):
        write_dem(self.name, i, self.model_grid)
