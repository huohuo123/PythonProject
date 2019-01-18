# (c) 2012-2016 Anaconda, Inc. / https://anaconda.com
# All Rights Reserved
#
# conda is distributed under the terms of the BSD 3-clause license.
# Consult LICENSE.txt or http://opensource.org/licenses/BSD-3-Clause.
'''
We use the following conventions in this module:

    dist:        canonical package name, e.g. 'numpy-1.6.2-py26_0'

    ROOT_PREFIX: the prefix to the root environment, e.g. /opt/anaconda

    PKGS_DIR:    the "package cache directory", e.g. '/opt/anaconda/pkgs'
                 this is always equal to ROOT_PREFIX/pkgs

    prefix:      the prefix of a particular environment, which may also
                 be the root environment

Also, this module is directly invoked by the (self extracting) tarball
installer to create the initial environment, therefore it needs to be
standalone, i.e. not import any other parts of `conda` (only depend on
the standard library).
'''
import os
import re
import sys
import json
import shutil
import stat
from os.path import abspath, dirname, exists, isdir, isfile, islink, join
from optparse import OptionParser


on_win = bool(sys.platform == 'win32')
try:
    FORCE = bool(int(os.getenv('FORCE', 0)))
except ValueError:
    FORCE = False

LINK_HARD = 1
LINK_SOFT = 2  # never used during the install process
LINK_COPY = 3
link_name_map = {
    LINK_HARD: 'hard-link',
    LINK_SOFT: 'soft-link',
    LINK_COPY: 'copy',
}
SPECIAL_ASCII = '$!&\%^|{}[]<>~`"\':;?@*#'

