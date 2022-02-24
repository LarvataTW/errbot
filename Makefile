.PHONY: docker
docker: ## 使用 docker container 啟動本地測試環境
	docker build -t errbot .
	docker run --rm -it -v $(PWD)/plugins:/app/plugins errbot

# Absolutely awesome: http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
