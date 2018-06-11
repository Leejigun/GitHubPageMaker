---
layout: post
current: post
navigation: True
title:  "Codable을 사용한 JSON 데이터 파싱"
date:   2018-06-11 00:00:00
cover: assets/images/Swift-JSON-Encoding.jpg
description: 인스타그램에서 공개한 라이브러리인 IGListKit을 소개하고 개념을 설명하고자 합니다.
tags: [ ios tip ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---

 

이번 포스트에서는 Swift4에서 추가된 **Codable** 프로토콜을 사용해 JSON 데이터를 처리하는 방법을 알아보겠습니다.

 과거 제가 처음으로 iOS를 공부할 때에는 `JSONSerialization` 을 사용한 방법이 책에 나와있었고 저도 한동안 그 방법으로 JSON 데이터를 처리했었습니다. (깊이 있는 책이었지만, 너무 오래된 책이었습니다.) JSON을 다루는데 이미 많은 라이브러리들이 있고, 처음으로 실무 프로젝트를 진행하게 되었을 때, 대부분의 프로젝트들이 JSON 관련 라이브러리를 사용하고 있었습니다.

 시간이 지나서 혼자 결정해야 할 경우가 생기자 JSON 라이브러리를 프로젝트에 추가하는 것을 고민하게 되었습니다. 물론 그런 라이브러리들은 단순히 JSON을 파싱하는데서 끝나는게 아닌 다양한 기능들을 내장하고 있지만, 그 중 실제로 사용하는 기능은 JSON 파싱정도가 전부였기에 Podfile에 한 줄 더 추가하는 일에 소극적이었습니다.

 이제는 개발할 때 JSON 을 만져야 할 경우 대부분 Codable을 사용하고 있습니다. Codable은 Swift4 버전에 추가된 프로토콜로 단순히 JSON을 만지는 것을 넘어서 다양한 쓰임세가 있습니다. 하지만, 이번 포스트에서는 제가 실제로 사용하는 코드를 보고 사용법을 알아보겠습니다.



# Codable 이전, 이후

* http://kka7.tistory.com/88

Codable을 사용하기 이전에는 JSON 파싱을 위해서 `JSONSerialization` 을 사용했습니다.

```
do { 
	if let todoJSON = try JSONSerialization.jsonObject(with: responseData, options: []) as? [String: Any], let todo = Todo(json: todoJSON) { 
		// created a TODO object 
		completionHandler(todo, nil) 
	} else { 
		// couldn't create a todo object from the JSON 
		let error = BackendError.objectSerialization(reason: "Couldn't create a todo object from the JSON") 
		completionHandler(nil, error) 
	} 
} catch { 
	// error trying to convert the data to JSON using JSONSerialization.jsonObject 			completionHandler(nil, error) return 
}	
출처: http://kka7.tistory.com/88 [때로는 까칠하게..]
```

 살펴보면`JSONSerialization` 을 사용해서 Data를 [String:Any] 형태의 딕셔너리로 만들어 그것을 하나하나 파싱해서 사용했습니다. 이 [String: Any] 데이터를 Todo의 객체로 만들기 위해 Todo 구조체에 하나 하나 파싱하는 생성자를 만들어 추가하는 방법을 사용했었는데, 이 방법을 쓰면 JSON관련 라이브러리를 사용하지 않고도 JSON 데이터를 파싱해서 사용 할 수 있었습니다. 

 하지만, 너무 번거롭고 많은 시간이 소요되기 때문에 단순히 JSON을 파싱하는 용도로 라이브러리를 추가해 사용하는 경우도 많았습니다.

 Codable이 추가된 이후에는 이렇게 사용하게 되었습니다.

```
let decoder = JSONDecoder() 
do { 
    let todo = try decoder.decode(Todo.self, from: responseData)
    completionHandler(todo, nil) 
} catch { 
    print("error trying to convert data to JSON") 
    print(error) 
    completionHandler(nil, error) 
}

출처: http://kka7.tistory.com/88 [때로는 까칠하게..]
```

자동으로 JSON Data를 Todo 구조체로 맵핑하는 동작을 수행합니다. 구조체마다 생성자를 사전에 만들 필요가 없기 때문에 코드도 짧아지고 코딩 시간도 줄었습니다.



# Codable 다양한 활용

#### 1. JSON 배열 파싱

만약, Todo의 배열이 내려온다고 해도 Codable을 추가했으면 똑같이 사용 가능합니다.

```
let decoder = JSONDecoder() 
do { 
    let todos = try decoder.decode([Todo].self, from: responseData) 
    completionHandler(todos, nil) 
} catch {
    print("error trying to convert data to JSON") 
    print(error) completionHandler(nil, error) 
}

출처: http://kka7.tistory.com/88 [때로는 까칠하게..]
```

 `decoder.decode([Todo].self, from: responseData)` 를 통해서 내려오는 데이터를 배열로 추측하고 디코딩을 수행합니다.



#### 2. toJSON

 `Codable` 은 두개의 프로토콜이 합쳐진 프로토콜입니다. 지금까지는 `Decodable` 만을 사용했는데, `Encodable` 역시 가지고 있습니다.

과거에는 `toJSON` 메소드를 내부에서 따로 만들어서 [String: Any] 로 만들도록 했습니다.

```
func toJSON() -> [String: Any] { 
    var json = [String: Any]() 
    json["title"] = title 
    json["userId"] = userId 
    json["completed"] = completed 
    if let id = id { 
    	json["id"] = id 
    } return json 
}

출처: http://kka7.tistory.com/88 [때로는 까칠하게..]
```

하지만, `Codable` 을 수행한다면,  디코더를 사용하는 것처럼 사용하면 됩니다.

```
let encoder = JSONEncoder() 
do { 
    let newTodoAsJSON = try encoder.encode(self) 
    todosUrlRequest.httpBody = newTodoAsJSON 
} catch { 
    print(error) 
    completionHandler(error) 
}

출처: http://kka7.tistory.com/88 [때로는 까칠하게..]
```



#### 3. 복잡한 JSON

 JSON 객체 내부가 복잡하게 JSON들로 중첩된 경우도 간단합니다. 내부에 들어가는 JSON 형태가 구조체로 정의되어있고 이 역시 `Codable` 을 사용한다면 자동으로 파싱해줍니다.

```
struct Address: Codable { 
    let city: String 
    let zipcode: String 
} 
struct User: Codable { 
    let id: Int? 
    let name: String 
    let email: String 
    let address: Address 
}

출처: http://kka7.tistory.com/88 [때로는 까칠하게..]
```



#### 4. 다른 프로퍼티 이름

 이제 실제 외부의 데이터를 파싱할 때 종종 경험하는 현상들인데, JSON의 프로퍼티 이름이 사용 언어의 지정어인 경우가 있습니다. 예를 들자면 특정 프로퍼티의 이름이 `id` 일 경우는 상당히 많이 경험했습니다. 이런 경우 Struct 내부에 `enum CodingKeys` 를 선언해주면 자동으로 맵핑되는 기능을 제공하고 있습니다.

```
struct Todo: Codable { 
    var displayTitle: String 
    var serverId: Int? 
    var userId: Int 
    var completed: Int 

    enum CodingKeys: String, CodingKey {
        case displayTitle = "title" 
        case serverId = "id" 
        case userId 
        case completed 
    }
}

출처: http://kka7.tistory.com/88 [때로는 까칠하게..]
```



# Tayga

  이제 제가 실제 `Tayga` 앱에서 사용한 코드를 한번 보겠습니다.

 저는 TwitchAPI를 통해서 데이터를 받아오기 때문에 먼저 Postman으로 API를 찔러서 데이터를 읽어왔습니다. 1개의 데이터만 요청해보겠습니다.

```
{
    "_total": 1549,
    "_links": {
        "self": "https://api.twitch.tv/kraken/games/top?limit=1",
        "next": "https://api.twitch.tv/kraken/games/top?limit=1&offset=1"
    },
    "top": [
        {
            "game": {
                "name": "Fortnite",
                "popularity": 127648,
                "_id": 33214,
                "giantbomb_id": 37030,
                "box": {
                    "large": "https://static-cdn.jtvnw.net/ttv-boxart/Fortnite-272x380.jpg",
                    "medium": "https://static-cdn.jtvnw.net/ttv-boxart/Fortnite-136x190.jpg",
                    "small": "https://static-cdn.jtvnw.net/ttv-boxart/Fortnite-52x72.jpg",
                    "template": "https://static-cdn.jtvnw.net/ttv-boxart/Fortnite-{width}x{height}.jpg"
                },
                "logo": {
                    "large": "https://static-cdn.jtvnw.net/ttv-logoart/Fortnite-240x144.jpg",
                    "medium": "https://static-cdn.jtvnw.net/ttv-logoart/Fortnite-120x72.jpg",
                    "small": "https://static-cdn.jtvnw.net/ttv-logoart/Fortnite-60x36.jpg",
                    "template": "https://static-cdn.jtvnw.net/ttv-logoart/Fortnite-{width}x{height}.jpg"
                },
                "_links": {},
                "localized_name": "Fortnite",
                "locale": "ko-kr"
            },
            "viewers": 129320,
            "channels": 8241
        }
    ]
}
```

 이 정도의 긴 데이터를 만약 `Codable` 없이 처리하려고 한다면 엄청나게 번거롭고 수고스러울 것 같습니다. 이제 제가 짠 구조체를 봅시다.

```
struct GamesStruct: Codable {
    let _total: Int
    let top: [TopGame]
}
struct TopGame: Codable {
    let channels: Int
    let viewers: Int
    let game: GameInfo
}
struct GameInfo: Codable {
    let _id: Int
    let box: BoxContainer
    struct BoxContainer: Codable {
        let large: String
        let medium: String
        let small: String
        let template: String
    }
    let giantbomb_id: Int
    let logo: Logo
    struct Logo: Codable {
        let large: String
        let medium: String
        let small: String
        let template: String
    }
    let name: String
    let popularity: Int
}
```

 `Codable` 구조체의 중첩된 형태로 들어가게 되었습니다.



# Rx와 궁합

 제가 ` Codable` 을 사용하는 것을 선호하는 다른 한가지 이유는 Rx를 사용할 때 더욱 가독성이 좋기 때문입니다.

```
provider.rx.request(.getTopGame(param))
    .observeOn(ConcurrentDispatchQueueScheduler(qos: .background))
    .retry(3)
    .asObservable()
    .map { try JSONDecoder().decode(GamesStruct.self, from: $0.data) }
    .catchErrorJustReturn(nil)
    .map { $0?.top ?? [] }
    .map { $0.enumerated()
    .map { GameViewModel(game: $1, offset: self.offset) }
}
```

 간단하게 한줄로 받아온 데이터를 파싱해서 사용하고 있습니다. 사실 Rx랑 전혀 연관이 없지만, 기존에 사용하던 방식은 가독성이 조금 떨어졌는데 Rx와 Codable을 한번에 사용하니 보기 편해서 많이 사용하고 있습니다.