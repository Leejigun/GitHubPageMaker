---
layout: post
current: post
navigation: True
title:  "[클린 소프트웨어] 애자일 설계"
date:   2023-07-20 00:00:01
cover: assets/images/CS/clean_software/2023-07-20-CleanSoftware_agile/agile.jpeg
description: "[클린 소프트웨어] 애자일 설계"
tags: [ cs ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---

# 애자일 설계

> 해당 포스트는 클린 소프트웨어를 읽고 정리한 내용입니다.
> 

좋은 소프트웨어를 만들기 위해서는 몇 가지 요소가 필요합니다.

(유연하고 유지보수 가능하며 재사용 가능한 좋은 구조)

### 잘못된 설계의 증상

해당 책에서는 잘못된 구조로 설계된 소프트웨어의 경우 다음과 같은 증상이 보여진다고 합니다.

1. 경직성: 설계를 변경하기 어려움
2. 취약성: 설계가 망가지기 쉬움
3. 부동성: 설계를 재사용하기 어려움
4. 점착성: 제대로 동작하기 어려움
5. 불필요한 복잡성: 과도한 설계
6. 불필요한 반복: 마우스 남용
7. 불투명성: 혼란스러운 표현

이러한 증상들은 클린 코드에서의 code smell과 비슷하지만, 좀 더 높은 설계 단계에서 보여지는 증상입니다.

### 악취와 원칙

앞서 소개한 잘못된 설계의 증상들을 제거하기 위해 SOLID 원칙을 소개하고 있습니다. 예를 들어 경직성의 악취는 대부분 개방 폐쇄 원칙(OCP)에 충분한 주의를 기울이지 않았기 때문에 발생합니다.

다만, 여기서 주의해야 할 점은 악취를 제거하기 위해 원칙을 적용하지만, 아무 악취가 없을 땐 어떠한 원칙도 적용하지 않는 것입니다. 원칙에 대한 맹종은 불필요한 복잡성이란 설계의 다른 악취로 이어질 수 있습니다.

## 악취

앞서 언급한 설계에서 발생하는 악취에 대해 좀 더 자세히 설명합니다.

1. 경직성

경직성은 소프트웨어를 변경하기 어려운 경향을 말합니다. 한 군데의 변경이 다른 모듈에 의존적이라 연쇄적으로 변경을 일으킬 때, 해당 설계는 융통성이 없는 설계로 볼 수 있습니다.

간단한 것처럼 보이는 변경을 요청받아 필요한 작업량을 추정하지만, 실제로 그 작업을 진행하면서 예상치 못한 곳에서 간접적으로 영향이 있다는 사실을 깨닫게 됩니다.

1. 취약성

취약성은 한 군데를 변경했을 때 프로그램의 많은 부분이 잘못되는 경향을 말합니다. 대부분의 경우 새로운 이슈는 변경한 영역과 개념적으로 아무런 관계가 없는 곳에서 발생합니다.

앞서 경직성과 마찬가지로 어느 한 부분의 수정이 전체에 영향을 미친다는 부분과 동일하지만, 경직성은 해당 부분을 수정하기 위해서 많은 관련 코드를 수정해야 하는 경우이고, 취약성은 어느 한 부분을 수정했는데, 다른 부분의 동작까지 영향을 미치는 경우를 뜻합니다.

쉽게 이해하기로는 경직성은 특정 부분을 수정했을 때 다른 곳에서 빌드 에러가 발생하는 것이고, 취약성은 QA 이슈가 발생하는 것이라 생각할 수 있을 것 같습니다.

1. 부동성

A 모듈이 B 시스템에서 유용하게 쓸 수 있는 부분이 있어서 재사용하고 싶지만, 해당 부분이 복잡하게 묶여있어 기존 시스템에서 분리하는데 수고와 위험성이 지나치게 클 때를 뜻합니다. 부동성이라 부르는 이유는 A 모듈을 B 모듈로 움직이게 해야하는데, 이동시킬 수 없기 때문에 움직일 수 없다는 뜻의 부동성을 사용하고 있습니다.

1. 점착성

점착성은 소프트웨어의 점착성과 환경의 점착성이라는 두 가지 형태로 나타납니다.

소프트웨어의 점착성은 무언가 변경사항이 있고, 설계를 유지하는 방법과 설계를 뜯어 고치는 방법이 있을 때 설계를 변경 사항을 적용하기 위해서 설계를 뜯어고치는게 더 쉽다면, 해당 소프트웨어의 구조는 점착성의 악취를 가지고 있다고 볼 수 있습니다. 점착성은 말 그대로 착 달라 붙어 있는 것으로 설계가 모든 부분에 착 달라붙어 무언가 수정이 필요할 때마다 설계를 뜯어 고치는게 쉬운 경우를 말합니다.

환경의 점착성은 이와 다르게 개발 환경이 느리고 비효율적일 때 발생합니다. 예를 들어서 컴파일 시간이 아주 길다면, 재컴파일이 적은 방법으로 변경하고 싶을 것입니다. 만약, 코드 관리 시스템에서 체크인하는데, 아주 많은 시간이 필요하다면, 적은 부분만 체크인 하고 싶을 것입니다.

양쪽 모두 소프트웨어의 설계를 유지하기 어려운 프로젝트입니다.

1. 불필요한 복잡성

현재 시점에 불필요한 요소가 포함된 설계를 뜻합니다. 흔히 요구사항에 대한 변경을 미리 예상하고, 잠재적인 변경을 처리하기 위해서 많은 기능을 집어넣을 때 자주 발생합니다.

처음에는 바람직해 보일 수 있지만, 필요없는 과도한 기능으로 구성 요소들이 어지러워 질 수 있고, 그로 인해 소프트웨어는 복잡하고 이해하기 어려워집니다.

1. 불필요한 반복

잘라내기와 붙여넣기는 작업 속도를 올려주는 아주 편리한 기능이지만, 자칫 몇십, 몇백 개의 반복된 코드 요소가 될 수 있습니다. 예를 들어서 A 코드를 복사해 B에서 조금 수정해 사용하고, B 코드를 복사해 C 에서 조금 수정해 사용하고를 반복하면 자칫 반복되는 코드가 엄청나게 쌓일 수 있고, A 부분의 수정을 위해서 B 부분 C 부분 수정이 필요 할 수 있고, 이 경우 유지보수하기 힘들게 됩니다.

2번 이상 사용할 시 공통화 하는 정책을 가져가도 좋습니다. 추상화를 통한 공통화를 통해서 해당 기능을 재사용하기 쉽게 할 수 있고, 테스트 코드 작성에도 쉽습니다.

1. 불투명성

모듈을 이해하기 어려운 경향을 말합니다. 시간이 지날수록 점점 더 코드가 이해하기 어렵고 불명료해지는 경향이 있습니다. 코드를 투명하게 유지하기 위해서는 지속적인 노력이 필요합니다.

따라서 개발자는 읽는 사람의 입장에서 생각하고 자신의 코드를 리팩토링하는 데 노력을 기울여 읽는 사람이 그것을 이해할 수 있도록 해야 합니다.

## 애자일 설계란?

결국 애자일 설계란 과정을 의미하는 것이지 결과를 의미하는 것은 아닙니다. 이것은 원칙, 패턴, 소프트웨어의 구조와 가독성을 향상하기 위한 방식의 연속적인 적용입니다. 모든 시점에서 시스템의 설계를 가능한 간단하고 명료하고 표현적으로 유지하려는 노력을 의미합니다.

매 순간 순간 악취를 캐치하고 원칙에 따라서 수정해 나가면, 클린 소프트웨어를 유지할 수 있습니다.