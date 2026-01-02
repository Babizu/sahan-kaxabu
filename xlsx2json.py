import pandas as pd
import json
import os

def convert_xlsx_to_kaxabu_json(input_file, output_file='kaxabu_words.json'):
    """
    將噶哈巫語詞彙表的 Excel/CSV 檔案轉換為應用程式所需的 JSON 格式。
    
    參數:
        input_file (str): 輸入檔案路徑 (.xlsx 或 .csv)
        output_file (str): 輸出 JSON 檔案路徑
    """
    
    print(f"正在讀取檔案: {input_file} ...")
    
    try:
        # 1. 讀取檔案
        # 根據副檔名決定讀取方式
        if input_file.endswith('.csv'):
            # 讀取 CSV
            df = pd.read_csv(input_file, dtype=str) # 強制讀取為字串，避免編號被轉成數字
        else:
            # 讀取 Excel
            df = pd.read_excel(input_file, dtype=str)
        
        print(f"成功讀取資料，共 {len(df)} 筆。")
        print("資料欄位:", df.columns.tolist())

        # 2. 資料清理與欄位對應
        # 應用程式需要的欄位: id, kaxabu, chinese, level, category, note
        
        # 移除完全空白的列
        df.dropna(how='all', inplace=True)
        
        # 處理 NaN 值，轉為空字串
        df = df.fillna('')
        
        # 準備輸出的列表
        output_data = []
        
        for index, row in df.iterrows():
            # 根據您的 CSV 格式進行對應
            # CSV 欄位: 編號, 原語會編號, 噶哈巫語, 中文, 難度, 類別, 備註
            
            # 檢查關鍵欄位是否有值
            kaxabu_word = str(row.get('噶哈巫語', '')).strip()
            chinese_word = str(row.get('中文', '')).strip()
            
            # 如果沒有噶哈巫語或中文，跳過此行
            if not kaxabu_word or not chinese_word:
                continue

            item = {
                # 使用 '原語會編號' 作為唯一 ID，如果沒有則使用 '編號'，再沒有則生成一個
                "id": str(row.get('原語會編號', '')).strip() or str(row.get('編號', '')).strip() or f"gen-{index}",
                
                "kaxabu": kaxabu_word,
                "chinese": chinese_word,
                
                # 預設難度為初級，如果欄位是空的
                "level": str(row.get('難度', '初級')).strip() or "初級",
                
                "category": str(row.get('類別', '')).strip(),
                "note": str(row.get('備註', '')).strip()
            }
            
            output_data.append(item)

        # 3. 輸出 JSON
        print(f"轉換完成，有效資料共 {len(output_data)} 筆。")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
            
        print(f"JSON 檔案已儲存至: {output_file}")
        
    except FileNotFoundError:
        print(f"錯誤: 找不到檔案 {input_file}")
    except Exception as e:
        print(f"發生未預期的錯誤: {e}")

if __name__ == "__main__":
    # 使用範例
    # 請將此處替換為您實際的檔案名稱
    input_filename = "噶哈巫語千詞表_分級0102.xlsx" 
    
    # 檢查檔案是否存在，如果不存在檢查是否為 CSV
    if not os.path.exists(input_filename):
        csv_name = input_filename + " - 已排序.csv"
        if os.path.exists(csv_name):
            input_filename = csv_name
    
    if os.path.exists(input_filename):
        convert_xlsx_to_kaxabu_json(input_filename)
    else:
        print(f"找不到預設檔案 '{input_filename}'，請修改腳本中的 input_filename 變數。")