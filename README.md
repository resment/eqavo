# Eqavo

<p align="center">
  <img src="./assets/brand/eqavo-logo.svg" alt="Eqavo logo" width="720" />
</p>

<p align="center">
  <img src="./assets/brand/eqavo-icon.svg" alt="Eqavo icon" width="128" />
</p>

<p align="center">
  中文 | <a href="./README_EN.md">English</a>
</p>

<p align="center">
  <a href="https://github.com/resment/eqavo/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/resment/eqavo?style=flat-square" /></a>
  <a href="https://github.com/resment/eqavo/network/members"><img alt="GitHub forks" src="https://img.shields.io/github/forks/resment/eqavo?style=flat-square" /></a>
  <a href="https://github.com/resment/eqavo/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/resment/eqavo?style=flat-square" /></a>
  <a href="https://github.com/resment/eqavo/commits/main"><img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/resment/eqavo?style=flat-square" /></a>
</p>

> 一个非官方、面向 macOS、中文优先、基于 Zed 源码构建的独立发行项目。

## 产品介绍

`Eqavo` 的目标很直接：

- 让 macOS 用户获得一个更完整的中文化编辑器体验
- 尽量降低终端用户使用门槛
- 尽量裁掉不必要的官方 Service 依赖，走本地优先路线

理想中的用户流程是：

1. 打开 GitHub Releases
2. 下载适合自己机器的 macOS 安装包
3. 拖到 `Applications`
4. 打开即用

## 当前定位

- 产品名：`Eqavo`
- 性质：非官方社区项目
- 平台：macOS 优先
- 语言：中文优先，英文补充
- 收费：免费
- 仓库：独立维护

## Star History

<a href="https://www.star-history.com/?repos=resment%2Feqavo&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=resment/eqavo&type=date&theme=dark&legend=bottom-right" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=resment/eqavo&type=date&legend=bottom-right" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=resment/eqavo&type=date&legend=bottom-right" />
 </picture>
</a>
详细任务见：

- [PROJECT_STATUS.md](./PROJECT_STATUS.md)

## 这个项目解决什么问题

现有社区方案对 macOS 不够友好，主要问题是：

- 以 Linux 构建流程为中心
- 对新版 Zed 源码结构适配不足
- 用户操作步骤太多
- 品牌和分发方式不够独立

Eqavo 选择的路线是：

1. 同步上游 Zed 源码
2. 应用结构化中文翻译
3. 裁剪不需要的官方 Service 相关入口
4. 构建 macOS 可分发产物
5. 发布独立品牌的安装包

## 仓库结构

```text
eqavo/
  README.md
  README_EN.md
  PROJECT_STATUS.md
  assets/
    brand/
  scripts/
    bootstrap.sh
    sync_zed.py
    apply_translations.py
    disable_services.py
    apply_branding.py
    generate_icons.py
    package_macos.sh
  src/
  translations/
```

## 合规说明

- `Eqavo` 是独立社区品牌
- 本项目不隶属于 Zed Industries，也不代表官方立场
- 发布与维护应遵守上游开源许可和相关品牌规则

## 路线图

近期优先级：

1. 做出可自动构建的 `.app` / `.dmg`
2. 落地 GitHub Actions 发布流程
3. 扩展新版 Zed 的中文覆盖
4. 进一步屏蔽登录、协作、遥测、自动更新等官方 Service 入口

## English

For the English version of this README, see:

- [README_EN.md](./README_EN.md)
