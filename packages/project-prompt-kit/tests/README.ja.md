# テスト（Tests）

v0.1.x のテスト基盤（test infrastructure）は意図的に最小限です。

パッケージ検証（package validation）には `../scripts/validate.sh` を使います。このコマンドには固定データ検証（fixture validation）も含まれます。

契約用固定データの検査ゲート（contract fixture gate）だけが必要な場合は `validate-fixtures.sh` を使います。

```bash
bash packages/project-prompt-kit/tests/validate-fixtures.sh
```

## 固定データ（Fixtures）

- `fixtures/valid/` には、対応モード（mode）全体、対応対象（target）全体、少なくとも一つのプロンプト依頼用固定データ（prompt request fixture）を含む有効なプロンプト契約（valid prompt contract）があります。
- `fixtures/invalid/` には、必須フィールド（required field）、列挙値（enum）、定数値（const value）、型チェック（type check）、文字列/配列の最小値（string/array minimum）、余分なプロパティ（extra property）、安全でない安全既定値（unsafe safety default）、ネストした安全設定の形（nested safety shape）、非対応のスキーマキーワード（unsupported schema keyword）の独立した失敗ケースがあります。
- `golden/` には、対応モード（mode）全体に対する静的な出力構造の例（static output shape）があります。

正解例ファイル（golden file）は例であり、描画器スナップショット（renderer snapshot）ではありません。このパッケージ（package）はまだ CLI や描画エンジン（renderer engine）を含みません。
