import dolfin as df
import numpy as np
import finmag.sim.helpers as h

from scipy.integrate import ode
from finmag.sim.llg import LLG

fh = open("data_M_dolfin.txt", "w")

mesh = df.Mesh("bar.xml")
mesh.coordinates()[:] = 1e-9 * mesh.coordinates() # from (implied) nm to m
llg = LLG(mesh)

llg.alpha = 0.5
llg.MS = 0.86e6 # A/m
llg.C = 1.3e-11 # J/m
llg.H_app = (0.43e6, 0, 0) # A/m
llg.initial_M_expr(("2*x[0]/L - 1","2*x[1]/W - 1","1"), L=3e-8, H=1e-8, W=1e-8)
llg.M = h.for_dolfin(h.normalise(h.vectors(llg.M), llg.MS))
llg.setup(exchange_flag=True)

t0 = 0; dt = 1e-12; tmax = 1e-9 # s
llg_wrap = lambda t, y: llg.solve_for(y, t)
r = ode(llg_wrap).set_integrator("vode", method="bdf", with_jacobian=False)
r.set_initial_value(llg.M, t0)
while r.successful() and r.t <= tmax:
    print r.t
    df.plot(llg._M)
    Mx, My, Mz = llg.average_M()
    fh.write(str(r.t) + " " + str(Mx) + " " + str(My) + " " + str(Mz) + "\n")
    r.integrate(r.t+dt)
fh.close()
df.interactive()
