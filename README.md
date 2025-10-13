# 哪吒探针多合一部署容器  Probe All-in-One 🐋

[![Docker Build](https://github.com/Sparklewink/Agent-Docker/actions/workflows/docker-build.yml/badge.svg)](https://github.com/Sparklewink/Agent-Docker/actions/workflows/docker-build.yml)

这是一个基于 Docker 的哪吒探针持久化部署方案，部署于各类免费或付费的容器托管平台（如 Koyeb, Claw Cloud, Render, Zeabur 等）。

本方案内置了 **Flask 伪装页面** 🎭 和**多探针支持** 🚀，可以在一个免费服务中高效、稳定地运行多个探针。

## ✨ 特性

- **📦 容器化部署**: 基于 `Dockerfile`。
- **🌐 多探针支持**: 在一个服务实例中，通过环境变量即可同时运行多个探针。
- **🎭 网页伪装**: 内置一个基于 Flask 的精美伪装页面，有效应对部分平台的闲置策略和审查。
- **🤖 自动构建**: 集成 GitHub Actions，每次更新代码后会自动构建最新的 Docker 镜像并推送到 GitHub Packages (GHCR)。
- **🌍 平台通用**: 适用于任何支持从公开 Docker 镜像部署的平台。

## 🔧 环境变量

需要在部署平台的 “Environment Variables” 或 “Secrets” 设置中添加以下变量来配置探针。

#### 探针 #1 (必需)

| 变量名             | 示例值                           | 描述 📝                                      |
| ------------------ | -------------------------------- | -------------------------------------------- |
| `NZ_SERVER`        | `agent.lty.qzz.io:8080`        | 哪吒面板服务器地址和端口。                      |
| `NZ_CLIENT_SECRET` | `CN19491001`                   | 哪吒面板探针密钥。                              |
| `NZ_TLS`           | `false`                        | 是否启用 TLS/SSL ( `true` 或 `false` )。       |

#### 探针 #2 (可选)

如果想在同一个服务中运行第二个探针，请添加以下变量：

| 变量名               | 描述 📝                                      |
| -------------------- | -------------------------------------------- |
| `NZ_SERVER_2`        | 第二个探针的服务器地址和端口。                |
| `NZ_CLIENT_SECRET_2` | 第二个探针的密钥。                           |
| `NZ_TLS_2`           | 第二个探针是否启用 TLS。                     |

> **💡 提示**: 可以按照 `_3`, `_4` 的规律，继续添加更多探针的变量（需稍微修改 `app.py` 脚本以支持）。

## 🚀 部署教程

#### 镜像地址

本仓库已通过 GitHub Actions 自动构建并发布了公开的 Docker 镜像，地址如下：
```bash
ghcr.io/sparklewink/agent-docker:latest
```

#### 部署步骤

1.  **登录容器平台** (如 Claw Cloud)。
2.  创建一个新应用，选择**从公开镜像 (Public Image) 部署**。
3.  在镜像地址输入框中，完整粘贴上面的镜像地址 `ghcr.io/sparklewink/agent-docker:latest`。
4.  根据上面的表格，在平台的环境变量设置中，添加探针密钥 (`NZ_SERVER`, `NZ_CLIENT_SECRET` 等)。
5.  选择免费套餐并点击 **“部署”**。

## ⚠️ 注意事项

- **镜像可见性**: 本仓库的 Docker 镜像 (`ghcr.io/sparklewink/agent-docker:latest`) 必须在 GitHub Packages 中设置为 **"Public" (公开)**，外部平台才能成功拉取。
- **自动更新**: 每当 `main` 分支有新的代码提交时，GitHub Actions 都会自动构建一个 `:latest` 标签的新镜像。如果想应用更新，只需在云平台上触发一次“重新部署(Redeploy)”即可。





