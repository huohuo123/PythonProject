

set -ex



conda inspect linkages -p $PREFIX krb5
conda inspect objects -p $PREFIX krb5
exit 0
