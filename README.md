# proxy_fastapi
This is proxy service

##  Build
```docker build -t proxy_test .```

##  Run
To run this you need to add env variables.
Variable ```TARGET_HOST``` string example ```https://site.com```
Variable ```RETRY_CODES``` string example ```503``` or ```503, 500```

```docker run -e TARGET_HOST='https://site.com' -e RETRY_CODES='503' -p 8080:8080 proxy_test```
