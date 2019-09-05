---
layout: post
current: post
navigation: True
title:  "Swift Moya Provider 커스텀"
date:   2019-09-05 00:00:01
cover: assets/images/ios_tips/moya.png
description: Swift Moya Provider 커스텀
tags: [ ios tip  ]
class: post-template
subclass: 'post tag-getting-started'
author: jglee
---
# Swift Moya Provider 커스텀
 예전에 Moya + RxSwift에 대한 포스트를 올린적이 있었는데, 이번에는 제가 프로젝트에서 사용하고 있는 Moya Provider를 커스텀 한 내용을 공유하고자 합니다.


## Plugins
- moya plugun : https://github.com/Moya/Moya/blob/master/docs/Plugins.md

  **Moya** 는 기본적으로 **Target** 을 정의하고 **Provider** 를 만들어 그 **Provider** 를 사용해 통신하는 방법으로 네트워크 프레임 워크를 구현하고 있습니다. 이것저것 기타 정보들은 타겟에 정의하고 밑에서는 **Provider** 를 사용해서 접근하게 되는데, 처음에 사용할 때에는 크게 문제없지만 규모가 커지면 어쩔 수 없이 **Provider** 를 커스텀 하는 단계까지 도달하게 됩니다. 그중 대부분의 사용자가 편리한 기능들을 추가할 때 사용하는 부분이 바로 플러그인입니다.  먼저 제가 사용하고 있는 **Provider** 의 전체 코드를 보여드리고 밑에서 하나하나 뜯어보겠습니다.

```swift
    class OpenitProvider<T:TargetType>: MoyaProvider<T> {
      init(stubClosure: @escaping StubClosure = MoyaProvider.neverStub) {
        /// NetworkActivityPlugin
        let networkClosure = {(_ change: NetworkActivityChangeType, _ target: TargetType) in
          switch change {
            case .began:
            UIApplication.shared.isNetworkActivityIndicatorVisible = true
            case .ended:
            UIApplication.shared.isNetworkActivityIndicatorVisible = false
          }
        }
        //Your custom configuration
        let configuration = URLSessionConfiguration.default
        configuration.httpAdditionalHeaders = Manager.defaultHTTPHeaders
        ///Add the network logger on the configuration
        //For Alamofire
        let manager = Manager(configuration: configuration)
        manager.startRequestsImmediately = false
        // make provider
        super.init(stubClosure: stubClosure,
                   manager: manager,
                   plugins: [APILoggingPlugin(),
                            NetworkActivityPlugin(networkActivityClosure: networkClosure)])
      }
    }
```


----------
## NetworkActivityPlugin

 Moya를 사용하면서 가장 먼저 부딪치는 문제로 Network Activity Indicator 문제일 겁니다. Alamofire나 다른 통신 방법들을 사용하면 공통 메소드를 만들어 간단하게 처리할 수 있는데, 저는 RxSwift와 Moya를 사용하는 케이스라 이게 공통으로 만들어서 쓰기 번거로웠습니다.
  처음 Moya와 RxSwift를 함께 사용했을 때에는 api 호출 전에 **do(onNext)** 에서 시작하고 종료하는 로직을 추가해서 사용했었는데, 이게 하나하나 추가해서 쓰는 게 여간 불편한 게 아녔습니다. 그래서 처음에 plugin이 있는지도 모르고 쓰고 있다가 moya 문서에서 plugin 내용을 발견했습니다. 문서 하단에 아주 친절하게 나와 있었습니다.


----------

**Network Activity Indicator**
One very common task with iOS networking is to show a network activity indicator during network requests, and remove it when all requests have finished. The provided plugin adds callbacks which are called when a requests starts and finishes, which can be used to keep track of the number of requests in progress, and show / hide the network activity indicator accordingly.
The plugin can be found at `[Sources/Moya/Plugins/NetworkActivityPlugin.swift](https://github.com/Moya/Moya/blob/master/Sources/Moya/Plugins/NetworkActivityPlugin.swift)`


----------

 덕분에 쉽게 사용 예시들을 찾아서 추가했는데 그 내용이 이 코드입니다.

