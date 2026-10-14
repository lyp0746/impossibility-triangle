# -*- coding: utf-8 -*-
"""set_repo_meta.py — 设置 GitHub 仓库的双语描述、主页与 topics。

Token 从 git credential helper 读取，不落盘、不打印。
用法：python scripts/set_repo_meta.py
"""
import os
import subprocess

import requests

REPO = "lyp0746/impossibility-triangle"
GIT = os.environ.get("GIT_BIN", r"D:\Git\cmd\git.exe")

DESCRIPTION = (
    "《选择的代价》——完备、可组合与可传递的三维权衡：任何有限复杂度的知识系统都不能同时满格拥有 C、A、T，至多两个；"
    "选择哪两个，就在第三个上留下一处可定位的缺口。附四个战场的现实诊断、优雅降级与可证伪登记簿。 "
    "The Price of Choice — the impossibility triangle of Completeness, Composability, and Transfer: "
    "how complex knowledge systems form, evolve, and renew. Text CC BY 4.0; code MIT."
)
HOMEPAGE = "https://github.com/lyp0746/impossibility-triangle"
TOPICS = [
    "impossibility-triangle", "complex-systems", "knowledge-evolution",
    "completeness", "composability", "transferability", "submodularity",
    "systems-science", "epistemology", "institutional-design",
    "cc-by-4-0",
]


def get_token():
    out = subprocess.run([GIT, "credential", "fill"],
                         input="protocol=https\nhost=github.com\n\n",
                         capture_output=True, text=True,
                         env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
    for line in out.stdout.splitlines():
        if line.startswith("password="):
            return line[len("password="):].strip()
    raise SystemExit("未能从 git credential helper 取得 token")


def main():
    tok = get_token()
    h = {"Authorization": f"token {tok}", "Accept": "application/vnd.github+json",
         "User-Agent": "book-meta"}
    r = requests.patch(f"https://api.github.com/repos/{REPO}", headers=h,
                       json={"description": DESCRIPTION, "homepage": HOMEPAGE,
                             "has_issues": True, "has_wiki": False}, timeout=60)
    print("repo PATCH:", r.status_code)
    if r.status_code >= 300:
        print(r.text[:400])
    t = requests.put(f"https://api.github.com/repos/{REPO}/topics", headers=h,
                     json={"names": TOPICS}, timeout=60)
    print("topics PUT:", t.status_code)
    if t.status_code >= 300:
        print(t.text[:400])
    else:
        print("topics:", ", ".join(t.json().get("names", [])))


if __name__ == "__main__":
    main()
