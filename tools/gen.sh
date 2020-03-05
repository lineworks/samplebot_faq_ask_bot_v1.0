#!/bin/bash

:<<!
Copyright 2020-present Works Mobile Corp.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
!

filename=$1
echo ${filename}

filename_pot=${filename/py/pot}
filename_po=${filename_pot/pot/po}
filename_mo=${filename_pot/pot/mo}

pwd_path=`pwd`
locals=$pwd_path"/locales/"

en_locals=$locals"en/LC_MESSAGES/"
ko_locals=$locals"ko/LC_MESSAGES/"
ja_locals=$locals"ja/LC_MESSAGES/"

file_path="faq_bot/actions"
if [ $# -eq 3 ];
then
    file_path=$3
fi

echo ${pwd_path}"/"${file_path}"/"${filename}

action=$2
if [ ${action} == "po" ]; then
    echo `${pwd_path}"/tools/pygettext.py" -o ${locals}/${filename_pot} ${pwd_path}"/"${file_path}"/"${filename}`
    echo `cp ${locals}/${filename_pot} ${en_locals}/${filename_po}`
    echo `cp ${locals}/${filename_pot} ${ja_locals}/${filename_po}`
    echo `cp ${locals}/${filename_pot} ${ko_locals}/${filename_po}` 
elif [ ${action} == "mo" ]; then
    echo `${pwd_path}"/tools/msgfmt.py" -o ${en_locals}/${filename_mo} ${en_locals}/${filename_po}`
    echo `${pwd_path}"/tools/msgfmt.py" -o ${ko_locals}/${filename_mo} ${ko_locals}/${filename_po}`
    echo `${pwd_path}"/tools/msgfmt.py" -o ${ja_locals}/${filename_mo} ${ja_locals}/${filename_po}`
else
    echo "第二个参数应该是 po 或者 mo"

fi