# these may be changed in main()
ROOT_PREFIX = sys.prefix
PKGS_DIR = join(ROOT_PREFIX, 'pkgs')
SKIP_SCRIPTS = False
IDISTS = {
  "_ipyw_jlab_nb_ext_conf-0.1.0-py37_0": {
    "md5": "a228105f769a28123941a782e05e9b97",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/_ipyw_jlab_nb_ext_conf-0.1.0-py37_0.tar.bz2"
  },
  "alabaster-0.7.12-py37_0": {
    "md5": "5f97e22330edf852b628c4fefc03f29e",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/alabaster-0.7.12-py37_0.tar.bz2"
  },
  "anaconda-2018.12-py37_0": {
    "md5": "b7b4135ed203956ae7985b997489dd7f",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/anaconda-2018.12-py37_0.tar.bz2"
  },
  "anaconda-client-1.7.2-py37_0": {
    "md5": "e9cd7886c95d9948b44f1b9b95311b01",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/anaconda-client-1.7.2-py37_0.tar.bz2"
  },
  "anaconda-navigator-1.9.6-py37_0": {
    "md5": "2d1187e837b14ea142cf0e4980dd00a3",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/anaconda-navigator-1.9.6-py37_0.tar.bz2"
  },
  "anaconda-project-0.8.2-py37_0": {
    "md5": "2482fe34d65abb914622f3117345001b",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/anaconda-project-0.8.2-py37_0.tar.bz2"
  },
  "appnope-0.1.0-py37_0": {
    "md5": "fe4765efddefcddec63efa641a5e1287",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/appnope-0.1.0-py37_0.tar.bz2"
  },
  "appscript-1.0.1-py37h1de35cc_1": {
    "md5": "0a4dff217cbd732ff3fcb651f1faf931",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/appscript-1.0.1-py37h1de35cc_1.tar.bz2"
  },
  "asn1crypto-0.24.0-py37_0": {
    "md5": "ff3b91bb94d406dc498f99fd8f1d24a8",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/asn1crypto-0.24.0-py37_0.tar.bz2"
  },
  "astroid-2.1.0-py37_0": {
    "md5": "4f4e9abcaaedb414ea1c7f33c2bb18b5",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/astroid-2.1.0-py37_0.tar.bz2"
  },
  "astropy-3.1-py37h1de35cc_0": {
    "md5": "bcef24c36c357036ebf143be22dc3cbf",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/astropy-3.1-py37h1de35cc_0.tar.bz2"
  },
  "atomicwrites-1.2.1-py37_0": {
    "md5": "39098be01e0c10b823be016bafafa817",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/atomicwrites-1.2.1-py37_0.tar.bz2"
  },
  "attrs-18.2.0-py37h28b3542_0": {
    "md5": "3915265e2a42eb0ed8f0b310c7510e89",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/attrs-18.2.0-py37h28b3542_0.tar.bz2"
  },
  "babel-2.6.0-py37_0": {
    "md5": "111a663527c73e9c4354a16b6232c5a9",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/babel-2.6.0-py37_0.tar.bz2"
  },
  "backcall-0.1.0-py37_0": {
    "md5": "b18ad93687ee10cfb727f82b11024580",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/backcall-0.1.0-py37_0.tar.bz2"
  },
  "backports-1.0-py37_1": {
    "md5": "30843079c82e830ddb93877954ae0d8c",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/backports-1.0-py37_1.tar.bz2"
  },
  "backports.os-0.1.1-py37_0": {
    "md5": "0799936861aa6e295fb11e456bbf36bd",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/backports.os-0.1.1-py37_0.tar.bz2"
  },
  "backports.shutil_get_terminal_size-1.0.0-py37_2": {
    "md5": "92e47d6e5fefa19d89a52b0b90260e56",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/backports.shutil_get_terminal_size-1.0.0-py37_2.tar.bz2"
  },
  "beautifulsoup4-4.6.3-py37_0": {
    "md5": "eb1eaa898250733d40520def4f78a056",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/beautifulsoup4-4.6.3-py37_0.tar.bz2"
  },
  "bitarray-0.8.3-py37h1de35cc_0": {
    "md5": "58c43a5453aa17bba016928eb52f6288",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/bitarray-0.8.3-py37h1de35cc_0.tar.bz2"
  },
  "bkcharts-0.2-py37_0": {
    "md5": "014462afee1bbd7a067aa648516c9287",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/bkcharts-0.2-py37_0.tar.bz2"
  },
  "blas-1.0-mkl": {
    "md5": "e2f3248e2a5009a02f7b8e54f83314ef",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/blas-1.0-mkl.tar.bz2"
  },
  "blaze-0.11.3-py37_0": {
    "md5": "3767073255c608c46c10761a283f535d",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/blaze-0.11.3-py37_0.tar.bz2"
  },
  "bleach-3.0.2-py37_0": {
    "md5": "a830f2d1dcd2b42af3ef3badea898584",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/bleach-3.0.2-py37_0.tar.bz2"
  },
  "blosc-1.14.4-hd9629dc_0": {
    "md5": "5369317eeea4c5d23ddd7d9d49d6dc59",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/blosc-1.14.4-hd9629dc_0.tar.bz2"
  },
  "bokeh-1.0.2-py37_0": {
    "md5": "b61a334aa6d43971315a7099ef47a634",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/bokeh-1.0.2-py37_0.tar.bz2"
  },
  "boto-2.49.0-py37_0": {
    "md5": "7e98e2e6810245395f943e9523c20d73",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/boto-2.49.0-py37_0.tar.bz2"
  },
  "bottleneck-1.2.1-py37h1d22016_1": {
    "md5": "9697f3415f0ea69a36be9c9a7240d1ea",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/bottleneck-1.2.1-py37h1d22016_1.tar.bz2"
  },
  "bzip2-1.0.6-h1de35cc_5": {
    "md5": "f6b2bc7a8c60d6723ddf7a5df56b289d",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/bzip2-1.0.6-h1de35cc_5.tar.bz2"
  },
  "ca-certificates-2018.03.07-0": {
    "md5": "8a61ffe6635a912082978bb8127b5f4b",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/ca-certificates-2018.03.07-0.tar.bz2"
  },
  "certifi-2018.11.29-py37_0": {
    "md5": "34934feeb0c3eaf53baf15cecf46fbf4",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/certifi-2018.11.29-py37_0.tar.bz2"
  },
  "cffi-1.11.5-py37h6174b99_1": {
    "md5": "cea35925b3d5c5e6a5d0433fc4ed28c7",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/cffi-1.11.5-py37h6174b99_1.tar.bz2"
  },
  "chardet-3.0.4-py37_1": {
    "md5": "5ea5d76c006b51927e757c692239c4fd",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/chardet-3.0.4-py37_1.tar.bz2"
  },
  "click-7.0-py37_0": {
    "md5": "bdf313a5ed0f42a2025ad54c9ee21185",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/click-7.0-py37_0.tar.bz2"
  },
  "cloudpickle-0.6.1-py37_0": {
    "md5": "616ff88fa0aa8c61783d4522fcb69edc",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/cloudpickle-0.6.1-py37_0.tar.bz2"
  },
  "clyent-1.2.2-py37_1": {
    "md5": "ed39128c6dec41a507d82c61bd26591c",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/clyent-1.2.2-py37_1.tar.bz2"
  },
  "colorama-0.4.1-py37_0": {
    "md5": "63af1d848e225258efd52c384a534fa5",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/colorama-0.4.1-py37_0.tar.bz2"
  },
  "conda-4.5.12-py37_0": {
    "md5": "c129bb91bd1f4e6355d488382ca84e71",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/conda-4.5.12-py37_0.tar.bz2"
  },
  "conda-build-3.17.6-py37_0": {
    "md5": "e8c44f2abe824396b21e119b091ce125",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/conda-build-3.17.6-py37_0.tar.bz2"
  },
  "conda-env-2.6.0-1": {
    "md5": "a29a55f26a84c182a3e9625ac2f6cef0",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/conda-env-2.6.0-1.tar.bz2"
  },
  "conda-verify-3.1.1-py37_0": {
    "md5": "f2ba5d6ae4f00623b31afd790ed57e14",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/conda-verify-3.1.1-py37_0.tar.bz2"
  },
  "contextlib2-0.5.5-py37_0": {
    "md5": "eb6a7bb416b5f08007d02daa26eb5bbc",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/contextlib2-0.5.5-py37_0.tar.bz2"
  },
  "cryptography-2.4.2-py37ha12b0ac_0": {
    "md5": "0bb00708f93976d69878d2f75d31234c",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/cryptography-2.4.2-py37ha12b0ac_0.tar.bz2"
  },
  "curl-7.63.0-ha441bb4_1000": {
    "md5": "35f85cb673dcc94e236020164d0b2bb6",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/curl-7.63.0-ha441bb4_1000.tar.bz2"
  },
  "cycler-0.10.0-py37_0": {
    "md5": "d49cf75c0f16d48fc655c179f08b59e2",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/cycler-0.10.0-py37_0.tar.bz2"
  },
  "cython-0.29.2-py37h0a44026_0": {
    "md5": "e45a299e100d01721e2997686e46ccac",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/cython-0.29.2-py37h0a44026_0.tar.bz2"
  },
  "cytoolz-0.9.0.1-py37h1de35cc_1": {
    "md5": "7d7043e75206bd3682d6d8e5be589f09",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/cytoolz-0.9.0.1-py37h1de35cc_1.tar.bz2"
  },
  "dask-1.0.0-py37_0": {
    "md5": "0124fb773409852d3cca2f3d6249f1a5",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/dask-1.0.0-py37_0.tar.bz2"
  },
  "dask-core-1.0.0-py37_0": {
    "md5": "db981f4e9baf8091dfe44d2986d332cb",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/dask-core-1.0.0-py37_0.tar.bz2"
  },
  "datashape-0.5.4-py37_1": {
    "md5": "efcbd1b5cb186ed87389b272e1e1aff9",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/datashape-0.5.4-py37_1.tar.bz2"
  },
  "dbus-1.13.2-h760590f_1": {
    "md5": "f31fd7b04ad946b9bd59973e3f12c7a1",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/dbus-1.13.2-h760590f_1.tar.bz2"
  },
  "decorator-4.3.0-py37_0": {
    "md5": "460cb881615a89125668d4739baac8c7",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/decorator-4.3.0-py37_0.tar.bz2"
  },
  "defusedxml-0.5.0-py37_1": {
    "md5": "8c1b8e3e98f828144eb0089e7383abbe",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/defusedxml-0.5.0-py37_1.tar.bz2"
  },
  "distributed-1.25.1-py37_0": {
    "md5": "2ccf8768a9ec106bbdc319783a5b820a",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/distributed-1.25.1-py37_0.tar.bz2"
  },
  "docutils-0.14-py37_0": {
    "md5": "fb0a12e750756972f37deaca974d2334",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/docutils-0.14-py37_0.tar.bz2"
  },
  "entrypoints-0.2.3-py37_2": {
    "md5": "abf3bc468253d2a81c80cbb2abb39c00",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/entrypoints-0.2.3-py37_2.tar.bz2"
  },
  "et_xmlfile-1.0.1-py37_0": {
    "md5": "615b129da03b8e9a78285763c85eeb32",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/et_xmlfile-1.0.1-py37_0.tar.bz2"
  },
  "expat-2.2.6-h0a44026_0": {
    "md5": "d27f3224144d6a0dc28ec1ca9c9a8562",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/expat-2.2.6-h0a44026_0.tar.bz2"
  },
  "fastcache-1.0.2-py37h1de35cc_2": {
    "md5": "38bb1f935c90818cd2e4ec1deb0fefdc",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/fastcache-1.0.2-py37h1de35cc_2.tar.bz2"
  },
  "filelock-3.0.10-py37_0": {
    "md5": "a735e2e42ecfe58458fc471cd10f6750",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/filelock-3.0.10-py37_0.tar.bz2"
  },
  "flask-1.0.2-py37_1": {
    "md5": "4a2734ec3733bf09cc05763615157a92",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/flask-1.0.2-py37_1.tar.bz2"
  },
  "flask-cors-3.0.7-py37_0": {
    "md5": "bef263f19868490209d0036c7ed901b5",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/flask-cors-3.0.7-py37_0.tar.bz2"
  },
  "freetype-2.9.1-hb4e5f40_0": {
    "md5": "621858a6df6e0b41955d13fb9d4af5f9",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/freetype-2.9.1-hb4e5f40_0.tar.bz2"
  },
  "future-0.17.1-py37_0": {
    "md5": "d169502dfaa1a35a205bbee42862b458",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/future-0.17.1-py37_0.tar.bz2"
  },
  "get_terminal_size-1.0.0-h7520d66_0": {
    "md5": "77ac7a22b3f4da13f9e52a2efd997c84",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/get_terminal_size-1.0.0-h7520d66_0.tar.bz2"
  },
  "gettext-0.19.8.1-h15daf44_3": {
    "md5": "7681fa7f32f81fc320919d828cd8c949",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/gettext-0.19.8.1-h15daf44_3.tar.bz2"
  },
  "gevent-1.3.7-py37h1de35cc_1": {
    "md5": "0bf550bc5af228cd7c186e986cd64dcb",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/gevent-1.3.7-py37h1de35cc_1.tar.bz2"
  },
  "glib-2.56.2-hd9629dc_0": {
    "md5": "d313d0857208f5ad3bcf041aeca8f148",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/glib-2.56.2-hd9629dc_0.tar.bz2"
  },
  "glob2-0.6-py37_1": {
    "md5": "e844d69ac8180ba84d85d7949c3cd8eb",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/glob2-0.6-py37_1.tar.bz2"
  },
  "gmp-6.1.2-hb37e062_1": {
    "md5": "ab1fc93279250a837aad914f547d9d6c",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/gmp-6.1.2-hb37e062_1.tar.bz2"
  },
  "gmpy2-2.0.8-py37h6ef4df4_2": {
    "md5": "49b2e8bee7735b66654d9985e2c61956",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/gmpy2-2.0.8-py37h6ef4df4_2.tar.bz2"
  },
  "greenlet-0.4.15-py37h1de35cc_0": {
    "md5": "49dd902ba2479be4b951fa95b3b5f07e",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/greenlet-0.4.15-py37h1de35cc_0.tar.bz2"
  },
  "h5py-2.8.0-py37h878fce3_3": {
    "md5": "f2b6a5165d836c8188646a79262abdc3",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/h5py-2.8.0-py37h878fce3_3.tar.bz2"
  },
  "hdf5-1.10.2-hfa1e0ec_1": {
    "md5": "659980e333c5cf1e580f9d3f8e552d01",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/hdf5-1.10.2-hfa1e0ec_1.tar.bz2"
  },
  "heapdict-1.0.0-py37_2": {
    "md5": "500ad8406569dea3e0a5b477bac53fd8",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/heapdict-1.0.0-py37_2.tar.bz2"
  },
  "html5lib-1.0.1-py37_0": {
    "md5": "db78fb03cb3d5549b974aff7f558072f",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/html5lib-1.0.1-py37_0.tar.bz2"
  },
  "icu-58.2-h4b95b61_1": {
    "md5": "323d1f0b75edbb03ea936ee4b47b566f",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/icu-58.2-h4b95b61_1.tar.bz2"
  },
  "idna-2.8-py37_0": {
    "md5": "1bdbe37cfece6b6221d354ac2ba4ef58",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/idna-2.8-py37_0.tar.bz2"
  },
  "imageio-2.4.1-py37_0": {
    "md5": "98cea441e8d39cadb6cac24f0f7ccb7b",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/imageio-2.4.1-py37_0.tar.bz2"
  },
  "imagesize-1.1.0-py37_0": {
    "md5": "e8040d3ed53488c60e6dda783f163ddd",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/imagesize-1.1.0-py37_0.tar.bz2"
  },
  "importlib_metadata-0.6-py37_0": {
    "md5": "09ff8c9d603e6b27eacd050748311329",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/importlib_metadata-0.6-py37_0.tar.bz2"
  },
  "intel-openmp-2019.1-144": {
    "md5": "580ee35fd18dd1b9d5476bb8c44a7a6a",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/intel-openmp-2019.1-144.tar.bz2"
  },
  "ipykernel-5.1.0-py37h39e3cac_0": {
    "md5": "4ceb4afc729de4b2e39f1bef79c8d062",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/ipykernel-5.1.0-py37h39e3cac_0.tar.bz2"
  },
  "ipython-7.2.0-py37h39e3cac_0": {
    "md5": "a787c246276d9a78d1822e50731319d9",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/ipython-7.2.0-py37h39e3cac_0.tar.bz2"
  },
  "ipython_genutils-0.2.0-py37_0": {
    "md5": "65b3b9c0365d8d3ff7b5c1c32af40654",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/ipython_genutils-0.2.0-py37_0.tar.bz2"
  },
  "ipywidgets-7.4.2-py37_0": {
    "md5": "15e81f8b48bac7df01bc81ce4b248ede",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/ipywidgets-7.4.2-py37_0.tar.bz2"
  },
  "isort-4.3.4-py37_0": {
    "md5": "f72377f0ed79e956084da9afc57f3165",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/isort-4.3.4-py37_0.tar.bz2"
  },
  "itsdangerous-1.1.0-py37_0": {
    "md5": "47af7fe917005070c9e3560ee8650ef4",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/itsdangerous-1.1.0-py37_0.tar.bz2"
  },
  "jbig-2.1-h4d881f8_0": {
    "md5": "46d73d4693f37ce7455d1c01677165fa",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/jbig-2.1-h4d881f8_0.tar.bz2"
  },
  "jdcal-1.4-py37_0": {
    "md5": "96fbfb47eefe780df9fc2439d89ed24d",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/jdcal-1.4-py37_0.tar.bz2"
  },
  "jedi-0.13.2-py37_0": {
    "md5": "750213e56bc584b37d3f2e7e1968f415",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/jedi-0.13.2-py37_0.tar.bz2"
  },
  "jinja2-2.10-py37_0": {
    "md5": "aebc0fa4a31b82b00762979312b90753",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/jinja2-2.10-py37_0.tar.bz2"
  },
  "jpeg-9b-he5867d9_2": {
    "md5": "6673bf8de2e92f337afbde69c363e240",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/jpeg-9b-he5867d9_2.tar.bz2"
  },
  "jsonschema-2.6.0-py37_0": {
    "md5": "e9eeab2d153c55bcf1420214e4e9191b",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/jsonschema-2.6.0-py37_0.tar.bz2"
  },
  "jupyter-1.0.0-py37_7": {
    "md5": "adf475583faa9c865ae70c798c4364ca",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/jupyter-1.0.0-py37_7.tar.bz2"
  },
  "jupyter_client-5.2.4-py37_0": {
    "md5": "10b5fbe4d71e2037db13f7a400f071f7",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/jupyter_client-5.2.4-py37_0.tar.bz2"
  },
  "jupyter_console-6.0.0-py37_0": {
    "md5": "f0e5755bb57b6379d37c561a6e189170",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/jupyter_console-6.0.0-py37_0.tar.bz2"
  },
  "jupyter_core-4.4.0-py37_0": {
    "md5": "389dc1a12c8c9da2c8c6893e767623fe",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/jupyter_core-4.4.0-py37_0.tar.bz2"
  },
  "jupyterlab-0.35.3-py37_0": {
    "md5": "aa0d6e457822a36a1077e662cc4a382a",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/jupyterlab-0.35.3-py37_0.tar.bz2"
  },
  "jupyterlab_server-0.2.0-py37_0": {
    "md5": "23dd8c5728d1c01d9482005773a44e55",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/jupyterlab_server-0.2.0-py37_0.tar.bz2"
  },
  "keyring-17.0.0-py37_0": {
    "md5": "027307e466b70dcbcbb2ab588cb590e2",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/keyring-17.0.0-py37_0.tar.bz2"
  },
  "kiwisolver-1.0.1-py37h0a44026_0": {
    "md5": "47468d59c789ab8db7ae0a51642fc926",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/kiwisolver-1.0.1-py37h0a44026_0.tar.bz2"
  },
  "krb5-1.16.1-hddcf347_7": {
    "md5": "754e04aebf54797a5a35306e14e217da",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/krb5-1.16.1-hddcf347_7.tar.bz2"
  },
  "lazy-object-proxy-1.3.1-py37h1de35cc_2": {
    "md5": "85b1b3bddf1bbfcfb48fc9caf4dca1e7",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/lazy-object-proxy-1.3.1-py37h1de35cc_2.tar.bz2"
  },
  "libarchive-3.3.3-h786848e_5": {
    "md5": "547d8538dee2a43f9efc299f2c9dd09e",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/libarchive-3.3.3-h786848e_5.tar.bz2"
  },
  "libcurl-7.63.0-h051b688_1000": {
    "md5": "0d2ebe69fb6234d32526d1473eb78281",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/libcurl-7.63.0-h051b688_1000.tar.bz2"
  },
  "libcxx-4.0.1-hcfea43d_1": {
    "md5": "20dfb0ac1fa34f5ebe5c559043181939",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/libcxx-4.0.1-hcfea43d_1.tar.bz2"
  },
  "libcxxabi-4.0.1-hcfea43d_1": {
    "md5": "b06555a43b9c0857b87b342115bea761",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/libcxxabi-4.0.1-hcfea43d_1.tar.bz2"
  },
  "libedit-3.1.20170329-hb402a30_2": {
    "md5": "cd69630cf3a53947340e573aeabd4d95",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/libedit-3.1.20170329-hb402a30_2.tar.bz2"
  },
  "libffi-3.2.1-h475c297_4": {
    "md5": "4b13e6ff2ef114361106e5780296a5eb",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/libffi-3.2.1-h475c297_4.tar.bz2"
  },
  "libgfortran-3.0.1-h93005f0_2": {
    "md5": "e3a6e2b1a232418bbac9c47866273bdd",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/libgfortran-3.0.1-h93005f0_2.tar.bz2"
  },
  "libiconv-1.15-hdd342a3_7": {
    "md5": "024290c8272958ca67b9648842bafb6c",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/libiconv-1.15-hdd342a3_7.tar.bz2"
  },
  "liblief-0.9.0-h2a1bed3_0": {
    "md5": "15d20498741092a39875d9b843ca2753",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/liblief-0.9.0-h2a1bed3_0.tar.bz2"
  },
  "libpng-1.6.35-ha441bb4_0": {
    "md5": "7c4f80fbfacb4436293ff5d6501a1765",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/libpng-1.6.35-ha441bb4_0.tar.bz2"
  },
  "libsodium-1.0.16-h3efe00b_0": {
    "md5": "e28d578dc79800d577059385d439fce6",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/libsodium-1.0.16-h3efe00b_0.tar.bz2"
  },
  "libssh2-1.8.0-ha12b0ac_4": {
    "md5": "fdbf3ba3c78b0f924746b8d9252011fa",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/libssh2-1.8.0-ha12b0ac_4.tar.bz2"
  },
  "libtiff-4.0.9-hcb84e12_2": {
    "md5": "4f3d3fc7c5053b526201672974726d57",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/libtiff-4.0.9-hcb84e12_2.tar.bz2"
  },
  "libxml2-2.9.8-hab757c2_1": {
    "md5": "cb5bcc83786c9745f8589a9e3773239d",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/libxml2-2.9.8-hab757c2_1.tar.bz2"
  },
  "libxslt-1.1.32-hb819dd2_0": {
    "md5": "714d3711fdb64529105e57b226fdf78b",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/libxslt-1.1.32-hb819dd2_0.tar.bz2"
  },
  "llvmlite-0.26.0-py37h8c7ce04_0": {
    "md5": "2170336a91d67a14234d85241c82baef",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/llvmlite-0.26.0-py37h8c7ce04_0.tar.bz2"
  },
  "locket-0.2.0-py37_1": {
    "md5": "3ab37b2de8b951e4ac7cdf309f0aa71c",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/locket-0.2.0-py37_1.tar.bz2"
  },
  "lxml-4.2.5-py37hef8c89e_0": {
    "md5": "ae893c6951929f06cba5e767561e96ed",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/lxml-4.2.5-py37hef8c89e_0.tar.bz2"
  },
  "lz4-c-1.8.1.2-h1de35cc_0": {
    "md5": "4de92db9f54a4b55311fc1133e56a2a2",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/lz4-c-1.8.1.2-h1de35cc_0.tar.bz2"
  },
  "lzo-2.10-h362108e_2": {
    "md5": "c7ca1407cfabfe555a53936cc206e0d9",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/lzo-2.10-h362108e_2.tar.bz2"
  },
  "markupsafe-1.1.0-py37h1de35cc_0": {
    "md5": "e59b9b73d89df82436e02f5fe2d71d20",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/markupsafe-1.1.0-py37h1de35cc_0.tar.bz2"
  },
  "matplotlib-3.0.2-py37h54f8f79_0": {
    "md5": "71a7d4f6b6614f968fd9526d0e84df3b",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/matplotlib-3.0.2-py37h54f8f79_0.tar.bz2"
  },
  "mccabe-0.6.1-py37_1": {
    "md5": "05f80748dba40f4f4abc3dd00ce88680",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/mccabe-0.6.1-py37_1.tar.bz2"
  },
  "mistune-0.8.4-py37h1de35cc_0": {
    "md5": "d1d60c6bb2b142ad18cb2052ff79212b",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/mistune-0.8.4-py37h1de35cc_0.tar.bz2"
  },
  "mkl-2019.1-144": {
    "md5": "c9598d7fb664a16f0abfc2cb71491b62",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/mkl-2019.1-144.tar.bz2"
  },
  "mkl-service-1.1.2-py37hfbe908c_5": {
    "md5": "dbccbb12badc6af5a28352b03ad102d4",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/mkl-service-1.1.2-py37hfbe908c_5.tar.bz2"
  },
  "mkl_fft-1.0.6-py37h27c97d8_0": {
    "md5": "7c1298ee514245162cd3ab0787648dfb",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/mkl_fft-1.0.6-py37h27c97d8_0.tar.bz2"
  },
  "mkl_random-1.0.2-py37h27c97d8_0": {
    "md5": "5ccfa0b96f972dff3d1a51f19ae64fd3",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/mkl_random-1.0.2-py37h27c97d8_0.tar.bz2"
  },
  "more-itertools-4.3.0-py37_0": {
    "md5": "ae719c718596f36a13169973b3c7d7e6",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/more-itertools-4.3.0-py37_0.tar.bz2"
  },
  "mpc-1.1.0-h6ef4df4_1": {
    "md5": "e3f4e5825d7495329009da2529626af2",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/mpc-1.1.0-h6ef4df4_1.tar.bz2"
  },
  "mpfr-4.0.1-h3018a27_3": {
    "md5": "85d0b6b6c4112b7044fad544f2e02258",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/mpfr-4.0.1-h3018a27_3.tar.bz2"
  },
  "mpmath-1.1.0-py37_0": {
    "md5": "980d6326f1f09da275ca3f817267f9ba",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/mpmath-1.1.0-py37_0.tar.bz2"
  },
  "msgpack-python-0.5.6-py37h04f5b5a_1": {
    "md5": "2c580f67beabc5664cf8631210789685",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/msgpack-python-0.5.6-py37h04f5b5a_1.tar.bz2"
  },
  "multipledispatch-0.6.0-py37_0": {
    "md5": "05464b2cfcdc4fc6ea8face77015a47a",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/multipledispatch-0.6.0-py37_0.tar.bz2"
  },
  "navigator-updater-0.2.1-py37_0": {
    "md5": "d58753126cd8d56c2986e12c72888e98",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/navigator-updater-0.2.1-py37_0.tar.bz2"
  },
  "nbconvert-5.4.0-py37_1": {
    "md5": "9bf8516472822ce7827e010fbb77f916",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/nbconvert-5.4.0-py37_1.tar.bz2"
  },
  "nbformat-4.4.0-py37_0": {
    "md5": "ac69c8ccba4014a379b8b3df3b462446",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/nbformat-4.4.0-py37_0.tar.bz2"
  },
  "ncurses-6.1-h0a44026_1": {
    "md5": "6b2728131239deb2ffa0236adb131fe0",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/ncurses-6.1-h0a44026_1.tar.bz2"
  },
  "networkx-2.2-py37_1": {
    "md5": "e899970778144174d156ef1583fd7099",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/networkx-2.2-py37_1.tar.bz2"
  },
  "nltk-3.4-py37_1": {
    "md5": "c51f6e90b74244e7374717038be17c71",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/nltk-3.4-py37_1.tar.bz2"
  },
  "nose-1.3.7-py37_2": {
    "md5": "762dd08fd5edd6477ad51a16fa5883c7",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/nose-1.3.7-py37_2.tar.bz2"
  },
  "notebook-5.7.4-py37_0": {
    "md5": "2bd850b1f325ef4cfd9de3125e86ee51",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/notebook-5.7.4-py37_0.tar.bz2"
  },
  "numba-0.41.0-py37h6440ff4_0": {
    "md5": "6f31e2aeae61e221cacd68190aecf3f9",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/numba-0.41.0-py37h6440ff4_0.tar.bz2"
  },
  "numexpr-2.6.8-py37h7413580_0": {
    "md5": "98ec2a4a6528e2a0a3a4a682fb18f3ce",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/numexpr-2.6.8-py37h7413580_0.tar.bz2"
  },
  "numpy-1.15.4-py37hacdab7b_0": {
    "md5": "33dc44d99f7a1eff40e316a7ba1f3164",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/numpy-1.15.4-py37hacdab7b_0.tar.bz2"
  },
  "numpy-base-1.15.4-py37h6575580_0": {
    "md5": "c278520f9db458d47ecf39e25a2497d9",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/numpy-base-1.15.4-py37h6575580_0.tar.bz2"
  },
  "numpydoc-0.8.0-py37_0": {
    "md5": "afb3d666efa38f9dd3fbc387f1b91339",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/numpydoc-0.8.0-py37_0.tar.bz2"
  },
  "odo-0.5.1-py37_0": {
    "md5": "f5b85741a3dc157c92631cac256539e4",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/odo-0.5.1-py37_0.tar.bz2"
  },
  "olefile-0.46-py37_0": {
    "md5": "8ccdf16277b606cebea5461777ba3787",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/olefile-0.46-py37_0.tar.bz2"
  },
  "openpyxl-2.5.12-py37_0": {
    "md5": "01720eab4205d0760f3c77fdde3f8d0d",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/openpyxl-2.5.12-py37_0.tar.bz2"
  },
  "openssl-1.1.1a-h1de35cc_0": {
    "md5": "f13cb6464eb5ce48f7b02a896fd8fe4d",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/openssl-1.1.1a-h1de35cc_0.tar.bz2"
  },
  "packaging-18.0-py37_0": {
    "md5": "86fd7a7985f199e7f5dc51330373e506",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/packaging-18.0-py37_0.tar.bz2"
  },
  "pandas-0.23.4-py37h6440ff4_0": {
    "md5": "495c11c94b42704630aaaf4c17e68fb0",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pandas-0.23.4-py37h6440ff4_0.tar.bz2"
  },
  "pandoc-1.19.2.1-ha5e8f32_1": {
    "md5": "f6e369d599448e3052f712ca9c3d9398",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pandoc-1.19.2.1-ha5e8f32_1.tar.bz2"
  },
  "pandocfilters-1.4.2-py37_1": {
    "md5": "3e54dc613e71a7a7479bd543642d1eb5",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pandocfilters-1.4.2-py37_1.tar.bz2"
  },
  "parso-0.3.1-py37_0": {
    "md5": "2ed9c2efd7e9a15e14532e0f1a448e4f",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/parso-0.3.1-py37_0.tar.bz2"
  },
  "partd-0.3.9-py37_0": {
    "md5": "e5ed75095a35d08c5fb17bf5f758bd25",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/partd-0.3.9-py37_0.tar.bz2"
  },
  "path.py-11.5.0-py37_0": {
    "md5": "ab7ac6a8ff1ba912ab8ec8a540bf1ad1",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/path.py-11.5.0-py37_0.tar.bz2"
  },
  "pathlib2-2.3.3-py37_0": {
    "md5": "060519dc7f2e4068aed8973273275fc0",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pathlib2-2.3.3-py37_0.tar.bz2"
  },
  "patsy-0.5.1-py37_0": {
    "md5": "cfbc75d58f74eeabd9c6787c1586e705",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/patsy-0.5.1-py37_0.tar.bz2"
  },
  "pcre-8.42-h378b8a2_0": {
    "md5": "54cfde0351f854e3e495479f4b217609",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pcre-8.42-h378b8a2_0.tar.bz2"
  },
  "pep8-1.7.1-py37_0": {
    "md5": "81cc85a24d2c19aaef693a8af9f6c82e",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pep8-1.7.1-py37_0.tar.bz2"
  },
  "pexpect-4.6.0-py37_0": {
    "md5": "222ebf919bdaf5885c2894609d968805",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pexpect-4.6.0-py37_0.tar.bz2"
  },
  "pickleshare-0.7.5-py37_0": {
    "md5": "7f3599bcf1cd105009525058e0145f05",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pickleshare-0.7.5-py37_0.tar.bz2"
  },
  "pillow-5.3.0-py37hb68e598_0": {
    "md5": "a12a8e84a3757c803c076fd7708d0efc",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pillow-5.3.0-py37hb68e598_0.tar.bz2"
  },
  "pip-18.1-py37_0": {
    "md5": "bf96efaede98d2811bba968fa1942531",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pip-18.1-py37_0.tar.bz2"
  },
  "pkginfo-1.4.2-py37_1": {
    "md5": "c54c77544be7bcac04b3bdbe67f4c057",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pkginfo-1.4.2-py37_1.tar.bz2"
  },
  "pluggy-0.8.0-py37_0": {
    "md5": "916fbf9b83eb5d4253b7f86f7e913baa",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pluggy-0.8.0-py37_0.tar.bz2"
  },
  "ply-3.11-py37_0": {
    "md5": "b46569b04f2c385f2b0a624177c95e88",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/ply-3.11-py37_0.tar.bz2"
  },
  "prometheus_client-0.5.0-py37_0": {
    "md5": "8061f0c34baac99efbd834a30c339e23",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/prometheus_client-0.5.0-py37_0.tar.bz2"
  },
  "prompt_toolkit-2.0.7-py37_0": {
    "md5": "5a3f57d00a36da796a22ae53df70e307",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/prompt_toolkit-2.0.7-py37_0.tar.bz2"
  },
  "psutil-5.4.8-py37h1de35cc_0": {
    "md5": "53ff464a308927b63350d81214e44402",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/psutil-5.4.8-py37h1de35cc_0.tar.bz2"
  },
  "ptyprocess-0.6.0-py37_0": {
    "md5": "eaf349de500a66aba0ef3b208cb8fabd",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/ptyprocess-0.6.0-py37_0.tar.bz2"
  },
  "py-1.7.0-py37_0": {
    "md5": "cafd5479b71188fa39d02a98cb6eb32b",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/py-1.7.0-py37_0.tar.bz2"
  },
  "py-lief-0.9.0-py37hd4eaf27_0": {
    "md5": "adaf48eea96d2d9e505ed3ddf4143778",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/py-lief-0.9.0-py37hd4eaf27_0.tar.bz2"
  },
  "pycodestyle-2.4.0-py37_0": {
    "md5": "a8bb842ca9ebdac327b932e57e88c359",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pycodestyle-2.4.0-py37_0.tar.bz2"
  },
  "pycosat-0.6.3-py37h1de35cc_0": {
    "md5": "f57ecdeef06cb7dbe274891fde71279e",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pycosat-0.6.3-py37h1de35cc_0.tar.bz2"
  },
  "pycparser-2.19-py37_0": {
    "md5": "1bcdc1ec5ab9cfdc4c06903e4539eab3",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pycparser-2.19-py37_0.tar.bz2"
  },
  "pycrypto-2.6.1-py37h1de35cc_9": {
    "md5": "a729737932c59cc366e2b95e808f2bda",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pycrypto-2.6.1-py37h1de35cc_9.tar.bz2"
  },
  "pycurl-7.43.0.2-py37ha12b0ac_0": {
    "md5": "5752f9f31b09c86ced7bf0507ee084aa",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pycurl-7.43.0.2-py37ha12b0ac_0.tar.bz2"
  },
  "pyflakes-2.0.0-py37_0": {
    "md5": "26d8215bee7018079e0fae6ed1bf728f",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pyflakes-2.0.0-py37_0.tar.bz2"
  },
  "pygments-2.3.1-py37_0": {
    "md5": "91afb45dccb632172037d5a49e8e967c",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pygments-2.3.1-py37_0.tar.bz2"
  },
  "pylint-2.2.2-py37_0": {
    "md5": "0216fa9a4e1e595d9ec9d1dfc45b0ac0",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pylint-2.2.2-py37_0.tar.bz2"
  },
  "pyodbc-4.0.25-py37h0a44026_0": {
    "md5": "2d9fab3e090f8dfbbaec9bde6e21a7fe",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pyodbc-4.0.25-py37h0a44026_0.tar.bz2"
  },
  "pyopenssl-18.0.0-py37_0": {
    "md5": "eabbe9ed9b083b7e9fdbc253f0934892",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pyopenssl-18.0.0-py37_0.tar.bz2"
  },
  "pyparsing-2.3.0-py37_0": {
    "md5": "75f727262e44ac70020e3bb48cc222f8",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pyparsing-2.3.0-py37_0.tar.bz2"
  },
  "pyqt-5.9.2-py37h655552a_2": {
    "md5": "d078e73e5de30bbbe8bc13bcdf4bf6e9",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pyqt-5.9.2-py37h655552a_2.tar.bz2"
  },
  "pysocks-1.6.8-py37_0": {
    "md5": "06b7a8e46c01b268bd7f9aeb68461ccc",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pysocks-1.6.8-py37_0.tar.bz2"
  },
  "pytables-3.4.4-py37h13cba08_0": {
    "md5": "ca08dad70213380ac56f4bbbe59ef20a",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pytables-3.4.4-py37h13cba08_0.tar.bz2"
  },
  "pytest-4.0.2-py37_0": {
    "md5": "a2d1d6589e355bb2f5fea924fddf0412",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pytest-4.0.2-py37_0.tar.bz2"
  },
  "pytest-arraydiff-0.3-py37h39e3cac_0": {
    "md5": "5add6e9c6d6cf9a48afdf1348f8d4d16",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pytest-arraydiff-0.3-py37h39e3cac_0.tar.bz2"
  },
  "pytest-astropy-0.5.0-py37_0": {
    "md5": "2f9c883480f1085a11ecca4ad9d555af",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pytest-astropy-0.5.0-py37_0.tar.bz2"
  },
  "pytest-doctestplus-0.2.0-py37_0": {
    "md5": "bf8a9248496bf36d1545d0d7615bc3c6",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pytest-doctestplus-0.2.0-py37_0.tar.bz2"
  },
  "pytest-openfiles-0.3.1-py37_0": {
    "md5": "bfb06837b11303a4176cbfa0f2482805",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pytest-openfiles-0.3.1-py37_0.tar.bz2"
  },
  "pytest-remotedata-0.3.1-py37_0": {
    "md5": "475419d2e2c6212d82bdf4a1a8b95b8c",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pytest-remotedata-0.3.1-py37_0.tar.bz2"
  },
  "python-3.7.1-haf84260_7": {
    "md5": "e9ebc0ef0fef7b3df77526cd9ca86448",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/python-3.7.1-haf84260_7.tar.bz2"
  },
  "python-dateutil-2.7.5-py37_0": {
    "md5": "3f7dde71e5ed7501ca0d014eed4e61fa",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/python-dateutil-2.7.5-py37_0.tar.bz2"
  },
  "python-libarchive-c-2.8-py37_6": {
    "md5": "fec296796377124ff33b06b9e19c2aad",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/python-libarchive-c-2.8-py37_6.tar.bz2"
  },
  "python.app-2-py37_9": {
    "md5": "bd62aa063f069b74dc2cb11eda00fc7e",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/python.app-2-py37_9.tar.bz2"
  },
  "pytz-2018.7-py37_0": {
    "md5": "0bccfe89426338ab60639d93fd045819",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pytz-2018.7-py37_0.tar.bz2"
  },
  "pywavelets-1.0.1-py37h1d22016_0": {
    "md5": "57d67936fc00c726cd8cefe161d737ec",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pywavelets-1.0.1-py37h1d22016_0.tar.bz2"
  },
  "pyyaml-3.13-py37h1de35cc_0": {
    "md5": "ddc275288ce17c1fb1146520c4fb16e8",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pyyaml-3.13-py37h1de35cc_0.tar.bz2"
  },
  "pyzmq-17.1.2-py37h1de35cc_0": {
    "md5": "e11d0937b5cef29b5075d81f03a1c55c",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/pyzmq-17.1.2-py37h1de35cc_0.tar.bz2"
  },
  "qt-5.9.7-h468cd18_1": {
    "md5": "c9357bdb42c8d8a3b643ddbd8d0d9730",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/qt-5.9.7-h468cd18_1.tar.bz2"
  },
  "qtawesome-0.5.3-py37_0": {
    "md5": "d23893cbd530d4de0724bf9e067a4721",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/qtawesome-0.5.3-py37_0.tar.bz2"
  },
  "qtconsole-4.4.3-py37_0": {
    "md5": "e8dffddcbab5df16da7c0fb7370d642f",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/qtconsole-4.4.3-py37_0.tar.bz2"
  },
  "qtpy-1.5.2-py37_0": {
    "md5": "7f10a09d9963edb065aabb0db5b90657",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/qtpy-1.5.2-py37_0.tar.bz2"
  },
  "readline-7.0-h1de35cc_5": {
    "md5": "e7e32610dc0b61aa5947789844175bbf",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/readline-7.0-h1de35cc_5.tar.bz2"
  },
  "requests-2.21.0-py37_0": {
    "md5": "0b1e91e6a09e58951ab06e587392a837",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/requests-2.21.0-py37_0.tar.bz2"
  },
  "rope-0.11.0-py37_0": {
    "md5": "ea655482866a6f2a111334d0148113c1",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/rope-0.11.0-py37_0.tar.bz2"
  },
  "ruamel_yaml-0.15.46-py37h1de35cc_0": {
    "md5": "b2a9f584102d1811c93c5739c6e4e37e",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/ruamel_yaml-0.15.46-py37h1de35cc_0.tar.bz2"
  },
  "scikit-image-0.14.1-py37h0a44026_0": {
    "md5": "914c4ab4c012f58cc1b2063dfa359043",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/scikit-image-0.14.1-py37h0a44026_0.tar.bz2"
  },
  "scikit-learn-0.20.1-py37h27c97d8_0": {
    "md5": "88f5138ddc51f54b8d2d67c5a4b32c7f",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/scikit-learn-0.20.1-py37h27c97d8_0.tar.bz2"
  },
  "scipy-1.1.0-py37h1410ff5_2": {
    "md5": "e7cac3b62092b756ebcf9a4f3f09b10f",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/scipy-1.1.0-py37h1410ff5_2.tar.bz2"
  },
  "seaborn-0.9.0-py37_0": {
    "md5": "c5831fdaa0c710d18132d6a520788703",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/seaborn-0.9.0-py37_0.tar.bz2"
  },
  "send2trash-1.5.0-py37_0": {
    "md5": "0885ff3f969d5f3f1d193940083a3db6",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/send2trash-1.5.0-py37_0.tar.bz2"
  },
  "setuptools-40.6.3-py37_0": {
    "md5": "a7773b2c06b191906bb30907a7e5d500",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/setuptools-40.6.3-py37_0.tar.bz2"
  },
  "simplegeneric-0.8.1-py37_2": {
    "md5": "0ebcc1f379c2d85c57a385ab54e7efc1",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/simplegeneric-0.8.1-py37_2.tar.bz2"
  },
  "singledispatch-3.4.0.3-py37_0": {
    "md5": "918e37449ea4f80f571089a818748cae",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/singledispatch-3.4.0.3-py37_0.tar.bz2"
  },
  "sip-4.19.8-py37h0a44026_0": {
    "md5": "208a900d36e6a5526f609f8bff1a7de1",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/sip-4.19.8-py37h0a44026_0.tar.bz2"
  },
  "six-1.12.0-py37_0": {
    "md5": "f19bf8e3ce7f75497850b1408be450e5",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/six-1.12.0-py37_0.tar.bz2"
  },
  "snappy-1.1.7-he62c110_3": {
    "md5": "c426f8ea8d075fc5e1052e129ce3f577",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/snappy-1.1.7-he62c110_3.tar.bz2"
  },
  "snowballstemmer-1.2.1-py37_0": {
    "md5": "e6b9da4b7366ece906dff6357646dc65",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/snowballstemmer-1.2.1-py37_0.tar.bz2"
  },
  "sortedcollections-1.0.1-py37_0": {
    "md5": "01ebb00c4321cd7e8fb50aa4b25d15d9",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/sortedcollections-1.0.1-py37_0.tar.bz2"
  },
  "sortedcontainers-2.1.0-py37_0": {
    "md5": "a108e94d6ade80064948100bc472efb9",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/sortedcontainers-2.1.0-py37_0.tar.bz2"
  },
  "sphinx-1.8.2-py37_0": {
    "md5": "2571d5c570e5cf044d70f0c40b72c21e",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/sphinx-1.8.2-py37_0.tar.bz2"
  },
  "sphinxcontrib-1.0-py37_1": {
    "md5": "bc5a262aeac3ed5cfe98895320ce91cf",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/sphinxcontrib-1.0-py37_1.tar.bz2"
  },
  "sphinxcontrib-websupport-1.1.0-py37_1": {
    "md5": "1a956805ba34d9006c04fa90733dd732",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/sphinxcontrib-websupport-1.1.0-py37_1.tar.bz2"
  },
  "spyder-3.3.2-py37_0": {
    "md5": "3efe3cbc86710a3541a18915ded23886",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/spyder-3.3.2-py37_0.tar.bz2"
  },
  "spyder-kernels-0.3.0-py37_0": {
    "md5": "81e49b6a7cc1a11994e82dbc63245c62",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/spyder-kernels-0.3.0-py37_0.tar.bz2"
  },
  "sqlalchemy-1.2.15-py37h1de35cc_0": {
    "md5": "1c8b59aad237f03eb1f58c66ed3d4769",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/sqlalchemy-1.2.15-py37h1de35cc_0.tar.bz2"
  },
  "sqlite-3.26.0-ha441bb4_0": {
    "md5": "f1d76b6c4ea427cacdcc8a5fbc94499e",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/sqlite-3.26.0-ha441bb4_0.tar.bz2"
  },
  "statsmodels-0.9.0-py37h1d22016_0": {
    "md5": "d342a4cc9d9cb38891e5faafb121d0ee",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/statsmodels-0.9.0-py37h1d22016_0.tar.bz2"
  },
  "sympy-1.3-py37_0": {
    "md5": "f2a044b073d472418c069a7a7fdf2b0f",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/sympy-1.3-py37_0.tar.bz2"
  },
  "tblib-1.3.2-py37_0": {
    "md5": "26b82696cb3d93a43cae500c4ff6aa41",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/tblib-1.3.2-py37_0.tar.bz2"
  },
  "terminado-0.8.1-py37_1": {
    "md5": "ae08da44e90cc3c22dc87273a6fa596d",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/terminado-0.8.1-py37_1.tar.bz2"
  },
  "testpath-0.4.2-py37_0": {
    "md5": "cf2ac1c7763209862520beb95ff51858",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/testpath-0.4.2-py37_0.tar.bz2"
  },
  "tk-8.6.8-ha441bb4_0": {
    "md5": "0873cb53427d63926617c1d3f477cdd9",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/tk-8.6.8-ha441bb4_0.tar.bz2"
  },
  "toolz-0.9.0-py37_0": {
    "md5": "477a4cd2cd54b67ad3c75e1276443147",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/toolz-0.9.0-py37_0.tar.bz2"
  },
  "tornado-5.1.1-py37h1de35cc_0": {
    "md5": "ae5f807acc55d84d9d46fea0b4869ba4",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/tornado-5.1.1-py37h1de35cc_0.tar.bz2"
  },
  "tqdm-4.28.1-py37h28b3542_0": {
    "md5": "55c764f59d13719ed87b04c5d08c6cef",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/tqdm-4.28.1-py37h28b3542_0.tar.bz2"
  },
  "traitlets-4.3.2-py37_0": {
    "md5": "d95d618fed09cc226ebcdbc3f44157ae",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/traitlets-4.3.2-py37_0.tar.bz2"
  },
  "unicodecsv-0.14.1-py37_0": {
    "md5": "27174b375b492adc5b80933786cb6df3",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/unicodecsv-0.14.1-py37_0.tar.bz2"
  },
  "unixodbc-2.3.7-h1de35cc_0": {
    "md5": "14e6f0c0fd15f6d6b7717b1760893a0d",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/unixodbc-2.3.7-h1de35cc_0.tar.bz2"
  },
  "urllib3-1.24.1-py37_0": {
    "md5": "e93b0a60c716566fa2a859b4a245b18e",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/urllib3-1.24.1-py37_0.tar.bz2"
  },
  "wcwidth-0.1.7-py37_0": {
    "md5": "5a1936a06fe901a4aebf3216d96a9c75",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/wcwidth-0.1.7-py37_0.tar.bz2"
  },
  "webencodings-0.5.1-py37_1": {
    "md5": "a14bd3b5746f475e9235e249131ab4e4",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/webencodings-0.5.1-py37_1.tar.bz2"
  },
  "werkzeug-0.14.1-py37_0": {
    "md5": "49c8eb1209e9f6390c0a4f7983ce3918",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/werkzeug-0.14.1-py37_0.tar.bz2"
  },
  "wheel-0.32.3-py37_0": {
    "md5": "383438c59c19d9441b53b1233226a94a",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/wheel-0.32.3-py37_0.tar.bz2"
  },
  "widgetsnbextension-3.4.2-py37_0": {
    "md5": "ff1e6e29589c5b406c9e3b23556a47b0",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/widgetsnbextension-3.4.2-py37_0.tar.bz2"
  },
  "wrapt-1.10.11-py37h1de35cc_2": {
    "md5": "c03342c5596c91f1f4cf3482b365e0d9",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/wrapt-1.10.11-py37h1de35cc_2.tar.bz2"
  },
  "wurlitzer-1.0.2-py37_0": {
    "md5": "cc72db5ee01007a55ae3b3d1a3a8b253",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/wurlitzer-1.0.2-py37_0.tar.bz2"
  },
  "xlrd-1.2.0-py37_0": {
    "md5": "7d20824dba1b3894e7952f8ed20db8ca",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/xlrd-1.2.0-py37_0.tar.bz2"
  },
  "xlsxwriter-1.1.2-py37_0": {
    "md5": "c9b5a0d90d0fc77ae6ab63c020c97fce",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/xlsxwriter-1.1.2-py37_0.tar.bz2"
  },
  "xlwings-0.15.1-py37_0": {
    "md5": "fdc59f203ac7100ed736110742a49f5c",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/xlwings-0.15.1-py37_0.tar.bz2"
  },
  "xlwt-1.3.0-py37_0": {
    "md5": "1b0754652b194d1b08342b0c7718d39c",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/xlwt-1.3.0-py37_0.tar.bz2"
  },
  "xz-5.2.4-h1de35cc_4": {
    "md5": "8b2f68c15aee680cead7680e6208e984",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/xz-5.2.4-h1de35cc_4.tar.bz2"
  },
  "yaml-0.1.7-hc338f04_2": {
    "md5": "dab654341f57e56b615a678800262b0e",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/yaml-0.1.7-hc338f04_2.tar.bz2"
  },
  "zeromq-4.2.5-h0a44026_1": {
    "md5": "b61bf3cafee1897bd8afe17c209e1679",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/zeromq-4.2.5-h0a44026_1.tar.bz2"
  },
  "zict-0.1.3-py37_0": {
    "md5": "b7b567ec794bf8b7ada510be5217b4a8",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/zict-0.1.3-py37_0.tar.bz2"
  },
  "zlib-1.2.11-h1de35cc_3": {
    "md5": "6fddebfbe8354dd5fdb5ac8d56dec5bf",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/zlib-1.2.11-h1de35cc_3.tar.bz2"
  },
  "zstd-1.3.7-h5bba6e5_0": {
    "md5": "d6692000414fafcca8fafb10306e889d",
    "url": "https://repo.anaconda.com/pkgs/main/osx-64/zstd-1.3.7-h5bba6e5_0.tar.bz2"
  }
}
C_ENVS = {
  "root": [
    "python-3.7.1-haf84260_7",
    "blas-1.0-mkl",
    "bzip2-1.0.6-h1de35cc_5",
    "ca-certificates-2018.03.07-0",
    "conda-env-2.6.0-1",
    "intel-openmp-2019.1-144",
    "jbig-2.1-h4d881f8_0",
    "jpeg-9b-he5867d9_2",
    "libcxxabi-4.0.1-hcfea43d_1",
    "libgfortran-3.0.1-h93005f0_2",
    "libiconv-1.15-hdd342a3_7",
    "libsodium-1.0.16-h3efe00b_0",
    "lz4-c-1.8.1.2-h1de35cc_0",
    "lzo-2.10-h362108e_2",
    "pandoc-1.19.2.1-ha5e8f32_1",
    "xz-5.2.4-h1de35cc_4",
    "yaml-0.1.7-hc338f04_2",
    "zlib-1.2.11-h1de35cc_3",
    "libcxx-4.0.1-hcfea43d_1",
    "libpng-1.6.35-ha441bb4_0",
    "mkl-2019.1-144",
    "openssl-1.1.1a-h1de35cc_0",
    "tk-8.6.8-ha441bb4_0",
    "zstd-1.3.7-h5bba6e5_0",
    "expat-2.2.6-h0a44026_0",
    "freetype-2.9.1-hb4e5f40_0",
    "gmp-6.1.2-hb37e062_1",
    "hdf5-1.10.2-hfa1e0ec_1",
    "icu-58.2-h4b95b61_1",
    "libffi-3.2.1-h475c297_4",
    "liblief-0.9.0-h2a1bed3_0",
    "libssh2-1.8.0-ha12b0ac_4",
    "libtiff-4.0.9-hcb84e12_2",
    "ncurses-6.1-h0a44026_1",
    "pcre-8.42-h378b8a2_0",
    "snappy-1.1.7-he62c110_3",
    "zeromq-4.2.5-h0a44026_1",
    "blosc-1.14.4-hd9629dc_0",
    "gettext-0.19.8.1-h15daf44_3",
    "libedit-3.1.20170329-hb402a30_2",
    "libxml2-2.9.8-hab757c2_1",
    "mpfr-4.0.1-h3018a27_3",
    "readline-7.0-h1de35cc_5",
    "glib-2.56.2-hd9629dc_0",
    "krb5-1.16.1-hddcf347_7",
    "libarchive-3.3.3-h786848e_5",
    "libxslt-1.1.32-hb819dd2_0",
    "mpc-1.1.0-h6ef4df4_1",
    "sqlite-3.26.0-ha441bb4_0",
    "unixodbc-2.3.7-h1de35cc_0",
    "dbus-1.13.2-h760590f_1",
    "libcurl-7.63.0-h051b688_1000",
    "qt-5.9.7-h468cd18_1",
    "alabaster-0.7.12-py37_0",
    "appnope-0.1.0-py37_0",
    "appscript-1.0.1-py37h1de35cc_1",
    "asn1crypto-0.24.0-py37_0",
    "atomicwrites-1.2.1-py37_0",
    "attrs-18.2.0-py37h28b3542_0",
    "backcall-0.1.0-py37_0",
    "backports-1.0-py37_1",
    "beautifulsoup4-4.6.3-py37_0",
    "bitarray-0.8.3-py37h1de35cc_0",
    "boto-2.49.0-py37_0",
    "certifi-2018.11.29-py37_0",
    "chardet-3.0.4-py37_1",
    "click-7.0-py37_0",
    "cloudpickle-0.6.1-py37_0",
    "colorama-0.4.1-py37_0",
    "contextlib2-0.5.5-py37_0",
    "curl-7.63.0-ha441bb4_1000",
    "dask-core-1.0.0-py37_0",
    "decorator-4.3.0-py37_0",
    "defusedxml-0.5.0-py37_1",
    "docutils-0.14-py37_0",
    "entrypoints-0.2.3-py37_2",
    "et_xmlfile-1.0.1-py37_0",
    "fastcache-1.0.2-py37h1de35cc_2",
    "filelock-3.0.10-py37_0",
    "future-0.17.1-py37_0",
    "glob2-0.6-py37_1",
    "gmpy2-2.0.8-py37h6ef4df4_2",
    "greenlet-0.4.15-py37h1de35cc_0",
    "heapdict-1.0.0-py37_2",
    "idna-2.8-py37_0",
    "imagesize-1.1.0-py37_0",
    "importlib_metadata-0.6-py37_0",
    "ipython_genutils-0.2.0-py37_0",
    "itsdangerous-1.1.0-py37_0",
    "jdcal-1.4-py37_0",
    "kiwisolver-1.0.1-py37h0a44026_0",
    "lazy-object-proxy-1.3.1-py37h1de35cc_2",
    "llvmlite-0.26.0-py37h8c7ce04_0",
    "locket-0.2.0-py37_1",
    "lxml-4.2.5-py37hef8c89e_0",
    "markupsafe-1.1.0-py37h1de35cc_0",
    "mccabe-0.6.1-py37_1",
    "mistune-0.8.4-py37h1de35cc_0",
    "mkl-service-1.1.2-py37hfbe908c_5",
    "mpmath-1.1.0-py37_0",
    "msgpack-python-0.5.6-py37h04f5b5a_1",
    "numpy-base-1.15.4-py37h6575580_0",
    "olefile-0.46-py37_0",
    "pandocfilters-1.4.2-py37_1",
    "parso-0.3.1-py37_0",
    "pep8-1.7.1-py37_0",
    "pickleshare-0.7.5-py37_0",
    "pkginfo-1.4.2-py37_1",
    "pluggy-0.8.0-py37_0",
    "ply-3.11-py37_0",
    "prometheus_client-0.5.0-py37_0",
    "psutil-5.4.8-py37h1de35cc_0",
    "ptyprocess-0.6.0-py37_0",
    "py-1.7.0-py37_0",
    "py-lief-0.9.0-py37hd4eaf27_0",
    "pycodestyle-2.4.0-py37_0",
    "pycosat-0.6.3-py37h1de35cc_0",
    "pycparser-2.19-py37_0",
    "pycrypto-2.6.1-py37h1de35cc_9",
    "pycurl-7.43.0.2-py37ha12b0ac_0",
    "pyflakes-2.0.0-py37_0",
    "pyodbc-4.0.25-py37h0a44026_0",
    "pyparsing-2.3.0-py37_0",
    "pysocks-1.6.8-py37_0",
    "python-libarchive-c-2.8-py37_6",
    "python.app-2-py37_9",
    "pytz-2018.7-py37_0",
    "pyyaml-3.13-py37h1de35cc_0",
    "pyzmq-17.1.2-py37h1de35cc_0",
    "qtpy-1.5.2-py37_0",
    "rope-0.11.0-py37_0",
    "ruamel_yaml-0.15.46-py37h1de35cc_0",
    "send2trash-1.5.0-py37_0",
    "simplegeneric-0.8.1-py37_2",
    "sip-4.19.8-py37h0a44026_0",
    "six-1.12.0-py37_0",
    "snowballstemmer-1.2.1-py37_0",
    "sortedcontainers-2.1.0-py37_0",
    "sphinxcontrib-1.0-py37_1",
    "sqlalchemy-1.2.15-py37h1de35cc_0",
    "tblib-1.3.2-py37_0",
    "testpath-0.4.2-py37_0",
    "toolz-0.9.0-py37_0",
    "tornado-5.1.1-py37h1de35cc_0",
    "tqdm-4.28.1-py37h28b3542_0",
    "unicodecsv-0.14.1-py37_0",
    "wcwidth-0.1.7-py37_0",
    "webencodings-0.5.1-py37_1",
    "werkzeug-0.14.1-py37_0",
    "wrapt-1.10.11-py37h1de35cc_2",
    "wurlitzer-1.0.2-py37_0",
    "xlrd-1.2.0-py37_0",
    "xlsxwriter-1.1.2-py37_0",
    "xlwt-1.3.0-py37_0",
    "astroid-2.1.0-py37_0",
    "babel-2.6.0-py37_0",
    "backports.os-0.1.1-py37_0",
    "backports.shutil_get_terminal_size-1.0.0-py37_2",
    "cffi-1.11.5-py37h6174b99_1",
    "cycler-0.10.0-py37_0",
    "cytoolz-0.9.0.1-py37h1de35cc_1",
    "html5lib-1.0.1-py37_0",
    "jedi-0.13.2-py37_0",
    "keyring-17.0.0-py37_0",
    "mkl_fft-1.0.6-py37h27c97d8_0",
    "mkl_random-1.0.2-py37h27c97d8_0",
    "more-itertools-4.3.0-py37_0",
    "multipledispatch-0.6.0-py37_0",
    "nltk-3.4-py37_1",
    "openpyxl-2.5.12-py37_0",
    "packaging-18.0-py37_0",
    "partd-0.3.9-py37_0",
    "pathlib2-2.3.3-py37_0",
    "pexpect-4.6.0-py37_0",
    "pillow-5.3.0-py37hb68e598_0",
    "pyqt-5.9.2-py37h655552a_2",
    "python-dateutil-2.7.5-py37_0",
    "qtawesome-0.5.3-py37_0",
    "setuptools-40.6.3-py37_0",
    "singledispatch-3.4.0.3-py37_0",
    "sortedcollections-1.0.1-py37_0",
    "sphinxcontrib-websupport-1.1.0-py37_1",
    "sympy-1.3-py37_0",
    "terminado-0.8.1-py37_1",
    "traitlets-4.3.2-py37_0",
    "xlwings-0.15.1-py37_0",
    "zict-0.1.3-py37_0",
    "bleach-3.0.2-py37_0",
    "clyent-1.2.2-py37_1",
    "cryptography-2.4.2-py37ha12b0ac_0",
    "cython-0.29.2-py37h0a44026_0",
    "distributed-1.25.1-py37_0",
    "get_terminal_size-1.0.0-h7520d66_0",
    "gevent-1.3.7-py37h1de35cc_1",
    "isort-4.3.4-py37_0",
    "jinja2-2.10-py37_0",
    "jsonschema-2.6.0-py37_0",
    "jupyter_core-4.4.0-py37_0",
    "navigator-updater-0.2.1-py37_0",
    "networkx-2.2-py37_1",
    "nose-1.3.7-py37_2",
    "numpy-1.15.4-py37hacdab7b_0",
    "path.py-11.5.0-py37_0",
    "pygments-2.3.1-py37_0",
    "pytest-4.0.2-py37_0",
    "wheel-0.32.3-py37_0",
    "bokeh-1.0.2-py37_0",
    "bottleneck-1.2.1-py37h1d22016_1",
    "conda-verify-3.1.1-py37_0",
    "datashape-0.5.4-py37_1",
    "flask-1.0.2-py37_1",
    "h5py-2.8.0-py37h878fce3_3",
    "imageio-2.4.1-py37_0",
    "jupyter_client-5.2.4-py37_0",
    "matplotlib-3.0.2-py37h54f8f79_0",
    "nbformat-4.4.0-py37_0",
    "numba-0.41.0-py37h6440ff4_0",
    "numexpr-2.6.8-py37h7413580_0",
    "pandas-0.23.4-py37h6440ff4_0",
    "pip-18.1-py37_0",
    "prompt_toolkit-2.0.7-py37_0",
    "pylint-2.2.2-py37_0",
    "pyopenssl-18.0.0-py37_0",
    "pytest-arraydiff-0.3-py37h39e3cac_0",
    "pytest-doctestplus-0.2.0-py37_0",
    "pytest-openfiles-0.3.1-py37_0",
    "pytest-remotedata-0.3.1-py37_0",
    "pywavelets-1.0.1-py37h1d22016_0",
    "scipy-1.1.0-py37h1410ff5_2",
    "bkcharts-0.2-py37_0",
    "dask-1.0.0-py37_0",
    "flask-cors-3.0.7-py37_0",
    "ipython-7.2.0-py37h39e3cac_0",
    "nbconvert-5.4.0-py37_1",
    "patsy-0.5.1-py37_0",
    "pytables-3.4.4-py37h13cba08_0",
    "pytest-astropy-0.5.0-py37_0",
    "scikit-image-0.14.1-py37h0a44026_0",
    "scikit-learn-0.20.1-py37h27c97d8_0",
    "urllib3-1.24.1-py37_0",
    "astropy-3.1-py37h1de35cc_0",
    "ipykernel-5.1.0-py37h39e3cac_0",
    "odo-0.5.1-py37_0",
    "requests-2.21.0-py37_0",
    "statsmodels-0.9.0-py37h1d22016_0",
    "anaconda-client-1.7.2-py37_0",
    "blaze-0.11.3-py37_0",
    "jupyter_console-6.0.0-py37_0",
    "notebook-5.7.4-py37_0",
    "qtconsole-4.4.3-py37_0",
    "seaborn-0.9.0-py37_0",
    "sphinx-1.8.2-py37_0",
    "spyder-kernels-0.3.0-py37_0",
    "anaconda-navigator-1.9.6-py37_0",
    "anaconda-project-0.8.2-py37_0",
    "jupyterlab_server-0.2.0-py37_0",
    "numpydoc-0.8.0-py37_0",
    "widgetsnbextension-3.4.2-py37_0",
    "ipywidgets-7.4.2-py37_0",
    "jupyterlab-0.35.3-py37_0",
    "spyder-3.3.2-py37_0",
    "_ipyw_jlab_nb_ext_conf-0.1.0-py37_0",
    "jupyter-1.0.0-py37_7",
    "anaconda-2018.12-py37_0",
    "conda-4.5.12-py37_0",
    "conda-build-3.17.6-py37_0"
  ]
}