```swift
    /// NetworkActivityPlugin
    let networkClosure = {(_ change: NetworkActivityChangeType, _ target: TargetType) in
      switch change {
        case .began:
          UIApplication.shared.isNetworkActivityIndicatorVisible = true
        case .ended:
          UIApplication.shared.isNetworkActivityIndicatorVisible = false
      }
    }

    NetworkActivityPlugin(networkActivityClosure: networkClosure)
```
네트워크 클로저에서는 이것 말고도 여러 작업을 할 수 있습니다. 따로 설명 없이도 쉽게 이해하실 수 있겠지만 내용을 보시면 네트워크 began일 때 네트워크 인디케이터를 돌리고 ended일 때 멈춥니다. 그리고 그 클로져를 **NetworkActivityPlugin** 에 집어넣어 **Provider** 를 만들어줍니다.


## Logging Plugin

 처음으로 **Provider** 를 확장해서 사용해보고 **Plugin** 의 존재를 알게 되고 이것저것 시험해봤습니다. 무엇을 할 수 있을까 고민하다가 다음으로 시도한 게 Logging입니다. 저희 프로젝트에서는 항상 Header에 사용자 정보를 담아서 API를 주고받고 있습니다. 근데 이게 잘못된 경우도 쉽게 알게 하기 위해서 통신 부분만 플러그인으로 로그를 찍어보기로 했습니다.
  문서를 보면 기본적으로 네트워크 로깅을 지원합니다.


----------

