"""数据分析工具组 — 提供简单的数据处理和计算功能"""

import json
import math
from typing import Any

from lc_agent import tool


@tool(group="data_analysis", group_description="数据分析")
def calculate(expression: str) -> str:
    """计算数学表达式。支持基本运算和 math 模块函数。

    Args:
        expression: 数学表达式，如 "2**10", "math.sqrt(144)", "sum([1,2,3,4,5])"
    """
    allowed_names = {
        k: v for k, v in math.__dict__.items() if not k.startswith("_")
    }
    allowed_names.update({"abs": abs, "round": round, "sum": sum, "min": min, "max": max})

    try:
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算错误: {e}"


@tool(group="data_analysis", group_description="数据分析")
def parse_json(json_string: str) -> str:
    """解析 JSON 字符串并格式化输出。

    Args:
        json_string: JSON 格式字符串
    """
    try:
        data = json.loads(json_string)
        formatted = json.dumps(data, ensure_ascii=False, indent=2)
        return f"解析结果:\n{formatted}"
    except json.JSONDecodeError as e:
        return f"JSON 解析失败: {e}"


@tool(group="data_analysis", group_description="数据分析")
def text_statistics(text: str) -> str:
    """统计文本的基本信息。

    Args:
        text: 要分析的文本
    """
    lines = text.split("\n")
    words = text.split()
    chars = len(text)
    chars_no_space = len(text.replace(" ", "").replace("\n", ""))

    return (
        f"文本统计:\n"
        f"  总字符数: {chars}\n"
        f"  字符数(不含空格): {chars_no_space}\n"
        f"  行数: {len(lines)}\n"
        f"  词数/段落数: {len(words)}"
    )


@tool(group="data_analysis", group_description="数据分析")
def csv_preview(file_path: str, max_rows: int = 10) -> str:
    """预览 CSV 文件的前几行。

    Args:
        file_path: CSV 文件路径
        max_rows: 最多显示的行数，默认10行
    """
    from pathlib import Path
    import csv

    p = Path(file_path).expanduser()
    if not p.exists():
        return f"错误: 文件不存在 - {p}"

    try:
        with open(p, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = []
            for i, row in enumerate(reader):
                if i >= max_rows + 1:
                    break
                rows.append(row)

        if not rows:
            return "CSV 文件为空"

        header = rows[0]
        data_rows = rows[1:]
        col_widths = [max(len(str(cell)) for cell in col) for col in zip(*rows)]

        lines = []
        lines.append(" | ".join(h.ljust(w) for h, w in zip(header, col_widths)))
        lines.append("-+-".join("-" * w for w in col_widths))
        for row in data_rows:
            lines.append(" | ".join(str(c).ljust(w) for c, w in zip(row, col_widths)))

        return f"CSV 预览 ({p.name}, 显示 {len(data_rows)} 行):\n\n" + "\n".join(lines)
    except Exception as e:
        return f"读取 CSV 失败: {e}"
