# serverless-web-driver

based on [this blog post](https://fisproject.jp/2021/01/aws-lambda-container-running-selenium-with-headless-chrome/)

## Dockerfile

- Selenium required not greater than Python 3.7
  - in Python 3.8, Chrome Web Driver returns 127 error
  - selenium==3.141.0

## binary

- beta-headless-chromium-87.0.4280.27-amazonlinux-2017-03 from [serverless-chrome v1.0.0-57](https://github.com/adieuadieu/serverless-chrome/releases/tag/v1.0.0-57)
- ChromeDriver 87.0.4280.88 from [here](https://chromedriver.storage.googleapis.com/index.html?path=87.0.4280.88/)

```sh
% tree
.
├── Dockerfile
├── README.md
├── app.py
├── bin
│   ├── chromedriver
│   └── headless-chromium
└── headlessdriver.py

1 directory, 6 files
```

## local build

```sh
docker build -t image-name .
```

## Local Debug

### install RIE

```sh
mkdir -p ~/.aws-lambda-rie && curl -Lo ~/.aws-lambda-rie/aws-lambda-rie https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie && chmod +x ~/.aws-lambda-rie/aws-lambda-rie
```

### start local RIE

```sh
docker run -p 9000:8080 image-name
```

### send request to local RIE

```sh
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"query": "Python"}'
```

## regist ecr

### authenticate docker client

```sh
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin registry.region.amazonaws.com
```

### create ecr repo

```sh
aws ecr create-repository \
    --repository-name image-name \
    --image-scanning-configuration scanOnPush=true \
```

### tagging

```sh
docker tag image-name:latest registry.region1.amazonaws.com/image-name:latest
```

### push

```sh
docker push registry.region.amazonaws.com/image-name:latest
```

### Performance

- need 1024MB memory to cold start
