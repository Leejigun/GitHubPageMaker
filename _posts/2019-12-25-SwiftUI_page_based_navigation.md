---
layout: post
current: post
navigation: True
title:  "SwiftUI에서 page based navigation 사용하기"
date:   2019-12-25 15:17:00
cover: assets/images/watchOS/2019-12-23-SwiftUI_page_based_navigation/background.png
description: SwiftUI에서 page based navigation 사용하기
tags: [ watchos, swiftui, project ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---

# SwiftUI에서 page based navigation 사용하기

apple watch의 UI 베이스는 주로 page base navigation 형태를 취하고 있다. apple watch는 작은 화면에서 사용자에게 같은 레벨의 UI를 제공하기 위해 페이지 형태를 제공하고 있다.

![](assets/images/watchOS/2019-12-23-SwiftUI_page_based_navigation/Untitled.png)

[Designing for the WATCH](https://webdesign.tutsplus.com/articles/designing-for-the-watch--cms-23818)

 storyboard를 사용할 경우 그냥 segue를 연결해주면 페이지들이 붙는 형태로 구성된다.

하지만 SwiftUI에서는 어떻게 이런 UI를 구현할까?

 SwiftUI에서 제공하는 View를 화면에 띄우기 위해서는 HostingController를 사용해야 한다. 프로젝트를 생성하면 WKHostingController를 가지고 시작한다. 이 WKHostingController의 애플 문서쪽을 확인해보면 다음과 같은 부분이 있다.

![](assets/images/watchOS/2019-12-23-SwiftUI_page_based_navigation/Untitled 1.png)

 내용을 살펴보면 page-based 라는 단어가 들어가 있는 것을 확인할 수 있다. 같은 이름으로 하나의 hosting controller만 집어넣으면 일반적으로 사용하는 modal, reaload 방식과 동일하지만 page based 네비게이션을 제공하기 위해서 배열로 받는 기능을 제공하고 있다.



---

  구조는 다음과 같다.

- 시간 선택 버튼에서 시간을 누른다.
- 타이머와 설정 화면이 page-based 상태로 나타난다.

 위 문서를 살펴보면 page-based 방식에는 2가지 방법이 있다.

- `presentController` - modal 형태로 추가
- `reloadRootControllers` - root를 교체

 목적에 따라서 다를 거 같지만 여기서는 `presentController` 메소드를 사용해 modal 형태로 추가하려 한다.

## Navigation Protocol

 시간 선택 화면(View)에서 이벤트가 발생하면 컨트롤러(WKHostingController) 로 `presentController`  이벤트를 요청해야 한다. 이를 위해서 protocol을 만들었다.

```swift
protocol NavigationHostProtocol: class {
    func moveTimer(sec: Double)
}

class HostingController: WKHostingController<TimerDefaultStartView> {

    override var body: TimerDefaultStartView {
        return TimerDefaultStartView(host: self)
    }
}
```
 TimerDefaultStartView에 host를 전달해 이벤트가 발생하면 `host.moveTimer(sec:)` 메소드를 호출하게 했다.

```swift
extension HostingController: NavigationHostProtocol{

    func moveTimer(sec: Double) {
        let service = TimerService(seconds: sec) as AnyObject
        let timer = ("TimerHostViewController", service)
        let dashbord = ("TimerDashboardViewController", service)

        self.presentController(withNamesAndContexts: [timer, dashbord])
    }
}
```

 여기서 service 오브젝트를 만들어 양쪽의 View가 공유할 수 있도록 했다. service를 공유함으로 완전히 다른 VIew 2개를 가지고 서로 설정을 처리할 수 있게 되었다.

 근데, 여기서 중요한 부분이 있다. 형태를 보면 (String, AnyObject) 형태의 tuple로 전달해야 하는데, 여기서 들어가는 identifier값이 storyboard에 저장된 WKHostingController의 id값이다. 따라서 storyboard에서 2개를 만들어줘야 한다.

![](assets/images/watchOS/2019-12-23-SwiftUI_page_based_navigation/Untitled 2.png)

---

## Context 전달

 다음으로 context로 넘기는 service를 WKHostingController에서 받아야 한다.

```swift
override func awake(withContext context: Any?) {
    guard let service = context as? TimerService else {
        fatalError()
    }
    self.timeService = service
    print(service.seconds)
}
```

이를 위해서 다음과 같이 메소드를 제공하고 있는데, 여기서 받은 다음에 넘겨주면 된다.

![](assets/images/watchOS/2019-12-23-SwiftUI_page_based_navigation/Untitled 3.png)
