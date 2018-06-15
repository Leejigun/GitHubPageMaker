---
layout: post
current: post
title: "IGListKit 가이드(2)- Action&relaodData"
date: 2018-04-06 00:00:00
cover: assets/images/IGListKit/profile.png
description: 1편에 이어서 이번에는 각각의 독립된 셀들의 이벤트를 관리하고 특정 셀을 갱신하는 방법에 대해서 알아보려 합니다.

navigation: True
tags: [ ios tip ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---

[이전 포스트](https://leejigun.github.io/IGListKit)에서는 IGListkit의 Model Binding의 개념을 살펴보고 데이터를 어떻게 설계하는지 고민해 봤습니다. Post라는 하 하나의 Post를 화면에 각각의 모델로 나눠서 여러 셀로 그려주면서 복잡할 수 있는 UI 구성을 단순하고 독립되게 표현할 수 있었습니다.
 독립된 셀을 구성하면서 외부의 요구사항에 맞춰서 간단하게 UI를 바꿀 수 있게 되었고, 많고 복잡한 데이터도 나눠서 처리할 수 있게 되었습니다. 다만, 각각의 모델과 셀로 나누면서 코드 파일을 만들고 작업 시간이 증가하는 단점이 있었지만. 각각의 데이터들이 결합성이 낮아졌기 때문에 복잡한 문제를 나눠서 간단하게 처리할 수 있어 유용한 방법이라 생각했습니다.

 이번에는 한 발짝 더 나아가 사용자와 셀의 상호작용을 통해 UI를 변경시키는 액션을 구현해 보겠습니다.

## Handling Cell Actions

 기억하시겠지만 우리가 만든 셀에는 좋아요 버튼을 누를 수 있는 Action Cell이 존재했습니다. 이 셀의 좋아요 버튼을 클릭하면 셀에 붙어있는 라벨의 좋아요 숫자가 올라가도록 하는 게 목표입니다.

 흐름을 생각해보면 좋아요 버튼을 누르면 그 액션이 `PostSectionController`까지 전달이 돼서 Post 객체의 데이터가 변동되고 그 변동된 데이터만큼 하위의 Cell이 변동되는 일련의 과정이 발생하기를 원합니다.

이를 위해서 **ActionCell.swift** 파일을 열어 아래와 같은 프로토콜을 추가합니다.

```
protocol ActionCellDelegate: class {
  func didTapHeart(cell: ActionCell)
}
```

그리고 ActionCell에 delegate를 추가합니다.

```
weak var delegate: ActionCellDelegate? = nil
```

그리고 `awakeFromNib()`을 오버라이드 하고 버튼에 액션을 추가합니다.

```
override func awakeFromNib() {
  super.awakeFromNib()
  likeButton.addTarget(self, action: #selector(ActionCell.onHeart), for: .touchUpInside)
}
```

버튼을 누르면 호출될 메소드 onHeart 를 추가합니다.

```
func onHeart() {
  delegate?.didTapHeart(cell: self)
}
```

  이 일련의 과정은 제가 안드로이드에서도 자주 사용했던 방법입니다. 인스타 그램에서 만든 예시도 이렇게 사용하는 것 보니 정석적인 방법인거 같습니다. `awakeFromNib`은 셀이 StoryBoard에서 읽어진 후 최초로 호출되는 메소드입니다. 보통 iOS 개발자 가이드 문서들을 보면 여기서 cell을 초기화 하는 동작을 수행하도록 했습니다.

 추가적으로  `prepareForReuse()`라는 메소드도 있는데 이름에서 알 수 있듯이 셀을 재사용 하기 전에 호출되는 메소드입니다. 셀을 초기화해야 할 필요가 있을 경우 여기서도 수행 할 수 있습니다.

 `onHeart`가 호출되면 delegate에 `didTapHeart`메소드를 실행시켜줍니다. 그렇다면 이 delegate에 왜 이벤트를 넘겨주는 것일까요? 바로 이 delegate는 `PostSectionController에 있는 델리게이트를 참조하고 있기 때문입니다.

 자 이제 `PostSectionController`에서 셀을 만든 후 delegate를 넘겨주도록 합시다.

```
// PostSectionController.swift
func sectionController(_ sectionController: ListBindingSectionController<ListDiffable>, cellForViewModel viewModel: Any, at index: Int) -> UICollectionViewCell {
...
    if let cell = cell as? ActionCell {
        cell.delegate = self
    }
...
}

// MARK: - ActionCellDelegate
extension PostSectionController: ActionCellDelegate {
    func didTapHeart(cell: ActionCell) {
        print("like")
    }
}
```

 `ActionCell` 의 `delegate`는 이제 `PostSectionController` 입니다. 따라서 `ActionCell`에서 이벤트를 넘겨주면 `PostSectionControlleer`에 있는 `didTapHeart`가 호출됩니다.

## Local Mutations

 우리는 저번 포스트에서 Post 모델을 디자인 할 때 안전한 디자인을 위해서 모든 내부 프로퍼티를 let으로 선언했다. let으로 선언된 프로퍼티는 변경될 수 없다. 그렇다면 우리는 어떻게 좋아요를 눌렀을 때 라벨의 숫자를 올라가게 할 수 있을까?

 인스타그램은 mutable locale variable을 사용해 이 문제를 해결했다. 먼저 **PostSectionController.swift** 파일에서 변수를 추가하자.

```
var localLikes: Int? = nil
```

그리고 좋아요 버튼을 누르면 이 변수에 1을 추가하자.

```
// MARK: - ActionCellDelegate
extension PostSectionController: ActionCellDelegate {
    func didTapHeart(cell: ActionCell) {
        // localLikes가 nil 이면 object?.likes 값을 찾아 꺼내보고 이것도 nil이면 0을 사용
        localLikes = (localLikes ?? object?.likes ?? 0) + 1
        update(animated: true, completion: nil)
    }
}
```

 이 경우 `localLikes`가  nil 이면 `object?.likes`를 꺼내온다. `object?.likes`는 절대 nil일 수 없다. 왜냐면 이미 `ActionCell`이 만들어져 클릭 이벤트가 넘어왔다는 것인데, nil이면 cell자체가 생길 수 없기 때문이다. 그저 컴파일러 경고를 무시하려 추가된 안전장치다.

 다음으로 `ListBindingSectionController`안에 있는`update(animated:,completion:)`를 호출하도록 했다. 이 메소드는 화면의 셀을 갱신하도록 한다.

 이제 `viewModelsFor` 에서 `localLikes`를 모델로 넘겨주면서 실제로 데이터를 변경 할 수 있게 되었다.

```
ActionViewModel(likes: localLikes ?? post.likes)
```



 이제 실제로 버튼을 눌러보면 숫자가 변하는 것을 볼 수 있다.

---

 인스타그램에서 제공하는 예제는 여기까지다. 하지만 여기서 몆가지 로직들을 더 추가해보자.



## Like Button

 지금 상태에서는 좋아요 버튼을 누르면 좋아요 숫자가 끝없이 올라간다. 이미 좋아요 버튼을 누른 적이 있으면 다른 상태값을 주고 좋아요 버튼을 또 누르면 좋아요가 해제되도록 해보자.

 먼저 `Post`에 좋아요 상태값을 내려주는 변수를 추가하자. 우리가 서버에서 Post 정보를 받아온다면 이 글에 사용자가 좋아요를 했는지 안 했는지 저장하고 있어야 한다. 그래야 비즈니스 로직 상 좋아요 숫자를 조작하는 행위를 막을 수 있다.

```
// Post.swift
let isClickedLikes:Bool
// ActionViewModel.swift
let isClickedLikes:Bool
```

 자 이제 ActionCell까지 데이터가 내려간다. 이제 `SectionController`까지 데이터가 넘어왔다. viewModel에 데이터를 넘겨 주기 전에 아까 `Likes`를 넘겨 주었던 일을 생각해보자. 변경 될 수 없는 데이터인 `Likes`를 넘겨주기 위해서 로컬 변수를 사용했었다. 똑같이 해본다.

```
var localIsClickedLikes:Bool? = nil
...
ActionViewModel(likes: localLikes ?? post.likes)
```

 그리고 자 이제 클릭 이벤트 쪽으로 내려가자. 클릭 여부를 확인해서 이미 클릭 했는데 이벤트가 오면 숫자를 1 뺴보자.

```
// MARK: - ActionCellDelegate
extension PostSectionController: ActionCellDelegate {
    func didTapHeart(cell: ActionCell) {
        // localLikes가 nil 이면 object?.likes 값을 찾아 꺼내보고 이것도 nil이면 0을 사용
        if localIsClickedLikes ?? object?.isClickedLikes ?? false {
            localLikes = (localLikes ?? object?.likes ?? 1) - 1
        } else {
            localLikes = (localLikes ?? object?.likes ?? 0) + 1
        }

        localIsClickedLikes = !(localIsClickedLikes ?? object?.isClickedLikes ?? false)

        update(animated: true, completion: nil)
    }
}
```



 이 외에도 IGListkit을 사용하면 간단하게 진행 할 수 있는 많은 기능들이 있다. 다음 포스트에서는 IGListkit의 샘플 예제를 살펴보고 유용한 기능들을 알아보자.
