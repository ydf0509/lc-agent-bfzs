

# 1. Python 解释器
```
D:/ProgramData/miniconda3/envs/py312/python.exe
```

# 2. 当需要编写ai agent项目时候，需要用到模型和apikey时候，用本地4000端口的lietllm转发的模型

baseurl 是 http://localhost:4000/v1    会自动变成(http://localhost:4000/v1/chat/completions)
模型id 选 ds-deepseek-v4-flash
apikey  随便乱写一个，因为litellm我没配置apikey，所以不需要具体的apikey

例如:
```
OPENAI_API_KEY=sk-no-key-needed
OPENAI_BASE_URL=http://localhost:4000/v1
OPENAI_MODEL=ds-deepseek-v4-flash
```