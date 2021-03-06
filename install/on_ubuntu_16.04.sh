# Need to run this with bash, not sh.

set -o errexit

if [ "$1" == "--help" -o "$1" == "-h" ]
then
    echo "
This script will install required libraries to run finmag.

Packages to build the documentation and additional suggested
packages can be installed by appending an --all argument when
calling this script."
    exit
fi

required="fenics libboost-python-dev libboost-thread-dev libsundials-serial-dev
    libboost-test-dev python-matplotlib python-visual python-scipy python-pip
    python-setuptools python-progressbar paraview-python cython python-zmq python-tornado git"

#Python-zmq and python-tornado are requirements for the ipython notebook.

building_doc="texlive-latex-extra texlive-latex-recommended texlive-fonts-recommended python-pygments"

suggested="mercurial grace gnuplot gmsh"

packages="$required"
if [ "$1" == "--all" ]
then
    packages="$packages $building_doc $suggested"
fi

sudo add-apt-repository ppa:fenics-packages/fenics
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install $packages
sudo python -m pip install -U sphinx pytest aeon sh diff-match-patch future
# [Observation: We need IPython installed to be able to import finmag. So
# we need to make sure to also install ipython.]

# the debian 1404 package for ipython is 1.2, i.e. too old, so install
# via pip:
sudo python -m pip install -U ipython pyzmq

# nbconvert for IPython 3.x seems to need mistune (caused fail on
# jenkins for target 'doc-html' when this was missing).
sudo python -m pip install mistune


# Eigenmodes need petsc4py. SLEPc and PETSc should also be installed for this.
sudo apt-get install libpetsc3.6 libpetsc3.6.2-dev\
 libslepc3.6.1 libslepc3.6.1-dev

# the following seems to have worked on osiris with ubunt14.04 but not on
# Hans virtual machine with Ubuntu 14.04.
# export PETSC_DIR=/usr/lib/petsc
# export SLEPC_DIR=/usr/lib/slepc
# PETSC_DIR=/usr/lib/petsc SLEPC_DIR=/usr/lib/slepc sudo pip install https://bitbucket.org/slepc/slepc4py/downloads/slepc4py-3.4.tar.gz

# The following works on virtual micromagnetics and Mark's machine.
sudo PETSC_DIR=/usr/lib/petsc SLEPC_DIR=/usr/lib/slepc python -m pip install\
 https://bitbucket.org/slepc/slepc4py/downloads/slepc4py-3.6.0.tar.gz\
 --allow-all-external

# fenicstools: this relies on pyvtk and h5py. Be sure to install the release of
# fenicstools that corresponds with the latest stable dolfin release, otherwise
# some functionality may be missing.
sudo apt-get install python-pyvtk python-h5py
sudo python -m pip install --upgrade\
 https://github.com/mikaem/fenicstools/archive/v1.4.0.tar.gz

sudo python -m pip install --upgrade git+https://github.com/fangohr/dolfinh5tools.git

# install netifaces for requesting binary license
sudo pip install netifaces

# Install a newer version of Netgen than that provided by Ubuntu.
# This is necessary to stop it from segfaulting all of the time!
sudo bash netgen-5.3.sh
