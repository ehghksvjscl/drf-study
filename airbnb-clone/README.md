## TODO LIST - Code 첼린지 - 

GET POST /experiences [x]
GET PUT DELETE / experiences/1 [x]
GET POST /experiences/1/bookings [x]
GET PUT DELETE /experiences/1/bookings/2 [x]


## MOCK JSON

### POST : /experiences
```
{
    "name" : "test",
    "description" : "test",
    "price" : 100,
    "address" : "어딘가",
    "start" : "11:00:00",
    "end" : "12:00:00",
    "category" : 1
}
```

### GET PUT DELETE / experiences/1
``` PUT 
{
    "name" : "test update 2",
    "description" : "test update 2",
    "price" : 120,
    "address" : "어딘가 2",
    "start" : "11:02:00",
    "end" : "12:02:00",
    "category" : 2
}
```

### GET POST /experiences/1/bookings
```
{
    "check_in": "2022-11-05",
    "check_out": "2022-11-06",
    "guests": 2,
    "experience_time": "2021-08-01 10:00:00",
}
```

### GET PUT DELETE /experiences/1/bookings/2
``` PUT
{
    "check_in": "2022-11-04",
    "check_out": "2022-11-04",
    "experience_time": "2022-09-26 14:10:23",
    "guests": 1
}
```