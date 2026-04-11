# 代码格式化

Hemlock 包含内置代码格式化工具，用于强制执行一致的代码风格。

## 使用方法

```bash
hemlock format <FILE>         # 就地格式化文件
hemlock format --check <FILE> # 检查文件是否已格式化（未格式化时退出码为 1）
```

## 风格规则

格式化工具强制执行以下约定：

| 规则 | 值 |
|------|------|
| 缩进 | Tab |
| 花括号风格 | K&R（左花括号在同一行） |
| 最大行宽 | 100 个字符 |
| 尾随逗号 | 是，在多行上下文中 |
| 最大连续空行数 | 1 |

## 自动换行

格式化工具会自动拆分过长的行：

- **函数参数** - 过长的参数列表拆分为每行一个参数
- **二元表达式** - 过长的逻辑/比较链在运算符处断行
- **导入语句** - 过长的导入列表拆分为每项一行
- **方法链** - 过长的链在点号前断行

## 示例

格式化前：
```hemlock
fn create_user(name: string, email: string, age: i32, active: bool, role: string) { return { name: name, email: email, age: age, active: active, role: role }; }
```

格式化后：
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

## CI 集成

在 CI 流水线中使用 `--check` 来强制格式化：

```bash
hemlock format --check src/main.hml || echo "File not formatted"
```
