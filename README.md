# Travel-Planner

基于 `travel-agent-next` 精简迁移的新项目，保留后端核心能力，移除非必要文件。

> 注：本项目当前以“后端核心能力可运行”为第一目标，前端与测试目录已按精简策略移除。

## 目录结构

- `backend/`: FastAPI 后端服务（保留运行所需核心代码）

## 迁移说明

- 已保留：`backend/app` 核心业务代码、`pyproject.toml`、运行文档。
- 已移除：`tests/`、`frontend/` 占位内容、`docs/`、缓存与本地环境文件。
