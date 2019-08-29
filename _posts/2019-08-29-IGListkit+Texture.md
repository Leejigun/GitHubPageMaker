---
layout: post
current: post
navigation: True
title:  "IGListkit + Texture 적용"
date:   2019-08-29 00:00:01
cover: assets/images/ios_tips/iglistkit_with_texture.jpg
description: 텍스쳐와 IGlistkit을 함께 사용 방법
tags: [ ios tip  ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---
# IGListkit+Texture 적용
 예전에 **Let us:Go** 에서 Texture에 대한 영상을 보고 이번 프로젝트에서 적용해봤습니다. 검색도 많이하고 이것 저것 시도도 많이 하며 적용했는데, 특히 제가 계속 써오던 IGListkit과 함께 사용하면 궁합이 아주 좋아서 소개해보려 합니다.

 IGListkit과 Texture를 함께 쓰는 예시가 그렇게 많지 않아서 처음 진입하려는 분들은 많이 힘들겁니다. 특히 Section header를 추가하는 경우에는 정말 아무리 찾아도 찾을 수 없어서 고생했습니다.
  이 포스트를 보시는 분들께 도움이 되면 좋겠습니다.


##   Texture

 처음 텍스쳐를 쓰게된 계기는 협업을 하는 도중에 다른 뷰 컨트롤러를 건들고 있지만, 파일은 하나의 스토리보드를 사용하기 때문에 계속 깃에서 충돌하는 문제가 있었습니다. 그래서 다른 파일에서 작업 후 옮기는 방법도 사용해봤는데, 스토리 보드 파일이 커지면서 어느 순간 이런 저런 에러들이 뜨면서 갱신이 안되는 문제가 발생했습니다.
 인터넷으로 여러 방법들을 해보면서 수정해봤지만 결국에는 또 발생하고 원천적으로 막는 방법을 찾지 못해서 고민하고 있다가 텍스쳐를 시도하게 되었습니다.


##  IGListKit

  IGlistkit을 사용하면서 단점이라고 생각했던 부분이 사전작업이 길다는 부분이었습니다. 셀을 만드는 부분까지는 문제 없는데, 셀의 사이즈를 사전에 정의해야 하기 떄문에 동적으로 사용하는데 번거로움이 있었고 뷰 모델을 셀에 맵핑하는 작업도 필요해서 간단하게 사용하기에는 오히려 오버스펙이라 생각했습니다.
  근데, 이 IGListkit을 Texture와 함께 사용하면 이러한 동작들이 상당히 간단해지고 화면 요소를 간단하게 재사용할 수 있어서 장점이 많습니다.


##   SectionController - Base

 앞서 말했듯이 IGListkit의 SectionController를 사용할 때에는 ListDiffable을 준수하는 뷰 모델을 토대로 셀의 사이즈와 셀을 반환해야 합니다. 이 셀의 사이즈를 구하고 셀을 반환하는 과정은 일반적인 리스트 형태의 화면에서는 크게 문제될 것이 없습니다.
 하지만 조금만 복잡해지면 데이터를 추가한 셀의 사이즈를 계산하는 로직이 들어가버리고 리스트 형태가 아닌 정적 화면에서 사용하는 경우에도 문제가 될 수 있습니다.
 ( 저는 IGListKit을 리스트 형태가 아닌 일반 화면에서도 유지 보수의 용이성을 위해서 바운스 없이 화면에 딱 맞게 IGListkit을 사용해서 화면을 구성하는 경우가 많았습니다.)
 하지만 Texture를 사용하면 이 두가지 로직을 Texture에 위임하고 사용하는 사람은 셀만 만들어주면 해결되는 경우가 많습니다.

```swift
    override func sizeForItem(at index: Int) -> CGSize {
      let size = ASIGListSectionControllerMethods.sizeForItem(at: index)
      return size
    }
    override func cellForItem(at index: Int) -> UICollectionViewCell {
      let cell = ASIGListSectionControllerMethods
        .cellForItem(at: index, sectionController: self)
      return cell
    }
```
  Texture에서 자체적으로 사이즈와 셀을 만들어서 반환해주기 때문에 모든 SectionController에서 이렇게 처리할 수 있습니다.
  그 대신에 텍스쳐에서 콜렉션뷰 셀을 대신하는 **ASCellNode** 을 반환하는 메소드만 지정해주면 해결됩니다.

  그래서 저는 이 중복되는 부분을 대신하는 **BaseSectionController** 를 만들어 사용하고 있습니다.

```swift
    class BaseASListSectionController: ListSectionController, ASSectionController {
        /// ViewModel
        var object: Any?

        override func didUpdate(to object: Any) {
            self.object = object
        }
        override func sizeForItem(at index: Int) -> CGSize {
            let size = ASIGListSectionControllerMethods.sizeForItem(at: index)
            return size
        }
        override func cellForItem(at index: Int) -> UICollectionViewCell {
            let cell = ASIGListSectionControllerMethods
              .cellForItem(at: index, sectionController: self)
            return cell
        }

        // MARK: - ASSectionController

        func nodeBlockForItem(at index: Int) -> ASCellNodeBlock {
            fatalError(" Must implements this Method ")
        }

        func nodeForItem(at index: Int) -> ASCellNode {
            fatalError(" Must implements this Method ")
        }
    }
```


##  실제 사용

 이번 프로젝트에서 배송조회 화면에서 사용한 섹션 컨트롤러 입니다.

```swift
     class TrackingDetailSectionController: BaseASListSectionController {

        // MARK: - ASSectionController

        override func nodeBlockForItem(at index: Int) -> ASCellNodeBlock {
            return { [weak self] in
                guard let `self` = self else { return ASCellNode() }
                return self.nodeForItem(at: index)
            }
        }
        override func nodeForItem(at index: Int) -> ASCellNode {

            if let viewModel = object as? TrackingDetailItemViewModel {
                return TrackingDetailItemCellNode(viewModel)
            } else if let viewModel = object as? TrackingDetailDeliveryViewModel {
                return TrackingDetailDeliveryCellNode(viewModel)
            } else if let viewModel = object as? TrackingDetailPaymentViewModel {
                return TrackingDetailPaymentCellNode(viewModel)
            } else {
                return ASCellNode()
            }
        }
    }
```
 셀을 만들고 사이즈를 반환하는 IGListkit의 메소드들은 앞서 보셨다시피 **BaseASListSectionController** 에서 텍스쳐로 위임했기 때문에 개발자는 들어온 뷰 모델을 토대로 **ASCellNode** 를 반환하면 해결되기 때문에 상당히 간략합니다.
 데이터를 넣고 셀을 만드는 과정은 일반적인 텍스쳐에서 테이블뷰나 콜렉션뷰를 사용하는 방법과 동일하기 때문에 검색하시면 금방 찾으실 수 있습니다.

 특히 저는 텍스쳐를 공부할 때 아래 사이트를 많이 참고했습니다.
 https://texture-kr.gitbook.io/wiki/



----------

 텍스쳐를 사용하면서 개발 속도와 안전성 등에서 큰 발전이 있었습니다. SwiftUI가 앞으로 대체하리라 예상하지만, 구글의 Flutter를 함께 공부해보면 아직 SwiftUI는 너무나도 미약하고 불편한 수준입니다.
 SwiftUI가 정식으로 적용되더라고 iOS13 이상 적용 가능하며 많이 미약함으로 실제로 적용하기까지는 오랜 시간이 걸리리라 생각합니다.
 Texture는 SwiftUI의 사용이 보편화되기 전까지 사용하는데 무리가 없고 UIkit과 함께 사용가능한 부분에서 굉장히 유용합니다.
 특히 IGListkit과 함께 사용하면 간단하게 코드를 재사용할 수 있기 때문에 앞으로도 사용할 예정이며 여러가지 팁을 포스팅할 예정입니다.
