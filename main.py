import ipaddress
import subprocess
from black import err
from fastapi import Body, FastAPI, HTTPException, Header
from bcrypt import checkpw, gensalt, hashpw

app = FastAPI()


def authenticated(passwd: str) -> bool:
    with open("passwd", "rb") as f:
        hashed_passwd = f.read()
    return checkpw(passwd, hashed_passwd)


@app.post(
    "/update",
)
async def update(passwd: str = Body(), x_real_ip: ipaddress.IPv4Address = Header()):
    if not authenticated(passwd.encode("utf-8")):
        print(hashpw(passwd.encode("utf-8"), gensalt()))
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )

    ret = subprocess.run(["sh", "update-ddns.sh", x_real_ip.exploded])
    if ret.returncode != 0:
        raise err("Failed to run DDNS update script")

    return {"msg": "Successfully updated ddns entry", "newIp": x_real_ip}
