This provides a basic interface for the brilliant daftlistings module

Todo

[] Find a non blocking solution/ run the cron in the background

[] Basic logging

[] Tests

[] Messaging

[] Include more search options

[Daft Listings Repo](https://github.com/AnthonyBloomer/daftlistings)

![interface](https://s9.postimg.cc/havwm5di7/Screen_Shot_2018-04-12_at_09.09.27.png)


App has been updated to use Docker


```chmod u+x build.sh run.sh clean.sh```


Build the app


```./build.sh```


Run the app

```./run.sh```

To remove the image

```./clean.sh```


I've added RabbitMQ which is currently checking if a passed string is a palindrome


To run Celery


```celery -A app worker --loglevel=info```

To run RabbitMQ

```rabbitmq-server```



Run the python shell


then


```from app import *```

then


```
>>> isPalindrome.delay('Racecar')
<AsyncResult: 882c4e2d-ae69-4721-ad7f-8da3893e5de9>
```

```http://localhost:15672/#/```


login:

user: guest

pass: guest





