"""文件管理工具组 — 提供文件读写、目录浏览等功能"""

from pathlib import Path
from typing import Annotated

from lc_agent import tool


@tool(group="file_mgmt", group_description="文件管理")
def read_file(
    file_path: Annotated[str, "文件的绝对或相对路径"],
) -> str:
    """读取指定文件的内容。"""
    p = Path(file_path).expanduser()
    if not p.exists():
        return f"错误: 文件不存在 - {p}"
    if not p.is_file():
        return f"错误: 路径不是文件 - {p}"
    try:
        return p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return f"错误: 无法以 UTF-8 读取文件（可能是二进制文件）"


@tool(group="file_mgmt", group_description="文件管理")
def write_file(
    file_path: Annotated[str, "文件路径"],
    content: Annotated[str, "要写入的内容"],
) -> str:
    """将内容写入指定文件（会覆盖已有内容）。"""
    p = Path(file_path).expanduser()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return f"已写入文件: {p} ({len(content)} 字符)"


@tool(group="file_mgmt", group_description="文件管理")
def list_directory(
    directory: Annotated[str, "目录路径"] = ".",
    show_hidden: Annotated[bool, "是否显示隐藏文件"] = False,
) -> str:
    """列出目录下的所有文件和子目录。"""
    p = Path(directory).expanduser()
    if not p.exists():
        return f"错误: 目录不存在 - {p}"
    if not p.is_dir():
        return f"错误: 路径不是目录 - {p}"

    items = []
    for item in sorted(p.iterdir()):
        if not show_hidden and item.name.startswith("."):
            continue
        prefix = "📁 " if item.is_dir() else "📄 "
        size = ""
        if item.is_file():
            s = item.stat().st_size
            size = f" ({_format_size(s)})"
        items.append(f"{prefix}{item.name}{size}")

    if not items:
        return f"目录为空: {p}"
    return f"目录: {p}\n\n" + "\n".join(items)


@tool(group="file_mgmt", group_description="文件管理")
def search_files(
    directory: Annotated[str, "搜索根目录"],
    pattern: Annotated[str, "glob 模式，如 *.py, **/*.md"],
) -> str:
    """递归搜索匹配模式的文件。"""
    p = Path(directory).expanduser()
    if not p.exists():
        return f"错误: 目录不存在 - {p}"

    matches = list(p.glob(pattern))
    if not matches:
        return f"未找到匹配 '{pattern}' 的文件"

    results = [str(m.relative_to(p)) for m in matches[:50]]
    total = len(matches)
    output = "\n".join(results)
    if total > 50:
        output += f"\n\n... 共 {total} 个匹配，仅显示前 50 个"
    return output


def _format_size(size: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f}{unit}" if unit != "B" else f"{size}{unit}"
        size /= 1024
    return f"{size:.1f}TB"
