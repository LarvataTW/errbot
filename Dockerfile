FROM python:3.9-alpine as base
FROM base as builder
RUN apk --no-cache --update add build-base
COPY requirements.txt /requirements.txt
RUN pip install --user -r /requirements.txt

FROM base
# copy only the dependencies installation from the 1st stage image
RUN apk --no-cache --update add git curl
COPY --from=builder /root/.local /root/.local
COPY . /app
WORKDIR /app

RUN mkdir -p backends && \
    cd backends && \
    git clone https://github.com/gbin/err-backend-discord.git

# update PATH environment variable
ENV PATH=/root/.local/bin:$PATH

CMD ["errbot"]
