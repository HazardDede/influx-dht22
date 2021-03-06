.PHONY: clean build

RELEASE_IMAGE_NAME = influx-dht22
CURRENT_TAG = latest

CONTAINER_NAME = influx-dht22

build:
	docker build -t $(RELEASE_IMAGE_NAME):$(CURRENT_TAG) .

shell: build
	docker run -it --rm --name $(CONTAINER_NAME) --privileged --cap-add SYS_RAWIO --device=/dev/mem $(RELEASE_IMAGE_NAME):$(CURRENT_TAG) bash

run: build
	docker run --rm --name $(CONTAINER_NAME) --privileged --cap-add SYS_RAWIO --device=/dev/mem $(RELEASE_IMAGE_NAME):$(CURRENT_TAG)

clean:
	docker ps -a | grep '$(CONTAINER_NAME)' | awk '{print $$1}' | xargs docker rm
	if [ $(shell docker image inspect $(RELEASE_IMAGE_NAME):$(CURRENT_TAG) > /dev/null 2>/dev/null ; echo $$?) -eq 0 ] ; then docker rmi $(RELEASE_IMAGE_NAME):$(CURRENT_TAG) ; fi

