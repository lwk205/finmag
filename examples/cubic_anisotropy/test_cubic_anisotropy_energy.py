import dolfin as df
import numpy as np
from finmag.energies import CubicAnisotropy

Ms = 876626  # A/m

K1 = -8608726
K2 = -13744132
K3 =  1100269
u1 = (0, -0.7071, 0.7071)
u2 = (0,  0.7071, 0.7071)
u3 = (-1, 0, 0)  # perpendicular to u1 and u2

def compute_cubic_energy():
    m=(0,0,1)
    u1m=np.dot(u1,m)
    u2m=np.dot(u2,m)
    u3m=np.dot(u3,m)
    energy = K1*(u1m**2*u2m**2+u1m**2*u3m**2+u2m**2*u3m**2)
    energy += K2*(u1m**2*u2m**2*u3m**2)
    energy += K3*(u1m**4*u2m**4+u1m**4*u3m**4+u2m**4*u3m**4)
    return energy

def test_cubic_anisotropy_energy():
    mesh = df.BoxMesh(0, 0, 0, 1, 1, 40, 1, 1, 40)
    S3 = df.VectorFunctionSpace(mesh, "Lagrange", 1)
    S1 = df.FunctionSpace(mesh, "Lagrange", 1)

    m = df.Function(S3)
    m.assign(df.Constant((0, 0, 1)))
    
    Ms_cg = df.Function(S1)
    Ms_cg.assign(df.Constant(Ms))

    ca = CubicAnisotropy(u1, u2, K1, K2, K3)
    ca.setup(S3, m, Ms_cg, unit_length=1e-9)

    energy = ca.compute_energy()
    #energy_expected = 8.3e-20  # oommf cubicEight_100pc.mif -> ErFe2.odt
    energy_expected = compute_cubic_energy()*40e-27
    print energy, energy_expected

    rel_diff = abs(energy - energy_expected) / abs(energy_expected)
    assert rel_diff < 1e-10