def _link(src, dst, linktype=LINK_HARD):
    if linktype == LINK_HARD:
        if on_win:
            from ctypes import windll, wintypes
            CreateHardLink = windll.kernel32.CreateHardLinkW
            CreateHardLink.restype = wintypes.BOOL
            CreateHardLink.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR,
                                       wintypes.LPVOID]
            if not CreateHardLink(dst, src, None):
                raise OSError('win32 hard link failed')
        else:
            os.link(src, dst)
    elif linktype == LINK_COPY:
        # copy relative symlinks as symlinks
        if islink(src) and not os.readlink(src).startswith(os.path.sep):
            os.symlink(os.readlink(src), dst)
        else:
            shutil.copy2(src, dst)
    else:
        raise Exception("Did not expect linktype=%r" % linktype)


def rm_rf(path):
    """
    try to delete path, but never fail
    """
    try:
        if islink(path) or isfile(path):
            # Note that we have to check if the destination is a link because
            # exists('/path/to/dead-link') will return False, although
            # islink('/path/to/dead-link') is True.
            os.unlink(path)
        elif isdir(path):
            shutil.rmtree(path)
    except (OSError, IOError):
        pass


def yield_lines(path):
    for line in open(path):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        yield line


prefix_placeholder = ('/opt/anaconda1anaconda2'
                      # this is intentionally split into parts,
                      # such that running this program on itself
                      # will leave it unchanged
                      'anaconda3')

