# QA

## 1) 低成本模型已經表現很好，為何還需要深度學習？目前兩個 ipynb 有沒有用到深度學習？

先說結論：目前兩個 notebook **都沒有使用深度學習**。

- `Project Bot-IoT.ipynb` 與 `ver2.ipynb` 都是傳統機器學習方法。
- 使用的主要分類器是：
  - Random Forest
  - Naive Bayes
  - Decision Tree（Entropy / Gini）
  - XGBoost（梯度提升樹）
- `XGBoost` 屬於集成式樹模型，不是神經網路。
- 兩個 notebook 都採用 chained 分類流程：`attack -> category -> subcategory`，也就是前一層預測結果會作為下一層輸入特徵。

那為何還可能考慮深度學習？

- 當資料型態變複雜（如原始封包序列、時序行為、圖結構關係）時，深度學習可能更有優勢。
- 當你需要端到端學習高維表示（representation）而不是人工挑特徵時，深度學習更合適。
- 但就目前這份「已抽好的 10 個數值特徵」資料型態來看，樹模型通常已經很強，成本也較低、可解釋性較好。

## 2) 當前兩個 ipynb 的訓練參數是什麼？

### A. `Project Bot-IoT.ipynb`（原版）

- 資料切分
  - `train_test_split(ten_best_features, target_features)`
  - 未指定 `random_state`
  - 未指定 `stratify`
- 前處理
  - `StandardScaler()`
- Random Forest
  - 類別初始化：`RandomForestClassifier(max_depth=max_depth)`
  - 實際使用：
    - 內部驗證階段：`max_depth=3`
    - 完整訓練/測試階段：`max_depth=5`
  - 其他參數為 sklearn 預設值
- Naive Bayes
  - `GaussianNB()`（全預設）
- Decision Tree
  - `DecisionTreeClassifier(criterion=criterion, max_depth=max_depth)`
  - `max_depth` 預設為 `5`
  - `criterion` 會用兩種：`entropy`、`gini`
- XGBoost
  - `XGBClassifier()`（幾乎全預設）
- 其他
  - 設有 `warnings.filterwarnings('ignore')`

### B. `ver2.ipynb`（新版）

- 全域設定
  - `RANDOM_STATE = 42`
- 資料切分
  - `train_test_split(..., test_size=0.25, random_state=42, stratify=attack_category_subcategory組合鍵)`
- 前處理
  - `StandardScaler()`
- Random Forest（每一層鏈結用不同深度）
  - attack: `RandomForestClassifier(max_depth=5, n_estimators=200, random_state=42, class_weight='balanced_subsample', n_jobs=-1)`
  - category: `max_depth=7`（其餘同上）
  - subcategory: `max_depth=9`（其餘同上）
- Naive Bayes
  - 三層皆為 `GaussianNB()`
- Decision Tree (Entropy)
  - attack: `DecisionTreeClassifier(criterion='entropy', max_depth=8, class_weight='balanced', random_state=42)`
  - category: `max_depth=10`
  - subcategory: `max_depth=12`
- Decision Tree (Gini)
  - attack/category/subcategory 分別 `max_depth=8/10/12`
  - 其餘：`criterion='gini', class_weight='balanced', random_state=42`
- XGBoost（三層皆有明確參數）
  - `n_estimators=300`
  - `max_depth=6`
  - `learning_rate=0.1`
  - `subsample=0.8`
  - `colsample_bytree=0.8`
  - `random_state=42`
  - `n_jobs=-1`
  - `eval_metric`：
    - attack: `logloss`
    - category/subcategory: `mlogloss`
- 評估指標（新增）
  - `accuracy`
  - `balanced_accuracy`
  - `macro_f1`
  - `weighted_f1`

---

如果你要，我可以再補一版 `QA.md` 的「口試版回答」（更短、可直接念），把每題壓到 30~60 秒。 

# 現有想法
以把三者都理解成同一件事的不同做法：監督式分類（Supervised Classification）。

共同目標：從網路流量的 10 個特徵（如 seq/stddev/drate/srate...）學出規則，預測三個標籤：attack、category、subcategory。
「從什麼到什麼」：從特徵 X → 到標籤 y。
X：10 個數值特徵
y：attack(是否攻擊)、category(DDoS/DoS/Reconnaissance...)、subcategory(TCP/UDP/Service_Scan...)
三者差別：不是目標不同，而是模型家族與訓練方式不同。
你目前三種版本可以這樣分：

1. Project Bot-IoT.ipynb：傳統機器學習基線版
 方法：Random Forest / Naive Bayes / Decision Tree / XGBoost 
 目標：比較哪個傳統模型分類最好

2. ver2.ipynb：傳統機器學習強化版
方法：同上，但加上可重現切分、分層抽樣、更多不平衡指標
目標：讓比較更公平、結果更可信

3. 我給你的深度學習範例：多任務 MLP（神經網路）
方法：共享主幹 + 三個輸出頭同時預測
目標：用 DL 方法做同一個三層分類任務，看看能否在某些指標（尤其少數類）更好
一句話總結：
三者都是「入侵偵測分類」，差別在用樹模型還是神經網路來學「特徵到標籤」的映射。



# 可能可以新增的方法
SMOTE
Data Balance
報告的訓練與測試切割方式一定要報告，訓練與測試是否有交叉比對(五交叉、十 交叉)