---
layout: post
current: post
navigation: True
title:  "Circle Timer 만들기_3_User_Interation(SwiftUI, gesture, DragGesture)"
date:   2019-12-19 17:17:00
cover: assets/images/watchOS/2019-12-19-Circle_Timer_3_User_Interation/background.png
description: 사용자 입력 처리하기.
tags: [ watchos, swiftui, project ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---
# Circle Timer 만들기_3_User_Interation(SwiftUI, gesture, DragGesture)

이제 타임 타이머와 마찬가지로 손가락을 이용해서 시간을 설정할 수 있는 기능을 넣겠습니다. 손가락으로 시간을 변경 하려면  사용자의 drag 제스쳐를 잡아낼 수 있어야 합니다.

 사전에 만든 CircleShape를 화면에 붙여줍니다.

```swift
@State var endAngle: Double = 260

var body: some View {
        CircleShape(endDegrees: self.$endAngle)
            .foregroundColor(Color.red)
}
```
 state와 binding의 개념은 다른 포스트에서 다루니 넘어가고 RxSwift BehviorRelay랑 비슷한 개념이라 보면 된다.

 여기에 사용자 제스처를 잡기 위해서 viewModifier를 붙여 준다. 처음에 뭐를 붙여야 할지 모를 때 상단에 + 버튼을 누르고 찾아보면 도움이 많이 된다.

![](assets/images/watchOS/2019-12-19-Circle_Timer_3_User_Interation/Untitled.png)

 Drag Gesture 를 추가해본다.

```swift
CircleShape(endDegrees: self.$endAngle)
  .foregroundColor(Color.red)
  .gesture(DragGesture().onChanged { value in
	/*
		angle을 변경하는 동작
	*/
}
```

 이제 angle을 변경하는 동작을 살펴봐야 하는데, 요점은 우리가 선택한 CGPoint가 가운데 Center CGPoint에서 어느 각도에 위치해 있는지 계산하는 로직이 필요하다.

 크게 고민 안하고 구글링했더니 바로 나왔다.

```swift
private func getAngle(center: CGPoint, target: CGPoint) -> CGFloat {
  let originPoint = CGPoint(x: target.x - center.x,
                            y: target.y - center.y)
  let bearingRadians = atan2f(Float(originPoint.y), Float(originPoint.x))
  var bearingDegrees = bearingRadians * (180.0 / Float.pi)
  bearingDegrees += 90
  bearingDegrees = (bearingDegrees > 0.0
      ? bearingDegrees : (360.0 + bearingDegrees))
  return CGFloat(bearingDegrees)
}
```
 근데 이제 다음으로 Center 값을 알아야 한다. 어떻게 해야 할까? 이 CircleShape가 할당된 공간을 알아야 하는데 이럴 때 쓰는게 GeometryReader다.

GeometryReader가 할당되는 사이즈가 담긴 geometryProxy를 제공하기 때문에 사이즈를 알 수 있다.

```swift
GeometryReader { geometryProxy in
            CircleShape(endDegrees: self.$endAngle)
                .foregroundColor(Color.red)
                .gesture(DragGesture().onChanged { value in
									/*
									화면 사이즈를 계산하고 Angle을 다시 그리는 과정
									*/
                },including: .gesture)
        }
        .frame(idealWidth: size.width,
               maxWidth: size.width,
               idealHeight: size.height,
               maxHeight: size.height,
               alignment: .center)
```

 내부 angle을 그리는 과정은 다음과 같다.

```swift
let minSize = min(geometryProxy.size.width,
					        geometryProxy.size.height)
let size = CGSize(width: minSize, height: minSize)
let angle = self.getAngle(center: CGPoint(x: size.width / 2.0,
                                y: size.height / 2.0),
								                target: value.location)
print(angle)
// 각도계가 뒤집힌 형태여야 하니까 360에서 빼준다.
self.endAngle = 360.0 - Double(angle)
```
