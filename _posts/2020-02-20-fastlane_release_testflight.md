---
layout: post
current: post
navigation: True
title:  "fastlane - release, testflight"
date:   2020-02-20 00:00:01
cover: assets/images/ios/fastlane_background.png
description: fastlane - release, testflight
tags: [ ios ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---

# fastlane_release_testflight

이전 포스트에서 실무에서 사용하고 있는 fastlane 베타 배포에 관해서 설명했다. 일반적인 단일 앱에 대한 베타 배포는 튜토리얼을 따라가도 충분하지만 지금 프로젝트는 두 개의 익스텐션을 포함하고 있기 때문에 어려움이 있었다. 각각의 타깃에 맞게 인증서를 다운받아 설치해주고 빌드 세팅을 커스텀 하는 과정에서 꽤 많은 시간을 들였다.

 이번 포스트에서는 fastlane을 통한 release 배포 방법을 알아보려 한다. 사실 beta를 구축할 때 이미 release 버전에 대한 스크립트도 같이 작성을 완료했다. 실제로 사용하면서 여러 가지 불편한 부분을 수정해 문제가 없어 포스트로 공개하려고 한다.

 기본적인 부분은 앞선 beta 배포의 스크립트와 크게 다르지 않지만, 인증서를 관리하는 부분에서 조금 차이가 있다. 기존의 Debug config에 맞춰 dev 인증서를 사용했지만 이제 테스트 플라이트에 올리고 테스트 후 스토어에 등록해야 하기 때문에 release config에 app store 인증서를 사용해야 한다.

## Cert 파일

    get_certificates(
      development: false,
      output_path: "./fastlane/certificate/"
    )

## Provisioning Profile

    get_provisioning_profile(
      development: false,
      app_identifier: "kr.co.juvis.dietapp",
      filename: "dietapp_store.mobileprovision",
      output_path: "./fastlane/profiles/"
    )
    # noti service profile
    get_provisioning_profile(
      development: false,
      app_identifier: "kr.co.juvis.dietapp.notificationServiceExt",
      filename: "notificationServiceExt_storev.mobileprovision",
      output_path: "./fastlane/profiles/"
    )
    # widget profile
    get_provisioning_profile(
      development: false,
      app_identifier: "kr.co.juvis.dietapp.JuvisWidget",
      filename: "JuvisWidget_store.mobileprovision",
      output_path: "./fastlane/profiles/"
    )

여기까지는 그저 development 옵션을 false로 설정해 app store 인증서를 사용하는 과정이었다. build number를 올리는 부분을 새롭게 추가했다.

    # 빌드번호 + 1
    increment_build_number(
      build_number: latest_testflight_build_number + 1,
      xcodeproj: "JuvisApp.xcodeproj"
    )

 튜토리얼의 샘플에서는 앱 스토어에 올라가 있는 상용 버전에 +1 하는 예시가 나와 있다. 하지만 나는 테스트 플라이트를 통한 테스트를 빈번하게 하고 마지막 버전으로 스토어에 등록하기 때문에 테스트 플라이트의 마지막 build number에 + 1을 하도록 하고 있다.

 빌드를 진행하는 부분은 앞선 부분과 다를 게 없고 마지막에 beta가 아닌 테스트 플라이트에 올리는 명령어가 추가된다.

    upload_to_testflight(
      ipa: "fastlane/ipa/JuvisAppRelease.ipa",
      skip_waiting_for_build_processing: true
    )

 테스트 플라이트에 올리기 위해서는 Appfile에 아이튠즈 커넥트 정보를 입력해야 한다.

    itunes_connect_id 'jglee@openit.co.kr'
    itc_team_name "JUVIS co., Ltd."

 이 정보를 기반으로 로그인을 수행하고 테스트 플라이트에 올리게 된다. skip_waiting_for_build_processing 명령어가 없으면 빌드를 업로드 후 처리 중인 상태를 계속 기다리게 된다. 처리가 완료되면 자동으로 테스트가 시작되도록 설정해 둬서 기다릴 필요가 없기 때문에 skip_waiting_for_build_processing를 true로 줬다.

 근데 이대로 진행하면 수출 규정 관련 문서가 누락됨 메세지와 함께 테스트 배포까지는 진행되지 않는다.

[수출 규정 관련 문서가 누락됨 경고 메세지 대처법](https://zetal.tistory.com/entry/수출-규정-관련-문서가-누락됨-경고-메세지-대처법)

 상단 링크에 들어가면 자세한 내용이 나와 있는데, info.plist 파일에 설정을 추가하면 된다.

    <key>ITSAppUsesNonExemptEncryption</key>
    <false/>

여기까지 진행했으면 fastlane release 명령어를 터미널에 입력하면 한 번에 테스트 플라이트 배포까지 진행된다. 지금 프로젝트에서는 build config를 통해서 앱의 api base url 같은 설정 부분을 관리하고 있다. 간단하게 인증서와 앱 설정을 변경할 수 있다는 점에서 시간을 절약할 수 있다. 특히 빌드 번호를 올리는 부분은 예전에는 만약 테스트 플라이트에 동일한 빌드 번호가 올라가 있다면 다시 아카이빙해야 하는 치명적인 문제가 발생하기 때문에 항상 테스트 플라이트에 들어가서 확인해 주고 있었다. fastlane을 사용하면 페이지에 들어가서 일일이 확인해야 하는 시간 낭비를 해결할 수 있다.
