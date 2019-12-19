---
layout: post
current: post
navigation: True
title:  "Circle Timer 만들기(SwiftUI, CoreGraphics, Paths)"
date:   2019-12-18 23:05:00
cover: assets/images/watchOS/2019-12-18-Circle_Timer_SwiftUI_CoreGraphics_Paths/background.png
description: SwiftUI, watchos 원형 UI 만들기
tags: [ watchos, swiftui, project ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---
# Circle Timer 만들기(SwiftUI, CoreGraphics, Paths)

목표

- 타임 타이머 형태의 원형 뷰를 만든다.
- 사용자의 움직임에 따라서 각도를 변경한다.

![Circle%20Timer%20SwiftUI%20CoreGraphics%20Paths/timtimer_01.png](assets/images/watchOS/2019-12-18-Circle_Timer_SwiftUI_CoreGraphics_Paths/timtimer_01.png)

## 원 그리기

 타임 타이머 Mod 의 핵심은 시각적으로 붉은색 원이 줄어드는데 있다. 따라서 자유 자제로 저 원을 그릴 수 있어야 한다. 원을 그리는 방법에는 다양한 방법이 있지만 코어 그래픽을 사용해서 그려야 자유롭게 그릴 수 있다고 판단했다.

 전통적(UIKit)으로 저런 형태의 도형을 그리는 방법은 이미 잘 알려져 있고 별반 다르지 않을거라 생각했다.

[Core Graphics Tutorial Part 1: Getting Started](https://www.raywenderlich.com/411-core-graphics-tutorial-part-1-getting-started)

 코어 그래픽을 사용해 커스텀 뷰를 만드는 방법으로는 2가지가 있다.

- Shape를 상속해 만들기
- Path를 사용해 만들기

 Path를 사용할지 Shape를 사용할지 고민이라면 다른 포스트를 보고 정리한 포스트가 있으니 확인해 보자.

[](https://leejigun.github.io/SwiftUI_Paths_Shapes)

 apple의 SwiftUI 가이드에서는 도형을 그리는 방법으로 Path를 사용해 그리는 방법이 나와있다.

[Apple Developer Documentation](https://developer.apple.com/tutorials/swiftui/drawing-paths-and-shapes)

 이 포스트에서는 Path를 사용해 화면을 그리는 방법을 확인한다.

## Custom View

 먼저 커스텀 뷰를 만든다. 이 뷰는 화면을 그리는 역할만 수행하려고 한다.

```swift
    struct CircleView: View {
    	var body: some View {
    	// 뷰 구현
    	}
    }
```

 우리가 그릴 원은 360도의 각도에서 어디서 어디까지 원을 채울지 알아야 한다.  그리고 원의 색상은 뭔지, 원을 채우지 않은 부분의 색상은 무슨 색인지 알 필요가 있다.

```swift
    // 시작하는 각도
    var startPercent: CGFloat = 0
    // 끝나는 각도
    var endPercent: CGFloat = 50
    // 원의 색상
    var color: Color = .red
    // 원의 배경 색상
    var backgroundColor: Color = .black
```

 시계와 마찬가지로 12시 방향을 0이라고 생각하고 50까지 늘리도록 했다.

![Circle%20Timer%20SwiftUI%20CoreGraphics%20Paths/Untitled.png](assets/images/watchOS/2019-12-18-Circle_Timer_SwiftUI_CoreGraphics_Paths/Untitled.png)

 Path를 이용해 위와 같은 화면을 그리려면 어떻게 해야 할까?

 ```swift
    GeometryReader { geometryProxy in
        ZStack(alignment: .center) {
            Circle()
                .foregroundColor(self.color)
            Path { path in
                let size = geometryProxy.size
                let center = CGPoint(x: size.width / 2.0,
                                     y: size.height / 2.0)
                let radius = min(size.width, size.height) / 2.0
                path.move(to: center)
                path.addArc(center: center,
                            radius: radius,
                            startAngle: .init(degrees: Double(self.startPercent)),
                            endAngle: .init(degrees: Double(self.endPercent)),
                            clockwise: true)
            }
            .rotation(.init(degrees: 270))
            .foregroundColor(self.backgroundColor)
            .frame(width: geometryProxy.size.width,
                   height: geometryProxy.size.height,
                   alignment: .center)
        }
    }
```

 GeometryReader 를 사용해 할당된 화면의 사이즈를 읽어온다. Shape의 경우 path(in:) 메소드에서 Rect 를 가져오기 때문에 사이즈를 알 수 있지만 Path에서는 사이즈를 알 수 없으니 GeometryReader를 사용해야 한다.

 Path의 내부를 확인해보면 사이즈와 Center 값을 가져와 path를 이용해 원을 그린다.

 그냥 그리면 원이 약간 틀어져서 실행된다. 그래서 뷰를 조금 돌려줬다.

![Circle%20Timer%20SwiftUI%20CoreGraphics%20Paths/Untitled%201.png](assets/images/watchOS/2019-12-18-Circle_Timer_SwiftUI_CoreGraphics_Paths/Untitled 1.png)

```swift
    .rotation(.init(degrees: 270))
```

다음 포스트에서는 Shape를 이용해 똑같이 그려보려한다.
