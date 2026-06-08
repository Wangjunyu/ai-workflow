#!/usr/bin/env python3
"""
Hermes Fleet — Profile Renderer

读取 host 定义 + layers + profiles，渲染目标机器的 profile 配置树。

用法:
  python deploy/render.py <host-name> [--staging-dir /tmp/hermes-staging]

输出:
  在 staging 目录生成每台机器需要的 profile 目录结构。

不负责:
  - .env 真实密钥（由 bitwarden / 手动注入）
  - 运行态文件（sessions/logs/auth）
  - 远程部署（由 sync.sh 负责）
"""

import os
import sys
import shutil
import yaml
from pathlib import Path
from copy import deepcopy


FLEET_ROOT = Path(__file__).resolve().parent.parent


def deep_merge(base: dict, override: dict) -> dict:
    """递归合并两个字典，override 优先。"""
    result = deepcopy(base)
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = deep_merge(result[k], v)
        elif isinstance(result.get(k), list) and isinstance(v, list):
            result[k] = list(dict.fromkeys(result[k] + v))  # 去重合并
        else:
            result[k] = deepcopy(v)
    return result


def load_yaml(path: Path) -> dict:
    """加载 YAML，文件不存在返回空 dict。"""
    if not path.exists():
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}


def render_config(profile_name: str, layers: list[str]) -> dict:
    """按 layer 顺序合并配置。"""
    merged = {}
    for layer_name in layers:
        layer_path = FLEET_ROOT / "layers" / f"{layer_name}.yaml"
        merged = deep_merge(merged, load_yaml(layer_path))

    profile_config_path = FLEET_ROOT / "profiles" / profile_name / "config.yaml"
    merged = deep_merge(merged, load_yaml(profile_config_path))

    return merged


def render_host(host_name: str, staging_dir: Path):
    """渲染一台机器的所有 profile 配置。"""
    host_path = FLEET_ROOT / "hosts" / f"{host_name}.yaml"
    if not host_path.exists():
        print(f"ERROR: host '{host_name}' not found at {host_path}")
        sys.exit(1)

    host = load_yaml(host_path)
    profiles = host.get("profiles", [])
    layers = host.get("layers", [])

    print(f"Rendering host: {host_name}")
    print(f"  Profiles: {profiles}")
    print(f"  Layers:   {layers}")
    print()

    for profile_name in profiles:
        profile_dir = staging_dir / "profiles" / profile_name

        # 渲染 config
        merged_config = render_config(profile_name, layers)
        config_out = profile_dir / "config.yaml"
        config_out.parent.mkdir(parents=True, exist_ok=True)
        with open(config_out, "w") as f:
            yaml.dump(merged_config, f, default_flow_style=False, allow_unicode=True)
        print(f"  → {config_out}")

        # 复制 personality（优先 profile 级，否则 fallback）
        personality_src = FLEET_ROOT / "profiles" / profile_name / "personality.md"
        if personality_src.exists():
            shutil.copy2(personality_src, profile_dir / "personality.md")
            print(f"  → {profile_dir / 'personality.md'}")

        # 复制 shared scripts
        scripts_src = FLEET_ROOT / "shared" / "scripts"
        if scripts_src.exists():
            scripts_dst = staging_dir / "shared" / "scripts"
            scripts_dst.parent.mkdir(parents=True, exist_ok=True)
            if not scripts_dst.exists():
                shutil.copytree(scripts_src, scripts_dst)
                print(f"  → {scripts_dst}")

        # 复制 shared skills
        skills_src = FLEET_ROOT / "shared" / "skills"
        if skills_src.exists() and any(skills_src.iterdir()):
            skills_dst = profile_dir / "skills"
            skills_dst.mkdir(parents=True, exist_ok=True)
            for item in skills_src.iterdir():
                if item.is_file():
                    shutil.copy2(item, skills_dst / item.name)
            print(f"  → {skills_dst}")

    print()
    print(f"Done. Staging: {staging_dir}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python deploy/render.py <host-name> [--staging-dir <path>]")
        sys.exit(1)

    host_name = sys.argv[1]
    staging_dir = Path(sys.argv[3]) if "--staging-dir" in sys.argv else Path(f"/tmp/hermes-staging-{host_name}")
    render_host(host_name, staging_dir)
