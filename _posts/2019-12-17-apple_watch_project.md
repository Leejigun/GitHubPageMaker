---
layout: post
current: post
navigation: True
title:  "apple watch 프로젝트"
date:   2019-12-17 22:05:00
cover: assets/images/watchOS/2019-12-17-apple_watch_project/watchOs_background.png
description: apple watch 도입부
tags: [ watchos ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---
# apple watch 프로젝트

최근 애플 워치를 구매하고 워치 앱에 관심이 생겼다. 워치 앱을 공부하며 타임 타이머와 유사한 기능을 가진 워치 앱을 만들어 보려 한다.

## 타임 타이머

![apple%20watch/timeTimer.png](assets/images/watchOS/2019-12-17-apple_watch_project/timeTimer.png)

 타임 타이머의 핵심은 시각적으로 시간의 경과를 체감할 수 있는 화면에 있다. 타임 타이머는 기능적으로는 일반적인 요리용 쿡 타이머와 다를 바 없지만, 숫자나 소리로 알려주는 다른 타이머와 다르게, 원이 줄어들며 사용자에게 시간의 경과를 감각적으로 체감하게 해주고 압박감 줘 회의, 작업 등에 불필요한 잡담 시간을 줄일 수 있다는 게 장점이다.

- 타임 타이머에 대한 이야기

[타임타이머(Time Timer) 이야기 - amati.io](https://amati.io/2019/04/09/time-timer-story/)

---

## WatchOS 6

 이번에 iOS 앱이 아닌 워치 앱을 만드는 이유는 첫째로 최근 애플 워치 5세대를 구매하게 되었기 때문이다. 실제로 애플 워치를 사용해 보니 활동량, 운동, 알림 등 생활 전반적으로 삶의 질을 올려 주는 기능들이 많았다.

 이번 애플 워치 5세대의 출시와 함께 WatchOS 6.0 버전이 출시 되었다. 이번 WatchOS에 Siri, 워치 페이스 등 많은 기능들이 추가되었다.

[watchOS 6](https://www.apple.com/kr/watchos/watchos-6/)

 하지만 그중에서 가장 주목한 변경 점은 Watch 단독 앱 스토어다. 기존의 워치 앱은 iOS 앱 스토어에서 앱을 받아 그 앱에 종속된 워치 앱을 사용하는 방식으로 iOS 디바이스가 없다면 기본 앱만 사용 가능했다. 하지만 이번에 애플 워치 전용 앱 스토어가 오픈하면서 워치 단독 앱을 만들어 출시 할 수 있게 되었다.

 iOS 앱에 붙은 워치 앱을 서비스하면 복잡한 설정을 iOS 앱을 통해 설정하면 되기 때문에 좋다. 하지만 간단한 타임 타이머 앱을 만들려는데 iOS 앱까지 개발하려면 리소스가 너무 많이 들 거 같아 워치 단독 앱으로 시작하려 한다.

## SwiftUI

 워치 단독 앱을 만드는 다른 이유는 이번 iOS 13과 함께 공개된 SwiftUI를 사용할 기회라 생각했기 때문이다. SwiftUI는 기존 구글의 Flutter와 유사하게 코드를 통해 화면을 구성하는 방식을 취하고 있는데, 기존에도 이미 Texture를 사용해 코드로 화면을 만드는 방식에 익숙해 SwiftUI의 공개는 희소식이었다.

[Xcode - SwiftUI- Apple Developer](https://developer.apple.com/kr/xcode/swiftui/)

 기존 Autolayout을 사용하는 개발 방법도 좋지만 많은 단점이 있었고 그 단점을 극복하기 위해 다양한 방법이 있었다. 코드를 통해 화면을 구성하는 방법도 그중 하나로 이를 원활하게 지원하는 다양한 라이브러리가 있었다.

 SwiftUI가 공개되고 beta에 들어가기 전에 한동안 Flutter에 대해서 공부했었다. 지금 SwiftUI와 Flutter를 비교해보면 편의성 부분에서 Flutter가 압도적으로 같다. 예를 들어 텍스트 필드에 포커스가 들어오게 하는 부분은 SwiftUI에서는 지원하지 않기 때문에 커스텀 클래스 뷰를 만들어 사용해야 하지만 Flutter에서는 포커스 노드라는 개념이 있어서 포커스를 관리할 수 있다.
