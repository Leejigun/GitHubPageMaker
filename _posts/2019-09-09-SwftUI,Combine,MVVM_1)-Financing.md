---
layout: post
current: post
navigation: True
title:  "SwiftUI, Combine, MVVM 1) - Financing UI"
date:   2019-09-09 00:00:01
cover: assets/images/SwiftUI/Financing_App_Volume_1.png
description: Dribbble을 보고 UI를 만들어보자.
tags: [ swiftui ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---
# SwftUI, Combine MVVM - Financing

 이전 포스트에서는 주로 SwiftUI를 공부하면서 화면을 디자인해보는 작업을 진행했었다. 이런 연습은 예전에 Flutter를 공부할 때 어느 유튜버가 매일매일 화면을 만드는 영상을 올렸던 것을 보고 따라 하기 시작한 것으로 처음 Flutter를 공부할 때 많이 도움이 되었다.
 SwiftUI는 Flutter와 정말 많은 부분이 비슷하다. 단순히 코드로 화면을 만드는 행위뿐만이 아니라 화면을 작은 뷰 단위로 분할해서 공략해 나가고 View와 로직을 분리하는 접근 방식이 익숙해지면 몹시 간결해진다.
 이번 포스트에서는 SwiftUI로 절반 정도 화면을 만들고 ViewModel을 붙여봤다.

- https://dribbble.com/shots/7096764-Financing-App-Volume-1


##  원본 화면

 일단 절반 정도만 진행하고 이번에는 ViewModel을 붙여보려 한다.

![원본](https://paper-attachments.dropbox.com/s_199A3E953151944B18DB109B9C152FCE49633CADF171E0396CFB88F9F527F320_1568010213987_image.png)
![1차 완성](https://paper-attachments.dropbox.com/s_199A3E953151944B18DB109B9C152FCE49633CADF171E0396CFB88F9F527F320_1568011578137_image.png)



##  화면 구성

 이번 포스트에서 진행할 화면 구성은 다음과 같습니다.

-  상단 네비게이션바
-  중단 사용자 정보
-  하단 버튼 그룹
-  하단 내 카드 목록


![](https://paper-attachments.dropbox.com/s_199A3E953151944B18DB109B9C152FCE49633CADF171E0396CFB88F9F527F320_1568010502185_image.png)


 특이 사항은 다음과 같습니다.
 상단 네비게이션 바의 오른쪽 벨 버튼의 붉은 배찌는 클릭하면 사라진다.
 (원래는 복잡한 로직이 있어야 하지만 나타나고 사라지게 하는 이벤트를 중심으로 넣습니다.)
 하단 사용자 카드 목록은 See All을 클릭하면 늘어나고 줄어들도록 한다.

 일단 이번 포스트에서는 여기까지만 적용하고 추가적으로 각종 상태 값들을 뷰 모델을 만들어 바인드 해보려 합니다.














##  네비게이션바
![](https://paper-attachments.dropbox.com/s_199A3E953151944B18DB109B9C152FCE49633CADF171E0396CFB88F9F527F320_1568011365431_image.png)


 상단 네비게이션 바를 그리기 앞서 배경에 파 색 백그라운드 뷰가 깔려있는 모습을 먼저 고민했다.
 고민하다가 나온 결론은 상단을 스택으로 감싸고 마지막 버튼 부분에서 하단으로 여백을 줘서 파란 부분 전체를 하나의 스택으로 구성하도록 했다.

```swift
    VStack {
    // 컨텐츠
    }.background(Color(red: 51/255,
                       green: 104/255,
                       blue: 252/255))
```
 이제 네비게이션 바를 구현해본다. 네비게이션 바는 왼쪽에 **Wallet** 이라는 타이틀과 오른쪽에 벨 형태의 버튼이 붙어있는 형태다. 오른쪽에 벨 아이콘은 붉은색 배찌가 붙어있어서 클릭하면 배찌가 사라지도록 하려한다.
 보통은 여기에 로직이 붙어있어서 새로운 알람이 있다면 배찌를 키고 알람을 다 확인하면 배찌를 사라지게 하는 형식으로 처리하는데 뒷단이 없기 때문에 다른 로직은 제거한다.
 배찌 역시 직접 그리기도 하지만 내가 했던 대부분의 프로젝트에서는 배찌가 있는 이미지가 따로 있었다. 이번에는 그런 지원이 없기 때문에 그려서 대충 위치에 올리려 한다.




![](https://paper-attachments.dropbox.com/s_199A3E953151944B18DB109B9C152FCE49633CADF171E0396CFB88F9F527F320_1568012258525_image.png)


 일단 화면에 Wallet 텍스트만 추가해봤다.
```swift
    var body: some View {
      VStack {
        VStack(alignment: .center) {
          Text("Wallet")
          .foregroundColor(Color.white.opacity(0.7))
          .font(Font.system(size: 20, design: .default))
          .bold()
        }.background(Color(red: 51/255,
                           green: 104/255,
                           blue: 252/255))
      }
      .edgesIgnoringSafeArea(.top)
      .edgesIgnoringSafeArea(.bottom)
    }
```
 그냥 배경에 테이터만 들어간 이상한 형태다. 하지만 컨텐츠 배경에만 파란색이 들어간 목적은 달성했다. 이제 이걸 상단부터 쌓아 내려가본다.


 HStack으로 감싸고 옆에 버튼을 그려넣었다. 참고로 포스트에서 사용되는 아이콘은 iOS 13부터 추가된 시스템 이미지로 iOS13 SF Symbols 검색하면 여러가지 아이콘들을 쉽게 검색해서 추가할 수 있다.
```swift
    ZStack(alignment: .center) {
      Image(systemName: "bell.fill")
          .resizable()
          .frame(width: 20, height: 20, alignment: .center)
          .foregroundColor(Color.white)
          .scaledToFit()
      Circle()
          .frame(width: 10, height: 10)
          .foregroundColor(Color.red)
          .padding(.top, -10)
          .padding(.trailing, -10)
    }
```
 상단부터 쌓고 싶어서 네비게이션 밑으로 Spacer() 를 넣어봤다. Spacer는 낮은 우선순위로 공간을 확장하는 컨포넌트로 양쪽 끝으로 붙이거나 동일한 간격을 유지하고 싶을 때 사용하면 유용하다.



![](https://paper-attachments.dropbox.com/s_199A3E953151944B18DB109B9C152FCE49633CADF171E0396CFB88F9F527F320_1568012647831_image.png)


 Spacer 를 넣었더니 문제가 생겼다. **.edgesIgnoringSafeArea(.top)** 를 사용하니 상단으로 공간이 넘어가 버린것이다. 이를 해결하기 위해서 상단에 적당한 padding을 넣어야 한다.
```swift
    HStack {
    // 타이틀
    // 아이콘
    }
    .padding(.top, UIApplication.shared.statusBarFrame.height)
    .padding(.horizontal, 30)
```
![](https://paper-attachments.dropbox.com/s_199A3E953151944B18DB109B9C152FCE49633CADF171E0396CFB88F9F527F320_1568013240185_image.png)


 이제 여기에 버튼에 배찌가 나타나고 사라지게 하는 상태값의 적용이 필요하다.
  State 변수를 추가한다. 그리고 알파값에 변수를 바인드해준다.
```swift
    struct MainContentsView: View {
      @State var isNew = false
    ...
    Circle()
      .frame(width: 10, height: 10)
      .foregroundColor(Color.red)
      .padding(.top, -10)
      .padding(.trailing, -10)
      .opacity(isNew ? 1.0 : 0)
    ...
    }
```
 이제 isNew가 true면 알파값이 1.0이고 false면 알파값이 0이 되서 나타나고 사라지게 된다.
 여기에 이벤트를 클릭 이벤트를 넣어보자.
 클릭 이벤트를 넣는 방법은 2가지가 있다. 일반적으로 사용하는 방법인 Button 뷰로 감싸서 처리하는 방법과 tapAction이라는 모디파이어를 사용해서 액션을 붙여넣는 방법이 있다.
```swift
    // Button
    Button(action: {
      self.isNew.toggle()
    }) {
      ZStack(alignment: .center) {
          Image(systemName: "bell.fill")
              .resizable()
              .frame(width: 20, height: 20, alignment: .center)
              .foregroundColor(Color.white)
              .scaledToFit()
          Circle()
              .frame(width: 10, height: 10)
              .foregroundColor(Color.red)
              .padding(.top, -10)
              .padding(.trailing, -10)
              .opacity(isNew ? 1.0 : 0)
      }
    }

    // tapAction
    ZStack(alignment: .center) {
        Image(systemName: "bell.fill")
            .resizable()
            .frame(width: 20, height: 20, alignment: .center)
            .foregroundColor(Color.white)
            .scaledToFit()
        Circle()
            .frame(width: 10, height: 10)
            .foregroundColor(Color.red)
            .padding(.top, -10)
            .padding(.trailing, -10)
            .opacity(isNew ? 1.0 : 0)
    }.tapAction {
        self.isNew.toggle()
    }
```
  두가지 방법 모두 별 문제 없이 잘 동작한다.


##   코드 분리

 하나의 화면이 만들어졌으면 이제 이걸 다른 Struct로 분리해서 처리해보자. Flutter나 Texture를 해보면 알겠지만, 이렇게 코드로 화면을 만드는 방법은 조금만 화면이 복잡해지면 코드는 엄청나게 길어지면서 보기 힘들어진다. 그래서 뷰 하나 하나를 다른 클레스나 구조체로 뽑아내서 관리해줘야 코드 관리가 편하다.

```swift
    fileprivate struct HomeNavigationBar: View {
      @Binding var isNew: Bool
      // 네비게이션바
      var body: some View {
          HStack {
              Text("Wallet")
                  .foregroundColor(Color.white.opacity(0.7))
                  .font(Font.system(size: 20, design: .default))
                  .bold()

              Spacer()
              Button(action: {
                  self.isNew.toggle()
              }) {
                  ZStack(alignment: .center) {
                      Image(systemName: "bell.fill")
                          .resizable()
                          .frame(width: 20, height: 20, alignment: .center)
                          .foregroundColor(Color.white)
                          .scaledToFit()
                      Circle()
                          .frame(width: 10, height: 10)
                          .foregroundColor(Color.red)
                          .padding(.top, -10)
                          .padding(.trailing, -10)
                          .opacity(isNew ? 1.0 : 0)
                  }
              }
          }
      }
    }
```
 특이점으로는 **@Binding** 으로 기존에 State에서 Binding으로 변경한 부분이다. 상위에 적용된 State를 그대로 가져다가 사용한다는 의미로 말 그대로 bind 한다. RxSwift를 사용해본 경험이 있다면 bind에 익숙할 것이다. 행위는 다르지만 의미는 비슷하다.
 나머지는 너무 길어지니까 그냥 코드로 보면 결국에는 다음과 같다.
```swift
    struct MainContentsView: View {

      @State var isNew = true
      @State var userMoney = "0.00"
      @State var userGrade = "Premium"
      @State var isSeeAll = false
      @State var myCards = [HomeCardInfo(),HomeCardInfo()]

      var body: some View {
          VStack {
              VStack(alignment: .center) {
                  // 네비게이션바
                  HomeNavigationBar(isNew: self.$isNew)
                      .padding(.top, 50)
                      .padding(.horizontal, 30)
                  // 사용자 금액과 등급을 표시하는 부분
                  HomeUserInfoView(userMoney: self.$userMoney,
                                   userGrade: self.$userGrade)
                      .padding(.horizontal, 30)
                  // 입급 출금 버튼 그룹
                  HomeButtonsView()
                      .padding(.bottom, 100)
              }.background(Color(red: 51/255,
                                 green: 104/255,
                                 blue: 252/255))
              // 중간 내 카드 표시 부분
              HomeMyCardList(isSeeAll: self.$isSeeAll,
                             myCards: self.$myCards)
                  .padding(.top, -80)
                  .padding(.horizontal, 30)

              Spacer()

          }
          .edgesIgnoringSafeArea(.top)
          .edgesIgnoringSafeArea(.bottom)
      }
    }
```

![See All Off](https://paper-attachments.dropbox.com/s_199A3E953151944B18DB109B9C152FCE49633CADF171E0396CFB88F9F527F320_1568093884967_image.png)
![See All On](https://paper-attachments.dropbox.com/s_199A3E953151944B18DB109B9C152FCE49633CADF171E0396CFB88F9F527F320_1568093903451_image.png)


 자세한 코드는 맨 하단에 표시합니다.


##  ViewModel Combine

 대충 1차적으로 완성된 화면에서 상태를 나타내는 부분은 다음과 같다.

```swift
    @State var isNew = true
    @State var userMoney = "0.00"
    @State var userGrade = "Premium"
    @State var isSeeAll = false
    @State var myCards = [HomeCardInfo(),HomeCardInfo()]
```
이 부분이 변경되면 화면이 변경된다. 원래 기존에 UIKit을 사용할 때부터 RxSwift와 MVVM 패턴을 사용했던 입장에서는 이번 iOS의 변경점이 너무나도 고마웠다. 다른 포스트에서도 말했는데, MVVM에서의 핵심은 Input과 Output을 구분하는 것으로 시작한다고 말씀드렸습니다.
그래서 제가 사용하던 기존의 MVVM 방식에서는 Input과 Outpu의 구조체를 만들어 물리적(?)으로 input과 output을 완전히 분리해버렸습니다. 간단한 로직이라도 Input을 정의하고 Output을 정의해야 하는 불편함은 있었지만 그럼에도 불구하고 유지보수가 쉽고 코드 자체가 명확했습니다.
SwiftUI에서 역시 Input과 Output을 분리하고 있습니다. 하지만 앞선 살펴본 isNew의 경우에는 값에 따라 화면을 그리기 때문에 Output이지만 벨 아이콘을 클릭하면 isNew 변수를 toggle 하기 때문에 input도 같이 수행하고 있습니다. 아직 엄격하게 분리했다고 볼 수는 없지만 앞으로 수정해 나가야 할 부분이라 생각합니다.

 제가 만든 뷰 모델은 다음과 같습니다.
```swift
    import Foundation
    import Combine
    import SwiftUI

    class MainContentsViewModel: BindableObject {
        var willChange = PassthroughSubject<Void, Never>()

        private var totalCards = [HomeCardInfo(),HomeCardInfo(),HomeCardInfo(),HomeCardInfo()]

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
 그리고 View를 수정합니다.

```swift
    struct MainContentsView: View {

        @ObjectBinding var viewModel = MainContentsViewModel()

        var body: some View {
            VStack {
                VStack(alignment: .center) {
                    // 네비게이션바
                    HomeNavigationBar(isNew: self.$viewModel.isNew)
                        .padding(.top, 50)
                        .padding(.horizontal, 30)
                    // 사용자 금액과 등급을 표시하는 부분
                    HomeUserInfoView(userMoney: self.$viewModel.userMoney,
                                     userGrade: self.$viewModel.userGrade)
                        .padding(.horizontal, 30)
                    // 입급 출금 버튼 그룹
                    HomeButtonsView()
                        .padding(.bottom, 100)
                }.background(Color(red: 51/255,
                                   green: 104/255,
                                   blue: 252/255))
                // 중간 내 카드 표시 부분
                HomeMyCardList(isSeeAll: self.$viewModel.isSeeAll,
                               myCards: self.$viewModel.myCards)
                    .padding(.top, -80)
                    .padding(.horizontal, 30)

                Spacer()

            }
            .edgesIgnoringSafeArea(.top)
            .edgesIgnoringSafeArea(.bottom)
        }
    }
```
 Flutter의 Bloc 패턴과는 조금 달라 보이지만 지향하는 목적 자체는 동일합니다. Flutter의 Bloc에서는 Action과 State를 분리 가지고 Action에 따라서 State를 넘겨주는 형식으로 로직과 화면을 분리했습니다. 하지만 여기서는 ViewModel 자체가 State를 가지고 있기 때문에 Action이 들어와서 ViewModel이 변경되면 뷰 모델을 바라보고 있는 View를 수정해서 화면을 갱신하고 있습니다.
 다음 포스트에서는 지금의 뷰 모델을 조금 더 MVVM 형태에 맞게 수정해보겠습니다.

##  뷰 코드
```swift
    /// 상단 네비게이션 뷰
    fileprivate struct HomeNavigationBar: View {

        @Binding var isNew: Bool

        // 네비게이션바
        var body: some View {
            HStack {
                Text("Wallet")
                    .foregroundColor(Color.white.opacity(0.7))
                    .font(Font.system(size: 20, design: .default))
                    .bold()

                Spacer()
                Button(action: {
                    self.isNew.toggle()
                }) {
                    ZStack(alignment: .center) {
                        Image(systemName: "bell.fill")
                            .resizable()
                            .frame(width: 20, height: 20, alignment: .center)
                            .foregroundColor(Color.white)
                            .scaledToFit()
                        Circle()
                            .frame(width: 10, height: 10)
                            .foregroundColor(Color.red)
                            .padding(.top, -10)
                            .padding(.trailing, -10)
                            .opacity(isNew ? 1.0 : 0)
                    }
                }
            }
        }
    }
    ```
    ```swift
    /// 사용자 정보가 표시되는 뷰
    fileprivate struct HomeUserInfoView: View {
        @Binding var userGrade: String

        var body: some View {
            VStack(alignment: .leading) {
                HStack(alignment: .center) {
                    Text("$18 624.00")
                        .foregroundColor(Color.white)
                        .font(Font.system(size: 40, design: .default))
                        .bold()
                    Spacer()
                    Image("usdIcon")
                        .resizable()
                        .frame(width: 60, height: 30, alignment: .center)
                        .scaledToFit()
                }
                .padding(.bottom, 0)
                Rectangle()
                    .frame(minWidth: 0,
                           idealWidth: UIScreen.main.bounds.width,
                           maxWidth: UIScreen.main.bounds.width)
                    .frame(height: 0.5)
                    .foregroundColor(Color.white.opacity(0.5))
                    .padding(.top, 0)

                Text(userGrade)
                    .bold()
                    .foregroundColor(Color.white)
            }
        }
    }
    ```
    ```swift
    /// 버튼 그룹
    fileprivate struct HomeButtonsView: View {

        var body: some View {
            HStack(alignment:.center) {
                ZStack {
                    RoundedRectangle(cornerRadius: 5)
                        .foregroundColor(Color.orange)
                        .frame(width: (UIScreen.main.bounds.width - 60 - 10) / 2 ,
                               height: 50,
                               alignment: .center)

                    Text("Deposit")
                        .foregroundColor(Color.white)
                        .font(Font.system(size: 20, design: .default))
                        .bold()
                }
                ZStack {
                    RoundedRectangle(cornerRadius: 10)
                        .foregroundColor(Color.black)
                        .frame(width: (UIScreen.main.bounds.width - 60 - 10) / 2 ,
                               height: 50,
                               alignment: .center)

                    Text("Withdraw")
                        .foregroundColor(Color.white)
                        .font(Font.system(size: 20, design: .default))
                        .bold()
                }
            }
        }
    }
    ```
    ```swift
    /// 카드가 적용된 리스트뷰
    fileprivate struct HomeMyCardList: View {

        @Binding var isSeeAll: Bool
        @Binding var myCards: [HomeCardInfo]

        var body: some View {
            VStack {
                HStack {
                    Text("Cards")
                        .foregroundColor(Color.white)
                        .bold()
                    Spacer()
                    Button(action: {
                        self.isSeeAll.toggle()
                    }) {
                        Text("See All")
                            .foregroundColor(isSeeAll ? Color.white : Color.white.opacity(0.7))
                    }
                }
                ForEach(myCards) { card in
                    HomeCardInfoView(card: card)
                }
                .animation(.default)
            }
        }

    }
    ```
    ```swift
    /// 홈 화면에서 표시되는 카드 정보
    struct HomeCardInfoView: View {

        let card: HomeCardInfo

        var body: some View {
            ZStack {
                RoundedRectangle(cornerRadius: 10)
                    .foregroundColor(Color(red: 242/255,
                                           green: 244/255,
                                           blue: 248/255))
                    .frame(minWidth: 0,
                           idealWidth: UIScreen.main.bounds.width,
                           maxWidth: UIScreen.main.bounds.width)
                    .frame(height: 80)

                HStack {
                    RoundedRectangle(cornerRadius: 10)
                        .foregroundColor(Color.white)
                        .frame(width: 80, height: 50, alignment: .center)

                    VStack(alignment: .leading) {
                        Text(card.cardName)
                            .foregroundColor(Color.black)
                            .font(Font.system(size: 18, design: .default))
                            .bold()
                        Spacer()
                        Text("\(card.typeName) * \(card.frontCardNumber)")
                            .font(Font.system(size: 15, design: .default))
                            .foregroundColor(Color.black.opacity(0.5))
                    }
                    .frame(height: 50, alignment: .center)

                    Spacer()

                    Text("$\(card.money)")
                }
                .padding(.horizontal, 20)
            }
        }
    }
```
