# AI any text clusterer & sorting
* Why: When your log files are very large and there are so many of them, and you don't know where to start, you can use ai-any-text-clusterer to classify your logs or files, git logs and other texts, so that you can clearly see where the relevant information is.

## Feature

- [x] File clustering (matching rules)
- [x] Filter markdown todos
- [x] Git log clustering
- [ ] Log clustering
- [ ] File sorting
- [ ] Visualization operate & process
- [ ] Support GPT ask for search or sorting

## Init

* Setup python env
```sh
conda create -n ai-any-text-clusterer python=3.11
conda activate ai-any-text-clusterer
poetry install
```
* [Ollama](https://ollama.com/) run embed model
```sh
ollama run nomic-embed-text
```

## Usage
* command
```sh
# function name: find_files_with_chinese_names, get_todo_items, get_git_log, ...
python ai_any_text_clusterer.py <function_name> <index_file_name>
```

## Visualization

![](./visualization.gif)
