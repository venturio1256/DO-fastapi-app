import os
import uvicorn
from app2 import app 

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)