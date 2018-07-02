# MVC에서 MVVM으로 신속한 iOS 앱 마이그레이션

 디자인 패턴은 코드의 일반적인 문제에 대한 재사용 가능한 솔루션입니다. MVVM (Model-View-Viewmodel)과 MVC (Model-View-Controller)는 모두 디자인 패턴입니다. MVC는 매우 보편적이고 구현하기 쉬운 디자인 패턴이지만 큰 코드 기반으로 작업하는 동안 매우 비효율적 입니다. 앱을 구축했다면 아마 MVC를 사용하여 개발했을 것 입니다. 다른 일반적인 디자인 패턴으로는 MVP (Model-view-presenter) 및 VIPER가 있습니다 ( [여기](https://themindstudios.com/blog/mvp-vs-mvc-vs-mvvm-vs-viper/)에 이에 대한 설명이 있습니다).

 이 글에서는 MVVM과 MVC에 집중할 것입니다.

 왜 디자인 패턴을 사용합니까? 검증되지 않은 설계보다 일반적으로 재사용 및 디버그하기가 쉽기 때문에 설계 패턴을 사용합니다. 어떤 특별한 디자인도없이 개발을 해보면 지금 당장은 문제 없습니다. 그러다 나중에 버그가 발생하게 된다면, 어떤 부분이 어디에 있는지, 왜 처음에 그 부분을 수행했는지 파악하는 것이 어려울 수 있습니다. 이 코드를 작성하지 않은 사람은 문제를 탐색하기가 얼마나 어려울 지 상상해보십시오. 이 게시물에서는 일반적인 iOS 패턴 인 MVVM을 사용하는 방법을 배우게됩니다. 

## 할 일(TODO) 목록 만들기

 MVC 및 MVVM 디자인 패턴을 이해하기 위해 우리는 할 일 목록 앱을 만들 것입니다. 응용 프로그램은 패턴을 보여줄 기본적인 기능을 모두 가지고 있습니다. To-do 활동을 작성하고, 할 일을 삭제하고, 활동을 완료로 표시 할 수 있습니다. 또한 앱은 배경으로 이동 한 후에도 앱 상태 (항목 수, 완료 여부)를 유지할 수 있도록 데이터를 유지합니다.

## MVC 대 MVVM

 더 나아 가기 전에 이해해야하는 것은 iOS 앱은 UI 로직과 비즈니스 로직이라는 두가지 필수적인 부분이 있습니다. 두 로직의 차이점은 무엇입니까?

 **비즈니스 로직**은 최종 사용자 인터페이스와 데이터베이스 간의 통신을 관리하는 프로그래밍입니다. 모델을 업데이트하고 데이터를 사람이 읽을 수있는 방식으로 처리하는 등의 작업을 수행합니다. 여기에는 데이터 업데이트, 목록에서 항목 삭제, 데이터 유형의 형식 지정 및 그런 종류의 작업이 포함됩니다. 이것은 더 간단한 용어로 **"처리"**라고 할 수 있습니다.

** UI 로직**은 사용자 인터페이스를 다루는 부분, 즉 사용자가보고 상호 작용하는 부분입니다. 여기에는 레이블, 테이블 업데이트, 화면 구성 요소 애니메이트 및 우리가보고 싶은 모든 예쁜 것들이 포함됩니다.

 이 두 파트의 구분은 일반적으로 데이터 분리를 자극하여 MVVM 및 MVC와 같은 디자인 패턴을 유발합니다.



### MVC 이해하기

 MVC는 Apple SDK가 구축된 아키텍처입니다. 이것은 세 가지 주요 섹션으로 구성됩니다.

- **모델 :** 데이터가있는 곳입니다. 우리의 경우 to-do 항목은 데이터 모델입니다.
- **뷰 :** 이것은 사용자가 화면에서 상호 작용하는 것입니다. 이 경우 할 일 항목의 이름 (예 : 레이블), 할 일 항목의 상태 (액세서리) 및 삭제할 제스처를 표시합니다.
- **컨트롤러 :** 뷰와 모델 간의 흐름을 제어합니다. 뷰가 할 일 항목을 표시하려면 제어기에 모델에 항목을 요청하도록 요청합니다. 컨트롤러는 모델에서 항목을 가져온 다음 그에 따라 뷰를 업데이트합니다. 모델이 변경되면 컨트롤러에 알리고 컨트롤러는 그에 따라 모델을 업데이트합니다.

![MVC](https://www.twilio.com/blog/wp-content/uploads/2018/05/JbBrTeO4KRUdKXs0PX8lqoDihF5vUDNLhMWdOxAd1GDah3nJkgYWthVltTsAUtkr2rkA42U8Wa-ACBgC4luF2yYg-MgUh13PHNYtRCXR_hQb3LnKXQomiModSvAiIqERDUCyHkF.png)

 다음은 MVC를 구현하는 방법의 두 가지 예입니다.

- 사례 1 : 사용자가 작업 항목을 스와이프하여 삭제합니다. 뷰 컨트롤러가 수행 할 모델을 업데이트해야합니다.
- 사례 2 : 잠시 후 취소 한 항목을 사용자에게 상기시키는 타이머가 있다고 가정 해보십시오. 타이머가 경과하면 모델은 뷰 측에서 조치가 필요하다는 것을 컨트롤러에 알립니다. 그러면 컨트롤러가 뷰를 업데이트하고 경고를 표시합니다.

 무엇보다도 MVC를 사용하는데 장단점이 있습니다. 가장 큰 장점 중 하나는 MVC가 학습하기 쉬운 디자인 패턴이라는 것입니다. 더 작은 코드베이스로 작업 할 때 MVVM 또는 다른 복잡한 패턴을 구현하려면 너무 많은 노력이 필요합니다. 

 그러나, 당신이 보았을 수도 있듯이, 뷰 컨트롤러는 꽤 많은 책임이 있습니다. 따라서 많은 코드가 복잡하게 뒤섞이게 됩니다. 이로 인해 점점 더 파일이 방대해집니다. **이것이 MVC가 "Massive View Controller"라고 불리는 이유입니다.** 이로 인해 코드베이스가 탐색 할 수없고 사실상 테스트 할 수없는 것과 같은 많은 문제가 발생했습니다.



### MVVM 이해

 MVC와 마찬가지로 MVVM은 여러 부분으로 구성됩니다.

- **뷰 :** MVC와 동일합니다. 그것은 데이터를 책임지고,해야할 일 목록 객체의 모든 작은 영역을 구성합니다.

- **모델 :** MVC와 동일합니다. 이것은 데이터가 살아있는 곳입니다. 이 경우 수행 할 항목은 데이터의 모델입니다.
- **뷰 컨트롤러 :** 뷰 컨트롤러는 UI뷰를 설정합니다. 그것은 모델과 전혀 상호 작용하지 않습니다. 대신 뷰 모델을 살펴보고 표시 할 수있는 형식으로 필요한 항목을 요청합니다. 비즈니스 로직이 전혀 없어야합니다.
- **뷰 모델 :** 뷰 모델은 기본적으로보기 컨트롤러를 나타냅니다. 뷰 컨트롤러에 레이블이 있으면 뷰 모델에 문자열 형식의 텍스트를 제공하는 속성이 있어야합니다. 모든 호출을 트리거하고 데이터를 송수신합니다. 뷰 모델을 다룰 때는 가능한 한 바보 같아야합니다. 즉, **가능한 한 뷰 컨트롤러에서 분리해야합니다.** **뷰 모델의 인스턴스를 뷰 모델에 삽입하지 않도록해야합니다.** 뷰 모델은 모든 뷰 컨트롤러와 완전히 독립적이어야합니다.

![MVVM](https://www.twilio.com/blog/wp-content/uploads/2018/05/w0ApU8yEXOQiOaKjv-wYaUGfcWOCtUzTWv8_EmGR5LX5wptM0eQ6DEBeQr0kEgX4cQHaGvxnQV3sHDC_sbvXSNUIl-WByh80uAx_srp92AX2XMSWwRAPAhCVN9nFvi2PN5jJ3rEr.png)

 다음은 MVVM을 구현하는 두 가지 예입니다.

- 사례 1 : 사용자가 작업 항목을 스 와이프하여 삭제합니다. 모델을 업데이트해야합니다. 뷰 컨트롤러는 뷰를 업데이트하기위한 모든 작업을 수행합니다. **그러나 모델을 업데이트하기 위해 뷰 컨트롤러는 뷰 모델과 통신하고 뷰 모델에서 모델을 업데이트하라고 요청합니다.** 
- 사례 2 : 잠시 후 취소 한 항목을 사용자에게 상기시키는 타이머가 있다고 가정 해보십시오. 타이머가 만료되면 **모델은 뷰 모델에 뷰 측면에서 작업이 필요함을 알립니다. 그런 다음 뷰 모델은 뷰 컨트롤러에서 작업을 실행하여 뷰를 업데이트하라고 전달합니다.** 

 MVC와 마찬가지로 MVVM을 사용하는 것이 장단점입니다. UI와 비즈니스 로직의 분리로 인해 MVVM 디자인 패턴은보다 유연하고 읽기 쉬운 클래스를 제공합니다. 그러나 MVVM의 바인딩 및 기타 기술 관련 문제를 파악하기가 어렵 기 때문에 MVVM의 학습 비용은 약간 높을 수 있습니다.



## MVC에서 MVVM으로 이동

앞서 언급했듯이 소스 코드가 [여기](https://github.com/angiemugo/MyToDo/tree/Angie/MVC) 에 호스팅 [됩니다](https://github.com/angiemugo/MyToDo/tree/Angie/MVC) .

![프로젝트](https://www.twilio.com/blog/wp-content/uploads/2018/05/iuu2fDJ_l3qekcxjHoDMGG60ok0PQRsTfJ6zFqXBP6RehWR1_g1WgtFht6pZZKwrvbX6NXI8FBVv_QssRGJVKMSb1uNb3cL5n4ujiGTilMQeEweLcr0ACOLIfoXqpvN1bWxcgu9r.png)



## MVVM에 도전 해보자.

 앞서 언급했듯이 MVVM의 목표는 모든 UI 로직을 비즈니스 로직과 분리하는 것입니다. 앱을 보면 UI 로직과 비즈니스 로직이 있습니다. **먼저 뷰 모델 데이터를 뷰 컨트롤러에 표시하는 방법이 필요합니다.** 이 작업에는 몇 가지 방법이 있습니다.

- **바인딩 :** 바인딩을 사용하여 뷰 모델 클래스를 뷰 컨트롤러에 바인딩하는 클래스를 사용합니다. 더 복잡한 클래스를 다룰 때 훌륭한 접근 방법입니다.
- **클로저 :** 여기에서는 클로저를 사용하여 뷰 모델 클래스의 특정 속성을 노출합니다. 네트워크 요청 및 외부 요인에 의존하는 기타 작업을 수행 할 때 특히 유용합니다. 예를 들어 API에서 데이터를 가져 오는 경우 Closure를 사용하여 View Controller를 업데이트합니다.
- **델리게이트 및 프로토콜 :** 속성의 변경 사항을 모니터링하고 뷰 컨트롤러를 업데이트하는 데 사용됩니다. 좋은 예는 데이터의 변경 사항을 모니터링하고 변경 사항을 기반으로 작업을 수행하는 경우입니다. 예를 들어 Wi-Fi 네트워크가 감지 될 때마다 알림을 보내려면 대표를 사용합니다.
- **변수 :** 이것은 가장 간단한 방법이며 우리가 사용할 방법입니다. 뷰 모델에서 속성을 만들고 뷰 컨트롤러에서 문자열 또는 다른 형식의 표현을 사용합니다. 뷰 컨트롤러는 viewModel의 변수에 즉시 사용할 수있는 형식으로 액세스합니다.

뷰 모델에서 속성을 생성하고 뷰 컨트롤러에 노출함으로써 가장 간단한 방법을 사용하여 앞으로 나아 갑시다.



#### 코드 분리하기

```
@IBAction func didTapAdd(_ sender: Any) {
    let alert = UIAlertController(title: "New To-Do Item", message: "Insert the title of the new to-do item:", preferredStyle: .alert)
    alert.addTextField(configurationHandler: nil)
    alert.addAction(UIAlertAction(title: "OK", style: .default, handler: { (_) in
        
        if let title = alert.textFields![0].text {
            guard !title.isEmpty else { return }
            let newIndex = self.todoList.count
            self.todoList.append(ToDoItem(title: title))
            
            self.tableView.insertRows(at: [IndexPath(row: newIndex, section: 0)], with: .top)
            
            self.saveData()
        }
    }))
    
    self.present(alert, animated: true, completion: nil)
    
}
```

  만약 위와 같은 코드가 뷰 컨트롤러에 있다면 MVVM을 지키지 않은 것 입니다. 화면에 얼럿 상자를 띄우기 뷰 컨트롤러에서 구현하는게 맞지만 얼럿 박스 안에 들어가는 문구까지 뷰 컨트롤러에서 정의 해서는 안됩니다. 이 것은 비지니스 로직입니다. 따라서 다음과 같이 변경되어야 합니다.

```
let alert = UIAlertController(title: viewModel.actionTitle, message: viewModel.alertMessage, preferredStyle: .alert)
alert.addTextField(configurationHandler: nil)           
alert.addAction(UIAlertAction(title: viewModel.actionTitle, style: .default, handler: { (_) in
...
```

 문구 등 비지니스 로직은 뷰 모델에 정의되어야 합니다.

 다음으로 아이템을 추가하는 행위는 `self.todoList.append(ToDoItem(title: title))` 는 UI와 전혀 상관이 없기 때문에 이 역시 뷰 모델로 옮겨야 합니다. 뷰 모델에 데이터를 저장할 배열을 선언하고 이 데이터를 참조할 경우 `viewModel.todoList` 를 통해서만 접근하도록 해야 합니다.

```
override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return viewModel.todoList .count
}
```

 

## 성장 기회

 우리가 UI 또는 비즈니스 로직 여부를 판단하는 데 사용되는 논리에 따라 분석해 볼 때, 당신은 여전히 뷰 컨트롤러에 많은 비즈니스 로직이 있다는 것을 알게 될 것입니다. 그것을 뷰 컨트롤러로 옮겨서 한 번 시도하십시오. 다음은 할 일 목록의 마지막 [MVVM](https://github.com/angiemugo/MyToDo/tree/Angie/MVVM)  버전입니다. MVVM 버전은 Angie / MVVM 브랜치에 있습니다. **새로운 클래스를 보면 viewController 클래스의 크기가 반드시 줄어들지는 않습니다. 그러나 테스트하는 것이 훨씬 쉽습니다.**

 가장 일반적인 실수 중 하나는 뷰 모델이 컨트롤러를 참조하도록하는 것입니다.



## MVC에서 MVVM으로

 보시다시피, MVVM은 디버깅, 테스트 및 코드 읽기를 더 쉽게 만듭니다. 따라서 다양한 방법을 해결할 수 있도록 다양한 기술을 습득하는 것이 필수적입니다. 위는 MVVM을 수행하는 한 가지 방법입니다. 그러나 더 복잡한 문제가 있으면 ReactiveCocoa 및 RXSwift와 같은 코코아 포드를 사용하는 것이 좋습니다. 이러한 솔루션은 MVVM을보다 쉽게 사용할 수 있도록 제작되었습니다.

 딱 맞는 단일 아키텍처는 없습니다. 각각은 가장 잘 작동하는 사용 사례를 가지고 있습니다. 그러므로 정보에 입각 한 결정을 내리기 위해서는 VIPER, MVVM 및 MVC에 대해 잘 알고 있어야합니다.