---
layout: post
current: post
navigation: True
title:  "WWDC22 Swift 제네릭 활용 - some, any"
date:   2023-03-04 00:00:00
cover: assets/images/ios/2023-03-04-WWDC22_Generic/2023-03-04_02-26-02.jpeg
description: WWDC22 Swift 제네릭 활용 - some, any
tags: [ ios ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---

# WWDC22 Swift 제네릭 활용 - some, any

제네릭은 Swift에서 추상 코드를 작성하는 기본 도구로, 코드가 진화할수록 복잡성을 관리하는 데 매우 중요합니다. 추상화는 아이디어를 구체적인 세부 사항과 구분하는데 유용하게 쓰입니다. 코드에는 추상화가 유용하게 쓰이는 여러 가지 방법이 있습니다. 

 코드를 함수나 로컬 변수로 인수분해하는 것은 추상화의 한 가지 형태입니다. 이렇게 하면 기능이나 값을 여러 번 사용해야 할 때 매우 편리합니다. 기능을 함수로 추출하면 세부 정보가 추상화되며, 이를 사용하는 코드는 세부 정보를 반복하지 않고 현재 일어나고 있는 일에 대한 아이디어를 표현할 수 있습니다.

```swift
let startRadians = startAngle * .pi/180.0
let endRadians = endAngle * .pi/180.0

func radians(angle: Double) -> Double {
    return angle * .pi / 180.0
}
```

 Swift에서는 구체적인 유형을 추상화할 수 있습니다. 동일한 아이디어의 다른 세부 정보를 가지는 유형 집합이 있을 때, 추상 코드를 작성하여 모든 구체적인 유형과 함께 작업할 수 있습니다. 이번 포스트에서는 구체적인 유형을 사용하여 코드를 모델링하고, 일련의 유형의 공통 기능을 식별하고, 이러한 기능을 나타내는 인터페이스를 구축하며, 해당 인터페이스를 사용하여 제네릭 코드를 작성하는 워크플로를 살펴보겠습니다.

```swift
<T> where T: Idea
```

## Model with concrrete types (구체적인 타입을 사용하는 경우)

Swift의 추상화 도구에 대해 자세히 알아보고 농장 시뮬레이션을 위한 코드를 구축해 보겠습니다.

먼저, '소'라는 구조체로 시작합니다.

'소' 구조체에는 건초 유형의 매개 변수를 허용하는 '먹기'라는 메서드가 있습니다. 

건초는 또 다른 구조체인데, 이 구조체는 건초를 생산하는 작물인 알팔파를 재배하기 위한 정적 메서드 '키우기'를 가지고 있습니다. 

알팔파 구조체에는 알팔파 인스턴스에서 건초를 수확하는 메서드가 있습니다.

마지막으로, '농장'이라는 구조체를 추가하겠습니다. 이 구조체는 소에게 먹이를 주는 메서드를 가지고 있습니다.

```swift
struct Cow {
	func eat(_ food: Hay) {...}
}

struct Hay {
	static func grow() -> Alfalfa {...}
}

struct Alfalfa {
	func harves() -> Hay {...}
}

struct Farm {
	func feed(_ animal: Cow) {...}
}
```

먹이 주기 메서드는 먼저 건초를 생산하는 알팔파를 재배하고, 건초를 수확한 다음 마지막으로 소에게 건초를 먹이는 방식으로 구현할 수 있습니다.

```swift
struct Farm {
	func feed(_ animal: Cow) {
		let alfalfa = Hay.grow()
		let haty = alfalfa.harvest()
		animal.eat(hay)
	}
}
```

이제는 농장에서 소에게 먹이를 주는 것이 가능합니다. 하지만 저는 동물 유형을 더 추가하고 싶습니다. 말이나 닭과 같은 다른 동물을 나타내는 구조체를 더 많이 추가할 수 있습니다. 농장에서는 소, 말, 닭에게 먹이를 주려고 합니다.

```swift
struct Cow {}
struct Horse {}
struct Chicken {}
```

먹이 주기 메서드를 각 매개 변수 유형별로 개별적으로 받아들일 수도 있지만, 매우 비슷한 구현이 존재할 것입니다. 이 구현은 더 많은 동물을 추가할수록 반복적일 것이며, 보일러플레이트가 될 가능성이 높습니다.

```swift
struct Farm {
	func feed(_ animal: Cow) {}
	func feed(_ animal: Horse) {}
	func feed(_ animal: Chicken) {}
}
```

## Identify common capabilities (공통적인 기능을 식별)

다음 단계는 동물 유형 간의 공통적인 기능을 식별하는 것입니다. 우리는 모두 특정 유형의 먹이를 먹을 수 있는 동물 유형의 집합을 구축했습니다. 각 동물 유형은 먹는 방법이 다를 것이고, 따라서 먹기 메서드의 각 구현은 행동에서 차이가 있을 것입니다. 우리는 여기서 추상 코드가 먹기 메서드를 호출하도록 허용하고, 추상 코드가 작동하는 구체적인 유형에 따라 다르게 동작하도록 구축하려고 합니다.

```swift
struct Cow {
	func eat(_ food: Hay) {...}
}
struct Horse {
	func eat(_ food: Hay) {...}
}
struct Chicken {
	func eat(_ food: Hay) {...}
}
```

다양한 구체적인 유형에 대해 추상 코드가 다르게 동작하는 능력을 '다형성'이라고 합니다. 이를 통해 코드 한 개는 사용되는 방식에 따라 여러 가지 동작을 가질 수 있습니다. 적절하게도, 다형성은 다양한 형태로 나타납니다.

- Overloads achieve `Ad-hoc polymoriphism`: 함수 오버로딩을 사용해 다형성을 구현하는 방법으로 앞서 Farm에 같은 이름인 feed 함수를 오버로드해 3가지 함수로 만든 것을 의미합니다.
- Subtypes achieve `subtypes polymoriphism`: 슈퍼 유형에서 작동하는 코드는 런타임 시 코드가 사용하는 특정 하위 유형에 따라 다른 동작을 가질 수 있습니다.
- Generics achieve `parametric polymoriphism`: 제네릭을 사용하여 달성되는 매개 변수 다형성도 있습니다. 제네릭 코드는 유형 매개 변수를 사용하여 서로 다른 유형으로 작동하는 하나의 코드를 작성할 수 있으며, 구체적인 유형 자체가 인수로 사용됩니다.

함수 오버로딩을 통한 다형성은 위에서 살펴봤기 때문에 하위 유형 다형성을 살펴보겠습니다.

하위 유형 관계를 나타내는 한 가지 방법은 클래스 계층을 사용하는 것입니다. 우리는 '동물'이라는 클래스를 도입할 수 있습니다. 다음으로 각 동물 유형을 구조체에서 클래스로 바꿉니다. 각 특정 동물 클래스는 동물 슈퍼 클래스로부터 상속되며 먹기 메서드를 재정의합니다. 이제 추상적인 기본 클래스 동물이 있습니다. 이를 통해 모든 특정 동물 유형을 나타낼 수 있습니다. 동물 클래스에서 먹기를 호출하는 코드는 하위 유형 다형성을 사용해 하위 클래스 구현을 호출합니다. 

```swift
class Animal<Food> {
	func eat(_ food: Food) { fatalError("subclass must implement 'eat'") }
}

class Cow: Animal<Hay> {
	override func eat(_ food: Hay) {...}
}
class Horse: Animal<Carrot> {
	override eat(_ food: Carrot) {...}
}
class Chicken: Animal<Grain> {
	override eat(_ food: Grain) {...}
}
```

여기 한 가지 문제가 있는데, `Food`는 분명 `Animal` 클래스를 구현하는 데 필요한 제네릭 파라미터입니다. 하지만 이렇게 하나씩 제네릭 파라미터를 추가하면 제네릭을 사용하는 의미가 없어집니다.

```swift
class Animal<Food, Habitat, Commodity> {
	func eat(_ food: Food) { fatalError("subclass must implement 'eat'") }
}
...
class Chicken: Animal<Grain, Coop, Egg> {
	override eat(_ food: Grain) {...}
}
```

## Build an interface

 근본적인 문제는 클래스가 데이터 유형이라는 것입니다. 우리는 기능의 작동 방식에 대한 세부 정보 없이 유형의 기능을 나타내도록 설계된 언어 구조를 원합니다. 동물들에게는 두 가지 공통 기능이 있습니다. 

- 각 동물에게는 특정 먹이 유형
- 그 음식 중 일부를 소비하는 작업

Swift에서는 프로토콜을 사용하여 이를 수행합니다. 프로토콜은 추상화 도구로 적합한 유형의 기능을 설명합니다. 프로토콜을 사용하여 유형이 수행하는 작업에 대한 아이디어를 구현하고, 세부 정보와 분리할 수 있습니다. 유형이 수행하는 작업에 대한 아이디어는 인터페이스를 통해 표현됩니다. 

```swift
protocol Animal {
	associatedtype Feed: AnimalFeed
	func eat(_ food: Feed)
}

struct Cow: Animal {
	func eat(_ food: Hay) {...}
}
struct Horse: Animal {
	func eat(_ food: Hay) {...}
}
struct Chicken: Animal {
	func eat(_ food: Hay) {...}
}
```

먼저, 제네릭 파라미터로 사용하던 타입을 `associatedtype` 키워드를 사용해 지정할 수 있습니다. 이는 프로토콜에서 플레이스 홀더 역할을 합니다. eat 메소드에서 앞서 선언한 `associatedtype Feed`를 자동으로 파라미터 타입에 매핑할 수 있습니다.

프로토콜은 클래스뿐만 아니라 구조체와 열거형에서도 사용할 수 있습니다. 또한 해당 메소드를 구현했는지 컴파일 타임에 알 수 있습니다.

## Write generic code

이전에 `Farm`에서는 다양한 타입 (`Cow`, `Horse`, `Chicken` 등)을 받는 feed 함수를 오버로딩하여 다형성을 구현했습니다. 그러나 `Animal`이라는 프로토콜로 통합함으로써, 이제는 제네릭을 사용할 수 있게 되었습니다.

제네릭에 타입을 지정하는 방법은 2가지가 있습니다. 파라미터 선언 부분에서 타입을 지정하는 것과 `where`을 사용하여 타입을 지정하는 것입니다.

```swift
protocol Animal {
	associatedtype Feed: AnimalFeed
	func eat(_ food: Feed)
}

// case 1
struct Farm {
	func feed<A: Animal>(_ animal: A) {...}
}

// case 2
struct Farm {
	func feed<A>(_ animal: A) where A: Animal {...}
}
```

`where` 절을 사용하는 경우 메소드가 실제보다 더 복잡해보일 수 있다는 단점이 있습니다. 제네릭 패턴에서 `where` 절을 사용하는 것은 일반적으로 많이 사용되지만, 더 쉽게 표현할 수 있는 방법이 있습니다.

```swift
func feed<A>(_ animal: A) where A: Animal
```

"`some`" 키워드를 사용하는 방법도 있습니다. 이 방법은 이전에 사용하던 `where`절이나 제네릭 파라미터를 사용하는 방법과 유사하지만, 더 간단합니다.

```swift
func feed(_ animal: some Animal)
```

 

`some` 키워드는 불투명 타입을 나타내는데 사용되는데, 키워드 '`some`'은 해당 타입에 subtype이 있다는 것을 의미합니다. 이 경우, `some` 타입은 `Animal` 프로토콜을 반드시 준수해야 하며, 매개변수 타입으로 `Animal`을 직접 사용할 수 있게 됩니다. SwiftUI를 사용하면 '`some View`' 타입이 나타나는데, 이는 `View`의 서브타입이 사용될 수 있다는 것을 의미합니다.

```swift
some Aniaml

// swiftUI에서의 some
var body: some View {...}
```

구체적인 타입을 나타내는 기본유형과 마찬가지로 불투명 유형은 Return Type으로도 사용될 수 있는데,

```swift
<A: Animal>
some Animal

func getValue(Parameter) -> Result
```

로컬 변수에 불투명 유형을 사용하는 경우 오른쪽의 값으로 타입을 결정한다. 따라서 불투명 유형의 로컬 변수는 항상 초기값을 가져야 한다. 이를 제공하지 않으면 컴파일러가 에러를 발생시킨다. 

```swift
let animal: some Animal = Horse()
```

`some` 키워드를 사용하는 불투명 타입은 실행 시 반드시 기본 유형이 고정되기 때문에 이후 변경하려고 하면 에러가 발생한다.

```swift
var animal: some Animal = Horse()
animal = Chicken()
```

불투명 타입의 함수의 경우 해당 함수를 호출해 파라미터로 특정 기본 유형을 넘겨줄 때 타입이 추론된다. 파라미터에 `some` 키워드가 사용되는 것은 swift 5.7의 신기능이다. `some` 매개변수를 가진 함수의 타입 추론은 함수를 실행 할 때 추론되기 때문에 다양한 기본유형을 사용할 수 있다.

```swift
func feed(_ animal: some Animal)
feed(Horse())
feed(Chicken())
```

불투명 유형을 파라미터로 받는 경우와는 달리 반환값으로 불투명 유형을 사용하는 경우, 반환값의 타입을 런타임에 결정할 수 없습니다. 즉, 모든 호출에서 반환 타입이 동일해야 합니다. 따라서 아래와 같은 경우 에러가 발생합니다.

```swift
func makeView(for farm: Farm) -> some View {
	if condition {
		return FarmView(farm)
	} else {
		return EmptyView()
	}
}
```

불투명한 SwiftUI 뷰의 경우 `ViewBuilder DSL`은 제어 흐름 구문을 변환하여 각 분기에서 동일한 기본 반환 유형을 갖도록 할 수 있습니다. 따라서 `View Builder DSL`을 사용하여 이 문제를 해결할 수 있습니다.

메서드에 `@ViewBuilder` 주석을 작성하고 반환 구문을 제거하면 `ViewBuilder` 유형별로 결과를 빌드할 수 있습니다.

```swift
@ViewBuilder
func makeView(for farm: Farm) -> some View {
	if condition {
		FarmView(farm)
	} else {
		EmptyView()
	}
}
```

### **불투명 유형을 여러번 참조해야 하는 경우**

지금까지 불투명 타입의 `some`에 대해서 알아봤습니다.

다시 농장 시뮬레이션 쪽 코드로 돌아가서, 불투명 타입을 여러번 참조해야 하는 경우 `associatedtype`을 유용하게 사용할 수 있습니다.

`Farm`에 `buildHome` 메소드를 추가하고 무엇인지 알 수 없는 `Animal`을 받아 그 `Animal`의 `Habitat`(서식지)를 만들도록 하는 함수를 가정해봅시다. 이 `Habitat` 값 역시 `Feed`와 마찬가지로 동물의 유형에 따라서 달라지기 때문에 `associatedtype`을 통해서 구체적으로 정하지 않고 추상화 할 수 있습니다.

```swift
protocol Animal {
    associatedtype Feed: AnimalFeed
    associatedtype Habitat
    
    func eat(_ food: Feed)
}

struct Farm {
    
    func feed(_ animal: some Animal) { ... }
    func buildHome<A>(for animal: A) -> A.Habitat where A: Animal { ... }
}
```

불투명 유형을 여러 번 참조해야 할 때 `associatedtype` 말고도 쓰기 좋은 방법은 제네릭을 활용하는 것입니다. 아래의 `Silo`를 보면 제네릭 변수로 `Material`을 선언하고, 내부 변수와 `생성자`에서 매개변수로 여러 번 반복해서 사용했습니다. 또한 해당 Silo를 사용할 때는 꺽쇠 괄호 안에 항상 불투명 유형에 대한 **구체적인 이름을 지정**해야 합니다.

```swift
struct Silo<Material> {
    private var storage: [Material]
    
    init(storing materials: [Material]) {
        self.storage = materials
    }
}

var hayStorage: Silo<Hay>
```

불투명 타입을 사용해 만든 `feed`를 구현하고 살펴보겠습니다. `feed` 함수의 목적은 무엇인지 알 수 없는 animal 을 받아서 해당 **animal의 알맞은 Feed를 만들어 eat 함수를 호출하는 것 입니다.**

1. `type(of:)` 메소드를 통해서 불투명 타입의 `Animal`의 타입에 접근 할 수 있습니다. 아래의 경우 `Cow`를 넣었으니 `Cow` 타입을 얻을 수 있습니다.
2. 그리고 해당 Cow 타입의 `associatedtype Feed` 값인 `Hay(목초)` 에 접근 할 수 있습니다.
3. 모든 `Feed` 타입은 `AnimalFeed` 프로토콜을 채택하고 있고, 거기에 `static grow 함수`를 통해서 수확물을 생산하고 `harvest 함수`를 통해 수확할 수 있습니다.
4. 마지막으로 얻은 수확물을 동물에게 먹입니다.

여기에는 3가지 추상화된 프로토콜을 사용했습니다. 해당 feed 함수에서 불투명 타입 animal을 통해 `Cow` → `Hay` → `Alfalfa` 까지 도달할 수 있도록 `some` 과 `associatedtype` 을 따라 올라 올 수 있었습니다.

```swift
struct Farm {
    func feed(_ animal: some Animal) {
        let crop = type(of: animal).Feed.grow()
        let produce = crop.harvest()
        animal.eat(produce)
    }
}

----

let farm = Farm()
let cow = Cow()
farm.feed(cow)
```

`Animal`이 어떤 타입인지 알 수 없기 때문에 직접적으로 `Hay` 타입을 집어넣으려하면 컴파일러가 에러를 만들어주게 됩니다.

```swift
animal.eat(Hay.gorw().harvest())
```

다음으로 불투명 타입 `Animal`의 배열을 받아서 `feed`를 호출하는 `feedAll`을 만들어보겠습니다. 앞서 `Aniaml`의 하위 타입으로 `Cow`, `Horse`, `Chicken`을 만들었습니다. 이 때도 `some` 키워드를 쓸 수 있을까요? 앞서 `some` 키워드를 쓰는 경우 컴파일 타임에 구체적인 타입이 정해져야 한다고 했습니다. 변수로 `some` 타입을 쓰는 경우 반드시 초기화를 통해서 타입을 지정해야 하고 함수에 쓰일 때는 함수 호출 과정에서 타입이 정해져야 합니다.

만약 우리가 받고 싶은 것이 특정 타입의 배열이라면, `[some Animal]`을 사용할 수 있습니다. 하지만 이 경우, 함수 호출 시점에서 `Animal`의 구체적인 타입이 정해져야 하기 때문에 한 가지 타입만 사용할 수 있습니다. 예를 들어 Cow 인스턴스를 만들어 넣는다면 `[some Animal]`을 사용할 수 있지만, 이는 `[Cow]`와 같은 의미이므로 이번 케이스에는 적합하지 않습니다.

그렇다면 이렇게 다양한 타입의 불투명 유형을 함께 혼합해서 사용해야 하는 경우 어떻게 해야 할까요? Swift에서는 불투명 타입을 구체화 할 수 없는 경우 `any` 키워드를 사용할 수 있습니다. `any` 키워드는 런타임에 `Animal` 타입이 달라질 수 있음을 나타냅니다.

```swift
struct Farm {
    func feed(_ animal: some Animal) { ... }

		func feedAll(_ animals: [any Animal]) { ... }
    }
}

----
let farm = Farm()
farm.feedAll([Cow(), Horse(), Chicken()])
```

`Any` 키워드는 임의의 `Animal` 타입을 저장할 수 있고, 구체적인 기본 타입은 런타임에 달라질 수 있습니다. 이 유형을 상자처럼 생각할 수 있습니다. 값이 직접 들어갈 수 있을 정도로 작은 경우도 있을 수 있고, 너무 큰 경우 포인터로 저장 될 수 있습니다. (컴파일 타임에 구체적 유형을 알 수 없어 유형소거라 부릅니다.)

이렇게 연관된 불투명 유형으로 배열을 만드는 건 Swift 5.7의 새로운 기능입니다.

![Untitled](assets/images/ios/2023-03-04-WWDC22_Generic/Untitled.png)

하지만, `Animal` 타입을 직접 사용할 수 없습니다. 전달받은 `Animal`이 어떤 타입인지 알 수 없기 때문에, `any` 키워드로 선언된 타입을 `some Animal` 타입으로 고정해야 합니다. Swift 5.7 버전에서는 언박싱 기능이 추가되어, `any` 타입을 `some` 타입으로 고정할 수 있습니다.

![Untitled](assets/images/ios/2023-03-04-WWDC22_Generic/Untitled%201.png)

Swift 5.7 버전에서는 언박싱 기능이 추가되어, `any` 타입을 `some` 타입으로 고정할 수 있습니다.

![Untitled](assets/images/ios/2023-03-04-WWDC22_Generic/Untitled%202.png)

```swift
func feedAll(_ animals: [any Animal]) {
    for animal in animals {
        feed(animal)
    }
}
```

`some`

- 구체적 기본 유형이 고정된다.
- 제네릭 타입에서 고정 타입을 의존할 수 있다. (프로토콜의 API에 접근 가능)

`any`

- 임의의 구체적인 기본 유형을 저장 할 수 있다.
- 유형 소거를 제공한다. (컴파일 타임에 유형을 정할 필요 없다)

`any` 키워드를 사용하면 스토리지의 유연성을 획득할 수 있지만, 인터페이스 접근을 위해서는 구체화를 위해 `some`을 사용해야 합니다. 따라서, 기본적으로 `some`으로 코드를 작성하고 필요에 따라 `any`로 확장해야 합니다.

## Warp-up

이번 WWDC 섹션에서 알아본 내용을 다시 한번 정리하면

- 구체적 유형을 작성
- 반복적인 보일러 코드를 발견
- 공통 기능을 발견해 프로토콜 작성
- any, some 키워드를 사용해 추상화 코드 작성
- 표현적인 코드에서는 some 을 더 선호한다는 것을 발견

### 전체 코드

```swift
protocol AnimalFeed {
  associatedtype CropType: Crop where CropType.Feed == Self
  static func grow() -> CropType
}

protocol Crop {
  associatedtype Feed: AnimalFeed where Feed.CropType == Self
  func harvest() -> Feed
}

protocol Animal {
  associatedtype Feed: AnimalFeed
  func eat(_ food: Feed)
}

struct Farm {
  func feed(_ animal: some Animal) {
    let crop = type(of: animal).Feed.grow()
    let produce = crop.harvest()
    animal.eat(produce)
  }

  func feedAll(_ animals: [any Animal]) {
    for animal in animals {
      feed(animal)
    }
  }
}

struct Cow: Animal {
  func eat(_ food: Hay) {}
}

struct Hay: AnimalFeed {
  static func grow() -> Alfalfa {
    Alfalfa()
  }
}

struct Alfalfa: Crop {
  func harvest() -> Hay {
    Hay()
  }
}
```