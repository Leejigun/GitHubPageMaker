---
layout: post
current: post
title: "[Tayga 개발기] (3) - RxSwift를 통한 Moya 비동기 처리"
date: 2018-06-07 00:00:00
cover: assets/images/tayga/ReactiveX_logo.png
description: RxSwift를 사용해 비동기 데이터 처리.
navigation: True
tags: [ project ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---

저번 포스트에 이어서 Moya 타겟에 실제로 RxSwift를 통해 데이터를 읽어오겠습니다.



 저번 포스트에서 만든 Endpoint로 이루어진 타겟 enum은 실제로는 아무 동작도 하지 않습니다. 그저 타겟 타입들을 정해주는 역할을 수행할 뿐 실제 동작을 위해서는 Provider가 필요합니다.



## MoyaProvider

 시작하기 앞서 GameListViewModel을 만들어줍니다.

 (이 ViewModel은 GameListViewController의 뷰 모델로 게임 리스트를 뿌려줄 로직을 정의하기 위해서 분리되었습니다. API를 통한 데이터 불러오기, 가공 등의 작업을 수행하고 controller에서 화면서 그리는 작업을 수행하도록 하겠습니다.)

```swift
struct GameListViewModel {
	let provider: MoyaProvider<TwitchAPI>
	init() {
        provider = MoyaProvider<TwitchAPI>()
    }
}
```



 Provider를 통해서 네트워크 통신을 수행합니다. 하지만 RxSwift를 사용하기 전에 Moya github에 나와있는 Rx를 사용하지 않는 Provider의 사용법을 먼저 확인해 봅시다.

```swift
provider = MoyaProvider<GitHub>()
provider.request(.zen) { result in
    switch result {
    case let .success(moyaResponse):
        let data = moyaResponse.data
        let statusCode = moyaResponse.statusCode
        // do something with the response data or statusCode
    case let .failure(error):
        // this means there was a network failure - either the request
        // wasn't sent (connectivity), or no response was received (server
        // timed out).  If the server responds with a 4xx or 5xx error, that
        // will be sent as a ".success"-ful response.
    }
}
```

 내용을 살펴보면 우리가 정의한 TwitchAPI enum 타겟과 마찬가지로 Moya의 예제에서는 GitHub라는 타겟을 사전에 정의해 놓고 비동기 컴플리트 클로져를 통해서 완료시 행동을 정의하고 있습니다.



이것을 RxSwift를 쓰면 어떻게 될까요?

```swift
provider = MoyaProvider<GitHub>()
provider.rx.request(.userProfile("ashfurrow")).subscribe { event in
    switch event {
    case let .success(response):
        image = UIImage(data: response.data)
    case let .error(error):
        print(error)
    }
}
```

 위와 별반 다를바 없어보이지만, 그것 호출하자 마자 바로 Subscribe를 바로 수행했기 때문입니다. 여기서 주목해야 할 것은 어떻게 subscribe를 바로 진행 할 수 있었냐는 것 입니다.

 Provider가 수행하는 request 메소드가 앞서 Rx를 사용하지 않을 땐 returen값이 없었지만, Rx를 사용하게되면 Obserable의 return 값이 반환됩니다. 이 값을 비동기적으로 사용이 가능합니다.



## RxSwift 연산자

 이제 제가 만든 게임 리스트 메소드를 봅시다.

```swift
/// get Games Struct from Server
///
/// - Parameters:
///   - limit: count of games
///   - offset: first item position of game list
/// - Returns: GamesStruct
internal func getGameList(limit:Int?,offset: Int?) -> Observable<[GameViewModel]> {
        let param = ["limit": "\(limit ?? self.limit)",
            "offset": "\(offset ?? 0)"]
        return provider.rx.request(.getTopGame(param))
        	.retry(3)
        	.asObservable()
            .map { try JSONDecoder().decode(GamesStruct.self, from: $0.data) }
            .catchErrorJustReturn(nil)
            .map { $0?.top ?? [] }
            .map { $0.enumerated().map { GameViewModel(game: $1, offset: self.offset) } }
}
```

  살펴보기 앞서 GameStruct라는 구조체가 있고, 그 안에 [TopGame] 배열을 가지고 있는 형태입니다. 이 형태는 Twitch에서 내려주는 API 때문이고, JSON 형태에 따라서 바뀔 수 있는 것이기 때문에 중요하지 않습니다.

 하나 하나 뜯어봅시다. provider의 request 메소드는 `PrimitiveSequence<SingleTrait, Response>` 를 반환합니다. 이 반환값을 그냥 구독해서 사용할 수도 있지만, Obserable에 있는 다양한 오퍼레이터를 사용해 사전 가공할 수 있습니다. 오퍼레이터에 대해서는 RxSwift 깃에 자세히 나와있고 여기서는 실제 제가 짠 코드를 뜯어봅시다.

```swift
.retry(3)
```

 Retry의 경우 에러가 발생하면 다시 시도하는 횟수를 지정할 수 있습니다. 여기서는 3회 반복하도록 했습니다.

Rx의 장점인 선언형 프로그래밍을 따라서 윗줄부터 한줄 한줄 뜯어보면 제일 `asObserable()` 은 앞서 리턴값인 시퀀스를 `Observable<>` 형태로 묶어주는 것입니다. 이 부분을 지나면 반환값은 `Observable<Response>`  형태가 됩니다.



  이 JSON Data를 GameStruct구조체에 담는 동작이 두번째 줄에서 벌어지는 동작입니다.

```swift
.map { try JSONDecoder().decode(GamesStruct.self, from: $0.data) }
```

 JSONDecoder를 사용해 디코딩 하는 방법은 Codable을 이용해 인코딩, 디코딩을 수행하는 방법입니다. 이에 대한 포스트는 ios tip 섹션에 설명해 놓겠습니다.

 try 를 보면 알겠지만, 이 메소드는 실패시 Error를 발생시킵니다. 이 메소드를 사용할 때에는 try {} catch {} 문과 함께 사용해야 하는데요. 여기서보면 그저 .map {} 오퍼레이터만을 사용하고 있습니다.

([map](http://rxmarbles.com/#map)은 이벤트를 다른 이벤트로 변환하는 역할을 수행합니다. `Obserable<Response>` 이벤트가 `Obserable<GamesStruct>` 이벤트로 바뀌는 용도로 사용했습니다.)

 만약, 여기서 실패해서 error를 만들게 된다면, `Obserable<Error>`가 반환됩니다.



 다음줄을 살펴봅시다.

```swift
.catchErrorJustReturn(nil)
```

 오퍼레이터 이름을 보면 알겠지만, 단순하게 에러가 발생하면 특정 값을 리턴하도록 하는 오퍼레이터입니다. 만약, 데이터 형태가 잘못되었거나, 서버에서 거부되는 등 에러가 발생하였을 때, 그에 따라 다른 처리도 가능하지만, 여기서는 그냥 return nil을 하도록 했습니다. 만약, 기본값이 있다면 기본 형태의 데이터를 반환하면 됩니다.

 이 오퍼레이터를 추가했기 때문에 이제 반환값은 nil일 수도 있는 `Observable<GameStruct?>` 입니다.



```swift
.map { $0?.top ?? [] }
```

다음줄은 이 GmaeStruct안에 있는 `let top: [TopGame]` 을 꺼내는 동작입니다. 앞서 말했듯이 이 map으로 들어오는 값은 `Observable<GameStruct?>` 형태로 옵셔널 값이기 때문에 만약 nil이면 빈 배열을 반환하게 됩니다.



```swift
.map { $0.enumerated().map { GameViewModel(game: $1, offset: self.offset) } }
```

 이제` [TopGame]` 배열의 요소를 하나 하나 꺼내서 `[GameViewModel]` 배열로 만드는 작업입니다. 이 부분을 다 수행하면 반환되는 값은 `Observable<[GameViewModel]>` 형태가 됩니다.

(만약, 앞서 디코딩 부분에서 에러가 발생했다면 빈 배열이 내려왔을 것이고 여기서도 map을 통해 연산했지만 빈 배열이 리턴될 것입니다.)

이제 이 값을 구독하면 데이터를 확인 할 수 있습니다.

```swift
func loadData() {
    getGameList(limit:10,offset: 0)
    	.subscribe(onNext: {
            print($0)
        }).disposed(by: disposeBag)
}
```



## Multithreading

 여기까지 크게 복잡한 로직은 아니지만, Moya와 RxSwift를 사용해 비동기 통신과 데이터 가공 로직을 살펴봤습니다. 여기서 로직을 확인해 보면, 네트워킹 이후 데이터를 파싱하고 가공하는 반복되는 동작을 수행합니다. 만약, 데이터 양이 많고 로직이 복잡하다면 충분히 많은 시간을 소요할 것으로 보입니다.

 따라서, 여기에 멀티 스레딩을 적용해서 데이터를 가져와 파싱하는 동작을 워커 스레드에서 수행하도록 해봅시다. Rx에서 멀티 스레딩을 할 때 알아야 할 오퍼레이터는 `observeOn()` 과` subscribeOn()` 입니다.

 ` subscribeOn()` 은 최초 Observable이 동작하는 스케줄러를 지정합니다. 만약, 모든 동작이 백그라운드 스레드에서만 동작하면 충분할 경우 `` subscribeOn()``  만 사용해 구현 가능합니다. `observeOn()` 은 중간에 흐름을 바꿀 때 사용합니다. `observeOn` 을 반복해서 사용해서 메인 스레드와 백그라운드 스레드를 왔다갔다 할 수 있습니다.

RxSwift 문서를 살펴보면 4가지 스케줄러가 나와있습니다.

## MainScheduler (Serial scheduler)

Abstracts work that needs to be performed on `MainThread`. In case `schedule` methods are called from main thread, it will perform the action immediately without scheduling.

This scheduler is usually used to perform UI work.

## SerialDispatchQueueScheduler (Serial scheduler)

Abstracts the work that needs to be performed on a specific `dispatch_queue_t`. It will make sure that even if a concurrent dispatch queue is passed, it's transformed into a serial one.

Serial schedulers enable certain optimizations for `observeOn`.

The main scheduler is an instance of `SerialDispatchQueueScheduler`.

## ConcurrentDispatchQueueScheduler (Concurrent scheduler)

Abstracts the work that needs to be performed on a specific `dispatch_queue_t`. You can also pass a serial dispatch queue, it shouldn't cause any problems.

This scheduler is suitable when some work needs to be performed in the background.

## OperationQueueScheduler (Concurrent scheduler)

Abstracts the work that needs to be performed on a specific `NSOperationQueue`.

This scheduler is suitable for cases when there is some bigger chunk of work that needs to be performed in the background and you want to fine tune concurrent processing using `maxConcurrentOperationCount`.



 스케줄러의 이름들을 보면 시리얼과 컨커런트로 나눌 수 있습니다. 시리얼은 직렬 큐 작업 큐를 만들어 동작을 수행하고, 컨커런트는 병렬로 작업 큐를 만들어 동시 수행합니다. 이해하기 쉽게 하기 위해서 간단하게 설명된 [예문](https://stackoverflow.com/questions/19179358/concurrent-vs-serial-queues-in-gcd)을 가져왔습니다.

- async - concurrent: 코드는 백그라운드에서 동작합니다. 제어는 즉각적으로 메인 스레드로 돌아오며 UI를 업데이트 할 수 있습니다. 이 때 실행중인 코드 블럭은 현재 이 큐에서 실행중인 유일한 블록임을 장담할 수 없습니다. 작업은 큐 순서대로 수행되지만, 다른 워커 스레드가 생긴다면 아직 다른 작업이 수행중이더라도 큐의 다음 블럭을 수행하도록 넘겨 줄 수 있습니다.
- async - serial: 코드는 백그라운드에서 동작합니다. 제어는 즉각적으로 메인 스레드로 돌아오며 UI를 업데이트 할 수 있습니다. 이 때 다른 스레드가 있더라고 이 큐의 코드는 한번에 하나의 블럭에서만 수행됩니다. 앞의 블럭이 끝나야 다음 블럭이 수행될 수 있습니다.
- sync - concurrent: 코드는 백그라운드에서 수행되지만, 메인 스레드는 작업이 완료될 때 까지 기다립니다. UI를 업데이트 할 수 없습니다. 작업은 큐 순서대로 수행되지만, 다른 워커 스레드가 생긴다면 아직 다른 작업이 수행중이더라도 큐의 다음 블럭을 수행하도록 넘겨 줄 수 있습니다.
- sync - serial: 코드는 백그라운드에서 수행되지만, 메인 스레드는 작업이 완료될 때 까지 기다립니다. UI를 업데이트 할 수 없습니다. 이 때 다른 스레드가 있더라고 이 큐의 코드는 한번에 하나의 블럭에서만 수행됩니다. 앞의 블럭이 끝나야 다음 블럭이 수행될 수 있습니다.

 Serial은 싱글 스레드, concurrent는 멀티 스레드 방식으로 큐의 작업들을 수행합니다. GCD에 대한 설명 링크들을 추가합니다.

* https://m.blog.naver.com/PostView.nhn?blogId=itperson&logNo=220915666962&proxyReferer=https%3A%2F%2Fwww.google.co.kr%2F
* https://brunch.co.kr/@tilltue/29



 다시 RxSwift로 돌아와 문서 내용을 읽어보면 친절하게 `MainScheduler` 는 UI 작업에 적합하고 `Concurrent Dispatch QueueScheduler` 는 백그라운드 작업을 수행할 때 사용하라고 달려있습니다.

```swift
return provider.rx.request(.getTopGame(param))
        	.retry(3)
        	.asObservable()
            .map { try JSONDecoder().decode(GamesStruct.self, from: $0.data) }
            .catchErrorJustReturn(nil)
            .map { $0?.top ?? [] }
            .map { $0.enumerated().map { GameViewModel(game: $1, offset: self.offset) } }
```

 기존에 사용했던 메소드입니다.

 ` SubscribeOn` 은 어디서 `Observable` 시작할 것인지, `ObserveOn()` 은 중간에 흐름을 바꿀 때 사용합니다. 그렇다면 여기서 모든 동작을 백그라운드에서 수행하도록 하겠습니다.

```swift
return provider.rx.request(.getTopGame(param))
        	.retry(3)
        	.observeOn(ConcurrentDispatchQueueScheduler(qos: .background))
        	.asObservable()
            .map { try JSONDecoder().decode(GamesStruct.self, from: $0.data) }
            .catchErrorJustReturn(nil)
            .map { $0?.top ?? [] }
            .map { $0.enumerated().map { GameViewModel(game: $1, offset: self.offset) } }
```

 간단하게 한줄 추가하는 것으로 백그라운드 작업을 가능하게 했습니다. 만약, 데이터를 가져오고 그 후 UI 작업을 수행하게 된다면, 흐름을 바꿔줘야 합니다.

```swift
func loadData() {
    getGameList(limit:10,offset: 0)
    	.observeOn(MainScheduler.instance)
    	.subscribe(onNext: {
            /// UI 작업
        }).disposed(by: disposeBag)
}
```

 앞서 RxSwift 문서에 나와있듯이 UI 작업을 하기 위해서 `MainScheduler` 를 사용했습니다. 만약, 굳이 UI 작업이 없다면 전부 백그라운드에서 수행해도 문제 없습니다.