def read_has_prefix(path):
    """
    reads `has_prefix` file and return dict mapping filenames to
    tuples(placeholder, mode)
    """
    import shlex

    res = {}
    try:
        for line in yield_lines(path):
            try:
                parts = [x.strip('"\'') for x in shlex.split(line, posix=False)]
                # assumption: placeholder and mode will never have a space
                placeholder, mode, f = parts[0], parts[1], ' '.join(parts[2:])
                res[f] = (placeholder, mode)
            except (ValueError, IndexError):
                res[line] = (prefix_placeholder, 'text')
    except IOError:
        pass
    return res


def exp_backoff_fn(fn, *args):
    """
    for retrying file operations that fail on Windows due to virus scanners
    """
    if not on_win:
        return fn(*args)

    import time
    import errno
    max_tries = 6  # max total time = 6.4 sec
    for n in range(max_tries):
        try:
            result = fn(*args)
        except (OSError, IOError) as e:
            if e.errno in (errno.EPERM, errno.EACCES):
                if n == max_tries - 1:
                    raise Exception("max_tries=%d reached" % max_tries)
                time.sleep(0.1 * (2 ** n))
            else:
                raise e
        else:
            return result


class PaddingError(Exception):
    pass


def binary_replace(data, a, b):
    """
    Perform a binary replacement of `data`, where the placeholder `a` is
    replaced with `b` and the remaining string is padded with null characters.
    All input arguments are expected to be bytes objects.
    """
    def replace(match):
        occurances = match.group().count(a)
        padding = (len(a) - len(b)) * occurances
        if padding < 0:
            raise PaddingError(a, b, padding)
        return match.group().replace(a, b) + b'\0' * padding

    pat = re.compile(re.escape(a) + b'([^\0]*?)\0')
    res = pat.sub(replace, data)
    assert len(res) == len(data)
    return res


