# Reference testing protocol

## Layer 1

> http -v POST localhost:3218/v1/HELLO
POST /v1/HELLO HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 0
Host: localhost:3218
User-Agent: HTTPie/1.0.3



HTTP/1.1 200 OK
Content-Length: 194
Content-Type: text/html; charset=UTF-8
Date: Thu, 05 Dec 2019 19:29:29 GMT
Server: TornadoServer/6.0.3

{
    "federated": false,
    "highest-supported-layer": 1,
    "servername": "localhost",
    "supported-auth-methods": [
        "AUTH-PLAIN"
    ],
    "supported-register-methods": [
        "REGISTER-PLAIN",
        "REGISTER-INSTRUCTIONS"
    ]
}


> http -v POST localhost:3218/v1/REGISTER-PLAIN login=vasya password='cXdlcnR5'
POST /v1/REGISTER-PLAIN HTTP/1.1
Accept: application/json, */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 42
Content-Type: application/json
Host: localhost:3218
User-Agent: HTTPie/1.0.3

{
    "login": "vasya",
    "password": "cXdlcnR5"
}

HTTP/1.1 200 OK
Content-Length: 0
Content-Type: text/html; charset=UTF-8
Date: Thu, 05 Dec 2019 19:31:00 GMT
Server: TornadoServer/6.0.3


> http -v POST localhost:3218/v1/REGISTER-INSTRUCTIONS
POST /v1/REGISTER-INSTRUCTIONS HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 0
Host: localhost:3218
User-Agent: HTTPie/1.0.3



HTTP/1.1 200 OK
Content-Length: 113
Content-Type: text/html; charset=UTF-8
Date: Thu, 05 Dec 2019 19:31:34 GMT
Server: TornadoServer/6.0.3

{
    "text": "Подайте заявление в бумажном виде",
    "url": "https://example.com/register"
}


> http -v POST localhost:3218/v1/AUTH-PLAIN login=vasya password='cXdlcnR5'
POST /v1/AUTH-PLAIN HTTP/1.1
Accept: application/json, */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 42
Content-Type: application/json
Host: localhost:3218
User-Agent: HTTPie/1.0.3

{
    "login": "vasya",
    "password": "cXdlcnR5"
}

HTTP/1.1 200 OK
Content-Length: 78
Content-Type: text/html; charset=UTF-8
Date: Thu, 05 Dec 2019 19:32:09 GMT
Server: TornadoServer/6.0.3

{
    "sessid": "bbf6adadd981dad01b7bc8febe4a3cffbeefb58396dde5800d65728855391ef9"
}



> http -v POST localhost:3218/v1/REGISTER-PLAIN login=vasya password='cXdlcnR5'
POST /v1/REGISTER-PLAIN HTTP/1.1
Accept: application/json, */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 42
Content-Type: application/json
Host: localhost:3218
User-Agent: HTTPie/1.0.3

{
    "login": "vasya",
    "password": "cXdlcnR5"
}

HTTP/1.1 403 Forbidden
Content-Length: 0
Content-Type: text/html; charset=UTF-8
Date: Thu, 05 Dec 2019 19:32:34 GMT
Server: TornadoServer/6.0.3


## Layer 2

> http -v POST localhost:3218/v2/CONTACTS-GET 'X-Session:bbf6adadd981dad01b7bc8febe4a3cffbeefb58396dde5800d65728855391ef9'
POST /v2/CONTACTS-GET HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 0
Host: localhost:3218
User-Agent: HTTPie/1.0.3
X-Session: bbf6adadd981dad01b7bc8febe4a3cffbeefb58396dde5800d65728855391ef9



HTTP/1.1 200 OK
Content-Length: 12
Content-Type: text/html; charset=UTF-8
Date: Thu, 05 Dec 2019 19:33:19 GMT
Server: TornadoServer/6.0.3

{
    "data": []
}


Actually, should not accept because alice@ doesn't exist yet:


