FROM python:3.9-alpine as base
FROM base as builder
RUN apk --no-cache --update add build-base
COPY requirements.txt /requirements.txt
RUN pip install --user -r /requirements.txt

FROM base
# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
COPY . /app
WORKDIR /app

# update PATH environment variable
ENV PATH=/root/.local/bin:$PATH

CMD ["errbot"]
