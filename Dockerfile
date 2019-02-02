FROM python:3.6-alpine

COPY ./dist/pasta-1.0.0-py3-none-any.whl /tmp/
ENV REDIS_HOST redis
ENV TLS yep

RUN pip install --no-cache-dir wheel /tmp/pasta-1.0.0-py3-none-any.whl waitress
RUN rm /tmp/pasta-1.0.0-py3-none-any.whl

CMD ["waitress-serve", "--call", "pasta:create_app"]
