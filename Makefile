
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
	echo "	- use the dry run option '-n' to show what make is attempting to do. example: make -n NEXT_WEEK"

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

.PHONY: raw_db ## ⬇️ To fetch specific entries of WeeklyCuration database in my personal Notion db, eg. make NEXT_WEEK ISSUE="17 Jul. 2023"
raw_db: ISSUE:=10th of July 2023
raw_db: check-notion-api-key check-notion-db
	echo "[⋆] Fetching entries of WeeklyCuration database for ${ISSUE}..."
	curl -s -X POST 'https://api.notion.com/v1/databases/${NOTION_DB}/query' \
		-H 'Authorization: Bearer '"$$NOTION_API_KEY"'' \
		-H 'Notion-Version: 2022-06-28' \
		-H "Content-Type: application/json" \
		--data "$$(envsubst < ls-notion-database.json)" > raw_db.json
	echo "[⋆] Newsletter entries are available @ file://$(PWD)/raw_db.json ..."

.PHONY: full_raw_db  ## ⏬ To fetch all entries of WeeklyCuration database in my personal Notion db
full_raw_db: check-notion-api-key check-notion-db
	echo "[⋆] Fetching entries of WeeklyCuration database for ${ISSUE}..."
	curl -s -X POST 'https://api.notion.com/v1/databases/${NOTION_DB}/query' \
		-H 'Authorization: Bearer '"$$NOTION_API_KEY"'' \
		-H 'Notion-Version: 2022-06-28' \
		-H "Content-Type: application/json" > full_raw_db.json
	echo "[⋆] Newsletter entries are available @ file://$(PWD)/full_raw_db.json ..."

.PHONY: ls-newsletter-headers  ## ❓ to list the newsletter headers that can be used as argument for raw_db target
ls-newsletter-headers: full_raw_db
	cat full_raw_db.json | jq "[.results[].properties.NewsletterIssueDateFormat.formula.string] | unique"

.PHONY: cleanup   ## 🧹 to clean up temporarily edited or downloaded file
cleanup:
	echo "[⋆] 🧹 Emptying NEXT_WEEK.md file ..." && > NEXT_WEEK.md
	echo "[⋆] 🧹 Removing JSON results files ..." && rm -f full_raw_db.json raw_db.json
	echo "[⋆] 🧹🧹 $@ done ✅🧹"

.PHONY: NEXT_WEEK  ## ⚙️ to transform JSON output from Notion API into Markdown content that can be copy/pasted in the README
NEXT_WEEK: raw_db
	cat raw_db.json | \
	jq "[.results[].properties | {Type: .Type.select.name, Category: .Category.select.name, Article: .Article.title[].text.content, Url: .URL.url, Subcategories: [.Subcategories.multi_select[].name]}]"  | \
	jq -r 'reduce .[] as $$item ({}; .[$$item.Category] += [$$item])' | \
	jq -r 'map({(.[0].Category): map("- \(.Type) [\(.Article)](\(.Url)) | #" + (.Subcategories | join(" #")))}) | add '  | \
	jq '.[] |= sort'  | \
	jq -r 'to_entries | sort_by(.key) | .[] |  "### \(.key)\n\n\(.value | join("\n"))\n"' > NEXT_WEEK.md
	echo "[⋆] Upcoming newsletter post is available @ file://$(PWD)/NEXT_WEEK.md ..."

.PHONY: add-issue  ## 📰 to generate and prepend an issue to README.md; safe to run again for the same ISSUE
add-issue:
	if [[ -z "$(ISSUE)" ]]; then
		echo '[!] ISSUE is required, e.g. make add-issue ISSUE="29th of August 2026"' >&2
		exit 2
	fi
	$(MAKE) NEXT_WEEK ISSUE="$(ISSUE)"
	if [[ ! -s NEXT_WEEK.md ]]; then
		echo '[!] NEXT_WEEK.md is empty; README.md was not changed.' >&2
		exit 1
	fi
	if grep -Fqx "## $(ISSUE)" README.md; then
		echo "[⋆] Issue '$(ISSUE)' is already present in README.md; nothing to do."
		exit 0
	fi
	tmp_file="$$(mktemp)"
	trap 'rm -f "$$tmp_file"' EXIT
	{
		sed -n '1,/^---$$/p' README.md
		printf '\n## %s\n\n' "$(ISSUE)"
		cat NEXT_WEEK.md
		printf '\n'
		sed '1,/^---$$/d' README.md
	} > "$$tmp_file"
	mv "$$tmp_file" README.md
	git diff --check -- README.md
	echo "[⋆] Issue '$(ISSUE)' was prepended to README.md."

.PHONY: release  ## 🚀 to tag and publish an issue as a GitHub Release; requires a clean, pushed working tree
release:
	if [[ -z "$(ISSUE)" || -z "$(ISSUE_NUMBER)" || -z "$(ISSUE_DATE)" ]]; then
		echo '[!] ISSUE, ISSUE_DATE and ISSUE_NUMBER are required, e.g. make release ISSUE_NUMBER=13 ISSUE="29th of August 2026" ISSUE_DATE="29 Aug. 2026"' >&2
		exit 2
	fi
	if ! command -v gh >/dev/null; then
		echo '[!] GitHub CLI (gh) is required.' >&2
		exit 1
	fi
	if ! git diff --quiet || ! git diff --cached --quiet; then
		echo '[!] Commit or discard local changes before creating a release.' >&2
		exit 1
	fi
	tag="issue#$(ISSUE_NUMBER)"
	if git rev-parse -q --verify "refs/tags/$$tag" >/dev/null; then
		echo "[!] Tag '$$tag' already exists." >&2
		exit 1
	fi
	if ! grep -Fqx "## $(ISSUE)" README.md; then
		echo "[!] Issue '$(ISSUE)' was not found in README.md." >&2
		exit 1
	fi
	notes_file="$$(mktemp)"
	trap 'rm -f "$$notes_file"' EXIT
	{
		printf '# Issue #%s\n\n## %s\n\n' "$(ISSUE_NUMBER)" "$(ISSUE_DATE)"
		awk -v heading="## $(ISSUE)" '$$0 == heading { inside = 1; next } inside && /^## / { exit } inside { print }' README.md
	} > "$$notes_file"
	git tag -a "$$tag" -m "Issue #$(ISSUE_NUMBER) - $(ISSUE_DATE)"
	git push origin "$$tag"
	gh release create "$$tag" --title "Issue #$(ISSUE_NUMBER) - $(ISSUE_DATE)" --notes-file "$$notes_file"
	echo "[⋆] GitHub Release '$$tag' was published."
