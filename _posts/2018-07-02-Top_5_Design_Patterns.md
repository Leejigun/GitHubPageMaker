---
layout: post
current: post
navigation: True
title:  "Top 5 스위프트 디자인 패턴 (번역)"
date:   2018-06-20 00:00:00
cover: assets/images/top_5_design_patterns.png
description: 스위프트에서 가장 많이 사용하는 5가지 디자인 패턴.
tags: [ ios tip ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---
# Top 5 Design Patterns in Swift for iOS App Development (번역)

* [Top 5 Design Patterns in Swift for iOS App Development](https://rubygarage.org/blog/swift-design-patterns?utm_source=mybridge&utm_medium=blog&utm_campaign=read_more)



 2014년에 공개된 애플의 프로그래밍 언어인 스위프트는 점점 더 인기를 끌고 있다. Swift는 개발자들이 여러 운영 체제에 적용 가능한 다목적 응용 프로그램을 만들 수 있게 해 주는 강력한 도구입니다.

 스위프트는 상당히 새로운 프로그래밍 언어이며, 많은 개발자들은 스위프트와 어떤 디자인 패턴을 사용하고 개발해야 하는지 모른다. 스위프트와 관련된 설계 패턴을 사용할 수 있어야 기능성, 고품질 및 보안이 뛰어난 엡을 만들 수 있습니다.

 이 포스트에서는 스위프트에서 가장 널리 사용되는 디자인 패턴을 자세히 살펴보고 모바일 개발의 일반적인 문제를 해결하기 위한 다양한 접근법을 보여 줌으로써 도움을 주기로 결정했습니다.



## 디자인 패턴:패턴이 무엇이고 왜 알아야 하는지

 소프트웨어 설계 패턴은 애플리케이션의 구조를 설계할 때 직면할 수 있는 특정 문제에 대한 해결책을 제공합니다. 그러나 기본으로 제공하는 서비스나 오픈 소스 라이브러리와 달리 설계 패턴은 코드가 아니기 때문에 응용 프로그램에 붙여 넣기만 할 수는 없습니다. 오히려, 그것은 문제를 해결하는 방법에 대한 일반적인 개념입니다. 디자인 패턴은 코드를 작성하는 방법을 알려 주는 템플릿이지만 이 템플릿에 코드를 맞추는 것은 사용자에게 달려 있습니다.



디자인 패턴은 다음과 같은 몇가지 이점을 제공합니다.

* **테스트된 솔루션:** 디자인 패턴은 이미 최고의 솔루션을 제공하고 구현 방법을 알려 주므로 특정 소프트웨어 개발 문제를 해결하기 위해 시간을 낭비하고 노력할 필요가 없습니다.
* **코드 통일:** 디자인 패턴은 애플리케이션 아키텍처를 설계할 때 실수를 덜 하도록 결점과 버그에 대한 테스트를 거친 일반적인 솔루션을 제공합니다.
* **공통 어휘:** 소프트웨어 개발 문제를 해결하는 방법에 대한 자세한 설명을 제공하는 대신, 사용한 디자인 패턴을 다른 개발자가 즉시 이해할 수 있도록 간단하게 말할 수 있습니다.



## 소프트웨어 설계 유형

 Swift에서 가장 일반적인 아키텍처 패턴을 설명하기 전에 먼저 세가지 유형의 소프트웨어 설계 패턴과 그 차이를 알아보아야 합니다.

### #1 Creational

**Creational**(창조적인) 소프트웨어 설계 패턴은 객체 생성과 관련된 메커니즘을 다룹니다. 그들은 특정 상황에 적합한 방식으로 객체를 인스턴스화하려고 합니다. 다음은 객체 생성과 관련된 설계 패턴입니다.

- Factory Method (팩토리)
- Abstract Factory (추상 팩토리)
- Builder (빌더)
- Singleton (싱글톤)
- Prototype (프로토타입)



### #2 Structural

 **Structural**(구조) 설계 패턴은 클래스와 객체 간의 관계를 쉽게 실현할 수 있는 방법을 찾아 설계를 단순화하는 것을 목표로 합니다. 다음은 구조적 아키텍처 패턴입니다.

- Adapter
- Bridge
- Facade
- Decorator
- Composite
- Flyweight
- Proxy



### #3 Behavioral

 행동 설계 패턴은 개체 간의 일반적인 통신 패턴을 분석하여 구현합니다. 행동 설계 패턴에는 다음이 포함됩니다.

- Chain of Responsibility
- Template Method
- Command
- Iterator
- Mediator
- Memento
- Observer
- Strategy
- State
- Visitor



 그러나 이러한 설계 패턴의 대부분은 거의 사용되지 않으며 쓰기도 전에 작동 방식을 잊어 버릴 수 있습니다. 그래서 우리는 iOS와 다른 운영 체제를 위한 애플리케이션을 개발하기 위해 스위프트에서 **가장 자주 사용되는 다섯가지 디자인 패턴**을 만들었습니다.



## Swift에서 가장 자주 사용되는 디자인 패턴

#### #1 Builder

 Builder패턴은 단순한 객체에서 복합한 객체를 단계적으로 생성할 수 있는 생성 설계 패턴입니다. 이 설계 패턴을 사용하면 다른 객체 뷰를 작성할 때 동일한 코드를 사용할 수 있습니다.

 여러 필드 및 중첩된 프로퍼티의 초기화가 필요한 복잡한 객체를 상상해 보십시오. 일반적으로 매개 변수가 수십개인 대규모 생성자 내에 이러한 프로퍼티의 초기화 코드가 숨겨져 있습니다. 더 나쁠 경우, 그것이 클라이언트 코드에 흩어져 있을 수 있다는 것 입니다.

 빌더 설계 패턴에서는 객체의 구조를 자체 클래스에서 분리해야 합니다. 대신에 이 물체의 구조는 빌더라고 불리는 특수한 물체에 할당되고 여러 단계로 나뉩니다. 객체를 작성하려면 빌더 방법을 연속적으로 호출합니다. 특정 구성을 사용하여 개체를 생성하는 데 필요한 단계만 거치면 됩니다.



##### 아래의 경우에 해당한다면 반드시 Builder설계 패턴을 적용해야 합니다.

* 만약, **점층적 생성자(*telescopic* constructor)** 패턴을 피하고 싶을 경우

  (***telescopic* constructor:** 다수의 생성자를 만들어 분기하는 패턴, 이 경우 생성자가 너무 많은 파라미터를 가지게 되고 이것들을 관리하기 힘들다.)

* 만약에 코드가 특정 다른 뷰를 생성해야 하는 경우

* 복잡한 객체를 다뤄야 하는 경우



#### 예제

 레스토랑의 iOS응용 프로그램을 개발하고 있으며 주문 기능을 구현해야 한다고 가정합니다. 여러분은 디쉬와 오더라는 두개의 구조물을 소개할 수 있고, 주문/구매자의 도움으로 다른 요리 세트로 주문을 작성할 수 있습니다.

```
// Design Patterns: Builder
import Foundation

// Models
enum DishCategory: Int {
    case firstCourses, mainCourses, garnishes, drinks
}

struct Dish {
    var name: String
    var price: Float
}

struct OrderItem {
    var dish: Dish
    var count: Int
}

struct Order {
    var firstCourses: [OrderItem] = []
    var mainCourses: [OrderItem] = []
    var garnishes: [OrderItem] = []
    var drinks: [OrderItem] = []

    var price: Float {
        let items = firstCourses + mainCourses + garnishes + drinks
        return items.reduce(Float(0), { $0 + $1.dish.price * Float($1.count) })
    }
}

// Builder
class OrderBuilder {
    private var order: Order?

    func reset() {
        order = Order()
    }

    func setFirstCourse(_ dish: Dish) {
        set(dish, at: order?.firstCourses, withCategory: .firstCourses)
    }

    func setMainCourse(_ dish: Dish) {
        set(dish, at: order?.mainCourses, withCategory: .mainCourses)
    }

    func setGarnish(_ dish: Dish) {
        set(dish, at: order?.garnishes, withCategory: .garnishes)
    }

    func setDrink(_ dish: Dish) {
        set(dish, at: order?.drinks, withCategory: .drinks)
    }

    func getResult() -> Order? {
        return order ?? nil
    }

    private func set(_ dish: Dish, at orderCategory: [OrderItem]?, withCategory dishCategory: DishCategory) {
        guard let orderCategory = orderCategory else {
            return
        }

        var item: OrderItem! = orderCategory.filter( { $0.dish.name == dish.name } ).first

        guard item == nil else {
            item.count += 1
            return
        }

        item = OrderItem(dish: dish, count: 1)

        switch dishCategory {
        case .firstCourses:
            order?.firstCourses.append(item)
        case .mainCourses:
            order?.mainCourses.append(item)
        case .garnishes:
            order?.garnishes.append(item)
        case .drinks:
            order?.drinks.append(item)
        }
    }
}

// Usage
let steak = Dish(name: "Steak", price: 2.30)
let chips = Dish(name: "Chips", price: 1.20)
let coffee = Dish(name: "Coffee", price: 0.80)

let builder = OrderBuilder()
builder.reset()
builder.setMainCourse(steak)
builder.setGarnish(chips)
builder.setDrink(coffee)

let order = builder.getResult()
order?.price

// Result:
// 4.30
```



#### #2 Adapter

 어댑터는 호환되지 않는 인터페이스를 가진 두개의 개체가 함께 작동할 수 있도록 해 주는 구조 설계 패턴입니다. 즉, 개체의 인터페이스를 변환하여 다른 개체에 적응시킵니다.

 어댑터는 개체를 감싸므로 다른 개체로부터 완전히 숨깁니다. 예를 들어 값을 미터에서 피트로 변환하는 어댑터로 미터를 처리하는 개체를 쌀 수 있습니다.

 **다음과 같은 경우 어댑터 패턴을 사용해야 합니다.**

* 만약, 외부 라이브러리 같은 서드 파티 클래스를 사용하고 싶은데, 인터페이스가 매치가 안 될 경우
* 여러 서브 클래스를 사용해야 하지만, 그것들이 특정 기능이 없고 확장이 불가능할 경우

##### 예제

 iOS응용 프로그램에서 일정 관리 및 이벤트 관리 기능을 구현하려고 합니다. 이를 위해서는 Even.it 프레임워크를 통합하고 이벤트 모델을 프레임워크에서 애플리케이션의 모델로 조정해야 합니다. 어댑터는 프레임워크의 모델을 포장하여 애플리케이션의 모델과 호환되도록 할 수 있습니다.

```
// Design Patterns: Adapter
import EventKit

// Models
protocol Event: class {
    var title: String { get }
    var startDate: String { get }
    var endDate: String { get }
}

extension Event {
    var description: String {
        return "Name: \(title)\nEvent start: \(startDate)\nEvent end: \(endDate)"
    }
}

class LocalEvent: Event {
    var title: String
    var startDate: String
    var endDate: String

    init(title: String, startDate: String, endDate: String) {
        self.title = title
        self.startDate = startDate
        self.endDate = endDate
    }
}

// Adapter
class EKEventAdapter: Event {
    private var event: EKEvent

    private lazy var dateFormatter: DateFormatter = {
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "MM-dd-yyyy HH:mm"
        return dateFormatter
    }()

    var title: String {
        return event.title
    }
    var startDate: String {
        return dateFormatter.string(from: event.startDate)
    }
    var endDate: String {
        return dateFormatter.string(from: event.endDate)
    }

    init(event: EKEvent) {
        self.event = event
    }
}

// Usage
let dateFormatter = DateFormatter()
dateFormatter.dateFormat = "MM/dd/yyyy HH:mm"

let eventStore = EKEventStore()
let event = EKEvent(eventStore: eventStore)
event.title = "Design Pattern Meetup"
event.startDate = dateFormatter.date(from: "06/29/2018 18:00")
event.endDate = dateFormatter.date(from: "06/29/2018 19:30")

let adapter = EKEventAdapter(event: event)
adapter.description

// Result:
// Name: Design Pattern Meetup
// Event start: 06-29-2018 18:00
// Event end: 06-29-2018 19:30
```

 event의 description을 호출했을 경우의 형태를 내가 원하는데로 커스텀하고 있습니다. **EKEventStore** 클래스를 건들지 않고 어탭터로 감싸 description을 호출했을 경우 출력을 컨트롤 하고 있습니다.



#### #3 Decorator

 Decorator패턴은 객체를 포장지에 포장하여 새로운 기능을 동적으로 부착할 수 있는 구조 설계 패턴입니다.

 이러한 디자인 패턴이 래퍼 디자인 패턴이라고도 부르는게 더 당연하게 보일 수 있습니다. 하지만, 데코데이터라는 이름은 이 패턴 뒤에 있는 핵심 아이디어를 보다 정확하게 설명 할 수 있습니다. 기본 동작을 하는 래퍼 객체 안에 타겟 객체를 넣고 이것이 가지는 기능을 추가합니다.

 두 개체는 동일한 인터페이스를 공유하므로 사용자가 래핑된 객체든 깨끗한 오리지널 객체든 어떤 개체와 상호 작용하든 상관 없습니다. 여러개의 포장지를 동시에 사용하여 모든 포장지의 결합된 동작을 확인할 수 있습니다.

**다음과 같은 경우 데코레이터 패턴을 사용해야 합니다.**

*  객체에 동적으로 기능을 추가하고 이런 코드의 추가를 숨기고 싶은 경우
* 상속을 통해서 객체를 확장할 수 없는 경우



##### 예제

 iOS애플리케이션에서 데이터 관리를 구현해야 한다고 가정해 보십시오. 데이터 암호화 및 암호 해독을 위한 암호 해독기와 인코딩 및 디코딩을 위한 암호 해독기를 만들 수 있습니다.

```
// Design Patterns: Decorator
import Foundation

// Helpers (may be not include in blog post)
func encryptString(_ string: String, with encryptionKey: String) -> String {
    let stringBytes = [UInt8](string.utf8)
    let keyBytes = [UInt8](encryptionKey.utf8)
    var encryptedBytes: [UInt8] = []

    for stringByte in stringBytes.enumerated() {
        encryptedBytes.append(stringByte.element ^ keyBytes[stringByte.offset % encryptionKey.count])
    }

    return String(bytes: encryptedBytes, encoding: .utf8)!
}

func decryptString(_ string: String, with encryptionKey: String) -> String {
    let stringBytes = [UInt8](string.utf8)
    let keyBytes = [UInt8](encryptionKey.utf8)
    var decryptedBytes: [UInt8] = []

    for stringByte in stringBytes.enumerated() {
        decryptedBytes.append(stringByte.element ^ keyBytes[stringByte.offset % encryptionKey.count])
    }

    return String(bytes: decryptedBytes, encoding: .utf8)!
}

// Services
protocol DataSource: class {
    func writeData(_ data: Any)
    func readData() -> Any
}

class UserDefaultsDataSource: DataSource {
    private let userDefaultsKey: String

    init(userDefaultsKey: String) {
        self.userDefaultsKey = userDefaultsKey
    }

    func writeData(_ data: Any) {
        UserDefaults.standard.set(data, forKey: userDefaultsKey)
    }

    func readData() -> Any {
        return UserDefaults.standard.value(forKey: userDefaultsKey)!
    }
}

// Decorators
class DataSourceDecorator: DataSource {
    let wrappee: DataSource

    init(wrappee: DataSource) {
        self.wrappee = wrappee
    }

    func writeData(_ data: Any) {
        wrappee.writeData(data)
    }

    func readData() -> Any {
        return wrappee.readData()
    }
}

class EncodingDecorator: DataSourceDecorator {
    private let encoding: String.Encoding

    init(wrappee: DataSource, encoding: String.Encoding) {
        self.encoding = encoding
        super.init(wrappee: wrappee)
    }

    override func writeData(_ data: Any) {
        let stringData = (data as! String).data(using: encoding)!
        wrappee.writeData(stringData)
    }

    override func readData() -> Any {
        let data = wrappee.readData() as! Data
        return String(data: data, encoding: encoding)!
    }
}

class EncryptionDecorator: DataSourceDecorator {
    private let encryptionKey: String

    init(wrappee: DataSource, encryptionKey: String) {
        self.encryptionKey = encryptionKey
        super.init(wrappee: wrappee)
    }

    override func writeData(_ data: Any) {
        let encryptedString = encryptString(data as! String, with: encryptionKey)
        wrappee.writeData(encryptedString)
    }

    override func readData() -> Any {
        let encryptedString = wrappee.readData() as! String
        return decryptString(encryptedString, with: encryptionKey)
    }
}

// Usage
var source: DataSource = UserDefaultsDataSource(userDefaultsKey: "decorator")
source = EncodingDecorator(wrappee: source, encoding: .utf8)
source = EncryptionDecorator(wrappee: source, encryptionKey: "secret")
source.writeData("Design Patterns")
source.readData() as! String

// Result:
// Design Patterns
```

 데이터 소스 기본형에 읽고 쓰기가 있는 가운데, 인코딩 데코레이터를 이용해 인코딩 기능을 추가하고, 엔크립션 데코레이터를 통해 암호화 기능을 추가할 수 있게 되었다.



#### #4 Facade

 Facade패턴은 라이브러리, 프레임워크 또는 복잡한 클래스 시스템에 대한 간단한 인터페이스를 제공하는 구조 설계 패턴입니다.

 코드가 복잡한 라이브러리나 프레임워크의 여러 객체를 처리해야 한다고 상상해 보십시오. 이러한 개체를 모두 초기화하고 올바른 종속성 순서를 따라서 사용해야 합니다. 그 결과, 클래스의 비즈니스 로직이 다른 클래스의 구현 세부 사항과 복잡하게 얽혀 있습니다. 그러한 코드는 읽고 유지하기 어렵습니다.

 Facade패턴은 많은 클래스를 포함하는 복잡한 서브 시스템을 사용하기 위한 간단한 인터페이스를 제공합니다. Facade패턴은 복잡한 하위 시스템을 직접 사용하여 확장할 수 있는 기능이 제한된 단순화된 인터페이스를 제공합니다. 이 단순화된 인터페이스는 클라이언트가 필요로 하는 기능만 제공하면서 다른 모든 기능은 숨깁니다.

**다음과 같은 경우 데코레이터 패턴을 사용해야 합니다.**

* 복잡한 시스템에 간단한 인터페이스를 제공하고 싶을 경우
* 하위의 시스템을 별도의 계층으로 분리해야 하는 경우



##### 예제

 많은 최신 모바일 응용 프로그램이 오디오 녹음 및 재생을 지원하므로 이 기능을 구현해야 한다고 가정해 보겠습니다. Facade패턴을 사용하여 파일 시스템(FileService), 오디오 세션(AudioSessionService), 오디오 녹음(RecordServe), 재생(재생/서비스)의 서비스 구현을 숨길 수 있습니다. Facade는 다소 복잡한 클래스 시스템을 위한 단순한 인터페이스를 제공합니다.

```
// Design Patterns: Facade
import AVFoundation

// Services (may be not include in blog post)
struct FileService {
    private var documentDirectory: URL {
        return FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first!
    }

    var contentsOfDocumentDirectory: [URL] {
        return try! FileManager.default.contentsOfDirectory(at: documentDirectory, includingPropertiesForKeys: nil)
    }

    func path(withPathComponent component: String) -> URL {
        return documentDirectory.appendingPathComponent(component)
    }

    func removeItem(at index: Int) {
        let url = contentsOfDocumentDirectory[index]
        try! FileManager.default.removeItem(at: url)
    }
}

protocol AudioSessionServiceDelegate: class {
    func audioSessionService(_ audioSessionService: AudioSessionService, recordPermissionDidAllow allowed: Bool)
}

class AudioSessionService {
    weak var delegate: AudioSessionServiceDelegate?

    func setupSession() {
        try! AVAudioSession.sharedInstance().setCategory(AVAudioSessionCategoryPlayAndRecord, with: [.defaultToSpeaker])
        try! AVAudioSession.sharedInstance().setActive(true)

        AVAudioSession.sharedInstance().requestRecordPermission { [weak self] allowed in
            DispatchQueue.main.async {
                guard let strongSelf = self, let delegate = strongSelf.delegate else {
                    return
                }

                delegate.audioSessionService(strongSelf, recordPermissionDidAllow: allowed)
            }
        }
    }

    func deactivateSession() {
        try! AVAudioSession.sharedInstance().setActive(false)
    }
}

struct RecorderService {
    private var isRecording = false
    private var recorder: AVAudioRecorder!
    private var url: URL

    init(url: URL) {
        self.url = url
    }

    mutating func startRecord() {
        guard !isRecording else {
            return
        }

        isRecording = !isRecording
        recorder = try! AVAudioRecorder(url: url, settings: [AVFormatIDKey: kAudioFormatMPEG4AAC])
        recorder.record()
    }

    mutating func stopRecord() {
        guard isRecording else {
            return
        }

        isRecording = !isRecording
        recorder.stop()
    }
}

protocol PlayerServiceDelegate: class {
    func playerService(_ playerService: PlayerService, playingDidFinish success: Bool)
}

class PlayerService: NSObject, AVAudioPlayerDelegate {
    private var player: AVAudioPlayer!
    private var url: URL
    weak var delegate: PlayerServiceDelegate?

    init(url: URL) {
        self.url = url
    }

    func startPlay() {
        player = try! AVAudioPlayer(contentsOf: url)
        player.delegate = self
        player.play()
    }

    func stopPlay() {
        player.stop()
    }

    func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
        delegate?.playerService(self, playingDidFinish: flag)
    }
}

// Facade
protocol AudioFacadeDelegate: class {
    func audioFacadePlayingDidFinish(_ audioFacade: AudioFacade)
}

class AudioFacade: PlayerServiceDelegate {
    private let audioSessionService = AudioSessionService()
    private let fileService = FileService()
    private let fileFormat = ".m4a"
    private var playerService: PlayerService!
    private var recorderService: RecorderService!
    weak var delegate: AudioFacadeDelegate?

    private lazy var dateFormatter: DateFormatter = {
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyy-MM-dd_HH:mm:ss"
        return dateFormatter
    }()

    init() {
        audioSessionService.setupSession()
    }

    deinit {
        audioSessionService.deactivateSession()
    }

    func startRecord() {
        let fileName = dateFormatter.string(from: Date()).appending(fileFormat)
        let url = fileService.path(withPathComponent: fileName)
        recorderService = RecorderService(url: url)
        recorderService.startRecord()
    }

    func stopRecord() {
        recorderService.stopRecord()
    }

    func numberOfRecords() -> Int {
        return fileService.contentsOfDocumentDirectory.count
    }

    func nameOfRecord(at index: Int) -> String {
        let url = fileService.contentsOfDocumentDirectory[index]
        return url.lastPathComponent
    }

    func removeRecord(at index: Int) {
        fileService.removeItem(at: index)
    }

    func playRecord(at index: Int) {
        let url = fileService.contentsOfDocumentDirectory[index]
        playerService = PlayerService(url: url)
        playerService.delegate = self
        playerService.startPlay()
    }

    func stopPlayRecord() {
        playerService.stopPlay()
    }

    func playerService(_ playerService: PlayerService, playingDidFinish success: Bool) {
        if success {
            delegate?.audioFacadePlayingDidFinish(self)
        }
    }
}

// Usage
let audioFacade = AudioFacade()
audioFacade.numberOfRecords()

// Result:
// 0
```

 불러오기, 재생 녹음등 모든 편의 기능을 묶어서 하나의 클래스로 만들어 제공하고 있습니다.



#### #5 Template Method

 **TemplateMethod(템플릿 방법)**패턴은 알고리즘의 골격을 정의하고 일부 단계에 대한 책임을 하위 분류에 위임하는 행동 설계 패턴입니다. 이 패턴을 통해 하위 클래스는 전체 구조를 변경하지 않고 알고리즘의 특정 단계를 재정의할 수 있습니다.

 이 설계 패턴은 알고리즘을 일련의 단계로 분할하고, 별도의 방법으로 이러한 단계를 설명하며, 단일 템플릿 방법을 사용하여 연속적으로 호출합니다.

**다음과 같은 경우 템플릿 메소드 패턴을 사용해야 합니다.**

* 서브클래스가 구조를 수정하지 않으면서 기존의 알고리즘을 확장해야 하는 경우
* 비슷한 동작을 취하는 여러 클래스를 가지고 있는 경우 (이 경우 하나의 클래스만 수정해도 다른 모든 클래스를 수정해야 합니다.)



##### 예제

 iOS앱에서 사진을 찍고 저장할 수 있어야 한다고 가정합니다. 따라서 응용 프로그램에서 iPhone(또는 iPad)카메라와 이미지 갤러리를 사용할 수 있는 권한을 얻어야 합니다. 이렇게 하려면 특정 알고리즘이 있는 PermissionService기본 클래스를 사용하면 됩니다. 카메라와 갤러리를 사용할 권한을 얻으려면 특정 단계를 공유하는 CameraPermissionService및 PhotoPermissionService라는 두개의 하위 클래스를 만듭니다.

```
// Design Patterns: Template Method
import AVFoundation
import Photos

// Services
typealias AuthorizationCompletion = (status: Bool, message: String)

class PermissionService: NSObject {
    private var message: String = ""

    func authorize(_ completion: @escaping (AuthorizationCompletion) -> Void) {
        let status = checkStatus()

        guard !status else {
            complete(with: status, completion)
            return
        }

        requestAuthorization { [weak self] status in
            self?.complete(with: status, completion)
        }
    }

    func checkStatus() -> Bool {
        return false
    }

    func requestAuthorization(_ completion: @escaping (Bool) -> Void) {
        completion(false)
    }

    func formMessage(with status: Bool) {
        let messagePrefix = status ? "You have access to " : "You haven't access to "
        let nameOfCurrentPermissionService = String(describing: type(of: self))
        let nameOfBasePermissionService = String(describing: type(of: PermissionService.self))
        let messageSuffix = nameOfCurrentPermissionService.components(separatedBy: nameOfBasePermissionService).first!
        message = messagePrefix + messageSuffix
    }

    private func complete(with status: Bool, _ completion: @escaping (AuthorizationCompletion) -> Void) {
        formMessage(with: status)

        let result = (status: status, message: message)
        completion(result)
    }
}

class CameraPermissionService: PermissionService {
    override func checkStatus() -> Bool {
        let status = AVCaptureDevice.authorizationStatus(for: .video).rawValue
        return status == AVAuthorizationStatus.authorized.rawValue
    }

    override func requestAuthorization(_ completion: @escaping (Bool) -> Void) {
        AVCaptureDevice.requestAccess(for: .video) { status in
            completion(status)
        }
    }
}

class PhotoPermissionService: PermissionService {
    override func checkStatus() -> Bool {
        let status = PHPhotoLibrary.authorizationStatus().rawValue
        return status == PHAuthorizationStatus.authorized.rawValue
    }

    override func requestAuthorization(_ completion: @escaping (Bool) -> Void) {
        PHPhotoLibrary.requestAuthorization { status in
            completion(status.rawValue == PHAuthorizationStatus.authorized.rawValue)
        }
    }
}

// Usage
let permissionServices = [CameraPermissionService(), PhotoPermissionService()]

for permissionService in permissionServices {
    permissionService.authorize { (_, message) in
        print(message)
    }
}

// Result:
// You have access to Camera
// You have access to Photo
```

 카메라 퍼미션 서비스와 포토 퍼미션 서비스를 구현하고 이 두개의 권한을 요청하고 성공 실패시 처리하는 서비스를 구현합니다. 어떤 권한 요청이 추가되든 변동이 없고, 권한 실패시 처리 로직이 변경되어도 템플릿의 퍼미션 서비스만 수정하면 모든 서비스 요청에 적용할 수 있습니다.
