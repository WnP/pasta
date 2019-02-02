IMAGE=57333v3/pasta:latest

.DEFAULT_GOAL := default

clean:
	rm -rf ./dist ./build ./pasta.egg-info

install:
	pip install -r ./requirements.txt

wheel:
	python setup.py bdist_wheel

image:
	docker build -t $(IMAGE) .

push:
	docker push $(IMAGE)

default: clean install wheel image push
