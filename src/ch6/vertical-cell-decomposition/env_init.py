#!/usr/bin/python3
import sys
sys.path.append("./support")
sys.path.append("./DCEL")
from DCEL import *
from BoundaryVertex import BoundaryVertex
from render_support import GeometryFxns as gfn
from render_support import MathFxns as mfn
from render_support import TransformFxns as tfn
from render_support import PygameArtFxns as pafn
from cell_decomp_support import VerticalCellDecomposition as vcd


import collections
