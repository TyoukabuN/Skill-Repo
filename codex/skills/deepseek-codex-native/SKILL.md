---
name: deepseek-codex-native
description: 帮助 Codex 用户把 DeepSeek 通过官方 Responses API 原生接入 Codex，并生成 switch-to-ds.ps1 与 switch-to-gpt.ps1 两个模型切换脚本。Use when the user asks to configure DeepSeek/DS for Codex, switch Codex between GPT and DeepSeek, repair DeepSeek Codex config, or package a repeatable DeepSeek Codex setup workflow.
---

# DeepSeek Codex 原生接入

## 目标

把 DeepSeek 作为 Codex 的原生模型提供方接入，而不是通过 DeepSeek Code Worker MCP。这个模式会切换 Codex 主线程模型；它不等价于“GPT 规划、DeepSeek 执行”的双模型协同。需要 GPT 主线程 + DeepSeek 执行时，继续使用 `deepseek-code-worker` MCP。

核心交付物：

- 配置用户级 Codex 配置目录中的 DeepSeek provider。
- 保留或生成可回滚的 GPT 配置快照。
- 必须生成 `switch-to-ds.ps1` 和 `switch-to-gpt.ps1`，方便用户日常切换模型。

## 安全规则

不要在回复、日志、命令输出、补丁或仓库文件中暴露 DeepSeek API Key。DeepSeek 官方 Codex 接入示例可能会把 key 写入用户级 `config.toml`；在这么做之前，明确告知用户这是本机用户配置，不应提交到 Git。

所有配置默认写到用户级 Codex 目录：

- 如果 `$env:CODEX_HOME` 存在，使用它。
- 否则 Windows 使用 `%USERPROFILE%\.codex`，类 Unix 使用 `~/.codex`。

除非用户明确要求，不要启动、重启或杀掉 Codex；只修改静态配置并告诉用户新开 Codex 进程后生效。

## 接入流程

1. 先查看 DeepSeek 官方文档的当前版本：
   - `https://api-docs.deepseek.com/zh-cn/quick_start/agent_integrations/codex/`
   - `https://api-docs.deepseek.com/zh-cn/guides/responses_api/`
2. 根据官方文档确认当前可用于 Codex Responses API 的模型名。不要假设 `deepseek-v4-flash` 或 `deepseek-v4-pro` 的支持状态永远不变。
3. 读取现有 Codex 配置时必须脱敏：只判断是否存在 `model`、`model_provider`、`model_catalog_json`、`[model_providers.deepseek]`、`experimental_bearer_token` 等字段，不打印 token 值。
4. 优先让用户在自己的终端交互式运行 DeepSeek 官方安装脚本并输入 API Key。若需要由 Codex 修改配置，先创建时间戳备份，并保留现有 MCP、profile、approval、sandbox 等无关配置段。
5. 完成 DeepSeek 配置后，创建模型 profile 与两个切换脚本。

## 必须生成的文件

在用户级 Codex 目录下生成：

- `switch-to-ds.ps1`
- `switch-to-gpt.ps1`

同时创建：

- `model-profiles/config.deepseek.toml`
- `model-profiles/config.gpt.toml`
- 如 DeepSeek 配置引用模型目录，也保存 `model-profiles/models.deepseek.json`

脚本必须满足：

- 使用脚本自身目录作为 Codex 目录，或显式解析 `$env:CODEX_HOME`；不要硬编码某个用户名。
- 执行前检查必需文件是否存在，缺失时抛出清晰错误。
- 如果当前已经是目标 provider，直接提示并退出，不重复覆盖。
- 切换前把当前 `config.toml` 保存回对应 profile，保留用户后续手动调整。
- `switch-to-ds.ps1` 先恢复 DeepSeek 的 `models.json`，再恢复 DeepSeek `config.toml`。
- `switch-to-gpt.ps1` 恢复 GPT `config.toml`；不要把 DeepSeek API Key 打印出来。
- 只切换配置文件，不自动启动 Codex。

推荐脚本骨架逻辑：

```powershell
$codexRoot = if ($env:CODEX_HOME) {
    $env:CODEX_HOME
} else {
    Split-Path -Parent $PSCommandPath
}

$activeConfig = Join-Path $codexRoot 'config.toml'
$profileDir = Join-Path $codexRoot 'model-profiles'
$gptProfile = Join-Path $profileDir 'config.gpt.toml'
$dsProfile = Join-Path $profileDir 'config.deepseek.toml'
```

在实际生成脚本时，把上面的骨架扩展为完整脚本，并按本机文件布局验证。

## 验证

配置完成后做静态验证：

- `config.toml` 的 `model_provider` 指向 DeepSeek 时，`wire_api` 应为官方文档要求的 Responses API 配置。
- `experimental_bearer_token` 只能检查“非空/存在”，不能输出值。
- `model_catalog_json` 指向的 JSON 文件存在且 JSON 语法有效。
- GPT 与 DeepSeek profile 都存在。
- 两个 `switch-to-*.ps1` 通过 PowerShell 语法检查。

如果用户允许产生 API 调用成本，再做一次最小 smoke test；否则只报告静态验证结果和“需要重启或新开 Codex 进程生效”。

## 日常使用说明

告诉用户：

- 切到 DeepSeek：运行 `switch-to-ds.ps1`，然后重启 Codex 或新开一个 Codex 进程。
- 切回 GPT：运行 `switch-to-gpt.ps1`，然后重启 Codex 或新开一个 Codex 进程。
- DeepSeek 官方安装脚本中的“恢复默认/删除备份”选项用于卸载或重置，不适合作为日常切换方式。
