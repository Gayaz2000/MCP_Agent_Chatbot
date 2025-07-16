# from fastapi import Request, HTTPException
# from mcp.server.fastmcp import FastMCP

# API_KEY = "your-secret-api-key"

# async def auth_middleware(request: Request, call_next):
#     api_key = request.headers.get("x-api-key")
#     if api_key != API_KEY:
#         raise HTTPException(status_code=401, detail="Unauthorized")
#     response = await call_next(request)
#     return response


# # mcp = FastMCP(
# #     name="My_Server",
# #     host="0.0.0.0",
# #     port=8040,
# #     middleware=[auth_middleware]
# # )

# mcp = FastMCP(
#     name="My_Server",
#     host="0.0.0.0",
#     port=8040
# )

# # If `mcp.app` exposes the underlying FastAPI app
# mcp.app.middleware("http")(auth_middleware)

# from fastapi import Depends

# def verify_api_key(request: Request):
#     if request.headers.get("x-api-key") != API_KEY:
#         raise HTTPException(status_code=401, detail="Unauthorized")

# @mcp.app.get("/secure-endpoint")
# async def secure_data(dep=Depends(verify_api_key)):
#     return {"message": "This is a protected endpoint"}