def update_prefix(path, new_prefix, placeholder, mode):
    if on_win:
        # force all prefix replacements to forward slashes to simplify need
        # to escape backslashes - replace with unix-style path separators
        new_prefix = new_prefix.replace('\\', '/')

    path = os.path.realpath(path)
    with open(path, 'rb') as fi:
        data = fi.read()
    if mode == 'text':
        new_data = data.replace(placeholder.encode('utf-8'),
                                new_prefix.encode('utf-8'))
    elif mode == 'binary':
        if on_win:
            # anaconda-verify will not allow binary placeholder on Windows.
            # However, since some packages might be created wrong (and a
            # binary placeholder would break the package, we just skip here.
            return
        new_data = binary_replace(data, placeholder.encode('utf-8'),
                                  new_prefix.encode('utf-8'))
    else:
        sys.exit("Invalid mode:" % mode)

    if new_data == data:
        return
    st = os.lstat(path)
    # unlink in case the file is memory mapped
    exp_backoff_fn(os.unlink, path)
    with open(path, 'wb') as fo:
        fo.write(new_data)
    os.chmod(path, stat.S_IMODE(st.st_mode))


def name_dist(dist):
    if hasattr(dist, 'name'):
        return dist.name
    else:
        return dist.rsplit('-', 2)[0]