> http -v POST localhost:3218/v2/CONTACTS-ADD 'X-Session:bbf6adadd981dad01b7bc8febe4a3cffbeefb58396dde5800d65728855391ef9' id=alice@localhost name=Alice group:='["Friends"]'
POST /v2/CONTACTS-ADD HTTP/1.1
Accept: application/json, */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 72
Content-Type: application/json
Host: localhost:3218
User-Agent: HTTPie/1.0.3
X-Session: bbf6adadd981dad01b7bc8febe4a3cffbeefb58396dde5800d65728855391ef9

{
    "id": "alice@localhost",
    "group": [
        "Friends"
    ],
    "name": "Alice"
}

HTTP/1.1 200 OK
Content-Length: 0
Content-Type: text/html; charset=UTF-8
Date: Thu, 05 Dec 2019 19:49:55 GMT
Server: TornadoServer/6.0.3


> http -v POST localhost:3218/v2/CONTACTS-ADD 'X-Session:bbf6adadd981dad01b7bc8febe4a3cffbeefb58396dde5800d65728855391ef9' id=alice@localhost name=Alice group:='["Friends"]'
POST /v2/CONTACTS-ADD HTTP/1.1
Accept: application/json, */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 72
Content-Type: application/json
Host: localhost:3218
User-Agent: HTTPie/1.0.3
X-Session: bbf6adadd981dad01b7bc8febe4a3cffbeefb58396dde5800d65728855391ef9

{
    "id": "alice@localhost",
    "group": [
        "Friends"
    ],
    "name": "Alice"
}

HTTP/1.1 409 Conflict
Content-Length: 0
Content-Type: text/html; charset=UTF-8
Date: Thu, 05 Dec 2019 19:50:18 GMT
Server: TornadoServer/6.0.3


> http -v POST localhost:3218/v2/CONTACTS-GET 'X-Session:bbf6adadd981dad01b7bc8febe4a3cffbeefb58396dde5800d65728855391ef9'
POST /v2/CONTACTS-GET HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 0
Host: localhost:3218
User-Agent: HTTPie/1.0.3
X-Session: bbf6adadd981dad01b7bc8febe4a3cffbeefb58396dde5800d65728855391ef9



HTTP/1.1 200 OK
Content-Length: 130
Content-Type: text/html; charset=UTF-8
Date: Thu, 05 Dec 2019 19:50:35 GMT
Server: TornadoServer/6.0.3

{
    "data": [
        {
            "contact": {
                "group": [
                    "Friends"
                ],
                "id": "alice@localhost",
                "name": "Alice"
            },
            "last-seen": "2000-09-09T14:22:31+0300"
        }
    ]
}


Should actually return 4xx:


> http -v POST localhost:3218/v2/CONTACTS-CHANGE 'X-Session:bbf6adadd981dad01b7bc8febe4a3cffbeefb58396dde5800d65728855391ef9' id=bob@localhost name=Alice group:='["Friends"]'
POST /v2/CONTACTS-CHANGE HTTP/1.1
Accept: application/json, */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 70
Content-Type: application/json
Host: localhost:3218
User-Agent: HTTPie/1.0.3
X-Session: bbf6adadd981dad01b7bc8febe4a3cffbeefb58396dde5800d65728855391ef9

{
    "id": "bob@localhost",
    "group": [
        "Friends"
    ],
    "name": "Alice"
}

HTTP/1.1 500 Internal Server Error
Content-Length: 93
Content-Type: text/html; charset=UTF-8
Date: Thu, 05 Dec 2019 19:53:31 GMT
Server: TornadoServer/6.0.3

<html><title>500: Internal Server Error</title><body>500: Internal Server Error</body></html>


