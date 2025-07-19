# GitHub page maker
 
* https://jekyllrb-ko.github.io/docs/posts/

# 노션 포스트 자동 변환
1. 노션에서 마크다운으로 전체 페이지를 다운로드합니다. (하위 페이지 포함)
2. 다운로드한 압축 파일의 압축을 해제합니다.
3. 생성된 폴더를 이 프로젝트의 `origin` 폴더로 이동시킵니다.
4. 터미널에서 `python3 script.py` 명령어를 실행합니다.
5. 스크립트가 자동으로 다음 작업을 수행합니다.
    - `_posts` 폴더에 Jekyll 형식의 마크다운 파일 생성
    - `assets/images` 폴더에 이미지 파일 복사 및 경로 수정
    - 처리가 완료된 원본 폴더는 `archive` 폴더로 이동
6. `bundle exec jekyll serve`로 로컬에서 변경 사항을 확인합니다.

---

1. bundle install로 새로 생성
    * 권한이 없다면 sudo로
2. ouput에 있는 것을 업로드
3. bundle exec jekyll serve 로 로컬 실행

# 수정해서 업로드 방법
1. 내용 수정하고 `bundle exec jekyll build` 수행하면 `output`에 정적 파일 생성됨
2. `cd output`으로 `output` 디렉토리로 이동
3. `git add .` 로 변경사항 스테이징
4. `git commit -m "커밋 메시지"` 로 커밋
5. `git push origin HEAD:master` 로 원격 저장소에 푸시 (detached HEAD 상태일 경우)
6. `cd ..` 로 상위 디렉토리로 이동
7. `git add output` 로 서브모듈 변경사항 스테이징
8. `git commit -m "서브모듈 업데이트"` 로 커밋
9. `git push` 로 상위 저장소에 푸시

# tag 추가
1. _data/tags에 추가할 것
2. navigation바에 그 테그를 추가할 것
   1. _includes/navigation.html
   2. href="{{site.baseurl}}tag/ios/" 에서 ios 부분이 포스트의 tag 값이다.

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
