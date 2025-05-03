from fastapi import FastAPI

app = FastAPI(title="GuardTree API", version="1.0")

@app.get("/")
async def root():
    return {"message": "Welcome to GuardTree API"}


"""
             ＿＿
　　　　 　／＞　　フ
　　　　　|   .　 .l
　 　　　／` ミ＿꒳ノ
　　 　 /　　　 　 |
　　　 /　 ヽ　　 ﾉ
　 　 │　　|　|　|
　／￣|　　 |　|　|
　| (￣ヽ＿_ヽ_)__)
　＼二つ
幸運貓貓在此，bug已經全部被我抓走了~
"""
