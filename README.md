# GitHub page maker

* https://jekyllrb-ko.github.io/docs/posts/

1. bundle install로 새로 생성
2. ouput에 있는 것을 업로드
3. bundle exec jekyll serve 로 로컬 실행

# 수정해서 업로드 방법
1. 내용 수정하고 bundle exec jekyll build 수행하면 output에 정적 파일 생성됨
2. cd ouput해서 add . commit push로 업로드하기
* output 부분을 submodule로 잡아놨음

# tag 추가
1. _data/tags에 추가할 것
2. navigation바에 그 테그를 추가할 것
