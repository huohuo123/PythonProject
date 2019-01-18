

set -ex



conda inspect linkages -p $PREFIX lxml
conda inspect objects -p $PREFIX lxml
exit 0
