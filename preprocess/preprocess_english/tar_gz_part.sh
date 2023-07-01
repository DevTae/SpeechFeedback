#!/bin/bash
# Developed by DevTae@2023

# 용량 등의 이유로 .tar.gz.part* 에 대한 압축해제와 압축 파일 삭제를 동시에 진행하고 싶을 때 사용할 수 있는 스크립트이다.
# 만약, 모든 .tar.gz.part* 압축 파일에 대한 압축 해제가 필요하다면 cat *.tar.gz.part* | tar xzvf - 를 실행하면 된다.

for partfile in $(find . -name "*.tar.gz.part*" | sort)
do
	tar xzvf $partfile
	rm $partfile
done
