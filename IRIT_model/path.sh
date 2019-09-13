export KALDI_ROOT=/home/pellegri/tools/kaldi/

source $KALDI_ROOT/tools/env.sh

export PATH=$PWD/utils/:$KALDI_ROOT/tools/openfst/bin:$PWD:$PATH
[ ! -f $KALDI_ROOT/tools/config/common_path.sh ] && echo >&2 "The standard file $KALDI_ROOT/tools/config/common_path.sh is not present -> Exit!" && exit 1
. $KALDI_ROOT/tools/config/common_path.sh
#export LC_ALL=C
#export LANG=fr_Fr.UTF-8
#export LANGUAGE=fr_FR.UTF-8
#export LC_ALL=fr_FR.UTF-8

# For now, don't include any of the optional dependenices of the main
# librispeech recipe
