import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

np.random.seed(42)


@pytest.fixture
def param_bounds():
    from ai_optimizer import PARAM_BOUNDS
    return PARAM_BOUNDS.copy()


@pytest.fixture
def param_names():
    from ai_optimizer import PARAM_NAMES
    return list(PARAM_NAMES)


@pytest.fixture
def param_default():
    from ai_optimizer import PARAM_DEFAULT
    return PARAM_DEFAULT.flatten().copy()


@pytest.fixture
def sample_params(param_bounds):
    return np.array([np.random.uniform(lo, hi) for lo, hi in param_bounds])


@pytest.fixture
def tmp_plot_dir(tmp_path):
    d = tmp_path / "plots"
    d.mkdir()
    return d
