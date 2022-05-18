---
layout: post
current: post
navigation: True
title:  "DI(의존성 주입) using Swinject"
date:   2020-04-25 13:02:00
cover: assets/images/ios/Swinject.png
description: DI(의존성 주입) using Swinject
tags: [ ios ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---

# DI(의존성 주입) using Swinject

 최근 이직한 회사에서 모듈화 과정에서 DI에 대해 다루는 모습을 보고 DI에 대해서 정리하려 한다. 혼자서 일할 때는 DI에 대해서 알고 있었고 구조를 잡으면서 DI에 대해서 고민하면서 했었지만, 여기처럼 본격적으로 DI에 대해서 고민하면서 코딩하지 않았다.

 단순한 예로 클래스 A와 클래스 B가 있고 A안에 B가 필요한 경우 B를 외부에서 만들어 init에 인자로 넣어주는 방식을 사용해 DI를 구현한다. 나 같은 경우 ViewController를 만들 때 ViewModel을 외부에서 만들어 전달하는 방식을 사용했다.

 하지만 이렇게 init로 넘겨주는 경우에 의존하는 객체가 많아질수록 init 메소드의 파라미터가 엄청나게 많아지고 구현할 때 까먹을 위험도 있다. 그래서 Swift의 DI 프레임워크들은 하나의 Container를 가지고 이 컨테이너 통해서 의존성을 주입하는 방식을 취한다.

 지금 회사에도 ViewContainer라는 것을 가지고 ViewController를 만드는 모습을 보인다. 이 안에 내부적으로 ViewModel을 만들어 ViewController를 주입하는 코드가 들어 있는 모양이다.

### Swinject

 Swift에서 사용하는 대표적인 Dependency Injection(의존성 주입) 프레임 워크로 Swinject가 있다. 우리 회사에서 모듈화하는 작업에도 이 프레임워크를 사용한 것으로 보인다.

 하단에 나와있는 참고 블로그에서 샘플을 가져와 읽어보자.

```swift
// 하나의 컨테이너를 만든다. (싱글톤이나 AppDelegate에서 만들어 앱 전체에서 사용한다.)
let container = Container()

// register는 등록
container.register(SplashViewModel.self) { r in SplashViewModel() }
container.register(LoginViewModel.self) { r in LoginViewModel() }
container.register(SignUpViewModel.self) { r in SignUpViewModel() }

// resolve는 사용
container.register(SplashViewController.self) { r in
      let controller = SplashViewController()
      controller.viewModel = r.resolve(SplashViewModel.self)
      return controller
    }
container.register(LoginViewController.self) { r in
  let controller = LoginViewController()
  controller.viewModel = r.resolve(LoginViewModel.self)
  return controller
}
container.register(SignUpViewController.self) { r in
  let controller = SignUpViewController()
  controller.viewModel = r.resolve(SignUpViewModel.self)
  return controller
}

// viewController resolve in AppDelegate.swift
self.window?.rootViewController = container.resolve(SplashViewController.self)
```

 내용을 살펴보면 register를 통해서 등록을 하고 resolve를 사용해 생성해 사용한다. 지금 이 코드를 보면 SplashViewController를 최초의 뷰 컨트롤러로 사용하기 위해서 SplashViewModel의 생성자를 등록하고 그 등록한 ViewModel을 사용해 SplashViewController를 만드는 방법을 등록한 모습을 확인 할 수 있다.

이제 SplashViewController를 만들 때 필요한 ViewModel을 외부에서 만들어 넣을 수 있기 때문에 DI를 준수하면서 동시에 등록 후 사용할 때 Init 과정을 몰라도 넘어갈 수 있게 된다. 지금 이 경우 SplashViewController는 한번만 쓰일 것으로 보이기 때문에 크게 와닿지 않지만, 여러 군데서 사용하는 경우와 만약에 누군가 이 화면을 수정해야 한다면 쉽게 수정이 가능한 장점이 있게 된다.

---

 이 정도가 일반적으로 DI와 Swinject에 대해서 찾아보면 나오는 단순한 사용법이다. 근데 회사에서는 이 부분에 대해서 더욱 깊게 사용하고 있고 개념적으로 고려해야 할 부분도 더욱 많다.

 내가 특히 이해하기 힘들었던 부분은 **의존성 분리** 부분이다. 의존성을 주입하기 위해서 각각의 의존을 분리시켜야 한다. 상위 계층이 하위 계층을 의존하는 상황을 반전 시켜 하위 계층의 구현으로부터 독립 시켜야 한다.

 간단한 방법으로 Interface를 만들어 Swinject를 사용할 때 SplahViewController를 등록해 사용하는 것이 아니라 SplahViewController의 필요 요소를 구현한 Interface를 만들어 이를 키값으로 사용해야 한다.

### 참고 자료:

* [Swinject로 DI(Dependency Injection)패턴 적용하기](https://ontheswift.tistory.com/m/18)
* [[DI] Dependency Injection 이란?](https://medium.com/@jang.wangsu/di-dependency-injection-%EC%9D%B4%EB%9E%80-1b12fdefec4f)