---
layout: post
current: post
navigation: True
title:  "SwiftUI 화면 만들기 - Challenges App"
date:   2019-08-28 00:00:01
cover: assets/images/SwiftUI/challengesApp.png
description: SwiftUI 앱 디자인 테스트
tags: [ swiftui ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---
# SwiftUI 화면 만들기 - Challenges App

- 이미지 출처: https://dribbble.com/shots/7047168-Challenges-App

##  원본



![](https://paper-attachments.dropbox.com/s_619B197BA64A8385C25262FF40C7091481BBE02E7B9BA78EA2EB3D5FB5A5ECE2_1566886774253_image.png)



----------
## 1. 화면 분석

 **상단**

- 전형적인 SwiftUI의 네비게이션 뷰 형태
-  타이틀을 제외하고 오른쪽에 검색 버튼

**중단**

-  횡 스크롤의 ListView 사용
-  카드 이미지는 새로 비율 구성

**하단**

-  하단으로 길어지는 ListView 사용
-  왼쪽의 가이드 라인은 Rect로 그리기


![](https://paper-attachments.dropbox.com/s_619B197BA64A8385C25262FF40C7091481BBE02E7B9BA78EA2EB3D5FB5A5ECE2_1566886810679_image.png)





----------
## 2. 상단
- 전형적인 SwiftUI의 네비게이션 뷰 형태
-  타이틀을 제외하고 오른쪽에 검색 버튼


![](https://paper-attachments.dropbox.com/s_619B197BA64A8385C25262FF40C7091481BBE02E7B9BA78EA2EB3D5FB5A5ECE2_1566983794613_image.png)
![](https://paper-attachments.dropbox.com/s_619B197BA64A8385C25262FF40C7091481BBE02E7B9BA78EA2EB3D5FB5A5ECE2_1566984028659_image.png)


  왼쪽 오른쪽 네비게이션 바의 버튼을 만들어 추가했습니다.
```swift
    /// 왼쪽 네비게이션 버튼
    struct LeadingNaviView: View {
      var body: some View {
        Image(systemName: "line.horizontal.3")
        .resizable()
        .scaledToFit()
        .padding(.top, 15)
        .padding(.trailing, 20)
        .padding(.bottom, 10)
        .frame(width: 50, height: 50, alignment: .center)
      }
    }

    /// 오른쪽 네비게이션 버튼
    struct TrailingNavView: View {
      var body: some View {
        Image(systemName: "person")
        .resizable()
        .scaledToFit()
        .padding()
        .frame(width: 50, height: 50, alignment: .center)
        .foregroundColor(Color.white)
        .background(Color.black)
        .cornerRadius(15, antialiased: true)
      }
    }
```
이벤트는 따로 추가하지 않았습니다. 여기까지는 별 문제 없이 생성해서 추가했습니다.
```swift
    .navigationBarItems(leading: LeadingNaviView(),
                        trailing: TrailingNavView())
```
 근데 타이틀이 문제인게 **.navigationBarTitle()** 로 만들어서 추가해주면 똑같은 형태로 보여주기는 하지만 오른쪽에 있는 검색 버튼을 추가 할 수 없었습니다.
```swift
     public func navigationBarTitle(_ title: Text) -> some View
```
 그래서 상단 타이틀을 커스텀해서 타이틀 뷰를 만들어서 해결했습니다.
```swift
     struct TitleView: View {

            @Binding var isSearch: Bool

            let title: String = "Home"

            var body: some View {
                HStack {
                    Text(self.title)
                        .font(Font.system(size: 30, design: .default))
                        .bold()

                    Spacer()
                    Button(action: {
                       self.isSearch = true
                    }) {
                        Image(systemName: "magnifyingglass")
                            .resizable()
                            .frame(width: 30, height: 30, alignment: .center)
                            .scaledToFit()
                            .foregroundColor(.secondary)
                    }
                }
                .padding(.leading, 20)
                    .padding(.trailing, 20)
            }
        }
```
 여기서 오른쪽 검색 버튼에 적용된 **isSearch** 는 검색 버튼을 누르면 검색 바로 변경하기 위해서 적용했습니다. 검색을 해도 이렇다할 기능은 없지만 화면 만드는 김에 만들어 봤습니다.

```swift
    if isSearching {
      SearchBar(searchText: $searchWord, isSearching: $isSearching)
    } else {
      TitleView(isSearch: $isSearching)
    }
```


![](https://paper-attachments.dropbox.com/s_619B197BA64A8385C25262FF40C7091481BBE02E7B9BA78EA2EB3D5FB5A5ECE2_1566984409995_image.png)
![](https://paper-attachments.dropbox.com/s_619B197BA64A8385C25262FF40C7091481BBE02E7B9BA78EA2EB3D5FB5A5ECE2_1566984424981_image.png)


 이 때 **Button** 으로 이미지를 감싸면 이미지가 버튼의 틴트 컬러를 적용받아서 파란색으로 변경되는데, 이를 막기 위해서 **.foregroundColor(.secondary)** 를 추가해주면 원래의 색상으로 돌아옵니다.
 그리고 여기서 사용하는 시스템 이미지들은 iOS 13에 추가된 이미지들로 **SF Symbols** 로 검색하면 찾을 수 있습니다.

 검색바는 SwiftUI에선 SearchBar가 따로 없기 때문에 적당하게 만들어 줍니다.
```swift
    struct SearchBar : View {

      @Binding var searchText: String
      @Binding var isSearching: Bool

      var body: some View {

        ZStack {

          RoundedRectangle(cornerRadius: 20)
          .frame(width: UIScreen.main.bounds.width - 40, height: 30)
          .foregroundColor(Color.gray.opacity(0.1))

        HStack {
            Image(systemName: "magnifyingglass").foregroundColor(.secondary)

            TextField($searchText,
            placeholder: Text("Search"),
            onEditingChanged: { _ in },
            onCommit: {
              UIApplication.shared.keyWindow?.endEditing(true)
              self.isSearching = false
            })

            Button(action: {
              self.searchText = ""
            }) {
              Image(systemName: "xmark.circle.fill")
              .foregroundColor(.secondary)
              .opacity(searchText == "" ? 0 : 1)
            }
          }
          .padding(.leading, 10)
          .padding(.trailing, 10)
        }
        .padding(.leading,20)
        .padding(.trailing, 20)
        .padding(.bottom, 30)
      }
    }
```
 저기서 잘 보면 text가 길어지면 자동으로 삭제 버튼이 나타나며 삭제 버튼을 클릭하면 text를 “”로 바꾸는 로직이 있는데 실제로 돌려보면 반응하지 않습니다.


## 3. 중단
-  횡 스크롤의 ListView 사용
-  카드 이미지는 새로 비율 구성



![](https://paper-attachments.dropbox.com/s_619B197BA64A8385C25262FF40C7091481BBE02E7B9BA78EA2EB3D5FB5A5ECE2_1566984915416_image.png)


횡으로 스크롤되는 카드뷰 형태의 아이템입니다.

```swift
    ScrollView(.horizontal, showsIndicators: false) {
      HStack {
        ForEach((1...20).reversed(), id: \.self) { _ in
          HomeCardView()
        }
      }
      .padding(.leading, 20)
      .padding(.trailing, 20)
    }
    .padding(.top, 30)
    .padding(.bottom, 30)
    .frame(height: (UIScreen.main.bounds.width - 40 ) * 0.5)
```
 일단 sample에는 20개 횡으로 붙여놨습니다만, 실제는 ListView를 사용해서 횡으로 붙여햐 합니다.

```swift
    struct HomeCardView: View {

      let text: String = "The future of healthy lifestyle."

      var body: some View {
        ZStack(alignment: .topLeading) {
          RoundedRectangle(cornerRadius: 20)
          .foregroundColor(Color.orange)

          VStack(alignment: .leading) {
            Text(self.text)
            .foregroundColor(Color.white)
            .font(Font.system(size: 30, design: .default))
            .bold()
            .lineLimit(4)
            .frame(width: 150)

            Spacer()

            Text("Read")
            .font(Font.system(size: 15, design: .default))
            .foregroundColor(Color.white)
            .underline()
          }
          .padding(20)
        }
        .frame(width: UIScreen.main.bounds.width - 80, height: (UIScreen.main.bounds.width - 40 ) * 0.5, alignment: .center)
      }
    }
```
 **RoundedRectangle** 로 배경 카드뷰를 만들고 그리고 **ZStack** 으로 안쪽에 데이터를 넣었습니다.
 **Tex**t에 **lineLimit** 을 넣지 않으면 …으로 짤리게 되기 때문에 4줄까지 표현하도록 처리했습니다.
 하단에 Read 버튼은 지금은 아무런 이벤트도 넣지 않았지만 Button으로 감싸서 화면 전환 이벤트 같은 것을 추가할 수 있습니다.


## 4. 하단
-  하단으로 길어지는 ListView 사용
-  왼쪽의 가이드 라인은 Rect로 그리기
![](https://paper-attachments.dropbox.com/s_619B197BA64A8385C25262FF40C7091481BBE02E7B9BA78EA2EB3D5FB5A5ECE2_1567042197102_image.png)
![](https://paper-attachments.dropbox.com/s_619B197BA64A8385C25262FF40C7091481BBE02E7B9BA78EA2EB3D5FB5A5ECE2_1567042207333_image.png)



```swift
    struct DayListCardView: View {

      var body: some View {
        HStack(alignment: .center) {
          ZStack(alignment: .center) {
            Circle()
            .frame(width: 20, height: 20, alignment: .center)
            .foregroundColor(Color.black)
            Circle()
            .frame(width: 7, height: 7, alignment: .center)
            .foregroundColor(Color.white)

          }
          .padding(30)

          Spacer()

          ZStack(alignment: .leading) {
            RoundedRectangle(cornerRadius: 20)
            .foregroundColor(Color.gray.opacity(0.1))

            HStack {
              Image(systemName: "hare")
              .resizable()
              .background(Color.gray.opacity(0.5))
              .frame(width: 70, height: 70)
              .cornerRadius(20)
              .scaledToFit()
              .padding(.leading, 15)

              VStack(alignment: .leading) {
                Text("Hydration")
                .font(Font.system(size: 20, design: .default))
                .bold()
                .padding(.top, 5)
                Spacer()
                Text("200 ml")
                .font(Font.system(size: 15, design: .default))
                .padding(.bottom, 5)
            }

            Spacer()

            Text("06:00 AM")
            .padding(.trailing, 10)
          }
          .frame(height: 70)

          }
        .frame(minWidth: 0, maxWidth: UIScreen.main.bounds.width, idealHeight: 100, maxHeight: 100)
        }
      }
    }
```
 똑같이 카드뷰 형태로 감싸서 만들었습니다. 여기서 특이사항은 원 두개를 ZStack으로 겹쳐서 검은 원에 흰색 구멍이 있는 것처럼 표현한 것인데 크게 어려운 부분은 아니라 생각됩니다.
 번거로워서 넘어간 부분이 하단이나 상단으로 라인을 그리는 부분인데 이거는 크게 어려운 부분이 아닐테니 넘어가도록 하겠습니다.
