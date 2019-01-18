

set -ex



type -P conda-build
conda-build -h
type -P conda-convert
conda-convert -h
type -P conda-develop
type -P conda-debug
conda-develop -h
type -P conda-index
conda-index -h
type -P conda-inspect
conda-inspect linkages -h \| grep "--name ENVIRONMENT"
conda-inspect objects -h \| grep "--name ENVIRONMENT"
conda-inspect -h
type -P conda-metapackage
conda-metapackage -h
type -P conda-render
conda-render -h
type -P conda-skeleton
conda-skeleton -h
python test_bdist_conda_setup.py bdist_conda --help
exit 0
