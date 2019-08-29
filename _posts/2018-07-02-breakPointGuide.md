---
layout: post
current: post
navigation: True
title:  "Edit Breakpoints in Xcode (번역)"
date:   2018-07-02 00:00:02
cover: assets/images/tdd/breakPoint.png
description: Edit Breakpoints in Xcode
tags: [ TDD ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---

# Edit Breakpoints in Xcode

 브레이크 포인트는 디버깅에 있어 중요한 역할을 하며, 함께 강력한 기능을 제공합니다. 다음은 디버깅 하는 동안 효율성을 높이기 위한 브레이크 포인트와 관련된 몇가지 팁입니다.

다음과 같이 루프에 대한 가 있다고 가정합니다.

```swift
var sum = 0
for i in 0...100 {
  sum += i
}
print(sum)
```

**Q: 저는 제가 60살이 되면 합계 가치를 알고 싶습니다. 어떻게 해야 할까요?**

 우리는 **조건**을 구성할 수 있습니다. 다음과 같은 단계가 있습니다.

1. 루프 내에 브레이크 포인트 설정
2. 브레이크 포인트를 더블 클릭하거나 마우스 오른쪽 버튼으로 클릭하고 **편집**을 선택합니다.
3. 조건에서 다음을 입력합니다.

![i==60](https://cdn-images-1.medium.com/max/800/1*CDd-8ynYOglKaYojibhfiQ.png)

 지금 우리는 현재 60에 해당하는 i를 더하기 전에 합계가 1770이라는 것을 안다. 우리는 그것을 단 한줄의 코드 없이도 얻을 수 있습니다. 꽤나 간단하죠?



**Q: 합계가 90보다 크거나 같은 경우에만 알고 싶습니다. 어떻게 해야할까?**

 조건 아래에 **무시**옵션이 있습니다.**무시**를 90으로 설정하면 90미만일 때 합계 값에 대해 걱정할 필요가 없습니다.

![ignore](https://cdn-images-1.medium.com/max/800/1*l_dv3Qm6fXqsRUy_cmYcjw.png)

 여기서 중단점은 내가 90까지 올랐을 때만 해당되고, 지금 이 순간에는 정확히 4005이다. 프로그램 실행을 계속하고 90보다 큰 해당 i를 사용하여 각 합계 값을 확인할 수 있습니다.



**Q:합계가 90보다 크거나 같은 경우에만 알고 싶습니다. 그러나 모든 합계 값을 한번에 확인할 수 있기를 바라면서 수동으로 프로그램 실행을 계속하고 싶지는 않습니다. 그런 방법이 있나요?**

 **작업 및 옵션**은 이 작업에만 해당됩니다. 다음 단계가 있습니다.

1. **무시**로 이동하여 이전과 같이 값을 90으로 설정합니다.

2 **AddAction**을 클릭하고 **`po sum`**를 채웁니다. 이는 합계 값을 인쇄함을 의미합니다.

**옵션**을 선택하면 **ignore**  를 충족한 후 모든 합계 값이 계속 출력됩니다.

추가적으로 브레이크 포인트의 트리거 되는 기능을 확인하려면 콘솔의 브레이크 포인트 이름에 **로그 메시지**로 작업을 추가합니다.

![](https://cdn-images-1.medium.com/max/800/1*8nR6Fh5g1hOaV_L2_Bcl3A.png)

 이제 브레이크 포인트의 기본적인 용도에 대해 배웠습니다.브레이크 포인트 또는 디버깅과 관련된 더 흥미로운 주제를 보려면 Apple의 디버깅 도구 페이지를 참조하는 것이 좋습니다.
