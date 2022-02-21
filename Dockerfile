FROM python:3.9-alpine as base
FROM base as builder
RUN apk --no-cache --update add build-base libffi-dev
COPY requirements.txt /requirements.txt
RUN pip install --user -r /requirements.txt

FROM base
RUN apk --no-cache --update add git curl bind-tools iputils
# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
COPY . /app
WORKDIR /app
RUN mkdir -p data plugins backends storages
RUN cd /app/backends && \
    git clone https://github.com/gbin/err-backend-discord.git
RUN cd /app/storages && \
    git clone https://github.com/errbotio/err-storage-sql.git
# update PATH environment variable
ENV PATH=/root/.local/bin:$PATH

CMD ["errbot"]
