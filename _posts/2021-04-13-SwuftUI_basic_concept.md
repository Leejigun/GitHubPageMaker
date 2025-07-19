---
layout: post
current: post
navigation: True
title:  "SwiftUI 의 5가지 기본 컨셉"
date:   2020-06-04 17:46:00
cover: assets/images/SwiftUI/2021-04-13-SwuftUI_basic_concept/6FB6D869-85BA-4704-A370-C5C6B68F1A3E.png
description: SwiftUI 의 5가지 기본 컨셉
tags: [ swuftui ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---

# SwiftUI 의 5가지 기본 컨셉

[https://youtu.be/51xIHDm_BDs](https://youtu.be/51xIHDm_BDs)

## 1. 화면에 View를 표현하는 Layout은 3가지 뿐이다.

### VStack

 화면에 수직으로 View를 표시한

```swift
VStack {
	Text("Hello, World!")
	Text("Hello, World!")
	Text("Hello, World!")
	Text("Hello, World!")
}
```

![Untitled](assets/images/SwiftUI/2021-04-13-SwuftUI_basic_concept/Untitled.png)

### HStack

```swift
HStack {
	RoundedRectangle(cornerRadius: 30)
	RoundedRectangle(cornerRadius: 30)
	RoundedRectangle(cornerRadius: 30)
	RoundedRectangle(cornerRadius: 30)
}
```

![Untitled](assets/images/SwiftUI/2021-04-13-SwuftUI_basic_concept/Untitled 1.png)

### ZStack

```swift
ZStack {
	Color.pink
	VStack {
		Text("Hello, World!")
		Text("Hello, World!")
		Text("Hello, World!")
		Text("Hello, World!")
	}
	HStack {
		RoundedRectangle(cornerRadius: 30)
		RoundedRectangle(cornerRadius: 30)
		RoundedRectangle(cornerRadius: 30)
		RoundedRectangle(cornerRadius: 30)
	}
}
```

![Untitled](assets/images/SwiftUI/2021-04-13-SwuftUI_basic_concept/Untitled 2.png)

## 2. SwiftUI에서 표현하는 모든 것들은 View

```swift
ZStack {
	Color.pink
	VStack {
		Text("Hello, World!")
		Text("Hello, World!")
		Text("Hello, World!")
		Text("Hello, World!")
	}
	HStack {
		RoundedRectangle(cornerRadius: 30)
		RoundedRectangle(cornerRadius: 30)
		RoundedRectangle(cornerRadius: 30)
		RoundedRectangle(cornerRadius: 30)
	}
}
```

- VStack, HStack, ZStack 같은 layout 역시 View
- Text, RoundedRectangle 같은 elements 역시 View
- [Color.pink](https://Color.pink) 같은

또한 modifier를 통해서 View를 수정, 변조하면 해당 View를 수정하는게 아닌 옵션이 적용된 다른 View를 반환해 교체하게 된다. 이는 SwiftUI의 모든 View는 class가 아닌 Struct이기 때문이다.

```swift
Text("Everything is a View!")
	.font(.largeTtitle)
```

## 모든 뷰는 부모 자식의 관계를 가진다.

```swift
ZStack {
	Color.pink
	VStack {
		Text("Hello, World!")
		Text("Hello, World!")
		Text("Hello, World!")
		Text("Hello, World!")
	}
	HStack {
		RoundedRectangle(cornerRadius: 30)
		RoundedRectangle(cornerRadius: 30)
		RoundedRectangle(cornerRadius: 30)
		RoundedRectangle(cornerRadius: 30)
	}
}
```

- Text는 VStack의 자식이고 VStack은 ZStack의 자식이며 최상위 레이아웃 역시 그 코드를 사용한 View의 자식이다.

자식의 모든 뷰의 속성을 부모뷰에서 제어할 수 있다. 다만 자식 뷰에서 직접 그 속성을 재정의한 경우에는 자식뷰의 속성을 사용. 

## SwiftUI의 View들은 서로 당기고 밀며 자리를 잡는다.

Text의 경우 자기가 필요한 만큼만 공간을 사용한다.

![Untitled](assets/images/SwiftUI/2021-04-13-SwuftUI_basic_concept/Untitled 3.png)

 그런데, 다른 뷰의 경우 자기가 더 큰 사이즈를 차지하기 위해서 서로 밀어내면서 공간을 채운다.

 같은 뷰 2개가 있다면 서로 밀다가 50:50을 채우게 된다

```swift
VStack {
	Color.pink
	RoundedRectangle(cornerRadius: 30)
}
```

![Untitled](assets/images/SwiftUI/2021-04-13-SwuftUI_basic_concept/Untitled 4.png)

 컨텐츠가 있는 경우에는 자기 컨텐츠 만큼의 사이즈를 채우는 경향이 있다. 하지만 Size를 설정할 근거가 없는 경우 확장하려고 하는 경향이 있고, 우선순위나 사이즈 지정이 없는 경우 서로 비비다 나눠같는 경향이 있다.

 이는 Texture framework의 flex와 유사한 것 같다.

## 데이터로 뷰를 수정하기

 앞서 Modifier의 경우 View를 수정하는게 아니라 새로운 View를 만들어서 교체했었다. 이는 컴파일 

모디파이어의 경우 오브젝트를 수정하지 않는다. 수정한 다른 뷰로 대체한다. 

 그러면 런타임 중 View를 수정하려면 어떻게 해야 할까? 

@State 라는 프로퍼티 래퍼를 통해서 변수를 감싸 사용한다. 

- @State 반드시 View의 Body에서 호출해야 한다.
- 모든 View는 Struct기 때문에 @State를 통해서 View를 수정해도 Modifier와 마찬가지로 수정이 아닌 교체를 통해서 UI를 갱신하게 된다.
- @State 는 Heap 메모리에 할당된다. View에 대한 포인터만 가지고 있고 View를 교체해도 포인터만 교체하게 된다.

```swift
struct ContentView: View {
    
    @State private var circleColor = Color.red
    
    var body: some View {
        VStack {
            Text("You change views with Data.")
                .font(.largeTitle)
            
            Button("Change Color") {
                self.circleColor = Color.green
            }
            
            Circle()
                .foregroundColor(circleColor)
        }
    }
}
```

## 출처

**[5 SwiftUI Concepts Every Beginning SwiftUI Developer Needs To Know (2020)](https://www.youtube.com/watch?v=51xIHDm_BDs)**