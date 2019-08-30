---
layout: post
current: post
navigation: True
title:  "RxSwift+Moya+MVVM 1) 현업 RxSwift - 네트워킹 처리"
date:   2019-08-29 00:00:01
cover: assets/images/RxSwift/RxSwift_MVVVM_Moya.jpg
description: 실제 현업에서 사용하고 있는 RxSwift와 Moya를 이용한 네티워크 로직
tags: [ RxSwift  ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---
# 현업 RxSwift + Moya - 네트워킹 처리
 저번 포스트에서 제가 실제로 사용하고 있는 RxSwift+MVVM 코드를 살펴봤습니다. 장바구니 화면이었는데, 네트워크 없이 로컬 DB를 사용하고 있는 부분이라 크게 복잡한 게 없었습니다.
 이번 포스트에서는 Moya를 통한 네트워크 통신을 적용한 코드 부분을 공유하려고 합니다.

##  개요

 화면은 실제 서비스 하는 앱이라 실제 화면을 보여드리기는 힘들거 같아서 제가 그냥 손으로 그려서 글과 함께 설명하겠습니다.

![](https://paper-attachments.dropbox.com/s_99D04CF0394BDDE57A7192F243FD57A382078ADA78559AE7642D731E45277DD7_1567131263862_image.png)



  여기서 보여드릴 코드는 체중 상세 페이지입니다.
    상단에 하나의 차트가 있고 이 차트는 상단 세그 컨트롤러를 이용해서 최근, 전체 데이터를 보여줍니다.
      하단에는 오전, 오후 체중을 표시하며 없으면 클릭 시 입력할 수 있는 팝업을 보여주는 버튼으로 사용하고 있습니다.    차트 데이터를 읽어오는 API의 경우에는 하나의 API를 파라미터로 최근, 전체를 불러오도록 나뉘어 있어서 처음 화면을 들어갈 때 찌르는 API만 3개입니다. (최근 차트, 전체 차트, 금일 오전 오후 체중)





----------


## 구조 잡기

 저번 포스트에서 MVVM 구조 잡는 방법을 설명했었는데, 요는 Input과 Output을 분리하는데 있었습니다.



![](https://paper-attachments.dropbox.com/s_99D04CF0394BDDE57A7192F243FD57A382078ADA78559AE7642D731E45277DD7_1567132520234_image.png)


 **Input**

-  차트 데이터 요청
-  오전, 오후 체중 등록, 수정 삭제

**Output**

-  최근 차트 데이터
-  전체 차트 데이터
-  금일 차트 데이터


 데이터 베이스가 서버단이라 모든 input에 대한 결과값이 Output으로 화면에 그려지게 되는 구조입니다. 이 포스트에서 알려드리고 싶은 네트워크 예시로 적당한거 같아 이 화면을 택했습니다.


----------
##  Input 로직

 제가 만든 커스텀 Moya Provider는 다른 포스트에서 설명하고 일단 Input으로 Output 까지 가공하는 네트워크 RxSwift 블록을 보여드리겠습니다.

```swift
    // 차트 데이터 API
    input.chartData
      .do(onNext: { _ in output.isLoading.accept(true)})
      .flatMapLatest { fddDate -> Observable<(Result, Result)> in
        // parameters
        let recentParam = ["fddDate": fddDate,"keyword" : "recent"]
        let totalParam = ["fddDate": fddDate]

        // 최근 차트 데이터
        let recent = provider.rx
          .request(.searchFoodDiaryWeightList(recentParam))
          .retry(3)
          .asObservable()
          .map { WeightDetailViewControllerModel.checkStatusCode($0) }
          .map { result -> Result in
            if case let .success(anyData) = result, let data = anyData as? Response {
            return Result.success(try data.map(WeightChartResponse.self))
            } else {
            return result
            }
          }.catchError {
            Crashlytics.sharedInstance().recordError($0)
            return Observable.just(Result.fail(.jsonMappingError($0)))
          }
        // 전체 차트 데이터
        let total = provider.rx
          .request(.searchFoodDiaryWeightList(totalParam))
          .retry(3)
          .asObservable()
          .map { WeightDetailViewControllerModel.checkStatusCode($0) }
          .map { result -> Result in
            if case let .success(anyData) = result, let data = anyData as? Response {
            return Result.success(try data.map(WeightChartResponse.self))
            } else {
            return result
            }
          }.catchError {
            Crashlytics.sharedInstance().recordError($0)
            return Observable.just(Result.fail(.jsonMappingError($0)))
          }
        return Observable.combineLatest(recent, total)
      }
      .do(onNext: {_ in output.isLoading.accept(false)})
      .bind(to: output.chartResults)
      .disposed(by: disposebag)
```
 길고 복잡해 보이지만 사실 간단합니다.
 먼저 **input.chartData** 에 onNext(param)이 들어오면 로직 시작과 끝에 있는 **.do(onNext: {})** 부분에서 로딩의 시작과 끝을 알려주고 **viewController** 에서 이 **isLoading** 을 보고 있다가 로딩을 해줍니다.
 로딩을 시작하고 종료하는 행위는 전체 로직과 상관없는 사이드 이펙트이기 때문에 **do** 부분에서 처리합니다.
 그리고 크게 보면 한번의 input으로 두개의 독립된 api 통신을 수행해야합니다. 그래서 recent 로직과 total 로직을 만들고 CombineLatest로 묶어서 믿으로 내렸습니다.

 그 중에서 최근 차트 데이터를 요청하는 부분만 확인해 봅시다.
```swift
    // 최근 차트 데이터
    let recent = provider.rx
      .request(.searchFoodDiaryWeightList(recentParam))
      .retry(3)
      .asObservable()
      .map { WeightDetailViewControllerModel.checkStatusCode($0) }
      .map { result -> Result in
        if case let .success(anyData) = result, let data = anyData as? Response {
        return Result.success(try data.map(WeightChartResponse.self))
        } else {
        return result
        }
      }.catchError {
        Crashlytics.sharedInstance().recordError($0)
        return Observable.just(Result.fail(.jsonMappingError($0)))
      }
```

provider.rx.request 부분은 Moya에 대한 부분이니까 넘어가고 **retry(3)** 은 재시도 3회를 의미합니다. status code 200에서 299까지는 성공이라고 보고 기타 사유는 자동으로 3회까지 재시도 합니다. 이 것 말고도 **timeout** 10초도 적용해뒀는데, 그건 제가 만든 **커스텀 provider** 안에 있습니다.
( **retry** 만 예외적으로 비지니스 로직상 밖으로 빼놨습니다.)
 그리고 다음줄에서 status code를 체크하는 부분이 있습니다. 이번 프로젝트에서는 일부 api 통신에 대한 결과값으로 status code를 보고 처리하는 케이스가 있습니다. 여기서는 204의 경우 데이터 없음으로 보고 있습니다.

```swift
    static func checkStatusCode(_ response: Response) -> Result {
      switch response.statusCode {
        case 204:
          return Result.fail(.noContent)
        case 200...299:
          return Result.success(response)
        default:
          return Result.fail(.statusCodeError(response.statusCode))
      }
    }
```
 그리고 다음 map에서는 response를 codable을 사용해서 모델로 파싱하는 부분입니다. 예전 포스트에서도 썼듯이 RxSwift와 Moya, Codable을 함께 사용하면 복잡한 로직이 상당히 가독성 좋고 간단해집니다.
 그리고 그 과정에서 발생하는 error 케이스를 잡기 위해서 catchError를 사용하고 있습니다.
```swift
    catchError {
      Crashlytics.sharedInstance().recordError($0)
      return Observable.just(Result.fail(.jsonMappingError($0)))
    }
```

 이렇게 하면 모든 api 통신과 모델 맵핑 사이에서 발생하는 모든 케이스의 error를 잡을 수 있습니다. 그리고 보시면 알겠지만 추가적으로 **Crashlytics** 에 기록까지 하고 있습니다. 이 때 기록된 에러들은 나중에 fabric에서 non-fatal error로 올라오게 됩니다.


----------


##  마무리

 이렇게 해서 api request와 response를 처리하는 부분을 살펴봤습니다. 대부분의 api 통신이 다 이런 구조로 되어있습니다. 실제 데이터를 가공하는 부분은 다른 로직에서 처리하게 되는데, 저는 하나의 로직을 너무 길지 않도록 유지하고 있습니다. 이런 식으로 input을 output으로 만드는 로직을 통신, 가공, 표시 등 다양한 로직의 뭉텅이로 분리해서 처리하고 있습니다. 이렇게 로직을 분리하고 error 처리를 다양하게 하면 가독성도 높일 수 있고 유지 보수도 쉬워집니다.
  실제 데이터를 가공해서 output으로 만드는 부분은 다음 포스트에서 설명하겠습니다.
