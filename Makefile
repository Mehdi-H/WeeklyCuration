
# This is an auto documented Makefile. For more information see the following article
# @see http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

SHELL := /bin/bash
.SHELLFLAGS = -ec
.SILENT:
MAKEFLAGS += --silent
.ONESHELL:

.EXPORT_ALL_VARIABLES:

.DEFAULT_GOAL: help

.PHONY: help ## 🛟 To display this prompts. This will list all available targets with their documentation
help:
	echo "❓ Use \`make <target>' where <target> is one of 👇"
	grep -E '^\.PHONY: [a-zA-Z0-9_-]+ .*?##' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = "(: |##)"}; {printf "\033[36m%-30s\033[0m %s\n", $$2, $$3}'
	echo "Tips 💡"
	echo "	- use tab for auto-completion"
	echo "	- use the dry run option '-n' to show what make is attempting to do. example: environmentName=dev make -n deploy"

.PHONY:
check-notion-api-key:
ifndef NOTION_API_KEY
	$(error Env variable "NOTION_API_KEY" is not defined)
endif

.PHONY:
check-notion-db:
ifndef NOTION_DB
	$(error Env variable "NOTION_DB" is not defined)
endif

.PHONY: raw_db ## ⬇️ To fetch specific entries of WeeklyCuration database in my personal Notion db, eg. make NEXT_WEEK.md NEWSLETTER="17 Jul. 2023"
raw_db: NEWSLETTER:="10 Jul. 2023"
raw_db: check-notion-api-key check-notion-db
	echo "[⋆] Fetching entries of WeeklyCuration database for ${NEWSLETTER}..."
	curl -s -X POST 'https://api.notion.com/v1/databases/${NOTION_DB}/query' \
		-H 'Authorization: Bearer '"$$NOTION_API_KEY"'' \
		-H 'Notion-Version: 2022-06-28' \
		-H "Content-Type: application/json" \
		--data "$$(envsubst < ls-notion-database.json)" > raw_db.json
	echo "[⋆] Newsletter entries are available @ file://$(PWD)/raw_db.json ..."

.PHONY: full_raw_db  ## ⏬ To fetch all entries of WeeklyCuration database in my personal Notion db
full_raw_db: check-notion-api-key check-notion-db
	echo "[⋆] Fetching entries of WeeklyCuration database for ${NEWSLETTER}..."
	curl -s -X POST 'https://api.notion.com/v1/databases/${NOTION_DB}/query' \
		-H 'Authorization: Bearer '"$$NOTION_API_KEY"'' \
		-H 'Notion-Version: 2022-06-28' \
		-H "Content-Type: application/json" > full_raw_db.json
	echo "[⋆] Newsletter entries are available @ file://$(PWD)/full_raw_db.json ..."

.PHONY: ls-newsletter-headers  ## ❓ to list the newsletter headers that can be used as argument for raw_db.json target
ls-newsletter-headers: full_raw_db.json
	cat full_raw_db.json | jq "[.results[].properties.Newsletter.select.name] | unique"

cleanup:
	> NEXT_WEEK.md
	rm -f full_raw_db.json raw_db.json

.PHONY: NEXT_WEEK  ## ⚙️ to transform JSON output from Notion API into Markdown content that can be copy/pasted in the README
NEXT_WEEK: raw_db
	cat raw_db.json | \
	jq "[.results[].properties | {Type: .Type.select.name, Category: .Category.select.name, Article: .Article.title[].text.content, Url: .URL.url, Subcategories: [.Subcategories.multi_select[].name]}]"  | \
	jq -r 'reduce .[] as $$item ({}; .[$$item.Category] += [$$item])' | \
	jq -r 'map({(.[0].Category): map("- \(.Type) [\(.Article)](\(.Url)) | #" + (.Subcategories | join(" #")))}) | add '  | \
	jq '.[] |= sort'  | \
	jq -r 'to_entries | sort_by(.key) | .[] |  "### \(.key)\n\n\(.value | join("\n"))\n"' > NEXT_WEEK.md
	echo "[⋆] Upcoming newsletter post is available @ file://$(PWD)/NEXT_WEEK.md ..."