**Logging**
During development it can be very useful to log network activity to the console. This can be anything from the URL of a request as sent and received, to logging full headers, method, request body on each request and response.
The provided plugin for logging is the most complex of the provided plugins, and can be configured to suit the amount of logging your app (and build type) require. When initializing the plugin, you can choose options for verbosity, whether to log curl commands, and provide functions for outputting data (useful if you are using your own log framework instead of `print`) and formatting data before printing (by default the response will be converted to a String using `String.Encoding.utf8` but if you'd like to convert to pretty-printed JSON for your responses you can pass in a formatter function, see the function `JSONResponseDataFormatter` in `[Examples/_shared/GitHubAPI.swift](https://github.com/Moya/Moya/blob/master/Examples/_shared/GitHubAPI.swift)` for an example that does exactly that)
The plugin can be found at `[Sources/Moya/Plugins/NetworkLoggerPlugin.swift](https://github.com/Moya/Moya/blob/master/Sources/Moya/Plugins/NetworkLoggerPlugin.swift)`

----------

 하지만 로깅을 찍는 결과가 제가 원하는 형태가 아니라서 너무 보기 불편해 커스텀 플러그인을 만들어서 사용하기로 했습니다.
  커스텀 플러그인을 만들려면 PluginType 을 구현해야 합니다.
```swift
    public protocol PluginType {
      func prepare(_ request: URLRequest, target: TargetType) -> URLRequest
      func willSend(_ request: RequestType, target: TargetType)
      func didReceive(_ result: Result<Moya.Response, MoyaError>, target: TargetType)
      func process(_ result: Result<Moya.Response, MoyaError>, target: TargetType) -> Result<Moya.Response, MoyaError>
    }
```
 메소드를 보면 아시겠지만 api 실행 전에 보내는 것의 로그를 찍고 api의 response를 받은 후에 그 내용을 찍으면 끝이기 때문에 **willSend** 와 **didReceive** 를 구현해주면 됩니다.

```swift
    final class APILoggingPlugin: PluginType {
      /// API를 보내기 직전에 호출
      func willSend(_ request: RequestType, target: TargetType) {
        let headers = request.request?.allHTTPHeaderFields ?? [:]
        let url = request.request?.url?.absoluteString ?? "nil"
        let path = url.replacingOccurrences(of: "\(juvisAPIbaseURL)", with: "")
        if let body = request.request?.httpBody {
          let bodyString = String(bytes: body, encoding: String.Encoding.utf8) ?? "nil"
          logInfo("""
                  <willSend - \(path) - \(Date().debugDescription)>
                  url: \(url)
                  headers : \(headers)
                  body: \(bodyString)
          """)
        } else {
          logInfo("""
                  <willSend - \(path) - \(Date().debugDescription)>
                  url: \(url)
                  headers : \(headers)
                  body: nil
          """)
        }
      }

      /// API Response
      func didReceive(_ result: Result<Response, MoyaError>, target: TargetType) {
        let response = result.value
        let error = result.error
        let request = response?.request
        let url = request?.url?.absoluteString ?? "nil"
        let method = request?.httpMethod ?? "nil"
        let statusCode = response?.statusCode ?? 0
        var bodyString = "nil"
        if let data = request?.httpBody, let string = String(bytes: data, encoding: String.Encoding.utf8) {
          bodyString = string
        }
        var responseString = "nil"
        if let data = response?.data, let reString = String(bytes: data, encoding: String.Encoding.utf8) {
          responseString = reString
        }
        logInfo("""
                <didReceive - \(method) statusCode: \(statusCode)>
                url: \(url)
                body: \(bodyString)
                error: \(error?.localizedDescription ?? "nil")
                response: \(responseString)
        """)
      }
    }
```

## Stub Closure

 추가적으로 제가 맨 앞에서 보여드린 코드를 보면 stubClosure라는게 있습니다.
```swift
     class OpenitProvider<T:TargetType>: MoyaProvider<T> {
      init(stubClosure: @escaping StubClosure = MoyaProvider.neverStub) {
        ...
        super.init(stubClosure: stubClosure,
                       manager: manager,
                       plugins: [APILoggingPlugin(),
                                 NetworkActivityPlugin(networkActivityClosure: networkClosure)])
      }
    }
```
 이 Stub Closure는 **Unit test** 에서 제가 사용하는 것으로 없을경우에는 기본적으로 NeverStub가 붙어있는데, 여기에 클로저를 추가할 경우 API를 타지 않고 sample data에서 json을 꺼내와서 사용할 수 있습니다.

```swift
    # SplashViewControllerUnitTest.swift
    ...
    override func setUp() {
      // Put setup code here. This method is called before the invocation of each test method in the class.
      viewModel = SplashControllerViewModel(provider: OpenitProvider<JuvisAPI>(stubClosure: MoyaProvider.immediatelyStub))
      disposeBag = DisposeBag()
    }
    ...
```
 unit test는 기본적으로 네트워크 상태에 영향을 받으면 안되는데, 테스트 케이스를 만들다보면 어쩔수 없이 로직이 api와 연결되는 경우가 많습니다. 특히 RxSwift를 사용할 경우 네트워크 통신과 로직이 함께 붙어있는 경우가 많아서 유용하게 사용하실 수 있습니다.

----------


## RxSwift Extension

 마지막으로 제가 만든 Provider 커스텀 파일에는 하나의 코드 구문이 더 있습니다. 바로 Rx 관련 구문인데 모든 부분에 timeout을 추가해야 하는 이슈가 있었습니다.
 앞선 이유와 같은 이유로 RxSwift의 extension을 만들어서 사용하고 있습니다.
```swift
    extension Reactive where Base: OpenitProvider<JuvisAPI> {
      /// Designated request-making method.
      ///
      /// - Parameters:
      ///   - token: Entity, which provides specifications necessary for a `MoyaProvider`.
      ///   - callbackQueue: Callback queue. If nil - queue from provider initializer will be used.
      /// - Returns: Single response object.
      internal func request(_ token: Base.Target, callbackQueue: DispatchQueue? = nil) -> Single<Response> {
        return Single.create { [weak base] single in
          let cancellableToken = base?.request(token, callbackQueue: callbackQueue, progress: nil) { result in
          switch result {
            case let .success(response):
              single(.success(response))
            case let .failure(error):
              single(.error(error))
            }
          }

          return Disposables.create {
            cancellableToken?.cancel()
          }
        }.timeout(10, scheduler: MainScheduler.asyncInstance)
      }
    }
```

## 마치며

 moya의 문서를 찾아보면 여러 가지 다양한 이슈에 대한 처리 방법이 자세히 나와 있습니다. 대부분의 사례에 대해서 지원하거나 커스텀 할 수 있도록 네트워크 계층을 분리하고 있습니다. 이러한 다양한 확장성과 이점 때문에 내가 스스로 만들어 쓸 수 있는 능력이 있다고 해도 Moya를 쓰지 말아야 할 이유는 없다고 생각합니다. 한번 익숙해지면 이거 없이는 개발 못 할 정도입니다. 다들 한번 배워보시는 것을 추천합니다.
