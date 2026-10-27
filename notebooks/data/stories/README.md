# 故事语料（完整文本）

| 文件 | 说明 |
|------|------|
| `alice_in_wonderland.txt` | 《Alice's Adventures in Wonderland》（Lewis Carroll），[Project Gutenberg #11](https://www.gutenberg.org/ebooks/11)，公版 |

HMM 需要词性：加载时用 NLTK `pos_tag` **自动标注**（不是人工金标）。

也可自行放入其它 `.txt` 公版小说，在 notebook 里改路径调用 `load_plain_story_tagged(path)`。

Kaggle 上更大的小说合集例如：

- [Project Gutenberg Fiction Books](https://www.kaggle.com/datasets/sukanto/project-gutenberg-fiction-books)
- [Classic Fantasy & Adventure Literature Corpus](https://www.kaggle.com/datasets/mehhti/classic-fantasy-and-adventure-literature-corpus)

体积较大，需自行下载后放到本目录或改加载代码。