def create_meta(prefix, dist, info_dir, extra_info):
    """
    Create the conda metadata, in a given prefix, for a given package.
    """
    # read info/index.json first
    with open(join(info_dir, 'index.json')) as fi:
        meta = json.load(fi)
    # add extra info
    meta.update(extra_info)
    # write into <prefix>/conda-meta/<dist>.json
    meta_dir = join(prefix, 'conda-meta')
    if not isdir(meta_dir):
        os.makedirs(meta_dir)
    with open(join(meta_dir, dist + '.json'), 'w') as fo:
        json.dump(meta, fo, indent=2, sort_keys=True)


def run_script(prefix, dist, action='post-link'):
    """
    call the post-link (or pre-unlink) script, and return True on success,
    False on failure
    """
    path = join(prefix, 'Scripts' if on_win else 'bin', '.%s-%s.%s' % (
            name_dist(dist),
            action,
            'bat' if on_win else 'sh'))
    if not isfile(path):
        return True
    if SKIP_SCRIPTS:
        print("WARNING: skipping %s script by user request" % action)
        return True

    if on_win:
        try:
            args = [os.environ['COMSPEC'], '/c', path]
        except KeyError:
            return False
    else:
        shell_path = '/bin/sh' if 'bsd' in sys.platform else '/bin/bash'
        args = [shell_path, path]

    env = os.environ
    env['PREFIX'] = prefix

    import subprocess
    try:
        subprocess.check_call(args, env=env)
    except subprocess.CalledProcessError:
        return False
    return True


