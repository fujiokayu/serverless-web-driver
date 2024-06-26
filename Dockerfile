FROM public.ecr.aws/lambda/python:3.7

RUN pip install --upgrade pip && \
    pip install -t ./ selenium==3.141.0
    
COPY *.py  ./
COPY bin/chromedriver /var/task/bin/
COPY bin/headless-chromium /var/task/bin/

CMD ["app.handler"]
