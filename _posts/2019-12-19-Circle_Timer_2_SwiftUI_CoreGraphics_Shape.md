---
layout: post
current: post
navigation: True
title:  "Circle Timer 만들기_2(SwiftUI, CoreGraphics, Shape)"
date:   2019-12-19 12:17:00
cover: assets/images/watchOS/2019-12-19-Circle_Timer_2_SwiftUI_CoreGraphics_Shape/background.png
description: SwiftUI, watchos Shape를 사용해 화면 만들기
tags: [ watchos, swiftui, project ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---

# Circle Timer 만들기_2(SwiftUI, CoreGraphics, Shape)

앞선 포스트에서는 Path를 사용화 화면을 그렸다. 타임 타이머와 유사한 화면을 그렸다. 이번 포스트에서는 Shape를 사용해 이전에 구현했던 것과 같은 화면을 그리려 한다.

 Shape와 Paths의 차이는 앞선 포스트를 설명했다.

[SwiftUI - Paths와 Shapes](https://leejigun.github.io/SwiftUI_Paths_Shapes)

## Shape 구현

 Shape를 프로토콜을 상속하는 CircleShape를 만들었다. Shape 프로토콜은 필수적으로 path 메소드를 구현해야 하는데, path 그린 내용대로 화면을 그리게 된다.

```swift
@available(iOS 13.0, OSX 10.15, tvOS 13.0, watchOS 6.0, *)
public protocol Shape : Animatable, View {
  func path(in rect: CGRect) -> Path
}
```

그러면 path 메소드를 사용해 화면을 그려 보자.
```swift
struct CircleShape: Shape {

    func path(in rect: CGRect) -> Path {
        // 정사각형으로 만들기
        let square: CGRect
        if rect.maxX - rect.minX > rect.maxY - rect.minY { // 가로가 더 길 경우
            square = CGRect(x: rect.midX - (rect.maxY / 2.0),
                            y: rect.minY,
                            width: rect.maxY,
                            height: rect.maxY)

        } else { // 세로가 더 길 경우
            square = CGRect(x: rect.minX,
                            y: rect.midY - (rect.maxX / 2.0),
                            width: rect.maxX,
                            height: rect.maxX)
        }

        var path = Path()
        let center = CGPoint(x: square.midX, y: square.midY)

        path.move(to: center)

        path.addArc(center: center,
                    radius: square.midX - square.minX,
                    startAngle: .init(degrees: 0),
                    endAngle: .init(degrees: 360.0 - 260),
                    clockwise: true)

        return path.rotation(.init(degrees: 270)).path(in: rect)
    }
}
```

![](assets/images/watchOS/2019-12-19-Circle_Timer_2_SwiftUI_CoreGraphics_Shape/Untitled.png)

 path를 살펴보면 화면을 그릴 수 있도록 CGRect를 제공하고 있다. 하지만 우리는 원을 그려야 하기 때문에 CGRect 안에서 정사각형의  CGRect를 다시 만들었다.

```swift
/*
	func path(in rect: CGRect) -> Path 내부
*/

// 정사각형으로 만들기
let square: CGRect
if rect.maxX - rect.minX > rect.maxY - rect.minY {
	// 가로가 더 길 경우
  square = CGRect(x: rect.midX - (rect.maxY / 2.0),
                  y: rect.minY,
                  width: rect.maxY,
                  height: rect.maxY)

} else {
	// 세로가 더 길 경우
  square = CGRect(x: rect.minX,
                  y: rect.midY - (rect.maxX / 2.0),
                  width: rect.maxX,
                  height: rect.maxX)
}
```


 공간을 다시 지정 했으면 그 공간 안에 path를 그려야 한다.

```swift
var path = Path()
let center = CGPoint(x: square.midX, y: square.midY)

path.move(to: center)

path.addArc(center: center,
            radius: square.midX - square.minX,
            startAngle: .init(degrees: 0),
            endAngle: .init(degrees: 360.0 - 260),
            clockwise: true)

return path.rotation(.init(degrees: 270)).path(in: rect)
```

 path에 center를 기준으로 Arc를 추가한다.  Arc를 추가하면 그 부분을 제외하고 화면을 칠하게 된다. 따라서 360도에서 우리가 그리려는 각도를 뺀 각도가 화면에 그려지는 각도이다.

![](assets/images/watchOS/2019-12-19-Circle_Timer_2_SwiftUI_CoreGraphics_Shape/Untitled 1.png)

 이 역시 12시 방향을 0이라 보기 때문에 살짝 돌려준다.

![](assets/images/watchOS/2019-12-19-Circle_Timer_2_SwiftUI_CoreGraphics_Shape/Untitled 2.png)
