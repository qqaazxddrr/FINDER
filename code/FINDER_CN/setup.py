
from distutils.core import setup
from distutils.extension import Extension
# from Cython.Build import cythonize
from Cython.Distutils import build_ext

setup(
    cmdclass = {'build_ext':build_ext},

    #################for ubuntu compile
    ext_modules = [
                    Extension('PrepareBatchGraph', sources = ['PrepareBatchGraph.pyx','src/lib/PrepareBatchGraph.cpp','src/lib/igraph.cpp','src/lib/graph_struct.cpp',  'src/lib/disjoint_set.cpp'],language='c++',extra_compile_args=['-std=c++11', '-stdlib=libc++']),    # *
                    Extension('igraph', sources=['igraph.pyx', 'src/lib/igraph.cpp'], language='c++',extra_compile_args=['-std=c++11', '-stdlib=libc++']),
                    Extension('inf_env', sources=['inf_env.pyx', 'src/lib/inf_env.cpp', 'src/lib/igraph.cpp'], language='c++',extra_compile_args=['-std=c++11', '-stdlib=libc++']),
                    Extension('utils', sources=['utils.pyx', 'src/lib/utils.cpp', 'src/lib/igraph.cpp', 'src/lib/graph_utils.cpp', 'src/lib/disjoint_set.cpp', 'src/lib/decrease_strategy.cpp'], language='c++',extra_compile_args=['-std=c++11', '-stdlib=libc++']),       # *
                    Extension('nstep_replay_mem', sources=['nstep_replay_mem.pyx', 'src/lib/nstep_replay_mem.cpp', 'src/lib/igraph.cpp', 'src/lib/inf_env.cpp', 'src/lib/disjoint_set.cpp'], language='c++',extra_compile_args=['-std=c++11', '-stdlib=libc++']),           # *
                    Extension('nstep_replay_mem_prioritized',sources=['nstep_replay_mem_prioritized.pyx', 'src/lib/nstep_replay_mem_prioritized.cpp','src/lib/igraph.cpp', 'src/lib/inf_env.cpp', 'src/lib/disjoint_set.cpp'], language='c++',extra_compile_args=['-std=c++11', '-stdlib=libc++']),     # *
                    Extension('graph_struct', sources=['graph_struct.pyx', 'src/lib/graph_struct.cpp'], language='c++',extra_compile_args=['-std=c++11', '-stdlib=libc++']),            # *
                    Extension('FINDER', sources = ['FINDER.pyx'])
                   ])