"""
Miscellaneous utility functions.
"""

__author__ = "Steven Kearnes"
__copyright__ = "Copyright 2014, Stanford University"
__license__ = "BSD 3-clause"

import cPickle
import gzip
import numpy as np
import os
import pandas as pd

from rdkit import Chem
from rdkit.Chem.Scaffolds import MurckoScaffold

def pad_array(x, shape, fill=0, both=False):
  """
  Pad an array with a fill value.

  Parameters
  ----------
  x : ndarray
      Matrix.
  shape : tuple or int
      Desired shape. If int, all dimensions are padded to that size.
  fill : object, optional (default 0)
      Fill value.
  both : bool, optional (default False)
      If True, split the padding on both sides of each axis. If False,
      padding is applied to the end of each axis.
  """
  x = np.asarray(x)
  if not isinstance(shape, tuple):
    shape = tuple(shape for _ in xrange(x.ndim))
  pad = []
  for i in xrange(x.ndim):
    diff = shape[i] - x.shape[i]
    assert diff >= 0
    if both:
      a, b = divmod(diff, 2)
      b += a
      pad.append((a, b))
    else:
      pad.append((0, diff))
  pad = tuple(pad)
  x = np.pad(x, pad, mode='constant', constant_values=fill)
  return x

class ScaffoldGenerator(object):
  """
  Generate molecular scaffolds.

  Parameters
  ----------
  include_chirality : : bool, optional (default False)
      Include chirality in scaffolds.
  """
  def __init__(self, include_chirality=False):
    self.include_chirality = include_chirality

  def get_scaffold(self, mol):
    """
    Get Murcko scaffolds for molecules.

    Murcko scaffolds are described in DOI: 10.1021/jm9602928. They are
    essentially that part of the molecule consisting of rings and the
    linker atoms between them.

    Parameters
    ----------
    mols : array_like
        Molecules.
    """
    return MurckoScaffold.MurckoScaffoldSmiles(
        mol=mol, includeChirality=self.include_chirality)
