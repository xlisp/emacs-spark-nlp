# AI any text clusterer & sorting
* Why: When your log files are very large and there are so many of them, and you don't know where to start, you can use ai-any-text-clusterer to classify your logs or files, git logs and other texts, so that you can clearly see where the relevant information is.

## Feature

- [x] File clustering (matching rules)
- [x] Filter markdown todos
- [ ] Log clustering
- [ ] Git log clustering
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

## Visualization

![](./visualization.gif)
