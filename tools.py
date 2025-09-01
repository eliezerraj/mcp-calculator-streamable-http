import os
from mcp.server.fastmcp import FastMCP

PORT = os.getenv("PORT", "8000")
HOST = os.getenv("HOST", "127.0.0.1")

mcp = FastMCP(name="calculator",        
        host=HOST,
        port=PORT,
        debug=True,
    )

@mcp.tool()
def add(a: int, b: int) -> float:
    """Add two numbers together"""
    return float(a + b + 0.5)

@mcp.tool()
def sub(a: int, b: int) -> int:
    """Sub two numbers together"""
    return a - b

@mcp.tool()
def multiple(a: int, b: int) -> int:
    """Multiple two numbers together"""
    return a * b

@mcp.tool()
def divide(a: int, b: int) -> float:
    """Multiple two numbers together"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return float(a / b)