> http -v POST localhost:3218/v2/CONTACTS-CHANGE 'X-Session:bbf6adadd981dad01b7bc8febe4a3cffbeefb58396dde5800d65728855391ef9' id=alice@localhost name=ALICE group:='["Friends"]'
POST /v2/CONTACTS-CHANGE HTTP/1.1
Accept: application/json, */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 72
Content-Type: application/json
Host: localhost:3218
User-Agent: HTTPie/1.0.3
X-Session: bbf6adadd981dad01b7bc8febe4a3cffbeefb58396dde5800d65728855391ef9

{
    "id": "alice@localhost",
    "group": [
        "Friends"
    ],
    "name": "ALICE"
}

HTTP/1.1 200 OK
Content-Length: 0
Content-Type: text/html; charset=UTF-8
Date: Thu, 05 Dec 2019 19:54:13 GMT
Server: TornadoServer/6.0.3



> http -v POST localhost:3218/v2/CONTACTS-GET 'X-Session:bbf6adadd981dad01b7bc8febe4a3cffbeefb58396dde5800d65728855391ef9'
POST /v2/CONTACTS-GET HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 0
Host: localhost:3218
User-Agent: HTTPie/1.0.3
X-Session: bbf6adadd981dad01b7bc8febe4a3cffbeefb58396dde5800d65728855391ef9



HTTP/1.1 200 OK
Content-Length: 130
Content-Type: text/html; charset=UTF-8
Date: Thu, 05 Dec 2019 19:54:40 GMT
Server: TornadoServer/6.0.3

{
    "data": [
        {
            "contact": {
                "group": [
                    "Friends"
                ],
                "id": "alice@localhost",
                "name": "ALICE"
            },
            "last-seen": "2000-09-09T14:22:31+0300"
        }
    ]
}


Should actually return 4xx:

> http -v POST localhost:3218/v2/CONTACTS-DELETE 'X-Session:bbf6adadd981dad01b7bc8febe4a3cffbeefb5
8396dde5800d65728855391ef9' id=bobe@localhost
POST /v2/CONTACTS-DELETE HTTP/1.1
Accept: application/json, */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 24
Content-Type: application/json
Host: localhost:3218
User-Agent: HTTPie/1.0.3
X-Session: bbf6adadd981dad01b7bc8febe4a3cffbeefb58396dde5800d65728855391ef9

{
    "id": "bobe@localhost"
}

HTTP/1.1 500 Internal Server Error
Content-Length: 93
Content-Type: text/html; charset=UTF-8
Date: Thu, 05 Dec 2019 20:01:10 GMT
Server: TornadoServer/6.0.3

<html><title>500: Internal Server Error</title><body>500: Internal Server Error</body></html>


> http -v POST localhost:3218/v2/CONTACTS-DELETE 'X-Session:bbf6adadd981dad01b7bc8febe4a3cffbeefb58396dde5800d65728855391ef9' id=alice@localhost
POST /v2/CONTACTS-DELETE HTTP/1.1
Accept: application/json, */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 25
Content-Type: application/json
Host: localhost:3218
User-Agent: HTTPie/1.0.3
X-Session: bbf6adadd981dad01b7bc8febe4a3cffbeefb58396dde5800d65728855391ef9

{
    "id": "alice@localhost"
}

HTTP/1.1 200 OK
Content-Length: 0
Content-Type: text/html; charset=UTF-8
Date: Thu, 05 Dec 2019 20:01:40 GMT
Server: TornadoServer/6.0.3



> http -v POST localhost:3218/v2/CONTACTS-GET 'X-Session:bbf6adadd981dad01b7bc8febe4a3cffbeefb58396dde5800d65728855391ef9'
POST /v2/CONTACTS-GET HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 0
Host: localhost:3218
User-Agent: HTTPie/1.0.3
X-Session: bbf6adadd981dad01b7bc8febe4a3cffbeefb58396dde5800d65728855391ef9



HTTP/1.1 200 OK
Content-Length: 12
Content-Type: text/html; charset=UTF-8
Date: Thu, 05 Dec 2019 20:01:56 GMT
Server: TornadoServer/6.0.3

{
    "data": []
}
