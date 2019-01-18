

set -ex



iconv --help
conda inspect linkages -p $PREFIX libiconv
conda inspect objects -p $PREFIX libiconv
exit 0
