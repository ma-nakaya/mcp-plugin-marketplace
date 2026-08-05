# ma-nakaya MCP Plugin Marketplace

[ma-nakaya](https://github.com/ma-nakaya)が公開・保守するMCPサーバー向けの、移植可能なAgent PluginとAgent SkillをまとめたMarketplaceです。

各MCPリポジトリをプラグインとスキルの正本とし、このリポジトリはコミットSHAを固定した軽量なカタログとして管理します。スキルの内容やMCPのソースコードは複製しません。

## 利用可能なプラグイン

| プラグイン | 提供するスキル | MCPランチャー | 実行環境・事前準備 |
|---|---|---|---|
| `onprem-gh-cli-mcp` | 安全なアカウント選択、範囲を限定したGitHubの読み取り、レビュー、明示的な書き込み | あり | Node.js 20以上、`npx`、GitHub CLI、許可リストを設定したアカウント構成 |
| `teams-mcp` | チャット、チャネル、会議、文字起こし、既読状態、明示的なメッセージ送信 | あり | `uv`、Python 3.11以上、対話形式のTeamsサインイン。書き込みは別途有効化し、許可リストへ登録しない限り無効 |
| `outlook-web-mcp` | Outlook Webのメール、既定カレンダー、既読状態、返信下書き | あり | `uv`、Python 3.11以上、対話形式のOutlookサインイン |
| `outlook-com-mcp` | Classic Outlookのメール、既定カレンダー、既読状態、返信下書き | あり | Windows、Classic Outlook、.NET 8 |
| `sharepoint-browser-mcp` | SharePointの読み取り専用検索、取得、対象を絞った文書取得 | 未対応 | 現在はテナント固有のサイトURLが必要。Agent Plugins v1には、ローカルMCPの環境変数へ利用者入力やSecret参照を移植可能な形で渡すフィールドがない |

ランチャーが含まれるプラグインは、初回利用時にプロジェクトの依存関係をインストールし、キャッシュやビルド成果物をプラグイン用の書き込み可能なデータディレクトリへ保存します。各サーバーに必要な認証、実行環境、組織ポリシー上の前提条件が不要になるわけではありません。

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

プラグインのインストールまたは更新後は、エージェントのセッションを再開してください。認証方法やローカル環境の前提条件は、選択したMCPリポジトリのセットアップ手順を確認してください。

## スキルのみインストール

各スキルは、オープンな`skills/<name>/SKILL.md`レイアウトと、MCPサーバーが公開する接頭辞なしのツール名を使用します。GitHub CLI 2.90以降では、MCPランチャーを導入せず、対応するエージェントへスキルだけをインストールできます。

```shell
gh skill install ma-nakaya/teams-mcp-server use-teams-mcp
```

ほかの対応ホストを指定する場合は、`--agent codex`や`--agent claude-code`のように`--agent`を使用します。MCPクライアントによっては実行時にツール識別子へ名前空間を付けますが、スキルはクライアント固有の接頭辞を固定せず、サーバーが公開するツール名と入力契約を照合します。

## 設計・信頼モデル

- 1つの公開MCPリポジトリが、1つのプラグインマニフェスト、1つ以上のスキル、起動契約を移植可能かつ再現可能にできる場合のみMCPランチャーを管理します。
- Marketplaceの各項目は、40文字の完全なコミットSHAへ固定します。更新時はカタログの明示的な変更が必要です。
- スキルの契約には検証に使用した公開MCPのリビジョンを記載し、破壊的またはプライバシーに関わる操作は、利用者の明示的な許可がある場合にだけ実行します。
- リポジトリ、メール、チャット、文字起こし、カレンダー、SharePointの内容は信頼できない入力として扱います。取得した内容に含まれる指示へ従う権限を、インストールしたスキルが付与することはありません。
- 認証情報、アカウント識別子、テナントURL、非公開リポジトリ名、クライアント固有のツール接頭辞は、このカタログへ含めません。

Agent Plugins v1は作業中のドラフト仕様です。クライアント固有のアダプターは薄く保ち、Agent SkillとMCPの各ソースリポジトリを正本とします。

## メンテナンス

詳細は[CONTRIBUTING.md](CONTRIBUTING.md)を参照してください。Pull Requestを作成する前に、カタログの変更を検証します。

```shell
python3 scripts/validate_marketplace.py
```

関連する仕様とクライアントのドキュメント:

- [Agent Plugins](https://agent-plugins.org/)
- [Agent Skills仕様](https://agentskills.io/specification)
- [GitHub Copilotプラグイン](https://docs.github.com/en/copilot/concepts/agents/about-plugins)
- [GitHub Copilot Plugin Marketplace](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace)
- [GitHub CLIによるスキルのインストール](https://cli.github.com/manual/gh_skill_install)
