---
layout: post
current: post
navigation: True
title:  "RxSwift MVVM 실무 적용"
date:   2019-08-27 00:00:01
cover: assets/images/RxSwift/RxSwift_MVVM_Title.png
description: RxSwift Deep Cuts 번역
tags: [ RxSwift ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---
# RxSwift MVVM 실무 적용
 최근 외부 프로젝트를 진행하면서 RxSwift와 MVVM 아키텍처를 사용했습니다. 여러 라이브러리를 사용하고 다양한 방법들을 시도한 도전적인 프로젝트였는데 RxSwift와 MVVM을 사용하면서 수행했던 실제 적용 사례를 소개하려 합니다.


## Protocol 정의 작업

 처음 MVVM 아키텍처에 대해서 여러가지 사용 예제들을 인터넷으로 확인해보니 Protocol을 사용해서 Inputr과 Output을 강제하는 방법을 사용하고 있어서 먼저 프로토콜을 정의했습니다.

```swift
     protocol ViewModelProtocol {
        associatedtype Result
        associatedtype ErrorType
        associatedtype Input
        associatedtype Output
        var input: Input { get }
        var output: Output { get }
        init(provider:OpenitProvider<JuvisAPI>)
    }
```

 이 프로토콜을 정의하고 뷰 모델에서 실제로 사용할 때에는 다음과 같이 사용했습니다.
 아래 내용은 실제로 제가 외부 프로젝트에서 사용한 장바구니 화면을 수정한 것 입니다.

```swift
     class ShoppingBasketViewControllerModel: ViewModelProtocol {
        enum Result {
            case success(Any)
            case fail(ErrorType)
        }

        enum ErrorType {
            case statusCodeError(Int)
            case jsonMappingError(Error)
            case noContent
            case httpError(Error)
        }

        enum CellAction {
            case orderBtnPressed
            case cancelBtnPressed
            case removeItem(ShoppingItem)
            case selectItem(ShoppingItem)
        }

      struct Input {
            let cellAction = ReplaySubject<CellAction>.create(bufferSize: 1)
            /// API Request
            let getBasketList = ReplaySubject<Void>.create(bufferSize: 1)
            // 아이템 제거
            let removeItem = ReplaySubject<ShoppingItem>.create(bufferSize: 1)
        }

        struct Output {
            /// 로딩 여부
            let isLoading = BehaviorRelay<Bool>(value: false)
            let basketList = BehaviorRelay<[ShoppingItem]>(value: [])

            // UI
            /// 상품가
            let productPrice = BehaviorRelay<Int>(value: 0)
            /// 할인가
            let dicsountPrice = BehaviorRelay<Int>(value: 0)
            /// 배송비
            let deliveryCharge = BehaviorRelay<Int>(value: 0)
            /// 총 배송비
            let totalPrice = BehaviorRelay<Int>(value: 0)
        }

        // MARK: - Variable
        var input: ShoppingBasketViewControllerModel.Input
        var output: ShoppingBasketViewControllerModel.Output
        let disposeBag = DisposeBag()

        required init(provider: OpenitProvider<JuvisAPI> = OpenitProvider<JuvisAPI>()) {
            self.input = Input()
            self.output = Output()
            requestBasketList(provider, input: input, output: output)
            bindUI(provider, input: input, output: output)
        }
    }
```
 실제 제가 이번 프로젝트에서 사용한 내용입니다. 상세한 로직은 **requestBasketList , bindUI** 메소드에 있는데, 이번 포스트는 RxSwift와 MVVM에 관한 첫 번째 내용이니 넘어가도록 합니다. **여기서 주의 깊게 봐야 하는 부분은 Input, Output 두 구조체입니다.** MVVM에 익숙하지 않으면 제일 힘든 부분이 Input과 output을 엄격하게 구분해서 구조를 잡는 게 제일 힘들 것입니다.


----------
## 분석

 getBasketList는 말 그대로 장바니에서 표시할 쇼핑 데이터 리스트를 불러오는 부분입니다. 아무 인자값도 필요없기 때문에 ReplaySubject<Void>.create(bufferSize: 1)로 생성해서 사용하고 있습니다.

 뷰 컨트롤러에서 데이터를 불러올 때 이렇게 사용하고 있습니다.

```swift
    # ShoppingBasketViewController
    override func viewDidAppear(_ animated: Bool) {
      super.viewDidAppear(true)
      viewModel?.input.getBasketList.onNext(())
    }
```
 주로 화면에 들어올 때, 갱신이 필요할 경우 등 전체 갱신이 필요할 경우 사용해주면 됩니다.

 다음으로 로직 부분을 살펴봅니다.
```swift
     private func requestBasketList(_ provider: OpenitProvider<JuvisAPI>, input: Input, output: Output) {
            input.getBasketList
                .do(onNext: { _ in output.isLoading.accept(true)})
                .map { _ -> [ShoppingItem] in
                    return appModel.basket
                }
                .map { list -> [ShoppingItem] in
                    list.forEach { $0.selected.accept(false) }
                    return list
                }
                .do(onNext: { _ in output.isLoading.accept(false)})
                .bind(to: output.basketList)
                .disposed(by: disposeBag)
        }
```
**input.getBasketList**에 이벤트가 들어오면 **.do(onNext: { _ in output.isLoading.accept(true)})** 에서 로딩 이벤트를 시작합니다.
 불러오기가 끝날 때 쯤에서 **.do(onNext: { _ in output.isLoading.accept(false)})** 에서 로딩 이벤트를 멈춥니다.
 저는 프로젝트 전반에서 이런직으로 로딩 이벤트를 수행해 왔습니다. 지금은 앱의 서비스 모델 DB에서 데이터를 읽어오지만 실제는 API 통신을 수행할 때 로딩을 시작 종료하며 사용하고 있습니다.
 그리고 output에 있는 저 로딩 객체는 ( **let isLoading = BehaviorRelay<Bool>(value: false)** ) 뷰 컨르롤러에서 subscribe해서 데이터가 변경될 때 마다 로딩 액션을 수행하고 있습니다.

```swift
     /// Loading
        private func bindLoading() {
            guard let viewModel = viewModel else { return }
            viewModel.output.isLoading.subscribe(onNext: {[weak self] isLoading in
                guard let `self` = self else { return }
                if isLoading {
                    self.loadingNode.startLoading(node: self.node)
                } else {
                    self.loadingNode.stopLoading()
                }
            }).disposed(by: disposeBag)
        }
```
 그리고 주목해야 할 부분은 DB에서 꺼낸 ShoppingItme 배열을 다른 Rx 객체에 바로 bind해주는 부분입니다.
```swift
     .bind(to: output.basketList)
```
 basketList에 들어가는 데이터는 **bindUI** 메소드에서 다시 UI로 바로 구성되게 되는데 내용은 아래와 같습니다.

```swift
    private func bindUI(_ provider: OpenitProvider<JuvisAPI>, input: Input, output: Output) {

      input.cellAction
      // 셀 액션 부분
      // ...
      }).disposed(by: disposeBag)

      output.basketList.subscribe(onNext: {[weak self] list in
      // UI 로직 부분
      // ...
      }).disposed(by: disposeBag)

      /// 아이템 제거
      input.removeItem.subscribe(onNext: { item in
      // 아이템 제거 이벤트
      // ...
      }).disposed(by: disposeBag)

      /// 금액 바인딩
      Observable
      .combineLatest(
        // 선택된 상품의 총 금액
         output.productPrice,
        // 할인 금액
         output.dicsountPrice,
        // 배송비
         output.deliveryCharge
      )
      .map { (product, discount, delivery) -> Int in
      return product - discount + delivery
      }.bind(to: output.totalPrice)
      .disposed(by: disposeBag)
    }
```
 전체 코드를 붙여넣으면 너무 길기 때문에 간단히 보면 Input의 데이터를 통해서 output의 데이터를 만들고 그 데이터를 실제 뷰에서 바인드해서 사용하고 있는 형태입니다.
 Rx에 대해서 이해하고 있으신 분들은 이 부분만 봐도 대부분 이해하셨을거 같습니다. UI 로직부분에서 아이템들을 가공해서 **productPrice, dicsountPrice, deliveryCharge** 를 만들고 그 데이터들을 **.combineLatest** 로 묶어서
**totalPrice** 를 생성하고 있습니다.

### 끝으로
 코드를 차근차근 읽어보시면 Input과 Output으로 모든 화면 구성이 끝난다는 것을 아실 수 있을 것입니다. 저는 MVVM을 만들면서 viewController에 변수를 최대한 없게 만드는 데 초점을 두고 구조를 잡았습니다. 처음 시작하시는 분들은 저처럼 헤매시지 않기를 바랍니다.
