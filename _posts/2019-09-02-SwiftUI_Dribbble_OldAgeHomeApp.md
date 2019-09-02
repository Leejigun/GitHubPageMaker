---
layout: post
current: post
navigation: True
title:  "SwiftUI 화면 만들기 - Old Age Home App"
date:   2019-09-02 00:00:01
cover: assets/images/SwiftUI/oldAgeHomeApp.png
description: SwiftUI 앱 디자인 테스트
tags: [ swiftui ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---

# SwiftUI 화면 만들기 - Old Age Home App


https://dribbble.com/shots/7074019-Old-Age-Home-App



##  원본
![](https://paper-attachments.dropbox.com/s_0C5B5B0D688EBF9B5C8128D090AEE98920DCD8C81B9D089DF1E9F05DFF470BDD_1567387551103_image.png)

----------
##  인트로 화면 구현


![](https://paper-attachments.dropbox.com/s_0C5B5B0D688EBF9B5C8128D090AEE98920DCD8C81B9D089DF1E9F05DFF470BDD_1567387614121_image.png)





-  화면 전체를 덮는 이미지, 상 하단 세이프 에어리어 무시
-  상단 앱 제목과 설명 노출
-  하단 시작 버튼

 배경 전체를 덮는 이미지는 대충 고화질 이미지를 받아서 전체를 덮도록 적용
 하단 Get Start 상자를 클릭시 메인 화면으로 진입하도록 버튼 적용













----------
## 인트로 구현 코드
    struct GetStartView: View {
      var body: some View {

        ZStack(alignment: .top) {

          Image("oldPeople")
            .resizable()
            .edgesIgnoringSafeArea(.top)
            .edgesIgnoringSafeArea(.bottom)
            .edgesIgnoringSafeArea(.leading)
            .edgesIgnoringSafeArea(.trailing)
            .scaledToFill()

          VStack {
            VStack {
              Text("Care app")
                .font(Font.system(size: 60, design: .default))
                .foregroundColor(Color(red: 255/255, green: 247/255, blue: 225/255))
                .padding(.top, 50)

              Text("we take care of parents, Those don't care")
                .foregroundColor(Color(red: 255/255, green: 247/255, blue: 225/255))
            }

              Spacer()

              VStack(alignment: .trailing) {

              ZStack(alignment: .center) {
                RoundedRectangle(cornerRadius: 15)
                .frame(width: 150, height: 50, alignment: .center)
                .foregroundColor(Color.yellow)

                Text("Get Start")
                .bold()
              }
            .padding(.trailing, 20)
            }
          .frame(width: UIScreen.main.bounds.width, alignment: .trailing)
          }
        }

      }
    }
![](https://paper-attachments.dropbox.com/s_0C5B5B0D688EBF9B5C8128D090AEE98920DCD8C81B9D089DF1E9F05DFF470BDD_1567392051507_image.png)

----------
## 트러블 슈팅

 상단 스테이터스바의 스타일을 변경하는 방법을 몰라서 검색해 봤는데, View 자체에서는 불가능하고 UIHostingController를 추가적으로 커스텀해서 스타일을 변경해야 하는 것으로 확인했다.
 (https://stackoverflow.com/questions/57063142/swiftui-status-bar-color)

 그런데, 화면마다 테마를 변경해야 하는 경우에는 어떻게 해야하는지 모르겠다.


     class DarkHostingController<Content>:
      UIHostingController<Content> where Content : View {
      @objc override dynamic open var preferredStatusBarStyle: UIStatusBarStyle {
          .lightContent
      }
    }


----------
## 메인 화면 구현
![](https://paper-attachments.dropbox.com/s_0C5B5B0D688EBF9B5C8128D090AEE98920DCD8C81B9D089DF1E9F05DFF470BDD_1567406850296_image.png)




- 상단에 배경화면과 그 배경화면을 절반정도 거쳐서 검색 바
- 하단으로 리스트 뷰
- 리스트 뷰 안에 카드 뷰

















----------


    ScrollView{
      VStack {
      // 상단 배경 이미지
      Rectangle()
      .foregroundColor(Color.yellow)
      .frame(width: UIScreen.main.bounds.width, height: UIScreen.main.bounds.width * 0.5)

      // 중단 검색 바
      ZStack(alignment: .center) {
      RoundedRectangle(cornerRadius: 30)
        .foregroundColor(Color.white)
        .frame(minWidth: 0,
        idealWidth: UIScreen.main.bounds.width,
        minHeight: 50,
        maxHeight: 50)
        .shadow(radius: 1)

        HStack {
          TextField($text, placeholder: Text("find more...")
            .foregroundColor(Color.gray))
          Image(systemName: "magnifyingglass")
        }
        .padding(.horizontal)
      }
      .padding(.top, -20)
      .padding(.horizontal)

      // 하단 리스트
      ForEach(0...20) {_ in
        HStack {
          MainCardView()
          Rectangle()
            .foregroundColor(Color.clear)
            .frame(width: 20)
          MainCardView()
        }
        .padding(.horizontal)
        Rectangle()
          .foregroundColor(Color.clear)
          .frame(width: 20)
        }
      }
    }
    .edgesIgnoringSafeArea(.top)


![](https://paper-attachments.dropbox.com/s_0C5B5B0D688EBF9B5C8128D090AEE98920DCD8C81B9D089DF1E9F05DFF470BDD_1567409965475_image.png)
![](https://paper-attachments.dropbox.com/s_0C5B5B0D688EBF9B5C8128D090AEE98920DCD8C81B9D089DF1E9F05DFF470BDD_1567409979122_image.png)


 하단 카드뷰

    struct MainCardView: View {
      var body: some View {
        ZStack(alignment: .center) {
          RoundedRectangle(cornerRadius: 30)
            .foregroundColor(Color.white)
            .shadow(color: Color.black.opacity(0.5), radius: 1, x: -0.2, y: 1)

          VStack {
            Rectangle()
              .foregroundColor(.yellow)
              .padding()

            VStack(alignment: .leading) {
              Text("Adopt")
                .font(.headline)
              Text("Adopt & Adopt & Adopt")
                .font(.caption)
            }
            .padding()
          }
        }
        .frame(width: (UIScreen.main.bounds.width / 2) - 50,
        height: ((UIScreen.main.bounds.width / 2) - 50) * 1.5,
        alignment: .center)
      }
    }
