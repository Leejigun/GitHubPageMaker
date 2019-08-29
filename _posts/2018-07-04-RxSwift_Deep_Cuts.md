---
layout: post
current: post
navigation: True
title:  "RxSwift: Deep Cuts (번역)"
date:   2018-07-04 00:00:01
cover: assets/images/RxSwift/Deep_Cuts.png
description: RxSwift Deep Cuts 번역
tags: [ RxSwift ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---

# RxSwift: Deep Cuts

 지난 몇년간, 반응형 프로그래밍 아이디어들은 iOS커뮤니티를 사로잡았습니다. 조금 열기가 가라앉은 지금, 우리는 때때로 혼란스럽고 읽을 수 없는 코드를 접하기 시작하고 있습니다. 하지만 이러한 중대한 책임을 어떻게 감당할 수 있을까요? 제 강연에서 이 질문에 대답하도록 하겠습니다.



##Introduction

 제 이름은 Kr.estof Siejkowski입니다. 이 프로그램에서는 한번 더 집중적인 프로그래밍에 대해 설명하겠습니다. 이 강연의 주제는 우리가 이 강연에 참여하고 있는 그 순간을 얼마나 잘 알지에 관한 것입니다.

 이 이야기는 한 디버깅과 세가지 중요한 질문에 대한 이야기입니다.

 알렉스, 우리 이야기의 주인공을 만나 봅시다. 알렉스는 인기 있는 앱을 개발하는 iOS개발자입니다. 그는 지역 사회의 동향을 예의 주시하고, 최신의 훌륭한 도구를 사용하며, 항상 최고의 해결책을 찾습니다.

 모바일 개발 컨퍼런스에서 연설자는 비동기식 코드를 통일된 방식으로 쓰는 더 나은 방법으로 반응형 프로그래밍을 제안했습니다. 반응형 프로그래밍은 타겟 액션, 완료 블록, 델리게이트 등과 같은 패턴보다 관측 가능하고 유지하기 쉽고 설득하기 쉽습니다.

 알렉스는 이 패러다임이 신선하고 매력적이라는 것을 알았고, 팀 전체가 아키텍처의 핵심으로 한 단계 도약하기로 합의했습니다. 다시 로드 버튼을 누르면 액티비티 인디케이터가 무한 회전하는 버그가 보고되기 전까지는 모든 작업이 순조롭게 진행되었습니다.

 제 생각에, 이것은 반응적인 프로그래밍을 사용할 때 가장 흔히 발생하는 버그의 종류입니다. 데이터가 제대로 전달되지 않기 때문입니다.

알렉스는 신선한 논리를 다루는 데에 책임이 있는 코드를 재빨리 찾았다.

```swift
dataProvider.refreshData()
	.subscribe(
		onNext: { [weak self] in
			self!?update(with: $0)
		},
		onError: { [weak self] in
			if let error = $0 as? ReasonableError {
				self!?showUserMessage(with: error.reason)
			}
		}
	)
	.disposed(by: disposeBag)
```

 첫째, `refreshData` 메서드는` dataProvide` 서비스에서 호출되며, 새로 고침 데이터를 방출하는 `Observable` 을 반환합니다. 우리는 이벤트들이 어떻게 소비되는지를 규정하는 두개의 클로져를 제공함으로써 관찰할 있는 이벤트를 구독한다. 모든 작업이 성공하면 새 데이터를 사용하여 업데이트 메소드를 호출합니다. 실패할 경우 지역화된 오류메시지가 생성됩니다.

 이와 같은 기본적인 문제의 원인은 무엇입니까?

첫째, 알렉스는 이벤트가 도착하는 시점에 구독 마감 안에 `self ` 가 nil인지 물었다. 만일 그렇다면, 업데이트는 아무것도 일어나지 않을 것이다.



## What References Does the Observable Carry?

 이것에 대답하기 위해서, `Observable`을 만들고 구독할 때 후드 아래에서 무슨 일이 일어나는지 고려해 보세요. 첫째, 개체는 메모리에 할당되며, 타입은 `Observable` 의 서브 클래스입니다.

 여기서는 단순 개체가 이벤트의 소스이며 이벤트의 흐름은 연산자를 추가하여 형성됩니다. 여기서는 `map` 과 `filter`입니다. 각 계층은 그것의 종류에 따라 다른 `Observable` 인스턴스이며, 각각의 인스턴스는 이전의 것에 대한 참조를 유지한다. 함께, 그들은 사슬을 만듭니다.

 클라이언트의 관점에서 보면 알 수 있듯 가장 바깥쪽에 `Observable<String>` 을 생성하고 내부는 완전히 숨겨집니다.

```swift
let observable: Observable<String> = Observable.just(42)
	.filter {$0>30}
	.map {"\($0)"}
	.distinctUntilChanged {
        $0 == $1
	}
```

 사용되는 연산자들 ( `filter`, `map`, `distinctUnitlChanged` )은 매개 변수로 클로저를 취하고 클로져 내부에서 사용되는 참조 변수들을 저장합니다.



```swift
let observable: Observable<String> = Observable.just(42)
	.filter {$0>30}
	.map {"\($0)"}
	.distinctUntilChanged {
        $0 == $1
	}
	.subscribe {
        print($0)
	}
```

 `Observable` 객체를 구독하면 새로운 객체의 스탭이 생깁니다. 이러한 스탭을 싱크라고 합니다. 각각의 싱크에서는 넘어오는 이벤트를 수행하는데 필요한 로직이 들어있습니다.

 이 로직을 수행하려면 싱크에 필요한 도구가 있어야 합니다. 예를 들어 `filter` 연산자에 의해서 `filter sink` 가 생성되었다면 이를 수행하기 위해서 필터 클로져가 필요합니다. 따라서 싱크 객체에 클로져가 전달되어야 한다는 것을 의미합니다.

 또한 구독하는 순간 `dispose` 가능한 디스포져들이 생성되는데 이 때 디스포져는 또 싱크를 참조하고 있기 때문에 `Observable` 을 생성하고 구독하는 과정에 참조 사이클이 복잡하게 생성되어 무기한 참조를 하게 됩니다.

 이 무기한 참조를 해제하기 위해 `dispose` 를 호출해야 합니다. 그 순간 싱크에 대한 참조가 없어지고 싱크는 또 클로져에 대한 참조가 없어집니다.



## Memory Management Bugs

RxSwift API에는 메모리 관리 관련 버그를 쉽게 만들 수있는 두 가지 속성이 있습니다.

- 그것은 많은 참조가있는 클로저를 광범위하게 사용합니다.
- 구독은 자체적으로 유지됩니다. 결과적으로 싱크 처리기와 싱크 사이의 참조주기가 포함됩니다.

RxSwift에서 제대로 할당이 해제되지 않으면 메모리 누수가 생깁니다.

다행히도 RxSwift를 사용한 반응형 프로그래밍에서 메모리 관련 버그가 발생할 가능성을 최소화하기위한 세 가지 간단한 규칙이 있습니다.

### 1. Dispose Your Subscriptions

 항상 구독을 수행 후 처리해야 합니다. 처분 방법은 특정 상황에 따라 달라집니다.

### 2. Watch Your References

 가능하다면 `strong` 참조나 `closure`  를 피해야합니다. 특히 자기 자신에 대한 강한 참조를 피해야합니다.

### 3. Take Care with Instance Methods

인스턴스 객체를 매개변수로 전달하지 말아야 합니다.



```swift
dataProvider.refreshData()
	.subscribe(
		onNext: { [weak self] in
			self?.update(with: $0)
		},
		onError: { [weak self] in
			if let error = $0 as? ReasonableError {
				self?.showUserMessage(with: error.reason)
			}
		}
	)
	.disposed(by: disposeBag)
```

  `self?` 를 통해서 참조 여부를 확인하고 `[weak self]` 를 통해서 클로져를 약한 참조로 유지하게 된다.



## Call UI from Main Thread

 Alex는 또한 버그가 스레딩 문제라고 생각했습니다. 결국 업데이트 메소드가 일부 백그라운드 스레드에서 UI 요소를 호출하면 이상하고 정의되지 않은 동작이 발생할 수 있습니다. 가끔 충돌하거나 때로는 결함이 생길 수 있습니다.

 관찰 가능한 스트림의 특정 부분이 어떤 스레드에서 실행되는지 알아내는 몇 가지 간단한 규칙이 있습니다.

### How Schedulers Work

 먼저 RxSwift에서 스케줄러 개념을 빠르게 새로 고쳐 봅시다. 스케줄러는 특정 컨텍스트에서 작업을 수행하는 다양한 방법에 대한 추상화입니다. 스케줄러는 어디서, 언제, 어떻게 작업이 실행될 것인지를 정의합니다. 컨텍스트를 수행하는 작업의 일부로 많은 것을 볼 수 있습니다. 이것은 기본 스케줄러의 프로토콜입니다.

```swift
func schedule<StateType>(
	_ state: StateType,
	action: @escaping (StateType) !- Disposable
) !- Disposable
```

 그것은 인수로 `_state`하고 `action` 를 취합니다. 그리고 그것은 스케줄러가 언제 어디서 무엇을 할지 결정합니다.

 당신이 커스텀 스케줄러를 만들면 그것은 계속 동작하지 않을 수 있다. 그러나 실제로 스케줄러는 스레딩 및 대기열, 작업 대기열 및 디스패치 대기열과 같은 Cocoa API의 기존 메커니즘에 대한 래퍼로 가장 많이 사용됩니다.

몇 가지 예를 살펴 보겠습니다. 은 `MainScheduler`메인 큐에 작업을 실행하기위한 것입니다 :

```swift
let mainQueue = DispatchQueue.main

// simplified essence of schedule method
if DispatchQueue.isMain {
	action(state)
} else {
	mainQueue.async {
		action(state)
	}
}
```

 먼저 메인 큐에 있는지 여부를 확인합니다. 그렇다면 바로 일을 처리합니다. 그리고 그렇지 않은 경우에는 `.async`메소드를 사용하여 수행 할 작업을 기본 대기열로 전달합니다.



 직렬 스케줄러 `DispatchQueue` 에서 수행하는 것은 매우 유사하지만 메인 큐가 아니여도 동작합니다.

```swift
// internal serial dispatch queue of given properties
let queue = DispatchQueue.global(qos: qos.qosClass)

// simplified essence of schedule method
queue.async {
	action(state)
}
```

 내부적으로는 이니셜 라이저에서 클라이언트가 제공 한 매개 변수를 사용하여 직렬 대기열을 만든 다음이 `.async`방법을 사용하여 수행 할 작업을 항상이 대기열에 전달합니다.

`OperationQueue`스케줄러도 매우 비슷하게 사용합니다. 당신은 `BlockOperation` 에 작업을 추가합니다.

```swift
// operation queue provided by client in the initializer
let operationQueue: OperationQueue

// simplified essence of schedule method
operationQueue.addOperation(
	BlockOperation {
		action(state))
	}
)
```

 RxSwift에는 많은 다른 스케줄러가 정의되어 있지만 개념은 같습니다. 예를 들어, 일부는 지연된 방식으로 작업을 실행할 수 있고 다른 작업은 반복적으로 수행 할 수 있습니다.



### Operators and Schedulers

 스케줄러를 만들 때 전달해야하는 연산자들이 있습니다. 스케줄러로 수행하는 작업은 실제 연산자에 따라 다릅니다.

```swift
interval(1, scheduler)

delay(2, scheduler)

throttle(3, scheduler)
```

 다른 연산자는 스케줄러에 독립적입니다. 작업 실행 컨텍스트에 대한 정보를 전달하지 않습니다.

```swift
map { foo($0) }

flatMap { bar($0) }

filter { $0 != wanted }
```

 마지막으로, 스케줄러의 동작을 정의하는 연산자가 있습니다.

```swift
observeOn(scheduler)

subscribeOn(scheduler)
```



예를들어 스케쥴러에 의존하지 않는 관측자로만 구성되는 관찰 대상이 있다고 가정합니다.

```swift
Observable
	.just(42)
	.filter { $0 > 33 }
	.map { "\($0)" }
	.subscribe { print($0) }
	.disposed(by: disposeBag)
```

 이 연산자 체인에는 실행 컨텍스트에 대한 정보가 없습니다. 따로 정의된 컨텍스트가 없기 때문에 `subscribe` 메소드가 호출 된 스레드에서 모든 작업이 실행됩니다. 왜냐하면 이것이 유일한 스레드이기 때문입니다.

 하지만 `observeOn`연산자 를 사용하여 변경할 수 있습니다 . 그것은 어떤 스케줄러가 모든 연산자의 실행을 위해 사용될 것인지를 정의합니다. `observable`은 이벤트 시퀀스이므로 항상 단일 `observeOn`스레드입니다.

```swift
Observable
	.just(42)
	.observeOn(greenScheduler)
	.filter { $0 > 33 }
	.map { "\($0)" }
	.subscribe { print($0) }
	.disposed(by: disposeBag)
```

 `observeOn`호출 위의 연산자 는 여전히 구독한 스레드에서 실행되고 있습니다. 따라서 이동 `observeOn` 연산자 이후의 경우에만 적용되며 이전에는 적용되지 않습니다. 원하는만큼의 `observeOn` 을 사용할 수 있습니다 . 하지만 `observeOn` 을 사용하는 경우 첫 번째 실행 컨텍스트 인 생성 스레드를 변경할 수 없습니다.

 그를 위해서 또 다른 연산자 `subscribeOn`가있다. 이 연산자는 구독이 실행될 스케줄러를 지정합니다.  모든 이벤트의 생성은 구독 로직의 일부이며 초기 스케줄러 또는 첫 번째 실행 컨텍스트를 정의합니다.

 이벤트 생성은 단일 단계이므로 여러 번 길을 따라 변경하는 것은 의미가 없습니다. 따라서 첫 번째  `subscribeOn`호출 만 중요하며 다른 호출은 무시됩니다. 또한 생성자를 생성 연산자로 명시 적으로 제공하는 커스텀 스케줄러를 사용한다면 스케줄러가 이미 정의되었으므로 늦은 호출이 무시됩니다.

```swift
Observable
	.just( 42, scheduler: blueScheduler)			//blueScheduler
	.observeOn(greenScheduler)						//greenScheduler
	.filter { $0 > 33 }								//greenScheduler
	.observeOn( redScheduler )						//redScheduler
	.subscribeOn( redScheduler )					//redScheduler
	.map { "\($0)" }								//redScheduler
	.observeOn( greenScheduler )					//greenScheduler
	.subscribe { print($0) }						//greenScheduler
	.disposed(by: disposeBag)
```

*  `.subscribeOn( redScheduler )` 을 통해 red로 스케줄러를 지정하고 있지만, 생성자에서 스케줄러를 blue로 지정하고 있기 때문에 무시된다.
* `.observeOn` 을 통해서 스케줄러가 변경되는 순간부터는 그 스케줄러에서 이후 연산자가 수행된다.



## What is the Protocol?

 이벤트가 관찰자에게 전달되지 않을 수있는 많은 방법이 있습니다. 구독이 이벤트가 생성되기 전에 끝나거나 생성 논리의 구현에 버그가 있거나 관찰 가능한 스트림이 이벤트 클래스를 필터링하는 방식으로 정의되어 전파되지 않을 수 있습니다.

`observable`은 일련의 이벤트를 생성하며, 각 시퀀스가 유지해야하는 기본적인 요구 사항 집합이 있습니다. 항상 0 개 이상의 `next`이벤트 로 구성되며 시퀀스를 닫는 이벤트, 즉 시퀀스의 마지막 요소는 `completed`또는 중 하나 `error`입니다.

```swift
.next(data)
.completed
.error(error)
```

 매우 기본적인 질문 중 하나는 이벤트의 순서가 끝날 것인가하는 것입니다. 그리고 그것이 끝나면 우리는 절대적으로 100 % 확신 할 것이며, 우리는 메모리 관리를 무시할 수 있습니다. 다음은 관찰 가능 항목에 의해 방출 된 완료 또는 오류 이벤트가 있기 때문에 구독이 종료된다는 것을 증명하는 몇 가지 예제 코드입니다.

```swift
let disposable = observable
	.subscribe(onNext: { [weak self] in
		self!?work(on: $0)
	})

// ensure subscription disposed
disposable.dispose()
disposable.disposed(by: disposeBag)
```

 우리의 일은 구독이 폐기 될 것임을 보증하는 것입니다. 따라서 관찰 가능 프로토콜의 통신 프로토콜이 실제로 완료되었거나 완료되지 않은 경우 실제로 우리가 일회용 객체를 사용하는지 여부를 정의합니다.



 긴 시퀀스 인 경우 다중 이벤트가 발생한다는 것을 의미하므로 데이터를 사용자에게 푸시하는 관찰 가능한 작업 일 수 있습니다. 그런 다음 한 번만 구독하고 앞으로 적절한 순간에 정보가 제공 될 것으로 기대합니다.

```swift
let disposeBag = DisposeBag()

// call only once in the object lifetime
func listenForFreshData() {
	observable
		.subscribe(onNext: { [unowned self] in
			self.work(on: $0)
	})
	.disposed(by: disposeBag)
}
```



## Exposing Communication Protocols

 숨겨진 통신 프로토콜의 미로에서 길을 잃지 않게하려면 어떻게해야합니까? 가장 좋은 방법은 그들에게 빛을 비추는 것이고, 그것을하는 방법은 여러 가지가 있습니다.

 먼저 유형 시스템에서 프로토콜을 노출합니다. 이것은 RxSwift와 RxCocoa가 이미하는 것입니다. RxCocoa에는 통신 프로토콜의 속성을 유지하는 많은 특성이 있습니다. 예를 들어, `Driver`, `Signal`, `ControlProperty ` 입니다.

 **핵심** RxSwift 라이브러리 에는 더 많은 특성이 있습니다. 예를 들어,가 `Single`, `Completable`, `Maybe`, 등 종류. 이러한 유형의 모든 목적은 통신 프로토콜에 대한 정보를 공개하는 것입니다 (예 : 전송되는 이벤트 수, 완료 여부).

 프로토콜을 훨씬 이해하기 쉽게 만들 때마다 특성을 사용합니다. 그러나 때로는 상황에 맞는 특성이 없습니다. 이러한 경우 사용자가 직접 래퍼를 작성할 수 있습니다. 또는 문서에서 일반적인 오래된 주석을 사용하여 다른 개발자가 관찰 할 수있는 프로토콜을 설명 할 수 있습니다. (사용 목적과 쓰임을 명시)

예를 들어, 관찰 할 수있는 복잡한 도메인 논리가 있습니다.

```swift
/*
Returns an Observable that emits at most three times,
starting with the first event emitted immediately
and synchronously upon subscription.
Times of other two events are not guaranteed.
May not complete, but never errors out.
Doesn’t cache any data.
*/

public func thirdTimeLucky() !- Observable<Data>

```

## Use Conventions

 대용량 응용 프로그램과 큰 팀에서 작업 할 때 종종 통신 프로토콜과 같이 개발되는 일반적인 패턴과 규칙이 있습니다.

 예를 들어, 다음은 뷰 모델에 대한 데이터를 제공하는 서비스의 일부입니다.

```swift
final class DataProvider {

private let proxySubject = PublishSubject<Data>()

var data: Observable<Data> {
	return proxySubject.asObservable()
}

func refreshData() !- Observable<Void> {
	return networkService
		.requestData()
		.do(onNext: { proxySubject.onNext($0) }
		.map { _ in }
	}
}
```

 이 `refreshData`방법은 데이터를 제공하지 않습니다. 새로 고침이 발생했는지 알려주고 새로 고침이 성공했는지 또는 오류가 발생했는지 알려줍니다.



## Code Distance

 프로토콜을 다루는 마지막 방법은 프로토콜에서 변경이나 특성의 영향을받는 위치의 수가 제한되도록 관찰 가능 범위를 제한하는 것입니다. 이것은 버그의 가능성을 제한합니다.

 범위를 제한 할 때 매우 유용하다고 생각한 개념이 하나 있습니다. 이 개념을 **코드 거리**라고합니다. 코드에 액션이있을 때 액션이 어떤 반응을 일으키는 거리가 중요합니다. 즉, 관계와 연결이 지역적인지 또는 개념적으로 관련이없는 것이 서로 영향을 줄 수 있는지를 보여줍니다.

 나는 앱 아키텍처 측면에서 실제 코드 거리를 생각하고 싶다. 따라서 네트워크 레이어의 변경 사항이 지속성 또는 뷰 모델의 어느 곳에도 표시되지 않지만 뷰 레이어에 영향을 주면 여기에는 긴 코드 거리 관계가 있음을 의미합니다.

 내가 싫어하는 한 가지 패턴이 [`NotificationCenter`](https://davidnix.io/post/stop-using-nsnotificationcenter/)있습니다. 이 긴 코드 거리 관계에 있습니다!

 그러나 어떤 레이어의 변경 사항이 근처의 어딘가에서 볼 수 있다면 로직이 짧은 코드 거리로 유지된다는 의미입니다. 예를 들어, 네트워크 계층에서 관찰 가능한 프로토콜의 변경이 서비스 계층 또는 지속성 계층에 영향을 주면 코드 거리가 짧음을 나타냅니다.

 엄지 손가락의 규칙은 가능한 한 작은 범위에서 관찰 가능을 유지하는 것입니다. 왜냐하면 이벤트의 원인, 보장 및 이벤트의 속성, 이벤트에 의해 생성되는 효과에 대해 추론하는 데 도움이되기 때문입니다.



## Conclusion

 그동안 Alex는 버그의 출처를 발견하고 수정했습니다! 문제는 `onError`종결에있었습니다. 코드 거리와 매우 밀접하게 관련되어 있습니다. 네트워크 서비스에서 작업 할 때 팀원 중 한 명은 던진 모든 오류가 해당 `ReasonableError`유형과 일치하는지 확인하는 것을 잊었습니다 . 사실 구독 코드에 아무런 문제가 없었습니다.

```swift
dataProvider.refreshData()
	.observeOn(MainScheduler.instance)
	.subscribe(
		onNext: { [unowned self] in
			self.update(with: $0)
		},
	onError: { [unowned self] in
		if let error = $0 as? ReasonableError {
			self.showUserMessage(with: error.reason)
		}
	}
)
.disposed(by: disposeBag)
```
