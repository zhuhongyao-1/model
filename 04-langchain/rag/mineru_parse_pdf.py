"""
    测试：使用MinerU解析PDF
"""
def mineru_upload_file():
    import requests

    token = "eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJqdGkiOiI1NzUwMDA1OSIsInJvbCI6IlJPTEVfUkVHSVNURVIiLCJpc3MiOiJPcGVuWExhYiIsImlhdCI6MTc3OTUyNjA0OCwiY2xpZW50SWQiOiJsa3pkeDU3bnZ5MjJqa3BxOXgydyIsInBob25lIjoiIiwib3BlbklkIjpudWxsLCJ1dWlkIjoiNWQxOWU0MzYtOTE1Ni00MjYyLTgzNWQtODQ1YjYyMDg3OGE2IiwiZW1haWwiOiIiLCJleHAiOjE3ODczMDIwNDh9.mhET5hZF0IsuaLAROb-QEQYbh2msjytdHUJRilRUNZS3cviU1X6RFJKY98jvoDTin185hH3K7Eo_QNYa1s3SQQ"
    url = "https://mineru.net/api/v4/file-urls/batch"
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {
        "files": [
            {"name": "demo.pdf", "data_id": "abcd"}
        ],
        "model_version": "vlm"
    }
    file_path = [
        r"D:\workspace\BJ260318\langchain\rag\assets\sample.pdf"
    ]
    try:
        response = requests.post(url, headers=header, json=data)
        if response.status_code == 200:
            result = response.json()
            print('response success. result:{}'.format(result))
            if result["code"] == 0:
                batch_id = result["data"]["batch_id"]
                urls = result["data"]["file_urls"]
                print('batch_id:{},urls:{}'.format(batch_id, urls))
                for i in range(0, len(urls)):
                    with open(file_path[i], 'rb') as f:
                        res_upload = requests.put(urls[i], data=f)
                        if res_upload.status_code == 200:
                            print(f"{urls[i]} upload success")
                        else:
                            print(f"{urls[i]} upload failed")
            else:
                print('apply upload url failed,reason:{}'.format(result["msg"]))
        else:
            print('response not success. status:{} ,result:{}'.format(response.status_code, response))
    except Exception as err:
        print(err)

def mineru_get_result():
    import requests

    token = "eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJqdGkiOiI1NzUwMDA1OSIsInJvbCI6IlJPTEVfUkVHSVNURVIiLCJpc3MiOiJPcGVuWExhYiIsImlhdCI6MTc3OTUyNjA0OCwiY2xpZW50SWQiOiJsa3pkeDU3bnZ5MjJqa3BxOXgydyIsInBob25lIjoiIiwib3BlbklkIjpudWxsLCJ1dWlkIjoiNWQxOWU0MzYtOTE1Ni00MjYyLTgzNWQtODQ1YjYyMDg3OGE2IiwiZW1haWwiOiIiLCJleHAiOjE3ODczMDIwNDh9.mhET5hZF0IsuaLAROb-QEQYbh2msjytdHUJRilRUNZS3cviU1X6RFJKY98jvoDTin185hH3K7Eo_QNYa1s3SQQ"
    batch_id = "257a46f8-616d-425d-a77c-4cf347fc43e9"
    url = f"https://mineru.net/api/v4/extract-results/batch/{batch_id}"
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    res = requests.get(url, headers=header)
    print(res.status_code)
    print(res.json())
    print(res.json()["data"])

if __name__ == '__main__':
    # mineru_upload_file()
    mineru_get_result()