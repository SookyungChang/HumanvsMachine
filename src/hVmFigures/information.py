from hVmFigures.plotting import FoM

class INFO:
    def __init__(self, ind_chains, joint_chains):
        self.ind_chains = ind_chains
        self.joint_chains = joint_chains

    def relative_form(self, target_name, reference_name = 'lyanna'):
        reference = self.ind_chains[reference_name]
        try:
            return FoM(self.ind_chains[target_name])/FoM(reference)
        except KeyError:
            return FoM(self.joint_chains[target_name])/FoM(reference)


    def RCI(self, St, Sr):
        St_Sr = St + '_' + Sr
        try:
            return (FoM(self.joint_chains[St_Sr]) - FoM(self.ind_chains[Sr]))/FoM(self.joint_chains[St_Sr])
        except KeyError:
            St_Sr = Sr + '_' + St
            return (FoM(self.joint_chains[St_Sr]) - FoM(self.ind_chains[Sr]))/FoM(self.joint_chains[St_Sr])
             