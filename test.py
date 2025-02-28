"""
Usage: python test.py
1. Installs part of dependencies (make sure `which pip` points to correct location)
2. Installs current version of einops in editable mode
3. Runs the tests
"""

import os
import sys
from subprocess import Popen, PIPE
from pathlib import Path

__author__ = 'Alex Rogozhnikov'


def run(cmd, **env):
    # keeps printing output when testing
    cmd = cmd.split(' ') if isinstance(cmd, str) else cmd
    p = Popen(cmd, cwd=str(Path(__file__).parent), env={**os.environ, **env})
    p.communicate()
    return p.returncode


# check we have nvidia-smi
import shutil
have_cuda = False
if shutil.which('nvidia-smi') is not None:
    output, _ = Popen('nvidia-smi'.split(' '), stdout=PIPE).communicate()
    if b'failed because' not in output:
        have_cuda = True

# install cupy. It can't be installed without cuda available (with compilers).
skip_cupy = not have_cuda
if not skip_cupy:
    return_code = run('pip install cupy --pre --progress-bar off')
    assert return_code == 0

# install dependencies
dependencies = [
    'numpy',
    'torch',
    'tensorflow',
    'chainer',
    'jax',
    'jaxlib',
    'flax',
    'nbformat',
    'nbconvert',
    'jupyter',
    'parameterized',
    'pillow',
    'pytest'
]

assert 0 == run('pip install {} --progress-bar off'.format(' '.join(dependencies)))
run('pip install paddlepaddle==0.0.0 -f https://www.paddlepaddle.org.cn/whl/linux/cpu-mkl/develop.html --no-cache-dir --user')
# oneflow provides wheels for linux, but not mac, so it is tested only on linux
skip_oneflow = 'linux' not in sys.platform
skip_oneflow = True

if not skip_oneflow:
    # oneflow installation: https://github.com/Oneflow-Inc/oneflow#install-with-pip-package
    assert 0 == run('pip install -f https://release.oneflow.info oneflow==0.7.0+cpu --user')

# install einops
assert 0 == run('pip install -e .')


return_code = run(
    'python -m pytest tests',
    EINOPS_SKIP_CUPY='1' if skip_cupy else '0',
    EINOPS_SKIP_ONEFLOW='1' if skip_oneflow else '0',
)
assert return_code == 0

if __name__ == '__main__':
    # minor convenience for lazy me to start debugging in pycharm
    pass