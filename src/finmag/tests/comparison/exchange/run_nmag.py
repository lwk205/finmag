# One dimensional magnetic system studied using nsim
import math
import numpy as np
import nmag
from nmag import SI
import nmeshlib.unidmesher as unidmesher

# Details about the layers and the mesh and the material
length = 20.0             # in nanometers
mesh_unit = SI(1e-9, "m")  # mesh unit (1 nm)
layers = [(0.0, length)]  # the mesh
discretization = 2.0      # discretization

# Initial magnetization
xfactor = float(SI("m") / (length * mesh_unit))


def m0(r):
    x = max(0.0, min(1.0, r[0] * xfactor))
    mx = (2.0 * x - 1.0) * 2.0 / 3.0
    mz = math.sin(2 * math.pi * x) / 2
    my = (1.0 - mx * mx - mz * mz) ** 0.5
    return [mx, my, mz]

# Create the material
mat_Py = nmag.MagMaterial(name="Py",
                          Ms=SI(0.86e6, "A/m"),
                          exchange_coupling=SI(13.0e-12, "J/m"),
                          llg_gamma_G=SI(0.2211e6, "m/A s"),
                          llg_damping=SI(0.2),
                          llg_normalisationfactor=SI(0.001e12, "1/s"))

# Create the simulation object
sim = nmag.Simulation("1d", do_demag=False)

# Creates the mesh from the layer structure
mesh_file_name = '1d.nmesh'
mesh_lists = unidmesher.mesh_1d(layers, discretization)
unidmesher.write_mesh(mesh_lists, out=mesh_file_name)

# Load the mesh
sim.load_mesh(mesh_file_name, [("Py", mat_Py)], unit_length=mesh_unit)

sim.set_m(m0)        # Set the initial magnetisation

# Save the exchange field and the magnetisation once at the beginning
# of the simulation for comparison with finmag
np.savetxt("H_exc_nmag.txt", sim.get_subfield("H_exch_Py"))
np.savetxt("m0_nmag.txt", sim.get_subfield("m_Py"))
