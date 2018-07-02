---
layout: post
current: post
navigation: True
title:  "The iOS Testing Manifesto (번역)"
date:   2018-07-02 00:00:01
cover: assets/images/tdd/tdd_cover.png
description: The iOS Testing Manifesto
tags: [ TDD ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---



# The iOS Testing Manifesto(번역)

* https://blog.usejournal.com/the-ios-testing-manifesto-e1bc821cc4c3



 대부분의 엔지니어는 테스트가 훌륭하다는 데 동의합니다. 테스트의 이점에 관한 기사와 블로그는 너무 많아 다 나열할 수 없습니다. 하지만 iOS 개발에서 유닛 테스트를 어떻게 작성해야 합니까?  좋은 유닛 테스트를 만드려면 어떻게 해야합니까? 테스트 할 필요가 있는 것은 무엇입니까?

 iOS개발자들은 유닛 테스트를 잘 작성하지 못하는 것으로 유명합니다. 많은 iOS 개발자들이 유닛 테스트를 사용하고 있지 않습니다.

 몇년 후, 저는 단위 테스트를 대체할 만한 것이 없다는 것을 깨달았습니다. 테스트를 잘 거친 코드를 사용하는 것은 앱 어딘가에 뭔가 크러쉬가 발생할 두려움 없이 변화와 실험을 할 자신감을 준다. 리펙토링 과정에서 문제가 생기거나 새로운 기능이 통합되어 있으면 이전에 구현했던 테스트들이 문제를 알릴 수 있습니다. 가장 중요한 것은, 코드 베이스의 테스트들이 테스트 하는 타겟들의 목적을 설명할 수 있다는 점 입니다.



### Rules For Writing A Good Unit Test

* 각각의 테스트는 **빨라야** 합니다.
* **단위 테스트에 네트워킹이 없습니다.** 단위 테스트에서 네트워킹 이벤트를 수행하면 단위 테스트가 아닙니다!
* **테스트는 독립적이고 격리되어야 한다.** 시험은 다른 시험에 대해서는 상태를 변화시키지 않아야 하며 서로가 종속되어서는 안됩니다. 
* **시험은 반복 가능해야 한다.** 시험을 망치는 것은 그것의 가치보다 더 큰 해를 끼친다. 수정하거나 삭제합니다. 
* **사용자가 제어할 수 없는 종속성이 없습니다.** 시스템 날짜, 표준 시간대 등에 따라 다른 테스트를 수행하지 마십시오. 이러한 테스트는 테스트 제품 군이나 테스트 환경에 있어야 합니다. 믿을 수 없는 데이터는 가까운 미래 날짜에 의존해서는 안 된다.



또한 좋은 테스트는 다음과 같은 형태를 취합니다.

```
// 1
func test_behaviorBeingTested_contextItsTestedUnder() {
    
    // 2
    objectUnderTest.service = SomeMockService()

    // 3
    objectUnderTest.performAction()  

    // 4
    let expected: String = "The expected change"
    let actual: String = objectUnderTest.text

    // 5
    XCTAssertEqual(expected, actual)
}
```

1. **Naming** 모든 테스트는 **test** 라는 단어로 시작해야 합니다. 밑줄은 논리적 그룹을 구분합니다. 두번째 논리적 그룹은 테스트되는 동작이고 세번째 논리적 그룹은 테스트되는 컨텍스트입니다. 컨텍스트에 장점이 있는 경우 네번째 논리 그룹을 추가할 수 있습니다.
2. **Setup** 원하는 상태에서 개체를 테스트하는 데 필요한 종속성을 명시적으로 나열합니다.
3. **Behavior Modification**. 메서드를 호출하거나 테스트 대상 개체의 변경을 발생시키는 값을 설정합니다.
4. **Capturing Changes**. 두 값을 비교할 때는 예상 값과 실제 값을 모두 명시적으로 캡처하십시오. 예상 값을 설정할 때는 가능한 고정 데이터를 사용하십시오.
5. **Assertion** 이것은 클래스의 행동에 대한 우리의 가정과 클래스의 실제 행동에 대해 테스트하는 것입니다.

 테스트가 이런 일정한 형식과 모양을 가지고 있을 때, 후임 개발자들이 테스트의 목표와 등급 기능을 쉽게 파악할 수 있다. 테스트는 흔히 후임 개발자들에게 기능과 대상에 대한 설명서의 한 형태로 사용된다.



## 테스트 중심 개발

 구현 전 또는 구현 중에 테스트를 작성하는 습관을 들이면 처음에는 이상한 느낌이 들 수 있습니다. 많은 iOS개발자들은 TDD가 이런 저런 이유로 인해 작업 흐름의 일부가 아니라고 말합니다. 루비나 JavaScript로 개발하는 사람이 할 수 있는 것과 같은 방식으로 TDD를 연습할 수는 없지만, 그래도 TDD를 해야 합니다.

 우리의 메소드와 클래스를 위한 유닛 시험을 쓸 때, 함수형 프로그래밍을 하는 친구들로부터 TDD의 개념을 빌리고 그리고 그들처럼 함수를 생각해야 합니다.

 우리는 항상 먼저 가장 간단하고 빈 형태의 메소드를 만들고 그것이 실패하는 테스트를 작성하고 테스트가 통과할때 까지 리펙토링을 진행해야 합니다.

```
/* in the production code */
// 1
func text(for trafficLight: TrafficLight) -> String { 
  return String()
}

/* in the test class */
// 2
func test_textForTrafficLight_red() {
  let expected = "Red"
  let actual = text(for: .red) 

  XCTAssertEqual(expected, actual)
}

func test_textForTrafficLight_yellow() {
  let expected = "Yellow"
  let actual = text(for: .yellow) 

  XCTAssertEqual(expected, actual)
}

func test_textForTrafficLight_green() {
  let expected = "Green"
  let actual = text(for: .green) 

  XCTAssertEqual(expected, actual)
}
```

1. 먼저, 완전히 실패할 것으로 예상되는 기본 타입을 반환하는 메소드를 작성했다.
2. 이 메소드에 대한 예상 테스트 사례를 모두 적었다.

 시험을 실제로 시행하고 실패하는 것을 지켜보는 것이 중요합니다. 일단 실패하면, 우리의 모든 시험 케이스가 성공할 때까지 리펙토링을 반복합니다.



#### Writing Tests for Existing Classes With No Tests

 엔지니어로서 우리가 하는 일의 대부분은 새로운 코드를 작성하는 것이 아니라 기존 코드를 유지하고 수정하는 것입니다. 레거시 코드에는 분석하기 쉬운 위험한 작업을 수행할 수 있는 단위 테스트가 없는 경우가 꽤 많습니다. 레거시 파일 또는 유닛 테스트가 없는 파일에서 작업하는 첫번째 단계는 변경될 기존 기능을 대상으로 하는 테스트를 작성하는 것입니다. **즉, 영향을 받는 파일의 기능 하위 집합을 이해하고 현재 동작을 기록하는 테스트를 작성합니다.**

 기존 클래스에 포함되지 않는 테스트를 작성할 때는 테스트를 수정하여 예상한 대로 테스트가 통과하지 못하도록 하여 테스트가 유효한지 다시 확인하는 것이 중요합니다. 만약 우리가 **녹색 테스트**만 쓴다면, 우리는 클래스의 원래 디자인과 의도를 잘 이해하지 못할 것이다. 쉽게 테스트할 수 있도록 원본 클래스의 구현 일부를 수정해야 할 수 있습니다. 종속성 주입을 염두에 두고 작성되지 않았거나 암묵적 의존 테스트 가능성을 위해 원래의 등급을 수정할 때, 우리는 가능한 한 원래 코드를 방해하지 않도록 변경의 수를 최소화하도록 노력해야 한다.

 기존 동작이 문서화되면 표준 TDD흐름을 시작할 수 있습니다.

 애플리케이션이 완전히 또는 대부분 테스트되지 않은 경우, 수정된 부품에 대해 클래스에 테스트를 점진적으로 추가하는 것이 좋습니다.



### Dependency Injection

 일반적으로 클래스를 설계할 때 클래스 내에 있는 속성이 생성자를 통해 전달되도록 클래스를 설정해 보십시오. 생성자가 커지면 개체에 setter를 만드는 것을 허용해야 합니다.

 경험에 비추어 볼 때, 로컬 변수(가급적이면 생성자에서 기본 값 사용)에 대한 생성자 주입과 공용 변수에 대한 설정 주입이 있습니다.

 테스트 가능성을 위해 접근자를 수정하지 마십시오. 프라이빗 변수를 테스트할 때는 참조를 잡고 삽입한 후 내부 상태를 테스트합니다.



### Mocks, Stubs, Fakes, Spies, Dummies

 우리의 테스트를 지역 환경에 격리시키는 것이 중요합니다. 객체에 네트워크 서비스, 딜러 등의 다른 항목에 대한 참조가 있는 경우  해당 개체를 단순화되거나 제어 가능한 버전을 주입하는 것이 중요합니다. 용도가 다른 테스트 개체에는 고유한 이름이 있습니다. 용어 자체는 아이디어만큼 중요하지 않지만, 이러한 개체를 식별하기 위한 일련의 빠른 규칙은 다음과 같습니다.

- **Mocks** 은 그들이 받을 호출을 등록하는 개체입니다.
- **Stubs** 은 미리 정의된 데이터를 보관하고 테스트 중에 호출에 응답하는데 사용하는 개체입니다. 네트워킹을 테스트하는 데 종종 사용됩니다.
- **Fakes** 는 작동하는 구현은 있지만, 실제 타겟과 다른 개체입니다.
- **Spies** 테스트 타겟의 정보를 기록하는 Stubs입니다. 함수가 호출되는 횟수, 전달된 파라미터의 참조를 유지하는 것 등 결과 확인을 위한 데이터를 저장하는데 사용됩니다.
- **Dummies** 는 테스트를 위해서 전달은 되지만 실제로는 사용되지 않는 개체를 의미합니다. 매개 변수 목록만 채우는 경우가 많습니다.



### Model Testing

 모델은 보통 코드를 쓸 때 제일 먼저 시작합니다. 대부분의 프로세싱보다 테스트하기가 쉽습니다. 비교적 독립적 입니다. 다음과 같은 모델에 대한 테스트를 작성하지 않아도 됩니다.

```
struct Card {
    let rank: Rank
    let suit: Suit
}
```

 하지만 모델에 대해서 뮤테이팅 함수, 공용함수, didSet, 프로퍼티 연산 등이 내부에 추가된다면 테스트를 진행해야 합니다. 이런 경우 각각의 모델에 대한 테스트 팩토리를 구현해야 합니다.



#### Model Factories

 모델 팩토리는 테스트를 위해서 변수가 없어도 객체를 만들 수 있습니다.

```
import XCTest 
@testable import MyModule
// 1
enum CardFactory {
    // 2
    static func create(
        rank: Rank = .ace, 
        suit: Suit = .spade
    ) -> Card {
        return Card(rank: rank, suit: suit)
    }
}
```

1. 모델 팩토리는 다른 곳에서 인스턴스로 사용할 수 없게 반드시 enum으로 선언해야 합니다.
2. `create` 메소드는 모델의 생성자에 필요한 인자를 가지고 있어야 합니다.



### View Testing

 뷰를 테스트하는 데는 여러가지 다른 철학들이 있습니다. 대부분의 사람들은 세개의 캠프로 나뉩니다.

1.  xcode에서 제공하는 `XCUITest`를 사용하여 뷰 테스트의 일부를 자동화합니다.
2. iOS 스냅 샷 테스트를 통해서 뷰를 테스트합니다.
3. 유닛 테스트를 작성하고 UI테스트는 잊어 버립니다.



#### 1. XCUITest

XCUITest는 애플의 UI 테스트 프레임워크에 있는 Xcode 테스트입니다. 이것은 UI 테스트 녹화 같은 유용한 기능들을 제공합니다.

안타깝게도 XCUITest는 두가지 테스트 규칙을 준수하지 않습니다.

1. 사용자 정의 테스트로 작성된 UI테스트는 느립니다. 로그인 흐름을 테스트하는 데 최대 10분이 걸릴 수 있습니다.
2. 지원되는 UI테스트를 사용하여 작성한 UI테스트는 손상될 수 있습니다.

이러한 이유로, 자동화된 통합 환경에서 프로젝트를 테스트 하는 것에 적합하지 않습니다.



#### 2. iOS-Snapshot-Test-Case

 스냅 샷 테스트에서는 이중 데이터를 사용하여 일부 코드의 정확성을 확인합니다. 이 경우 스냅 샷 테스트는 iOS 뷰의 스크린 샷을 기록하고 예기치 않게 변경되지 않도록 합니다. 스냅 샷 테스트에 실패하면 검사를 위한 Diffe가 생성됩니다.

 많은 프로젝트에서 [iOS-Snapshot-Test-Case](https://github.com/uber/ios-snapshot-test-case) 를 사용하고 있고 XCUITest와 달리 빠르고 신뢰할 수 있습니다.

```
import FBSnapshotTestCase

// 1
class FBSnapshotTestCaseSwiftTest: FBSnapshotTestCase {

  override func setUp() {
    super.setUp()
    // 2
    recordMode = false
  }

  func testExample() {
    let view = UIView(frame: CGRect(x: 0, y: 0, width: 64, height: 64))
    view.backgroundColor = UIColor.blue

    // 3
    FBSnapshotVerifyView(view)
    FBSnapshotVerifyLayer(view.layer)
  }
}
```

1. 우리는 XCTestCase가 아닌 FBSnapshotTestCase를 import해 사용합니다.
2. 녹화 모드를 설정합니다. 처음 실행할 때 이 값을 true로 설정하면 테스트할 디스크에 참조 이미지가 생성됩니다.
3. 현재 뷰를 기준 이미지에 대해 테스트합니다.

 스냅샷 테스트의 더 자세한 내용은 [여기](https://www.stephencelis.com/2017/09/snapshot-testing-in-swift) 를 참고해주세요.



### Controller Testing

 컨트롤러의 모든 책임을 테스트하는 것이 중요합니다. 본 문서에서는 컨트롤러에 다음과 같은 책임이 있다고 가정합니다.

1. Navigation
2. View presentation
3. Delegate conformance
4. Networking

 네트워킹 또는 네비게이션 같은 책임 중 일부가 다른 개체(예:ViewModel, Interactor)에 위임된 경우에도 이러한 지침이 해당 개체에 적용됩니다.

#### Testing Navigation and View Presentation

 네비게이션을 테스트하려면 UIWindow가 필요하다.

```
/* in the test class */

// 1 
var window: UIWindow!
var controller: MyController!
var navigationController: UINavigationController!

override func setUp() {
  super.setUp()
  controller = MyController()
  // 2
  navigationController = UINavigationController(rootViewController: controller)
  // 3
  window = UIWindow()
  window.rootViewController = controller
  window.makeKeyAndVisible()
}
```

1. 필요한 요소들을 참조할 변수를 생성
2. UINavigation에 푸쉬를 통해서 테스트할 액션 수행
3. UIWindow의 내부 프로퍼티를 통해서 컨트롤러의 계층 구조를 확인



 아래와 같은 방법으로 안정하게 네비게이션 테스트를 진행할 수 있습니다.

```
// Testing Push Navigation
func test_tableViewSelection_displaysCar_whenSelectingCarRow() {
  controller.tableView(controller.tableView, didSelectRowAt: IndexPath(item: 0, section: MyController.Section.cars.rawValue)
  XCTAssert(navigation.viewControllers.last is MyViewController)
}

// Testing Presentation Navigation
func test_carFilterButton_presentsCarFilterView() {
  controller.didSelectFilterButton() 
  XCTAssertNotNil(controller.presentedViewController)
  XCTAssert(controller.presentedViewController is CarFilterView) 
}
```

 만약, 테이뷰나 콜렉션뷰 컨트롤러를 테스트할 필요가 있을 경우 데이터를 외부에서 주입하는게 좋다.



#### Delegate Conformance

 델리게이트를 테스트할 경우 우리는 델리게이트를 통해 수행되는 조치가 수행되었는지 테스트하는데 목적을 둡니다. 이 기능은 다른 기능을 테스트하는 것과 다르지 않아야 합니다. 

```
/* in the controller */
func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
  /* some code to return a configured cell */
}

/* in the test class */ 
func test_cellForRowAt_emptyState() {
  // 1
  let indexPath = IndexPath(item: 0, section: 0)
  let state: MyController.State = .empty
  // 2
  controller.state = state

  // 3
  let actual = controller.tableView(controller.tableView, cellForRowAt: indexPath)

  // 4
  XCTAssert(actual is EmptyTableCell)
}
```

1. 의존성을 선언
2. 이 기능을 호출하거나 컨트롤러가 특정 방식으로 움직이도록 값을 설정
3. 테스트할 값을 탐색
4. 값이 우리가 원하는 결과를 수행된 값이라고 가정하고 비교



#### Testing Networking

 네트워킹을 테스트할 때는 실제로 네트워크에 연결하지 않는다는 점을 기억하는 것이 중요합니다. 네트워킹을 테스트할 때는 Stubs 데이터를 사용해 응답에 대해 작업하는 것이 표준입니다.

```
/* in PersonStub.json */
{
  "name": "Hesham Salman",
  "age": 25
}

/* in test helper */ 
func stubbedResponse(filename: String) -> Data {
    @objc class TestClass: NSObject { }

    let bundle = Bundle(for: TestClass.self)
    guard let path = bundle.path(forResource: filename, ofType: "json"),
        let data = try? Data(contentsOf: URL(fileURLWithPath: path))
        else { XCTFail() }

    return data
}

/* in test class */ 

var controller: MyController!

func test_instantiation() {
  // 1 
  let decoder = JSONDecoder() 
  let data = stubbedResponse(filename: "PersonStub")
  let apiClient = MockApiClient(response: data)

  // 2
  controller = MyController(service: PersonService(apiClient: apiClient))
  // 3
  let expectation = expectation(description: "received data") 

  // 4
  controller.fetchPeople { result in
    // 5
    guard case let .success(response) = result,
    let people = try? decoder.decode([Person].self, from: response.data)
    else { return XCTFail() }

    // 6
    let expectedCount = 1
    let actualCount = people.count
    XCTAsssertEqual(expectedCount, actualCount)

    let expectedState: MyController.State = .results(people)
    let actualState = controller.state
    XCTAssertEqual(expectedState, actualState)

    // 7
    expectation.fulfill()
  }

  // 8
  waitForExpectations(timeout: 1.0, handler: nil)
}
```



### Testing Other Objects

#### Delegates

 델리게이트를 보유하고 있는 클래스에서 델리게이트를 테스트합니다. 예를 들어 아래와 같은 클래스가 있는 경우.

```
protocol NotifierDelegate: class {
  func notifierDidUpdate() 
}

class Notifier {
  weak var delegate: NotifierDelegate? 

  init(delegate: NotifierDelegate) {
    self.delegate = delegate
  }

  func update() {
    /* impl */
    delegate?.notifierDidUpdate()
  }
} 
```



아래와 같은 테스트에서 호출했을 때 델리게이트를 호출하는지 확인하면 됩니다.

```
// 1
class MockNotifierDelegate: NotifierDelegate {
  var didUpdateWasCalled = false
  // 2
  func notifierDidUpdate() {
    didUpdateWasCalled = true
  }
}

/* in test class */ 
var delegate: MockNotifierDelegate!
var notifier: Notifier!

override func setUp() {
  super.setUp()
  delegate = MockNotifierDelegate() 
  notifier = Notifier(delegate: delegate)
}

func test_update_callsDelegateMethod() {
  // 3
  notifier.update()
  // 4
  XCTAssertTrue(delegate.didUpdateWasCalled)
}
```



#### View Models

```
struct CarViewModel {
    private let car: Car

    var titleText: String {
        return NSAttributedString(
            string: "\(car.year) \(car.make) \(car.model)",
            attributes: StyleGuide.Text.header1Attributes(color: StyleGuide.Color.primaryText)
        )
    }

    var subtitleText: String {
        return NSAttributedString(
            string: car.mileage.description,
            attributes: StyleGuide.Text.header3Attributes(color: StyleGuide.Color.secondaryText)
        )
    }

    var image: UIImage { return car.image }
}
```

 이런 경우 입력에 대한 출력이 예상 가능한 값인지 테스트하는 로직이 필요합니다.