url_pat = re.compile(r'''
(?P<baseurl>\S+/)                 # base URL
(?P<fn>[^\s#/]+)                  # filename
([#](?P<md5>[0-9a-f]{32}))?       # optional MD5
$                                 # EOL
''', re.VERBOSE)

def read_urls(dist):
    try:
        data = open(join(PKGS_DIR, 'urls')).read()
        for line in data.split()[::-1]:
            m = url_pat.match(line)
            if m is None:
                continue
            if m.group('fn') == '%s.tar.bz2' % dist:
                return {'url': m.group('baseurl') + m.group('fn'),
                        'md5': m.group('md5')}
    except IOError:
        pass
    return {}


def read_no_link(info_dir):
    res = set()
    for fn in 'no_link', 'no_softlink':
        try:
            res.update(set(yield_lines(join(info_dir, fn))))
        except IOError:
            pass
    return res


def linked(prefix):
    """
    Return the (set of canonical names) of linked packages in prefix.
    """
    meta_dir = join(prefix, 'conda-meta')
    if not isdir(meta_dir):
        return set()
    return set(fn[:-5] for fn in os.listdir(meta_dir) if fn.endswith('.json'))


def link(prefix, dist, linktype=LINK_HARD, info_dir=None):
    '''
    Link a package in a specified prefix.  We assume that the packacge has
    been extra_info in either
      - <PKGS_DIR>/dist
      - <ROOT_PREFIX>/ (when the linktype is None)
    '''
    if linktype:
        source_dir = join(PKGS_DIR, dist)
        info_dir = join(source_dir, 'info')
        no_link = read_no_link(info_dir)
    else:
        info_dir = info_dir or join(prefix, 'info')

    files = list(yield_lines(join(info_dir, 'files')))
    # TODO: Use paths.json, if available or fall back to this method
    has_prefix_files = read_has_prefix(join(info_dir, 'has_prefix'))

    if linktype:
        for f in files:
            src = join(source_dir, f)
            dst = join(prefix, f)
            dst_dir = dirname(dst)
            if not isdir(dst_dir):
                os.makedirs(dst_dir)
            if exists(dst):
                if FORCE:
                    rm_rf(dst)
                else:
                    raise Exception("dst exists: %r" % dst)
            lt = linktype
            if f in has_prefix_files or f in no_link or islink(src):
                lt = LINK_COPY
            try:
                _link(src, dst, lt)
            except OSError:
                pass

    for f in sorted(has_prefix_files):
        placeholder, mode = has_prefix_files[f]
        try:
            update_prefix(join(prefix, f), prefix, placeholder, mode)
        except PaddingError:
            sys.exit("ERROR: placeholder '%s' too short in: %s\n" %
                     (placeholder, dist))

    if not run_script(prefix, dist, 'post-link'):
        sys.exit("Error: post-link failed for: %s" % dist)

    meta = {
        'files': files,
        'link': ({'source': source_dir,
                  'type': link_name_map.get(linktype)}
                 if linktype else None),
    }
    try:    # add URL and MD5
        meta.update(IDISTS[dist])
    except KeyError:
        meta.update(read_urls(dist))
    meta['installed_by'] = 'Anaconda3-2018.12-MacOSX-x86_64.pkg'
    create_meta(prefix, dist, info_dir, meta)


