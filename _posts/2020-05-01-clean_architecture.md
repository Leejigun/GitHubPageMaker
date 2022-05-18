---
layout: post
current: post
navigation: True
title:  "클린 아키텍처 (Data-Domain-Presentation)"
date:   2020-05-01 09:05:00
cover: assets/images/CS/the-clean-architecture.png
description: 클린 아키텍처 (Data-Domain-Presentation)
tags: [ cs ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---

# 클린 아키텍처 (Data-Domain-Presentation)

Created: May 1, 2020 9:05 PM
Tags: NotUploaded, iOS

최근 회사 발표에서 아키텍처에 대한 내용이 언급되었다. 여기 회사에 와서 당황했던 부분이 지금까지 혼자서 프로젝트를 관리할 때와 너무 달라서 뭐가 어디에 있는지 찾기 힘들었다. 8명이라는 인원이 한 프로젝트를 관리하기 때문에 분명 명확한 기준이 있는 것 같은데, 그 기준을 잘 몰랐었다. 그러다 살짝 언급된 Presentation - Domain - Data 로 묶여있는 Layer에 대한 내용을 보고 이에 관해서 공부하려 한다.

 소프트웨어 공학에서 앱을 개발할 때 디자인 패턴과 아키텍처 패턴을 사용하는 건 중요하다. 나는 지금까지 MVVM 패턴을 사용하면서 View - View Model - Model 으로 폴더를 나누고 관리했었다. 그러면서 항상 생각했던 부분이 각각의 부분이 다른 폴더에 있어서 너무 사용하기 힘들었다. 항상 이렇게 나누는 게 맞는 건지 고민했었는데, 알려줄 사람이 없었다.

 iOS Clean Architecture MVVM 샘플 프로젝트:

[kudoleh/iOS-Clean-Architecture-MVVM](https://github.com/kudoleh/iOS-Clean-Architecture-MVVM)

---

## Clean Architecture in MVVM

![assets/images/CS/clean_architecture/Untitled.png](assets/images/CS/clean_architecture/Untitled.png)

 클린 아키텍처 그래프에서 보면 알 수 있듯이, 각각 각각의 기능이 레이어에 따라서 나뉘어 있다. 제일 중요한 규칙은 내부 계층에서 외부 계층으로 종속성을 갖지 않는 것이다. 안쪽에 있는 방향으로만 의존을 가지고 있어야 한다. 붉은 색 화살표가 의존성을 가지는 방향을 표현한다.

**Dependency rule**

[Clean Coder Blog](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

### 종속성 방향

![assets/images/CS/clean_architecture/Untitled%201.png](assets/images/CS/clean_architecture/Untitled%201.png)

## Domain Layer - Business logic

 도메인 계층은 가장 안쪽에 위치하고 있다. 위에서 말했듯이 의존성은 안쪽으로만 존재하기 때문에 제일 안쪽에 있는 도메인 계층은 다른 계층에 의존하지 않고 완전히 격리된다.

 여기에는 엔티티(비즈니스 로직), 유스케이스 그리고 인터페이스가 있다. 이 계층은 다른 계층과 완전히 분리되어 있기 때문에 다른 프로젝트에서 재사용 할 수 있다. 이러한 의존성 분리를 통해서 호스트 앱을 사용하지 않고 유닛 테스트를 쉽게 구축할 수 있다.

 UseCase가 뭔지 감이 잘 안오는데, 비지니스 로직이 여기 들어간다 한다.

 **도메인 계층은 다른 계층의 어떤 것도 포함하면 안 된다.**

## Presentation Layer - UI

 프레젠테이션 계층에는 ViewController나 View 같은 UI 컴포넌트가 위치한다. View는 하나 이상의 UseCase를 실행하는 VIewModel을 통해서 조정된다. MVVM의 경우 ViewModel도 여기에 해당한다.

 **프레젠테이션 계층은 도메인 계층에만 의존한다.**

## Data Layer

 데이터 계층에는 레포지토리 구현과 많은 데이터 소스를 통해서 구성된다. 레포지토리는 서로 다른 데이터 소스의 데이터를 조정하는 역할을 한다. 데이터 소스는 로컬 DB나 서버일 수 있다. 데이터 계층은 도메인 계층을 의존한다.

 필요에 따라 네트워크 JSON 데이터를 맵핑하는 모델을 도메인 계층에 추가할 수 있다.

### 데이터 플로우

![assets/images/CS/clean_architecture/Untitled%202.png](assets/images/CS/clean_architecture/Untitled%202.png)

1. VIew는 ViewModel에 있는 메소드를 호출한다.
2. ViewModel은 UseCase를 실행한다.
3. UseCase는 User와 Repositories를 결합한다.
4. 각각의 Repositories는 서버, DB 등의 데이터 소스에서 데이터를 가져온다.
5. Data는 다시 화면을 표시하기 위해 View 쪽으로 흘러간다.

---

### 의존성 방향

**Presentation Layer → Domain Layer ← Data Repositories Layer**

프레젠테이션 레이어와 데이터 레이어가 도메인 레이어를 의존한다.

MVVM에서의 각각의 레이어에 해당하는 항목들은 다음과 같다.

- Presentation Layer = ViewModel + View
- Domain Layer = Entities + Use Case + Repositories Interface
- Data Layer = Repositories Implementations + API(Network) + DB

### 참고 자료:

[Clean Architecture and MVVM on iOS](https://tech.olx.com/clean-architecture-and-mvvm-on-ios-c9d167d9f5b3)

[Clean Coder Blog](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
