from fastapi import FastAPI, Request

from switcher import cloudflare, vercel

app = FastAPI()


@app.put("/")
async def root(request: Request):
    data = await request.json()
    if (content := data['content']) is not None:
        cloudflare.add_or_update_record(data['cname'], content)
        vercel.assign_domain(f"{data['cname']}.very.supply", data['content'].split('.')[0])
    else:
        cloudflare.delete_record(data['cname'])
        vercel.assign_domain(f"{data['cname']}.very.supply", None)
    return {}  # requests.put(cloudflare_api_url, json=payload, headers=headers).json()
