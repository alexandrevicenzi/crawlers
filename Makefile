.PHONY: clean

setup:
	pip install -r requirements.txt

serve:
	docker-compose up

deploy:
	scrapyd-deploy

crawl:
	scrapy crawl $(spider)

schedule:
	curl http://localhost:6800/schedule.json -d project=crawler -d spider=$(spider)

clean:
	rm -rf build
	rm -rf project.egg-info
