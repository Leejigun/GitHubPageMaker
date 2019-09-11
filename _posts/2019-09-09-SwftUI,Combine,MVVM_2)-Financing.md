---
layout: post
current: post
navigation: True
title:  "SwiftUI, Combine, MVVM 2) - Financing UI"
date:   2019-09-09 00:00:01
cover: assets/images/SwiftUI/Financing_App_Volume_1.png
description: SwuftUI MVVM을 적용해보자
tags: [ swiftui ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---
# SwiftUI, Combine, MVVM 1) - Financing MVVM을 중점으로

 저번 [포스트](https://leejigun.github.io/SwftUI,Combine,MVVM_1)-Financing)에서 SwiftUI를 사용해 예제 디자인의 절반 정도 화면을 만들어보고 State를 이용해 MVVM viewModel을 만들어봤다. 사실 저번에 만든 viewModel은 MVVM 아키텍처를 구체화했다고 하기 뭐할 정도로 형편없었다.
 이번 포스트에서는 저번에 만들었던 View Model을 조금씩 개선해 나가려 한다.


##  기존의 View Model
```swift
    class MainContentsViewModel: BindableObject {
        var willChange = PassthroughSubject<Void, Never>()

        private var totalCards = [HomeCardInfo(),
                                  HomeCardInfo(),
                                  HomeCardInfo(),
                                  HomeCardInfo()]

        /// 상단 벨 아이콘에 배찌 표시 여부
        var isNew = true {
            didSet {
                willChange.send()
            }
        }
        /// 사용자 금액
        var userMoney = "0.00"
        /// 사용자 등급
        var userGrade = "Premium"
        /// 전체 보기 여부
        var isSeeAll = false {
            didSet {
                if !self.isSeeAll {
                    myCards = Array(totalCards[0...1])
                } else {
                    myCards = totalCards
                }
                willChange.send()
            }
        }
        /// 화면에 표시할 카드 모델
        var myCards = [HomeCardInfo(),HomeCardInfo()]
    }
```
 저번 포스트에서 만들었던 뷰 모델입니다. 간단하게 isSeeAll에 대한 로직이 붙어 있는데 예전에 제가 올렸던 MVVM 포스트를 확인해보면 확연히 다른 것을 아실 수 있을 겁니다. MVVM 아키텍처 패턴은 단순히 로직과 뷰를 분리하는데 끝나는 게 아니라 기존에 MVC 패턴에 있었던 뷰와 모델이 직접적으로 영향을 주고받는 개발 오류를 방지하기 위해서 엄격하게 Input과 Output을 구분하여 구조를 잡는다.
하지만 위에서 만든 뷰 모델은 isSeeAll이라는 변수가 화면을 구성하는데 영향을 줌과 동시에 이벤트를 받아 값을 바꾸는 행위도 동시에 수행하고 있다. 따라서 먼저 Input과 Output을 구분하는 작업을 먼저 해야 한다.


##  전통적인 형태의 MVVM

MVVM에 대해서 찾아보면 일반적으로 많이들 사용하는 형태와 패턴이 있다. 나 역시 그 방법으로 사용해 왔고 번거로운 부분도 있지만 크게 불편함 없이 사용해 왔다. 특히 유지 보수, 갑작스러운 기획 변경 등 코드를 수정해야 하는 일이 생기면 크게 도움이 됐다.

 예전 MVVM 포스트에서 소개했던 View Model 프로토콜입니다. 프로토콜 자체는 인터넷에 찾아보면 유사한 내용을 많이 봤을거라 생각합니다. 저도 예전에 어디서 보고 쓰기 시작한 프로토콜 입니다. 제가 현업에서 사용하고 있는 형태는 여기서 이것 저것 조금 추가된 형태지만 MVVM 자체는 이 형태와 동일합니다.

```swift
    protocol ViewModelProtocol {
        associatedtype Input
        associatedtype Output
        var intput: Input { get set}
        var output: Output { get set }
    }
```
 이제 이 MVVM 프로토콜을 적용해 봅시다. 뷰 모델에 프로토콜을 추가하면 다음과 같은 형태입니다.

```swift
     class MainContentsViewModel: BindableObject, ViewModelProtocol {
        struct Input {}
        struct Output {}

        var intput: MainContentsViewModel.Input
        var output: MainContentsViewModel.Output
        var willChange = PassthroughSubject<Void, Never>()

        init() {
            self.intput = Input()
            self.output = Output()
        }
    }
```
이제 기존에 있던 화면을 구성하는데 영향을 주었던 변수들을 Output에 추가합니다.

```swift
    struct Output {
      /// 상단 벨 아이콘에 배찌 표시 여부
      var isNew = true
      /// 사용자 금액
      var userMoney = "0.00"
      /// 사용자 등급
      var userGrade = "Premium"
      /// 전체 보기 여부
      var isSeeAll = false
      /// 화면에 표시할 카드 모델
      var myCards = [HomeCardInfo(),HomeCardInfo()]
    }
```
output을 정의했으면 이제 Input을 정의해야 한다. 여기서 Input은 무엇이 있을까?


-  상단 벨 아이콘을 클릭
-  전체 보기 버튼을 클릭

 이제 여기서 Input 이벤트를 처리하기 위해서 Combine 프레임워크를 사용해보겠습니다. 기존 프로젝트와 예전 포스트에서는 RxSwift를 사용해서 비동기 이벤트를 처리했었는데 여기서는 Combine 프레임워크를 사용해 보겠습니다.
 RxSwift에서 이런 이벤트가 있을 때 ReplaySubject<Void>로 변수를 만들어 사용했었는데, Combine에서 역시 똑같습니다. Subject로 검색하면 PassthroughSubject 와 CurrentValueSubject가 있습니다. 만약 데이터를 저장하는 기능을 같이 사용한다면 CurrentValueSubject를 사용하겠지만 여기서는 그냥 이벤트가 발생했음을 알려주기만 하면 되기 때문에 PassthroughSubject를 사용하겠습니다.

 이렇게 정의된 Input은 다음과 같습니다.
```swift
    struct Input {
      var onTapBellIcon = PassthroughSubject<Void, Never>()
      var onTapSellAllBtn = PassthroughSubject<Void, Never>()
    }
```
 여기에 이벤트를 바라보는 로직을 연결하면 됩니다.
```swift
    init() {
      self.intput = Input()
      self.output = Output()

      self.intput.onTapBellIcon.sink {[weak self] _ in
          self?.output.isNew.toggle()
          self?.willChange.send()
      }
      self.intput.onTapSellAllBtn.sink {[weak self] _ in
          self?.output.isSeeAll.toggle()

          if let cards = self?.totalCards {
              if self?.output.isSeeAll ?? false {
                  self?.output.myCards = cards
              } else {
                  self?.output.myCards = Array(cards[0...1])
              }
          } else {
              self?.output.myCards = []
          }
          self?.willChange.send()
      }
    }
```
 근데 여기서 문제가 발생합니다.


![](https://paper-attachments.dropbox.com/s_9D46B0BB6082816C529AC0B391139222D8C05D93D867FD65E51C17DF10D62FCC_1568103378866_image.png)


 RxSwift를 사용해보면 아시겠지만 Subscribe까지 내려오는 이벤트의 로직은 그 로직의 크기만큼 메모리를 차지하게 됩니다. RxSwift의 경우에는 단순하게 DisposeBag에 넣어두면 그 변수가 초기화 되면서 잡혀있던 모든 오퍼레이션 메모리가 해제됩니다. Combine에서는 어떻게 처리해야 할까요? RxSwift에서는 Subscribe 혹은 Bind에서 반환되는 리턴값은 Disposeable입니다. 쉽게 말해서 해제될 수 있는 로직의 변수라고 볼 수 있습니다. 이걸 변수로 잡고 있다가 메모리에서 해제하거나 Dispose 메소드를 수행하면 메모리에서 로직이 제거되면서 더 이상 동작하지 않습니다.
 Combine에서도 동일하게 Cancellable이라는 변수에 담을 수 있습니다.

```swift
    var onTapBellCancellable: Cancellable?
    var onTapSeeAllCancellable: Cancellable?

    ...

    self.onTapBellCancellable = self.intput.onTapBellIcon.sink {[weak self] _ in
      self?.output.isNew.toggle()
      self?.willChange.send()
    }

    self.onTapSeeAllCancellable = self.intput.onTapSellAllBtn.sink {[weak self] _ in
      self?.output.isSeeAll.toggle()

      if let cards = self?.totalCards {
          if self?.output.isSeeAll ?? false {
              self?.output.myCards = cards
          } else {
              self?.output.myCards = Array(cards[0...1])
          }
      } else {
          self?.output.myCards = []
      }
      self?.willChange.send()
    }
```
 그런데 모든 로직마다 Cancellable 변수를 만들어 관리하는 것은 너무 번거롭습니다. Cancellable을 따로 따로 cancel할 용도가 아니라면 따로 RxSwift에서처럼 관리하고 싶습니다.
 심플하게 배열로 만들면 해결됩니다.

```swift
    var cancellableBag: [Cancellable] = []
      ...

    let onTapBellCancellable = self.intput.onTapBellIcon.sink {[weak self] _ in
        self?.output.isNew.toggle()
        self?.willChange.send()
    }
    let onTapSeeAllCancellable = self.intput.onTapSellAllBtn.sink {[weak self] _ in
        self?.output.isSeeAll.toggle()

        if let cards = self?.totalCards {
            if self?.output.isSeeAll ?? false {
                self?.output.myCards = cards
            } else {
                self?.output.myCards = Array(cards[0...1])
            }
        } else {
            self?.output.myCards = []
        }
        self?.willChange.send()
    }
    self.cancellableBag.append(onTapBellCancellable)
    self.cancellableBag.append(onTapSeeAllCancellable)
```
 이렇게 하면 ViewModel이 메모리에서 해제될 때 같이 메모리에서 모든 로직이 함께 메모리에서 해제됩니다. 이렇게 하면 거의 RxSwift와 차이가 없습니다.

 로직은 동일한데 이대로 적용하려고 하면 할 수 없습니다. 앞서 MainContentsView에서 ObjectBinding으로 뷰 모델을 잡고 있었습니다. 그래서 self.$viewModel.isNew로 하면 문제 없었던 것이 이제 output.isNew로 불가능합니다.

```swift
     @ObjectBinding var viewModel = MainContentsViewModel()
```
 우리가 BindableObject로 만든 것은 MainContentsViewModel로 뷰 모델의 내부 데이터가 변경되면 찾을 수 있지만 그 하단에 있는 Output의 내부가 변경된 것 까지는 알 수 없는 모양입니다.

조금 수정해서 Ouput을 BindableObject로 수정해줍니다. 이렇게 하고 화면에 연결해주면 문제 없이 동작합니다.

```swift
    class Output: BindableObject {

      var willChange = PassthroughSubject<Void, Never>()

      /// 상단 벨 아이콘에 배찌 표시 여부
      var isNew = true
      /// 사용자 금액
      var userMoney = "0.00"
      /// 사용자 등급
      var userGrade = "Premium"
      /// 전체 보기 여부
      var isSeeAll = false
      /// 화면에 표시할 카드 모델
      var myCards = [HomeCardInfo(),HomeCardInfo()]
    }
```

## Bloc 패턴

 이제까지 일반적인 MVVM 형태로 수정했습니다. 이렇게 입력, 로직, 출력을 파트별로 분리해서 사용해봤습니다. 이렇게 하면 장점이 로직 부분을 분리하게 되서 기존의 라이브러리나 코드를 재사용할 수 있다는 점이 있습니다.
 그런데 여기까지 오면 구조가 Flutter에서 사용했던 Bloc 패턴과 많이 유사합니다. 왜 Flutter는 Bloc 패턴이 대세가 되었을까요? 다음 포스트에서는 Flutter에서 사용하는 Bloc 패턴에 대해서 알아보고 지금의 구조를 Bloc으로 변경해보겠습니다.
