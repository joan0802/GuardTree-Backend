1. 建立虛擬環境並啟動
```
python -m venv venv
source venv/bin/activate  -- for mac venv\Scripts\activate     -- for Windows
```
2. 安裝套件
```
pip install -r requirements.txt
```
3. 執行程式
```
uvicorn main:app --reload
```