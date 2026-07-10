#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Auto Run All Model (then you can sleep savely)
    python run_all_notebooks.py
"""

import os
import sys
import subprocess
import time
from datetime import datetime
from pathlib import Path

# 設定 notebook 檔案路徑
NOTEBOOK_DIR = Path(__file__).parent
NOTEBOOKS = [
    "Project Bot-Iot(TOP10 Feature - RF)(Chain vs Independent).ipynb",
    "Project Bot-Iot(ALL Feature - RF)(Chain vs Independent).ipynb",
    "Project Bot-Iot(TOP10 Feature - MLP).ipynb",
    "Project Bot-Iot(ALL Feature - MLP).ipynb"
]

# 日誌檔案
LOG_FILE = NOTEBOOK_DIR / "notebook_execution_log.txt"

def log_message(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    
    print(log_entry)
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")


def run_notebook(notebook_path):

    notebook_name = notebook_path.name
    
    log_message(f"開始執行: {notebook_name}", "INFO")
    print(f"\n{'='*80}")
    print(f"執行 Notebook: {notebook_name}")
    print(f"{'='*80}\n")
    
    try:
        # 使用 jupyter nbconvert 執行 notebook
        # 輸出結果到新的 notebook（帶有 _output 後綴）
        output_notebook = notebook_path.parent / f"{notebook_path.stem}_output.ipynb"
        
        cmd = [
            "jupyter",
            "nbconvert",
            "--to", "notebook",
            "--execute",
            "--ExecutePreprocessor.timeout=-1",  
            "--ExecutePreprocessor.kernel_name=python3",  # ✅ 加這行
            "--inplace",          # ✅ 結果寫回原檔，VS Code 開就能看
            str(notebook_path)
        ]
        
        # 執行命令
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            log_message(f"✓ 成功完成: {notebook_name}", "SUCCESS")
            print(f"\n✓ {notebook_name} 執行成功!")
            print(f"  輸出檔案: {output_notebook}\n")
            return True
        else:
            log_message(f"✗ 執行失敗: {notebook_name}", "ERROR")
            log_message(f"錯誤信息:\n{result.stderr}", "ERROR")
            print(f"\n✗ {notebook_name} 執行失敗!")
            print(f"  錯誤: {result.stderr}\n")
            return False
            
    except Exception as e:
        log_message(f"✗ 異常錯誤: {str(e)}", "ERROR")
        print(f"\n✗ 執行出錯: {str(e)}\n")
        return False


def main():
    
    print("\n" + "="*80)
    print("Bot-IoT 自動化 Notebook 執行系統")
    print("="*80)
    
    log_message("="*80, "INFO")
    log_message("開始執行 Bot-IoT 分析 Notebook 流程", "INFO")
    log_message("="*80, "INFO")
    
    # 檢查 Jupyter 是否安裝
    try:
        subprocess.run(["jupyter", "--version"], capture_output=True, check=True)
    except subprocess.CalledProcessError:
        log_message("錯誤: 未安裝 Jupyter", "ERROR")
        print("\n✗ 請先安裝 Jupyter:")
        print("  pip install jupyter nbconvert\n")
        return False
    
    # 執行每個 notebook
    results = []
    start_time = time.time()
    
    for notebook_name in NOTEBOOKS:
        notebook_path = NOTEBOOK_DIR / notebook_name
        
        # 檢查檔案是否存在
        if not notebook_path.exists():
            log_message(f"✗ 找不到檔案: {notebook_path}", "ERROR")
            print(f"\n✗ 找不到 notebook 檔案: {notebook_path}\n")
            results.append(False)
            continue
        
        # 執行 notebook
        success = run_notebook(notebook_path)
        results.append(success)
        
        # 檔案之間間隔 5 秒
        if notebook_name != NOTEBOOKS[-1]:
            log_message("等待 5 秒後執行下一個 notebook...", "INFO")
            time.sleep(5)
    
    # 總結
    elapsed_time = time.time() - start_time
    elapsed_minutes = elapsed_time / 60
    elapsed_hours = elapsed_minutes / 60
    
    print("\n" + "="*80)
    print("執行完成!")
    print("="*80)
    
    successful = sum(results)
    total = len(results)
    
    log_message(f"\n執行結果統計:", "INFO")
    log_message(f"  成功: {successful}/{total}", "INFO")
    log_message(f"  耗時: {elapsed_hours:.2f} 小時 ({elapsed_minutes:.1f} 分鐘)", "INFO")
    
    print(f"\n📊 執行結果:")
    for notebook_name, success in zip(NOTEBOOKS, results):
        status = "✓ 成功" if success else "✗ 失敗"
        print(f"  {status}: {notebook_name}")
    
    print(f"\n⏱️  總耗時: {elapsed_hours:.2f} 小時 ({elapsed_minutes:.1f} 分鐘)")
    print(f"📁 日誌檔案: {LOG_FILE}\n")
    
    log_message("="*80, "INFO")
    log_message("所有 Notebook 執行完畢", "INFO")
    log_message("="*80, "INFO")
    
    return all(results)


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        log_message("執行被用戶中斷", "WARNING")
        print("\n⚠️  執行已中斷\n")
        sys.exit(1)
    except Exception as e:
        log_message(f"未預期的錯誤: {str(e)}", "ERROR")
        print(f"\n❌ 發生錯誤: {str(e)}\n")
        sys.exit(1)
