---
layout: post
current: post
navigation: True
title:  "HealthKit - Steps Counter"
date:   2019-09-04 00:00:01
cover: assets/images/ios/healthkit.png
description: HealthKit - Steps Counter
tags: [ ios  ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---
# HealthKit - Steps Counter
 프로젝트에서 걸음 수 기능이 추가된다고 해서 사전에 만보계 기능을 추가하려 합니다. 보통 걸음 수 기능을 구현할 때에는 Healthkit을 사용하거나 CoreMotion을 사용한다고 합니다. CoreMotion을 사용하면 실시간으로 데이터를 수집할 수 있지만 다른 디바이스의 데이터, 예를 들어 애플 워치 데이터를 수집할 수 없다고 합니다. 우리 프로젝트에서는 실시간 걸음 수는 수집할 필요가 없기 때문에 Healthkit을 사용해보려 합니다.
  사실 healthkit을 사용하기에 많이 늦었습니다. 이미 건강을 주로 다루는 앱이기 때문에 진작에 healthkit을 붙였어야 했는데, 이미 서버 베이스로 돌아가는 프로젝트에 2.0을 진행하는 것이었고 프로젝트 기간도 짧아서 붙이지 못했습니다.

Healthkit을 적용하는 방법은 다른 잘 만들어진 포스트가 있습니다. 여기를 참고하시길 바랍니다.
(https://medium.com/aubergine-solutions/healthkit-data-reading-writing-f10688cfda6b)


##  수정사항

 저는 여기서 추가적으로 걸음수를 시간별로 읽어와야 합니다. 근데, 그냥 날짜 쿼리로 뽑아버리면 데이터 형태가 시간별로 나눠서 나오는게 아니라 데이터가 들어온 기간으로 시작 시간, 종료 시간으로 뽑아져 나오게됩니다. 그래서 1시 50분부터 3시 10분까지 2000걸음 이런 식으로 어정쩡한 결과가 나오기 때문에 이걸 나눠서 사용하는 것은 문제가 있었습니다.
 그래서 위 사이트의 예시에서 조금 수정했습니다.

```swift
        func readStepCountWithBlock(finish: @escaping (Error?, [String]) ->Void) {
            let date = "2019-09-01"

            for i in 0...23 {
                let startDate = dateFromString("\(date) \(i)")
                let endDate = dateFromString("\(date) \(i+1)")


                guard let sampleSteps = HKSampleType.quantityType(forIdentifier: .stepCount) else { fatalError() }

                let predicate = HKQuery.predicateForSamples(withStart: startDate, end: endDate, options: HKQueryOptions.strictStartDate)

                let query = HKSampleQuery(sampleType: sampleSteps,
                                          predicate: predicate,
                                          limit: 0,
                                          sortDescriptors: nil) {[weak self] (hkSamleQuery,hkSamleArray,error) in
                                            guard let `self` = self else { return }
                                            if let error = error {
                                                print(error.localizedDescription)
                                            } else {
                                                for sample: HKQuantitySample in (hkSamleArray as? [HKQuantitySample]) ?? [] {
                                                    print(self.stringFromDate(sample.startDate))
                                                    print(self.stringFromDate(sample.endDate))
                                                    print(sample.quantity.doubleValue(for: .count()))
                                                }
                                            }
                }

                healthStore.execute(query)
            }
        }
```


----------


 쿼리를 생성할 때 01 ~ 02시 처럼 시간별로 뽑도록 지정해서 데이터를 뽑아왔습니다. 이렇게 데이터를 뽑았더니 다행히 제가 원하는 형태로 데이터가 뽑혔습니다.


![](https://paper-attachments.dropbox.com/s_5689B5119B301B2F3320EFD6B62220CF7F6D69A4DF60E1E0C568B1579E459BB9_1567568001265_IMG_34FEA881C12D-1.jpeg)
```
    2019-09-01 01
    22.0
    2019-09-01 09
    19.0
    2019-09-01 10
    9.0
    2019-09-01 12
    94.0
    2019-09-01 12
    22.0
    2019-09-01 18
    24.0
    2019-09-01 16
    14.0
    2019-09-01 19
    7.0
    2019-09-01 23
    9.0
    2019-09-01 22
    16.0
```



----------


##  출력

 이제 이 데이터를 화면에 뿌려주는 일이 남아있습니다.
이제 출력 데이터를 화면에 찍겠습니다.
```swift
    # HealthKitManager.swift
    ...
    for sample: HKQuantitySample in (hkSamleArray as? [HKQuantitySample]) ?? [] {
      print(self.stringFromDate(sample.startDate))
      print(self.stringFromDate(sample.endDate))
      print(sample.quantity.doubleValue(for: .count()))
      finish(nil, "\(self.stringFromDate(sample.startDate)): \(sample.quantity.doubleValue(for: .count()))" )
    }
    ...

    #ViewController.swift
    DispatchQueue.main.asyncAfter(deadline: .now() + 1, execute: {
      HealthKitManager.sharedInstance.readStepCountWithBlock(finish: { (error, value) in
        if let error = error {
          print(error.localizedDescription)
        } else {
          DispatchQueue.main.async { [weak self] in
            guard let `self` = self else { fatalError() }
            self.countLabel.text?.append("\n\(value)")
          }
        }
      })
    })
111
```
![](https://paper-attachments.dropbox.com/s_5689B5119B301B2F3320EFD6B62220CF7F6D69A4DF60E1E0C568B1579E459BB9_1567569670771_IMG_63C99B0A4033-1.jpeg)

----------
##  개선

 지금 살펴보면 버그가 있습니다.
 데이터를 보면 9월 1일 12시에 데이터가 2개여서 시간별로 나오다가 12시만 2개가 찍히는 케이스입니다. 12시부터 13시로 쿼리를 뽑았지만 12시에서 13시에 데이터를 합쳐서 표현하는 것이 아니라 12시에서 13시 사이에 있는 데이터들을 보여주는 것이죠. 그래서 같은 시간을 다 더해주도록 수정했습니다.

```swift
    var steps = 0.0
    var date = ""
    for sample: HKQuantitySample in (hkSamleArray as? [HKQuantitySample]) ?? [] {
      date = self.stringFromDate(sample.startDate)
      steps += sample.quantity.doubleValue(for: .count())
    }
    if steps == 0 {
      return
    }
    finish(nil, "\(date)): \(steps))" )
```
