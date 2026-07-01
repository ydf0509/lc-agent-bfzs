"""
单独启动 lc-agent 桌面客户端窗口（服务器需已在运行）。

D:/ProgramData/miniconda3/envs/py312/pythonw.exe D:/codes/lc-agent-bfzs/bfzs/start_desktop.py

"""

from lc_agent.desktop import launch_desktop

launch_desktop(host='127.0.0.1', port=8001, title="心有灵犀")
