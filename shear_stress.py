import copy

import numpy as np
from landlab import Component


class ShearStress(Component):  # classe do componente criado

    _name = "Shear_Stress"

    # parametros iniciais do objeto
    def __init__(self, dem, fluid_density=1050, g=9.80665, runoff=1, k_Q=2.5e-07, c_sp=1,
                 drain_area_threshold=None):

        super().__init__(dem)
        self._dem = dem
        # The rate of excess overland flow production at each node (i.e.,rainfall rate less infiltration).
        self._runoff = runoff
        # Prefactor on A**c_sp to give discharge.
        self._k_Q = k_Q
        # Power on drainage area to give discharge.
        self._c_sp = c_sp
        self._g = g  # gravidade
        # Limiar da area de drenagem para ser considerado grao tipo 7
        self._drain_area_threshold = drain_area_threshold
        self._fluid_density = fluid_density
        # profundidade:
        # node_Q = self._k_Q * self._runoff * node_A ** self._c_sp
        # pgd da formula do shear stress

    def discrete_shear_stress(self, ss):  # divisao do shear stress para escala de tamnhos da escala de Roux (1998)

        if ss <= 0:
            return 0
        if ss <= 1:
            return 1
        if ss <= 1.2710:
            return 1.2710
        if ss <= 1.7423:
            return 1.7423
        if ss <= 2.1964:
            return 2.1964
        if ss <= 2.8541:
            return 2.8541
        if ss <= 6.6074:
            return 6.6074
        if ss <= 14.503:
            return 14.503
        if ss <= 29.138:
            return 29.138
        if ss <= 58.275:
            return 58.275

        return 60

    def get_size_grain(self, shear_stress):
        if shear_stress == 0:
            return 0.0031
        if shear_stress == 1:
            return 0.004
        if shear_stress == 1.2710:
            return 0.0063
        if shear_stress == 1.7423:
            return 0.0125
        if shear_stress == 2.1964:
            return 0.0250
        if shear_stress == 2.8541:
            return 0.0500
        if shear_stress == 6.6074:
            return 0.1
        if shear_stress == 14.503:
            return 0.2
        if shear_stress == 29.138:
            return 0.4
        if shear_stress == 58.275:
            return 0.8

        return 100

    def classify_grain(self, size):
        if size <= 0.004:
            return 1
        if size <= 0.062:
            return 2
        if size <= 0.25:
            return 3
        if size <= 0.5:
            return 4
        if size <= 1:
            return 5
        if size <= 4:
            return 6

        return 7

    def add_grid_to_dem(self, mg, name, value):
        if name in mg.at_node.keys():
            mg.delete_field("node", name)

        mg.add_field(name, value, at="node", copy=True, clobber=False)

    def calc_shear_stress(self, slope, profundidade):
        # pgd da formula do shear stress
        return self._fluid_density * self._g * profundidade * slope

        # Area com baixo acumulo será arbitrariamente um grao tipo 7

    def update_drainage_area(self, da, slope):
        _da = copy.copy(da)
        sc = self.calc_critical_slope(da)
        _da[sc < slope] = 9999999
        return _da

    #     def update_drainage_area(self, da, treshold):
    #         _da = copy.copy(da)
    #         _da[_da < treshold] = 9999999
    #         return _da

    def calc_critical_slope(self, da):
        b = 0.000008
        k = 0.001
        p = 0.3
        m = 0.5
        n = 1

        Sc = ((b / k) * da ** (p - m)) ** 0.5
        Sc[Sc == np.inf] = 0

        return Sc

    def calc_profundidade(self, A, c, f, k):
        return c * (k * A) ** f

    def run_one_step(self):
        dem = self._dem
        node_z = dem.at_node["topographic__elevation"]  # elevaçao
        node_S = dem.at_node["topographic__steepest_slope"]  # slope, vem do flow accumulator(?)

        node_A = dem.at_node["drainage_area"]
        node_A = self.update_drainage_area(dem.at_node["drainage_area"], node_S)

        # profundidade
        node_Q = self._k_Q * node_A  # Calcula profundidade, parte que tem a ver com PAR_1, PAR_2

        profundidade = self._runoff * node_Q ** self._c_sp
        counter = 0

        while 1:

            # funçao clip atribui o valor zero a valores negativos que venham a ser encontrados
            # depressoes podem possuir valores negativos (lago, fosso, buraco negro)
            downward_slopes = node_S.clip(0.0)
            slopes_tothe07 = downward_slopes ** 0.5  # nao sei pq
            shear_stress = self.calc_shear_stress(slopes_tothe07, profundidade)

            # classifica os resultados anteriores com o intervalo definido
            shear_stress_discrete = list(map(self.discrete_shear_stress, shear_stress))

            grains_size = list(map(self.get_size_grain, shear_stress_discrete))
            grain_type = list(map(self.classify_grain, grains_size))

            # adiciona grid ao DEM
            self.add_grid_to_dem(dem, 'shear_stress', shear_stress)
            self.add_grid_to_dem(dem, 'shear_stress_discrete', shear_stress_discrete)
            self.add_grid_to_dem(dem, 'grain_type', grain_type)

            break_flag = True
            if break_flag:
                break