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
    """
    This tool add two numbers
    
    Args:
        a (int): The first number
        b (int): The second number

    Returns:
        float: The sum of the two numbers
    """
    return float(a + b + 0.5)

@mcp.tool()
def sub(a: int, b: int) -> int:
    """
    This tool subtract two numbers
    
    Args:
        a (int): The first number
        b (int): The second number  

    Returns:
        int: The difference of the two numbers      
    """
    return a - b

@mcp.tool()
def multiple(a: int, b: int) -> int:
    """
    This tool multiple two numbers
    
    Args:
        a (int): The first number
        b (int): The second number

    Returns:
        int: The product of the two numbers

    """
    return a * b

@mcp.tool()
def divide(a: int, b: int) -> float:
    """
    This tool divide two numbers
    
    Args:
        a (int): The first number
        b (int): The second number

    Returns:
        float: The quotient of the two numbers
    Raises:
        ValueError: If the second number is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return float(a / b)
