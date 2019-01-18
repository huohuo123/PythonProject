

set -ex



export MPLBACKEND=Agg
pytest --pyargs skimage
exit 0
