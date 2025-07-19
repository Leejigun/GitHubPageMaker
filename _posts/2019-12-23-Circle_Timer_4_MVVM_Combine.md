---
layout: post
current: post
navigation: True
title:  "Circle Timer 만들기_4_MVVM_Combine"
date:   2019-12-23 15:17:00
cover: assets/images/watchOS/2019-12-19-Circle_Timer_4_MVVM_Combine/background.png
description: Combine을 활용해 MVVM 구조 잡기
tags: [ watchos, swiftui, project ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---
# Circle Timer 만들기_4_MVVM_Combine

앞서 타이머 UI를 만들었는데, 이제 실제 UI를 만들어 보려 한다. 실제 프로젝트에서는 RxSwift와 MVVM을 사용해 개발하는데, 이번에 SwiftUI로 화면을 만들기 시작했으니 이번 기회에 Combine을 사용해보려 한다.

## MVVM

 예전에 SwiftUI와 MVVM에 대해서 글을 포스트를 올렸었다. 간단한 부분이었지만 이 포스트와 함께 보면 좋을 거 같다.

[SwiftUI, Combine, MVVM 1) - Financing UI](https://leejigun.github.io/SwiftUI,Combine,MVVM_1)-Financing)

 mvvm 아키텍처를 사용하기 위해서 view model 클래스를 만들어준다.
```swift
class MainFrontViewModel: ObservableObject {
	// ...
}
```
 우리가 만든 타이머에서 view와 커뮤니케이션 하는 부분을 생각해보자. 먼저 타이머 기능에 필요한 부분이 뭐가 있을까?

- 카운트 다운 이기 때문에 시간이 점점 줄어드는 형식이다. 따라서 줄어들 처음 시간값이 필요하.
- 시간이 줄어듬에 따라서 붉은 부분이 감소해야 하기 때문에 지금 시간값을 알아야 한다.
- 우리는 360도 중에서 어디에 시간부가 위치해야 할지 알아야 하기 때문에 각도 값이 필요하다.

 그래서 3개의 변수를 만들었다.

```swift
/// 360도 중에서 지금 어디인지
@Published var angle: Double = 360 {
/// 전체 범위
@Published var maxSecond: Double = 600 // 10분
/// 현재 위치
@Published var currentSecond: Double = 600
```

 그리고 카운트 다운을 타이머니까 카운트 다운을 시작 종료 하는 메소드를 정의해야 한다.

```swift
protocol TimerProtocol {
    func startCountDown()
    func pauseCountDown()
    func stopCountDown()
}
```

 다음으로 타이머 관련 변수를 확인해보자. Timer를 Combine에서 사용하는 방법을 찾아보니 쉽게 나온다.

```swift
static let timeInterval: Double = 0.1

/// Timer -> Publisher
private let currentTimePublisher
  = Timer.TimerPublisher(interval: timeInterval, runLoop: .main,mode: .default)
/// 카운트 다운
private var cancellable: AnyCancellable?
```

- Timer에 있는 TimerPublisher 생성자를 통해서 Publisher를 만든다.
- 로직이 붙은 Publisher에서 나온 cancellable을 변수에 저장한다. (Rx에서 disposeable과 같은 개념)

 카운트 다운을 시작해 달라고 요청하면 Publisher에 로직을 붙여 cancellable을 만든다.

weak self를 사용하는 이유는 메모리 관리 측면과 timer의 경우 잘못하면 해지되지 않는 문제가 생길 수 있기 때문에 추가했다.

```swift
/// 카운트 다운 시작
func startCountDown() {
    cancellable?.cancel()
		self.isCountdown = true
    let timer = currentTimePublisher.autoconnect()
        .sink {[weak self] (_) in
        guard let self = self else { return }
        self.currentSecond -= ViewModelType.timeInterval
        let percent = self.currentSecond / self.maxSecond * 100
        self.angle = 360.0 * percent / 100

        if self.currentSecond <= 0 {
            self.stopCountDown()
        }
    }
    self.cancellable = timer
}

/// 카운트 다운이 끝나는 경우
func stopCountDown() {
    self.cancellable?.cancel()
    self.currentSecond = 0
    self.angle = 0
    self.isCountdown = false
}
```
 여기서 추가적으로 isCountdown 플래그를 만들어 UI 변화를 줄 예정이다.

뷰 모델을 적용하면 다음과 같다.

```swift
// MainFrontView.swift
...
@ObservedObject var viewModel = MainFrontViewModel()
...
var body: some View {

GeometryReader { geometryProxy in
    TimerShape(endDegrees: self.$viewModel.angle)
        .foregroundColor(Color.red)
        .cornerRadius(36, antialiased: true)
        .gesture(DragGesture().onChanged { value in
            // 카운트 다운이 시작되고 있으면 시간 변경 못하게
            if self.viewModel.isCountdown { return }
            let minSize = min(geometryProxy.size.width,
                              geometryProxy.size.height)
            let size = CGSize(width: minSize, height: minSize)
            let angle = self.getAngle(center: CGPoint(x: size.width / 2.0,
                                                      y: size.height / 2.0),
                                      target: value.location)
            // 각도계가 뒤집힌 형태여야 하니까 360에서 빼준다.
            self.viewModel.angle = 360.0 - Double(angle)
        },including: .gesture)
        .onLongPressGesture {
						// 롱 클릭으로 시작 종료를 했다.
            if !self.viewModel.isCountdown {
                self.viewModel.startCountDown()
            } else {
                self.viewModel.stopCountDown()
            }
        }
        .frame(width: geometryProxy.size.width,
               height: geometryProxy.size.height,
               alignment: .center)
}
.frame(idealWidth: size.width,
       maxWidth: size.width,
       idealHeight: size.height,
       maxHeight: size.height,
       alignment: .center)

}
```
 아직 미흡한 부분이 많은데 조금씩 수정해 나가자.
