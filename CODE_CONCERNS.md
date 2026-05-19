# Current Codebase Concerns

This document records the main risks and technical concerns observed in `Project Bot-IoT.ipynb`.

## 1) Severe class imbalance can hide real model weakness

- The `attack` label is extremely imbalanced (`1` dominates, `0` is very rare).
- Reported high overall accuracy can be misleading under this distribution.
- Several minority classes in `category` and `subcategory` have very low support, so weak recall can be masked by weighted averages.

## 2) Data split is not reproducible and not stratified

- `train_test_split(ten_best_features, target_features)` is used without `random_state`.
- The split is also not stratified, which can worsen minority-class instability.
- Results may vary run-to-run and are harder to compare reliably.

## 3) Warnings are globally suppressed

- `warnings.filterwarnings('ignore')` hides potentially important diagnostics.
- This can conceal data-type issues, convergence problems, and API deprecation messages.

## 4) Chained prediction design can propagate errors

- The pipeline predicts `attack -> category -> subcategory`.
- If `attack` prediction is wrong, downstream predictions can degrade.
- Current reporting focuses on end metrics but does not explicitly analyze error propagation across stages.

## 5) Very high XGBoost performance needs extra validation

- XGBoost results are near-perfect across multiple tasks.
- This may be valid, but should still be stress-tested for overfitting and distribution sensitivity.
- Additional checks (cross-validation, holdout from different time/source slices, and robust per-class metrics) are recommended.

## 6) Metric selection should better reflect minority-class behavior

- The notebook prints confusion matrices and classification reports (good).
- However, decision conclusions appear to rely heavily on overall accuracy.
- Macro-F1, balanced accuracy, and per-class recall should be treated as primary signals for this dataset.

## 7) Notebook-only structure hurts maintainability

- Most logic is embedded in a single notebook, which limits reuse and reproducibility.
- Refactoring into modular scripts (data prep, training, evaluation, inference) would improve long-term maintainability.

---

## ver2 調整思考方向（中文補充）

以下是我在 `ver2.ipynb` 的修改思路。原本上面的 core concerns 保留不變，這一段是接續說明「如何對應改善」。

### A) 先處理「可重現性」與「資料切分穩定性」

- 固定 `RANDOM_STATE = 42`，讓每次切分與訓練結果可重現。
- 將 `train_test_split` 加上 `stratify`（用 `attack + category + subcategory` 的組合鍵），降低少數類在驗證集分佈飄移的風險。
- 目的：讓模型比較有一致基準，避免每次跑完結論都不一樣。

### B) 讓不平衡資料的評估更「看得見」

- 除了原本常見的 accuracy，我新增：
  - `balanced_accuracy`
  - `macro_f1`
  - `weighted_f1`
- 目的：避免只看整體準確率，忽略 minority class 的失真表現。

### C) 保留原本核心建模邏輯，但做工程化整理

- 保留原流程的 chained 預測概念：`attack -> category -> subcategory`。
- 將流程包成 `ChainedMultiTargetClassifier`，統一 `fit/predict`。
- 加入通用評估函式，讓各模型用同一套規則產生可比較的結果。
- 目的：維持原專案方法論，同時提升可讀性與可維護性。

### D) 改善警告處理與 XGBoost 設定透明度

- 移除全域 `warnings.filterwarnings('ignore')`，避免隱藏重要訊息。
- XGBoost 明確指定 `eval_metric`（如 `logloss` / `mlogloss`），避免預設值變更警告並提升可解釋性。
- 目的：讓訓練行為更可追蹤、除錯成本更低。

## ver2 實際修改項目清單

- 新增檔案：`ver2.ipynb`
- 保持原檔不動：`Project Bot-IoT.ipynb`
- 在 `ver2.ipynb` 中的主要變更：
  - 新增固定亂數種子常數與路徑常數
  - 新增 stratified train/valid split
  - 新增標準化流程與一致化評估函式
  - 新增 `balanced_accuracy` / `macro_f1` / `weighted_f1` 報表
  - 保留並重構 chained multi-target 模型類別
  - 明確設定 XGBoost 的 `eval_metric`

## 還沒改、但下一步建議

- 加入交叉驗證（特別是針對少數類）
- 對 error propagation 做顯式分析（例如 attack 預測錯誤時，後兩層惡化幅度）
- 將 notebook 再拆成可重跑的 `.py` 模組與設定檔（data/train/eval/infer）
