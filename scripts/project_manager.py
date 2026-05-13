#!/usr/bin/env python3
"""
mck-html-design 项目管理脚本
管理 HTML 演示文稿项目的生命周期：初始化、导入源文件、查看状态、清理输出。
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime
from enum import Enum


class CanvasFormat(Enum):
    PPT169     = ("ppt169",    1333, 750,  "16:9 PPT 演示文稿")
    STORY      = ("story",     1080, 1920, "9:16 短视频/Story")
    XHS        = ("xhs",       1242, 1660, "3:4 小红书图文")
    WECHAT     = ("wechat",    1080, 1080, "1:1 朋友圈/方图")
    WECHAT_HDR = ("wechat_hdr", 900, 383,  "2.35:1 公众号头图")

    @property
    def key(self):
        return self.value[0]

    @property
    def width(self):
        return self.value[1]

    @property
    def height(self):
        return self.value[2]

    @property
    def description(self):
        return self.value[3]

    @classmethod
    def from_key(cls, key):
        for member in cls:
            if member.key == key:
                return member
        raise ValueError(
            f"未知格式 '{key}'，可用格式: {', '.join(m.key for m in cls)}"
        )


# 项目根目录：scripts/ 的 ../../projects/（即 skill 根目录下的 projects/）
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPTS_DIR)
PROJECTS_ROOT = os.path.join(SKILL_ROOT, "projects")


def get_project_dir(name):
    return os.path.join(PROJECTS_ROOT, name)


def load_project_json(project_dir):
    path = os.path.join(project_dir, "project.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_project_json(project_dir, data):
    path = os.path.join(project_dir, "project.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── 子命令实现 ──────────────────────────────────────────────────────────────

def cmd_init(args):
    """初始化一个新项目。"""
    fmt = CanvasFormat.from_key(args.format)
    project_dir = get_project_dir(args.project_name)

    if os.path.exists(project_dir):
        print(f"错误：项目 '{args.project_name}' 已存在（{project_dir}），请换一个名称。")
        sys.exit(1)

    os.makedirs(os.path.join(project_dir, "sources"), exist_ok=True)
    os.makedirs(os.path.join(project_dir, "output"), exist_ok=True)

    project_data = {
        "name": args.project_name,
        "format": fmt.key,
        "canvas": {"width": fmt.width, "height": fmt.height},
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "initialized",
        "spec_lock_path": None,
        "output_path": None,
    }
    save_project_json(project_dir, project_data)

    print(f"项目已创建：{project_dir}")
    print(f"  格式：{fmt.key}（{fmt.description}，{fmt.width}×{fmt.height}）")


def cmd_import_sources(args):
    """将源文件复制（或移动）到项目的 sources/ 目录。"""
    project_dir = get_project_dir(args.project_name)
    if not os.path.isdir(project_dir):
        print(f"错误：项目 '{args.project_name}' 不存在。")
        sys.exit(1)

    sources_dir = os.path.join(project_dir, "sources")
    imported = []
    failed = []

    for src in args.files:
        if not os.path.isfile(src):
            failed.append((src, "文件不存在"))
            continue
        dst = os.path.join(sources_dir, os.path.basename(src))
        try:
            if args.move:
                shutil.move(src, dst)
                action = "移动"
            else:
                shutil.copy2(src, dst)
                action = "复制"
            imported.append((action, src, dst))
        except Exception as e:
            failed.append((src, str(e)))

    for action, src, dst in imported:
        print(f"  [{action}] {src} → {dst}")
    for src, reason in failed:
        print(f"  [失败] {src}：{reason}")

    if failed:
        sys.exit(1)


def cmd_list(args):
    """列出所有项目。"""
    if not os.path.isdir(PROJECTS_ROOT):
        print("（尚无项目）")
        return

    entries = sorted(
        d for d in os.listdir(PROJECTS_ROOT)
        if os.path.isdir(os.path.join(PROJECTS_ROOT, d))
    )
    if not entries:
        print("（尚无项目）")
        return

    header = f"{'项目名':<20} {'格式':<12} {'画布尺寸':<14} {'状态':<14} 创建时间"
    print(header)
    print("-" * len(header))

    for name in entries:
        project_dir = os.path.join(PROJECTS_ROOT, name)
        try:
            data = load_project_json(project_dir)
            canvas = data.get("canvas", {})
            size = f"{canvas.get('width','?')}×{canvas.get('height','?')}"
            print(
                f"{data.get('name','?'):<20} "
                f"{data.get('format','?'):<12} "
                f"{size:<14} "
                f"{data.get('status','?'):<14} "
                f"{data.get('created_at','?')}"
            )
        except Exception as e:
            print(f"{name:<20} （读取 project.json 失败：{e}）")


def cmd_info(args):
    """查看项目详细信息。"""
    project_dir = get_project_dir(args.project_name)
    if not os.path.isdir(project_dir):
        print(f"错误：项目 '{args.project_name}' 不存在。")
        sys.exit(1)

    data = load_project_json(project_dir)
    print("=== project.json ===")
    print(json.dumps(data, ensure_ascii=False, indent=2))

    sources_dir = os.path.join(project_dir, "sources")
    print("\n=== sources/ 文件列表 ===")
    if os.path.isdir(sources_dir):
        files = sorted(os.listdir(sources_dir))
        if files:
            for f in files:
                fpath = os.path.join(sources_dir, f)
                size = os.path.getsize(fpath)
                print(f"  {f}  ({size:,} bytes)")
        else:
            print("  （空）")
    else:
        print("  （sources/ 目录不存在）")


def cmd_clean(args):
    """清理项目的 output/ 目录（不删除源文件）。"""
    project_dir = get_project_dir(args.project_name)
    if not os.path.isdir(project_dir):
        print(f"错误：项目 '{args.project_name}' 不存在。")
        sys.exit(1)

    output_dir = os.path.join(project_dir, "output")
    if not os.path.isdir(output_dir):
        print(f"output/ 目录不存在，无需清理。")
        return

    removed = 0
    for item in os.listdir(output_dir):
        item_path = os.path.join(output_dir, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
            removed += 1
        except Exception as e:
            print(f"  [警告] 删除 {item} 失败：{e}")

    # 重置 project.json 中的 output_path 和 status（若已完成则退回 spec_locked）
    try:
        data = load_project_json(project_dir)
        data["output_path"] = None
        if data.get("status") in ("generating", "done"):
            data["status"] = "spec_locked" if data.get("spec_lock_path") else "initialized"
        save_project_json(project_dir, data)
    except Exception as e:
        print(f"  [警告] 更新 project.json 失败：{e}")

    print(f"已清理 output/，共删除 {removed} 个条目。")


# ── 参数解析 ────────────────────────────────────────────────────────────────

def build_parser():
    parser = argparse.ArgumentParser(
        prog="project_manager.py",
        description="mck-html-design 项目管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "可用画布格式：\n"
            + "\n".join(
                f"  {m.key:<14} {m.description}（{m.width}×{m.height}）"
                for m in CanvasFormat
            )
        ),
    )
    sub = parser.add_subparsers(dest="command", metavar="<命令>")
    sub.required = True

    # init
    p_init = sub.add_parser("init", help="初始化新项目")
    p_init.add_argument("project_name", metavar="项目名称", help="项目目录名称（英文，无空格）")
    p_init.add_argument(
        "--format",
        default="ppt169",
        metavar="格式",
        help=f"画布格式（默认：ppt169），可选：{', '.join(m.key for m in CanvasFormat)}",
    )
    p_init.set_defaults(func=cmd_init)

    # import-sources
    p_import = sub.add_parser("import-sources", help="导入源文件到项目")
    p_import.add_argument("project_name", metavar="项目名称")
    p_import.add_argument("files", metavar="文件路径", nargs="+", help="要导入的文件（支持多个）")
    p_import.add_argument("--move", action="store_true", help="移动文件而非复制（默认复制）")
    p_import.set_defaults(func=cmd_import_sources)

    # list
    p_list = sub.add_parser("list", help="列出所有项目")
    p_list.set_defaults(func=cmd_list)

    # info
    p_info = sub.add_parser("info", help="查看项目详细信息")
    p_info.add_argument("project_name", metavar="项目名称")
    p_info.set_defaults(func=cmd_info)

    # clean
    p_clean = sub.add_parser("clean", help="清理项目输出（保留源文件）")
    p_clean.add_argument("project_name", metavar="项目名称")
    p_clean.set_defaults(func=cmd_clean)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