def duplicates_to_remove(linked_dists, keep_dists):
    """
    Returns the (sorted) list of distributions to be removed, such that
    only one distribution (for each name) remains.  `keep_dists` is an
    interable of distributions (which are not allowed to be removed).
    """
    from collections import defaultdict

    keep_dists = set(keep_dists)
    ldists = defaultdict(set) # map names to set of distributions
    for dist in linked_dists:
        name = name_dist(dist)
        ldists[name].add(dist)

    res = set()
    for dists in ldists.values():
        # `dists` is the group of packages with the same name
        if len(dists) == 1:
            # if there is only one package, nothing has to be removed
            continue
        if dists & keep_dists:
            # if the group has packages which are have to be kept, we just
            # take the set of packages which are in group but not in the
            # ones which have to be kept
            res.update(dists - keep_dists)
        else:
            # otherwise, we take lowest (n-1) (sorted) packages
            res.update(sorted(dists)[:-1])
    return sorted(res)


def yield_idists():
    for line in open(join(PKGS_DIR, 'urls')):
        m = url_pat.match(line)
        if m:
            fn = m.group('fn')
            yield fn[:-8]


def remove_duplicates():
    idists = list(yield_idists())
    keep_files = set()
    for dist in idists:
        with open(join(ROOT_PREFIX, 'conda-meta', dist + '.json')) as fi:
            meta = json.load(fi)
        keep_files.update(meta['files'])

    for dist in duplicates_to_remove(linked(ROOT_PREFIX), idists):
        print("unlinking: %s" % dist)
        meta_path = join(ROOT_PREFIX, 'conda-meta', dist + '.json')
        with open(meta_path) as fi:
            meta = json.load(fi)
        for f in meta['files']:
            if f not in keep_files:
                rm_rf(join(ROOT_PREFIX, f))
        rm_rf(meta_path)


def determine_link_type_capability():
    src = join(PKGS_DIR, 'urls')
    dst = join(ROOT_PREFIX, '.hard-link')
    assert isfile(src), src
    assert not isfile(dst), dst
    try:
        _link(src, dst, LINK_HARD)
        linktype = LINK_HARD
    except OSError:
        linktype = LINK_COPY
    finally:
        rm_rf(dst)
    return linktype


def link_dist(dist, linktype=None):
    if not linktype:
        linktype = determine_link_type_capability()
    prefix = prefix_env('root')
    link(prefix, dist, linktype)


def link_idists():
    linktype = determine_link_type_capability()
    for env_name in sorted(C_ENVS):
        dists = C_ENVS[env_name]
        assert isinstance(dists, list)
        if len(dists) == 0:
            continue

        prefix = prefix_env(env_name)
        for dist in dists:
            assert dist in IDISTS
            link_dist(dist, linktype)

        for dist in duplicates_to_remove(linked(prefix), dists):
            meta_path = join(prefix, 'conda-meta', dist + '.json')
            print("WARNING: unlinking: %s" % meta_path)
            try:
                os.rename(meta_path, meta_path + '.bak')
            except OSError:
                rm_rf(meta_path)


def prefix_env(env_name):
    if env_name == 'root':
        return ROOT_PREFIX
    else:
        return join(ROOT_PREFIX, 'envs', env_name)


def post_extract(env_name='root'):
    """
    assuming that the package is extracted in the environment `env_name`,
    this function does everything link() does except the actual linking,
    i.e. update prefix files, run 'post-link', creates the conda metadata,
    and removed the info/ directory afterwards.
    """
    prefix = prefix_env(env_name)
    info_dir = join(prefix, 'info')
    with open(join(info_dir, 'index.json')) as fi:
        meta = json.load(fi)
    dist = '%(name)s-%(version)s-%(build)s' % meta
    if FORCE:
        run_script(prefix, dist, 'pre-unlink')
    link(prefix, dist, linktype=None)
    shutil.rmtree(info_dir)


def multi_post_extract():
    # This function is called when using the --multi option, when building
    # .pkg packages on OSX.  I tried avoiding this extra option by running
    # the post extract step on each individual package (like it is done for
    # the .sh and .exe installers), by adding a postinstall script to each
    # conda .pkg file, but this did not work as expected.  Running all the
    # post extracts at end is also faster and could be considered for the
    # other installer types as well.
    for dist in yield_idists():
        info_dir = join(ROOT_PREFIX, 'info', dist)
        with open(join(info_dir, 'index.json')) as fi:
            meta = json.load(fi)
        dist = '%(name)s-%(version)s-%(build)s' % meta
        link(ROOT_PREFIX, dist, linktype=None, info_dir=info_dir)


def main():
    global ROOT_PREFIX, PKGS_DIR

    p = OptionParser(description="conda link tool used by installers")

    p.add_option('--root-prefix',
                 action="store",
                 default=abspath(join(__file__, '..', '..')),
                 help="root prefix (defaults to %default)")

    p.add_option('--post',
                 action="store",
                 help="perform post extract (on a single package), "
                      "in environment NAME",
                 metavar='NAME')

    opts, args = p.parse_args()
    if args:
        p.error('no arguments expected')

    ROOT_PREFIX = opts.root_prefix.replace('//', '/')
    PKGS_DIR = join(ROOT_PREFIX, 'pkgs')

    if opts.post:
        post_extract(opts.post)
        return

    if FORCE:
        print("using -f (force) option")

    link_idists()


def main2():
    global SKIP_SCRIPTS, ROOT_PREFIX, PKGS_DIR

    p = OptionParser(description="conda post extract tool used by installers")

    p.add_option('--skip-scripts',
                 action="store_true",
                 help="skip running pre/post-link scripts")

    p.add_option('--rm-dup',
                 action="store_true",
                 help="remove duplicates")

    p.add_option('--multi',
                 action="store_true",
                 help="multi post extract usecase")

    p.add_option('--link-dist',
                 action="store",
                 default=None,
                 help="link dist")

    p.add_option('--root-prefix',
                 action="store",
                 default=abspath(join(__file__, '..', '..')),
                 help="root prefix (defaults to %default)")

    opts, args = p.parse_args()
    ROOT_PREFIX = opts.root_prefix.replace('//', '/')
    PKGS_DIR = join(ROOT_PREFIX, 'pkgs')

    if args:
        p.error('no arguments expected')

    if opts.skip_scripts:
        SKIP_SCRIPTS = True

    if opts.rm_dup:
        remove_duplicates()
        return

    if opts.multi:
        multi_post_extract()
        return

    if opts.link_dist:
        link_dist(opts.link_dist)
        return

    post_extract()


def warn_on_special_chrs():
    if on_win:
        return
    for c in SPECIAL_ASCII:
        if c in ROOT_PREFIX:
            print("WARNING: found '%s' in install prefix." % c)


if __name__ == '__main__':
    if IDISTS:
        main()
        warn_on_special_chrs()
    else: # common usecase
        main2()
