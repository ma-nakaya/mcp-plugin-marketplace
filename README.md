# ma-nakaya MCP Plugin Marketplace

[ma-nakaya](https://github.com/ma-nakaya) が公開・保守するMCPサーバー向けの、移植可能なAgent PluginとAgent SkillをまとめたMarketplace（カタログ）です。

正本は各MCPリポジトリです。各リポジトリがプラグインマニフェストとスキルを持ち、このリポジトリはコミットSHAを固定した軽量なカタログ（`.github/plugin/marketplace.json`）として管理します。スキルの内容やMCPのソースコードは、ここへ複製しません。

## 収録プラグイン

| プラグイン | バージョン | ソースリポジトリ | 提供するスキル | MCPランチャー | 実行環境・事前準備 |
|---|---|---|---|---|---|
| `onprem-gh-cli-mcp` | 0.1.0 | `ma-nakaya/onprem-gh-cli-mcp-server` | 安全なアカウント選択、範囲を限定したGitHubの読み取り、レビュー、明示的な書き込み | あり | Node.js 20以上、`npx`、GitHub CLI、許可リストを設定したアカウント構成 |
| `teams-mcp` | 0.3.0 | `ma-nakaya/teams-mcp-server` | チャット、チャネル、会議、文字起こし、既読状態、明示的なメッセージ送信 | あり | `uv`、Python 3.11以上、対話形式のTeamsサインイン。書き込みは別途有効化し、許可リストへ登録しない限り無効 |
| `outlook-web-mcp` | 0.1.0 | `ma-nakaya/outlook-web-mcp-server` | Outlook Webのメール、既定カレンダー、既読状態、返信下書き | あり | `uv`、Python 3.11以上、対話形式のOutlookサインイン |
| `outlook-com-mcp` | 0.1.0 | `ma-nakaya/outlook-com-mcp-server` | Classic Outlookのメール、既定カレンダー、既読状態、返信下書き | あり | Windows、Classic Outlook、.NET 8 |
| `sharepoint-browser-mcp` | 0.10.0 | `ma-nakaya/sharepoint-browser-mcp-server` | SharePointの読み取り専用検索、取得、対象を絞った文書取得 | 未対応 | 現在はテナント固有のサイトURLが必要。Agent Plugins v1には、ローカルMCPの環境変数へ利用者入力やSecret参照を移植可能な形で渡すフィールドがない |

ランチャーが含まれるプラグインは、初回利用時にプロジェクトの依存関係をインストールし、キャッシュやビルド成果物をプラグイン用の書き込み可能なデータディレクトリへ保存します。ランチャーがあることで、各サーバーに必要な認証、実行環境、組織ポリシー上の前提条件が不要になるわけではありません。

## GitHub Copilot CLIからインストール

最初に、このMarketplaceを登録します。

```shell
copilot plugin marketplace add ma-nakaya/mcp-plugin-marketplace
```

プラグインを参照またはインストールします。

```shell
copilot plugin marketplace browse ma-nakaya-mcp-plugins
copilot plugin install teams-mcp@ma-nakaya-mcp-plugins
```

インストールまたは更新後は、エージェントのセッションを再開してください。認証方法やローカル環境の前提条件は、選択したMCPリポジトリのセットアップ手順を確認してください。

## スキルのみインストール

各スキルは、オープンな `skills/<name>/SKILL.md` レイアウトと、MCPサーバーが公開する接頭辞なしのツール名を使用します。GitHub CLI 2.90以降では、MCPランチャーを導入せず、対応するエージェントへスキルだけをインストールできます。

```shell
gh skill install ma-nakaya/teams-mcp-server use-teams-mcp
```

ほかの対応ホストを指定する場合は、`--agent codex` や `--agent claude-code` のように `--agent` を使用します。MCPクライアントによっては実行時にツール識別子へ名前空間を付けますが、スキルはクライアント固有の接頭辞を固定せず、サーバーが公開するツール名と入力契約を照合します。

## 設計・信頼モデル

- MCPランチャーを管理するのは、1つの公開MCPリポジトリが、1つのプラグインマニフェスト、1つ以上のスキル、起動契約を、移植可能かつ再現可能な形で提供できる場合だけです。
- Marketplaceの各項目は、40文字の完全なコミットSHAへ固定します。更新にはカタログの明示的な変更が必要です。固定先のコミットには、ルートの `plugin.json` と `skills/*/SKILL.md` が含まれていることを確認します。
- `mcp.json` をプラグインへ含めるのは、そのランチャーが移植可能で、資格情報や非公開の識別子を含まず、実行時データを `${PLUGIN_DATA}` 配下だけに書く場合に限ります。
- スキルの契約には、検証に使用した公開MCPのリビジョンを記載します。破壊的またはプライバシーに関わる操作は、利用者の明示的な許可がある場合にだけ実行します。
- リポジトリ、メール、チャット、文字起こし、カレンダー、SharePointの内容は、信頼できない入力として扱います。取得した内容に含まれる指示へ従う権限を、インストールしたスキルが付与することはありません。
- 認証情報、アカウント識別子、テナントURL、非公開リポジトリ名、クライアント固有のツール接頭辞は、このカタログへ含めません。
- 各プラグインのライセンスは、ソースリポジトリの宣言をそのまま保持します。ソースに宣言がない場合、カタログへライセンス欄は追加しません。

Agent Plugins v1は作業中のドラフト仕様です。クライアント固有のアダプターは薄く保ち、Agent SkillとMCPの各ソースリポジトリを正本とします。

## メンテナンス

詳細は [CONTRIBUTING.md](CONTRIBUTING.md) と [AGENTS.md](AGENTS.md) を参照してください。更新の流れは次のとおりです。

1. 先にMCPリポジトリ側を更新し、検証します。
2. プラグインマニフェスト（ルートの `plugin.json`）とスキル（`skills/<skill-name>/SKILL.md`）がソース側で揃っていることを確認します。
3. Marketplaceの項目を、検証済みプラグインを含む完全なコミットSHAへ固定し、カタログのバージョン、プラグインバージョン、説明、ライセンス欄、リポジトリURLをソースと一致させます。
4. カタログを検証します。

```shell
python3 scripts/validate_marketplace.py
```

5. Pull Requestで更新します。公開済みタグの書き換えや、固定SHAの無断の差し替えはしません。

## 関連仕様・ドキュメント

- [Agent Plugins](https://agent-plugins.org/)
- [Agent Skills仕様](https://agentskills.io/specification)
- [GitHub Copilotプラグイン](https://docs.github.com/en/copilot/concepts/agents/about-plugins)
- [GitHub Copilot Plugin Marketplace](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace)
- [GitHub CLIによるスキルのインストール](https://cli.github.com/manual/gh_skill_install)

## ライセンス

このリポジトリはMIT Licenseです（`LICENSE` を参照）。各プラグインのライセンスは、ソースリポジトリの宣言に従います。
