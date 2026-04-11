# コードフォーマット

Hemlockには一貫したスタイルを強制するための組み込みコードフォーマッタが含まれています。

## 使い方

```bash
hemlock format <FILE>         # ファイルをインプレースでフォーマット
hemlock format --check <FILE> # フォーマット済みかチェック（未フォーマットの場合exit 1）
```

## スタイルルール

フォーマッタは以下の規約を強制します：

| ルール | 値 |
|------|-------|
| インデント | タブ |
| ブレーススタイル | K&R（開きブレースは同じ行） |
| 最大行幅 | 100文字 |
| 末尾カンマ | はい、複数行コンテキストで |
| 最大連続空行 | 1 |

## 自動改行

フォーマッタは長い行を自動的に改行します：

- **関数パラメータ** - 長いパラメータリストはパラメータごとに改行
- **二項式** - 長い論理/比較チェーンは演算子で改行
- **import文** - 長いインポートリストは各項目を独自の行に改行
- **メソッドチェーン** - 長いチェーンはドットの前で改行

## 例

フォーマット前：
```hemlock
fn create_user(name: string, email: string, age: i32, active: bool, role: string) { return { name: name, email: email, age: age, active: active, role: role }; }
```

フォーマット後：
```hemlock
fn create_user(
	name: string,
	email: string,
	age: i32,
	active: bool,
	role: string,
) {
	return {
		name: name,
		email: email,
		age: age,
		active: active,
		role: role,
	};
}
```

## CI統合

CIパイプラインで`--check`を使用してフォーマットを強制：

```bash
hemlock format --check src/main.hml || echo "File not formatted"
```
