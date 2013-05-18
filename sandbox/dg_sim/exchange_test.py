import pytest
import numpy as np
import dolfin as df
from exchange import ExchangeDG as Exchange
#from finmag.energies.exchange import  Exchange


@pytest.fixture(scope = "module")
def fixt():
    """
    Create an Exchange object that will be re-used during testing.

    """
    mesh = df.UnitCubeMesh(10, 10, 10)
    S3 = df.VectorFunctionSpace(mesh, "DG", 0)
    Ms = 1
    A = 1
    m = df.Function(S3)
    exch = Exchange(A)
    exch.setup(S3, m, Ms)
    return {"exch": exch, "m": m, "A": A, "S3": S3, "Ms": Ms}


def test_interaction_accepts_name():
    """
    Check that the interaction accepts a 'name' argument and has a 'name' attribute.
    """
    exch = Exchange(13e-12, name='MyExchange')
    assert hasattr(exch, 'name')


def test_there_should_be_no_exchange_for_uniform_m(fixt):
    """
    Check that exchange field and energy are 0 for uniform magnetisation.

    """
    TOLERANCE = 1e-6
    fixt["m"].assign(df.Constant((1, 0, 0)))

    H = fixt["exch"].compute_field()
    print "Asserted zero exchange field for uniform m = (1, 0, 0), got H =\n{}.".format(H.reshape((3, -1)))
    assert np.max(np.abs(H)) < TOLERANCE

   



if __name__ == "__main__":
    mesh = df.BoxMesh(0,0,0,2*np.pi,1,1,10, 1, 1)
     
    S = df.FunctionSpace(mesh, "DG", 0)
    S3 = df.VectorFunctionSpace(mesh, "DG", 0)

    expr = df.Expression(("0", "cos(x[0])", "sin(x[0])"))
    
    m = df.interpolate(expr, S3)
    
    exch = Exchange(1)
    exch.setup(S3, m, 1)
    print exch.compute_field()
    
    field=df.Function(S3)
    field.vector().set_local(exch.compute_field())
    
    df.plot(m)
    df.plot(field)
    df.interactive()
