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

# 검색 기능 추가
1. https://blog.hax0r.info/2018-02-18/using-search-from-jekyll/
2. https://github.com/webhacking/light-Jekyll-search
3. UI 는 수정이 필요해 보인다.

# 구글 애널리틱스 추가
1. https://rextarx.github.io/jekyll/2017/02/03/Applying_Google_Analytics_to_a_blog_using_Jekyll/
2. https://analytics.google.com/analytics/web/?authuser=0#/a154736789w218333510p208206940/admin/tracking/tracking-code/

# 구글 검색 추가
1. https://support.google.com/webmasters/answer/7451184?hl=ko
2. https://www.google.com/search?client=safari&rls=en&sxsrf=ACYBGNTOdplzxqPut-tnLo3IJqybEvybTg%3A1576641450033&ei=qqP5XZ3gAa-2mAXM8LAQ&q=site%3Aleejigun.github.io&oq=site%3Aleejigun.github.io&gs_l=psy-ab.3...17460.17460..17996...0.0..0.130.321.2j1......0....2j1..gws-wiz.4qlPZdLVNkQ&ved=0ahUKEwid3cSMp77mAhUvG6YKHUw4DAIQ4dUDCAo&uact=5
3. https://search.google.com/search-console?resource_id=https%3A%2F%2Fleejigun.github.io%2F
