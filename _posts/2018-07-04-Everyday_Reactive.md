---
layout: post
current: post
navigation: True
title:  "Everyday Reactive (번역)"
date:   2018-07-04 00:00:00
cover: assets/images/RxSwift/Everyday_Reactive_cover.jpeg
description: Everyday Reactive 번역
tags: [ RxSwift ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---



# Everyday Reactive

* https://academy.realm.io/posts/everyday-reactive/



 이 챕터에서는 일상적인 경험을 바탕으로 앱 개발 과정에서 반응적인 프로그래밍을 실제로 사용하는 방법에 대해 살펴보겠습니다. 우리는 언제 반응적인 프로그래밍이 강력한 도구가 될 수 있는지를 결정하기 위한 팁과 요령, 그리고 코드 품질과 성능을 위협하지 않는 시나리오를 살펴볼 것이다. 이 포스트는 반응적 프로그래밍의 개념에 초점을 맞출 것이며, 이 코드는 다양한 스위프트 반응적 구현을 보여 줄 것입니다.

---

 제 이름은 아그네스입니다. 저는 여러분과 함께 제가 반응적인 프로그래밍을 배우는 동안 알게된 몇가지 팁, 요령, 그리고 피해야 할 것들을 나누려고 합니다.

 저는 Ustream의 iOS개발자입니다. 즉, 사람들이 비디오를 보고방송하는 데 사용하는 앱을 개발하고 있습니다. 또한 수백만명의 사용자에게 앱을 제공하기 때문에 안정적이고 읽기 쉽고 느슨하게 연결된 코드 기반을 유지하여 품질을 높게 유지할 수 있었습니다. 우리는 이를 위해 반응적인 코드를 쓰고 있습니다. 하지만 그렇다고 우리가 반응형 프로그래밍을 성배라고 생각한다는 의미는 아닙니다. 우리는 의도적으로 여러 패러다임을 혼합하고 있으며, 우리는 우리의 코드에서 원하는 수준의 품질을 유지하는 데 도움이 되는 다른 패턴을 사용하고 있습니다.

## Reactive Programming

 비동기 데이터의 문제를 해결함으로써 얻을 수 있는 이점을 살펴보겠습니다.



### Is There A Framework For That?

 iOS에서는 어떤 기술로 반응형 코드를 쓸 수 있을까요? RxSwift, ReactiveCocoa, ReactiveSwift 등 많은 것들이 있습니다.

 이 프레젠테이션에서는 여러가지 다른 프레임워크의 소스 코드를 살펴보겠습니다. 개념이 비슷하기 때문에 한번만 배우면 다른 것들은 익숙하게 대응 할 수 있을 것 입니다.

### When Do I Apply It?

 저희는 우리팀에 언제부터 반응형 프로그래밍을 적용할 것인가 토론했습니다. 저희는 특정한 수준에서는 반응형이 복잡하지만, 어느 시점 이후로는 복잡한 코드를 더 간단하게 만든다고 합니다.

 복잡한 애플리케이션에서 반응형 프로그래밍을 선택했다고 가정해 보겠습니다. 일반적으로 뷰와 뷰 모델 간의 바인딩에 반응적으로 사용하거나 네트워크 요청과 같은 특정 비동기 작업에 대응하는 경우 쉽게 적용할 수 있습니다. 이것을 MVVM이라 할 수 있지만, 뷰와 뷰 모델간의 바인딩 로직이라고 할 수도 있습니다. 이 기능은 비동기 이벤트를 기반으로 상태를 업데이트하기 때문에 쉽게 적용할 수 있습니다. 이 같이 UI 또는 네트워크 비동기 이벤트의 많은 상태 변경 작업이 반응적 프로그래밍이 해결해야 하는 복잡성의 전형적인 예입니다.

### Observation

 반응형 프로그래밍에서 가장 단순하고 일반적으로 사용되는 패턴은 관심 있는 데이터의 흐름을 관찰하는 것입니다.

 우리가 어떻게 특정한 사건의 흐름을 관찰할 수 있는지 봅시다.

```swift
let (signal, observer) = Signal<String, NoError>.pipe()

signal.observeValues { animal in print( "value: \(animal)") }

observer.sendNext(value: "😸")
observer.sendNext(value: "🐰")
```

 여기서 여러분은 ReactiveCocoa의 핵심 개념인 시그널을 볼 수 있습니다. 이는 관찰 가능한 이벤트 스트림을 나타내며, 다음 값 또는 오류, 완료된 이벤트 또는 해당 스트림에서 중단된 이벤트를 채울 수 있습니다. 신호에 새로운 값이 있는 경우 값은 신호를 통해 이동한 다음 관찰 기능한 바디로 들어갑니다.

### Let’s Reduce Some state

 우리의 반응형 프로그래밍으로 다수의 상태를 합쳐 나가는 방법을 알아봅시다.

```swift
var loading: Bool
var userLoggedIn: Bool
var didShowAlert: Bool
```

 여기에는 세가지 플래그가 있습니다. 예를 들어, 어떤 클래스가 API요청의 콜백 또는 특정 UI작업을 기준으로 상태가 변한다고 가정합니다. 우리가 세개의 플레그를 가지고 있을 때, 이 플래그의 상태 변화로 8가지의 상태값을 가질 수 있습니다.

 반응형 프로그래밍을 통해 특정 상태를 관찰할 수 있습니다.

```swift
var loading =
reactive(userLoggedIn) &&
reactive(didShowAlert)
```

### Transform / Combine

 스트림을 변환하거나 결합하면 복잡성을 줄이고 코드를 단순화하는 데 도움이 될 수 있습니다.

```swift
let loading = Observable.combineLatest(userLoggedIn, didLoadContent) {
    !($0 && $1)
}

loading.subscribe(onNext: { print("loading: \($0)") })

userLoggedIn.onNext(false)
didLoadContent.onNext(false)
userLoggedIn.onNext(true)
didLoadContent.onNext(true)

> loading: true
> loading: true
> loading: false
```

 여기서는 두개의 데이터 스트림을 병합할 수 있습니다. 그 이후부터는 결합된 스트림의 요소를 사용하여 작업하게 됩니다. 우리는 두개의 관측치를 결합하고, 둘 다 최신 값을 조합할 수 있는 값을 갖게 되면, 두 값의 최신 값으로 트리거 됩니다. 이것은 스트림을 결합하는 특정 전략이지만 조합할 때 필요한 전략이 다를 수 있으므로 병합과 같은 모든 값을 얻을 수 있는 방법이 있습니다.

### Simplify / Unify Async Operations

 다른 비동기 작업을 반응적 스트림으로 변환할 수 있습니다. 예를 들어 버튼 클릭 이벤트가 있습니다. 이벤트를 결합할 수도 있고 이러한 작업을 체인으로 묶을 수도 있습니다. 즉, 이러한 작업에 응답하거나 IP작업 방법을 정의하고 적절한 동작을 위해 상태를 유지하기 위해 더 이상 특정 메타 데이터가 필요하지 않습니다. 그것들은 사실상 동일한 스트림이며, 당신은 그것들을 서로 결합할 수 있습니다.

```swift
let catButton = UIButton(title: "😸")
let url = URL(string: "http://catfacts-api.appspot.com/api/facts?
number=1")

let catFact = URLSession.shared.rx.json(url:url!)
  .map( { return "\(parsedCatFact($0))" })

Observable.combineLatest(catButton.rx.tap, catFact) { c, fact in
    "\(c) 👉 \(fact)"
  }.subscribe(onNext: { print("\($0)") })


> 😸: Cats can be right-pawed or left-pawed.
```

 여기서는 버튼 클릭과 요청 응답을 결합하여 버튼을 클릭하면 매우 쉽게 이벤트를 알 수 있습니다.



##Trade-offs, Complications

 첫번째 문제는 당신의 호출 스택이 더 이상 당신의 가장 익숙히 사용하던 형태가 아니기 때문에 디버깅 하는데 어려움을 격을 수 있습니다. 최소한 전통적인 필수적인 호출 스택에서 일어났던 것만큼 정확한 이벤트를 알려 줄 수는 없을 것입니다.

```swift
func logAnimals() {
    let animal = MutableProperty<String>("😸")
    let animalStream = animal.producer.logEvents(identifier: "📋")

    animalStream.start()
    animal.value = "🐰"
}

[📋] starting fileName: (...)/A.swift, functionName: logAnimals(), lineNumber: 16
[📋] value 🦊 fileName: (...)/A.swift, functionName: logAnimals(), lineNumber: 16
[📋] started fileName: (...)/A.swift, functionName: logAnimals(), lineNumber: 16
[📋] value
```

 이를 도와줄 트릭이 있습니다. 문제를 일으키는 특정 스트림이 의심스러운 경우 프레임워크의 일부 이벤트 스트림에 콘솔 로그를 첨부하는 방법이 있습니다. 예를 들어, 여기 로그 이벤트가 있습니다. 로그는 스트림의 값이 어디서 발생했는지를 보여 준다. 이 로그는 이미 시간과 골치를 줄여 줄 수 있지만, 당신이 이를 보고 직접 해결해야 하는 어려움은 피할 수 없다.



 두번째 문제는 반응형 프로그래밍을 배우는 단계에서 생깁니다. 사람들이 옵져버 패턴의 힘을 깨닫고 그것을 어디서나 사용하고 싶어 할 때는 괜찮지만, 약간의 상용화 코드를 줄이기 위해서 반응형 프로그래밍을 도입하는 것은 오버 헤드일 수 있다.

 관찰 결과를 사용하여 수동으로 상태를 업데이트하면 반응성을 잃을 수 있습니다. 이미 해당 용도로 반응형 프레임워크를 사용 중인 경우 대신 바인딩을 사용할 수 있습니다.

```swift
viewModel.title.bind(to: titleLabel)
```

 여기서 우리는 뷰 모델의 제목을 레이블에 묶고, 뷰 모델이 새로운 제목을 얻을 때마다 텍스트로 라벨을 업데이트할 것입니다. 만약, 조건 적용이 필요한 경우, 로직에 조건을 추가할 수 있습니다.

 이것은 Bond의 예입니다. 뷰와 뷰모델 사이의 연결을 정의할 때 유용한 단 방향 바인딩 또는 양방향 바인딩을 사용할 수 있습니다. 예를 들어 사용자 입력과 해당 데이터의 모델 표현 방법입니다. 스트림에 사이드 이펙트를 수동으로 주입할 수 있다는 것은 좋은 일입니다. 부작용이 나쁘다고 여겨진다는 사실과 상관 없이, 사이드 이펙트들은 복잡성을 야기한다. 어떤 것이 더 많은 부작용을 가질수록, 한번의 변화 후에 무슨 일이 일어날지 측정하거나 정의하기가 더 어렵습니다.

 만약, 특정 행동의 사이드 이펙트가 필요하다면 추가하고 제거하기 용이합니다. 여기 코드에서는 제목을 라벨과 바인드하기 전, nil 체크를 하는 로직을 추가한 것 입니다.

```swift
viewModel.title.map { n -> Bool in
    return n != nil
}.bind(to: refreshButton.reactive.isEnabled)
```

 다양한 사용 방법들이 존재합니다.

```swift
viewModel.title.bind(to: titleLabel)
viewModel.title
  .bidirectionalBind(to: titleTextField.reactive.bnd_text)
```



  반응형 프로그래밍의 세번째 어려움으로는 뜨거운 옵져버블과 차가운 옵져버블과 같은 다양한 관측 가능성이 있다. cold의 경우 시그널에 사이드 이펙트를 주입하면 해당 시그널에 새로운 가입자가 생길 때마다 효과가 나타납니다. 이것은 좋습니다. 왜냐하면 그것이 의도한 설계 방식이기 때문입니다. 하지만 여러분은 반드시 구현이 어떻게 되어 있는지 상기해야 합니다. 따라서 꼭 필요한 경우에만 사이드 이펙트를 추가해야 합니다. 예를 들어 앱의 사용 추적 기능을 추가하려면 이벤트 스트림에 사이드 이펙트를 추가하는 것이 좋습니다.

```swift
let catFact = URLSession.shared.rx.json(url:url!)
  .map( { return "\(parsedCatFact($0))" })
  .do(onNext: { _ in
      print("EFFECT")
  })

catFact.subscribe(onNext: { print("1. 😸: \($0)") })
catFact.subscribe(onNext: { print("2. 😸: \($0)") })

> EFFECT
> 1. 😸: Most cats adore sardines.
> EFFECT
> 2. 😸: In 1987 cats overtook dogs as the number one pet in America.

...
    .do(onNext: { fact in
        Analytics.trackEvent("cat fact generated: \(fact)")
    })
```

 또한, 사용할 관측 가능성이 로직에 맞는 종류인지 확인해야 합니다. 예를 들어, 버튼 클릭인 경우 뜨거운 시그널이여야 하므로 이 업데이트에 가입한 사용자가 기준이 아니라 아니라 버튼을 누를 때 분석 이벤트를 보내는 것이 좋습니다. 이는 가장 준비하기 어려운 문제입니다. 나중에 변경하기 어려울 수 있기 때문입니다.



 마지막으로 불필요하게 반응형 코드를 강제 될 수 있습니다. (이는 시간이 많이 걸리고 유용하지 않다.)

 반응형 없이도 쉽게 수행할 수 있지만 불필요하게 반응형을 추가 할수 도 있습니다. 이 동작으로 인해 예기치 않은 결과가 발생할 수 있습니다. 하지만 일반적으로 여러분의 상태를 변하지 않게 설계함으로써 쉽게 해결할 수 있습니다.

 또한, 하나의 작은 스위치만으로 복잡한 로직을 수행할 수도 있습니다. 이것은 멋진 일이지만, 단순하게 하는 것이 좋다고 생각합니다. 그렇지 않으면 한가지 변화의 효과는 한 사람이 항상 기억할 수 있는 것보다 더 클 것입니다. 구현된 코드를 잘 이해하지 못한 채 이벤트가 어디서 발생하는지조차 알 수 없는 신입 개발자들은 말할 것도 없습니다.
