# 代码生成时间: 2025-08-22 15:02:35
# sorting_service.py

"""
Sorting Service using Falcon framework.
This service provides functionality to sort a list of numbers using different algorithms.
"""

from falcon import Falcon, HTTPNotFound, HTTPBadRequest
from falcon.asgi import ASGIApp
import json

# Sort algorithms
def bubble_sort(arr):
    """
    Simple bubble sort algorithm.
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


def quick_sort(arr):
    """
    Quick sort algorithm with Lomuto partition scheme.
    """
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        less = [x for x in arr[1:] if x <= pivot]
        greater = [x for x in arr[1:] if x > pivot]
        return quick_sort(less) + [pivot] + quick_sort(greater)

# Falcon service class
class SortingService:
    """
    A Falcon resource for sorting numbers.
    """
    def on_get(self, req, resp):
        """
        Handle GET requests.
        """
        try:
            # Get the list of numbers from query parameters
            numbers_str = req.get_param("numbers")
            algorithm = req.get_param("algorithm")
            if not numbers_str or not algorithm:
                raise ValueError("Missing required parameters.")
            # Convert string to a list of integers
            numbers = [int(n) for n in numbers_str.split(",")]
            # Sort the list based on the selected algorithm
            if algorithm == "bubble":
                sorted_numbers = bubble_sort(numbers)
            elif algorithm == "quick":
                sorted_numbers = quick_sort(numbers)
            else:
                raise ValueError("Unsupported algorithm.")
            # Return the sorted list as JSON
            resp.media = {"sorted_numbers": sorted_numbers}
        except ValueError as e:
            raise HTTPBadRequest("Invalid request", str(e))
        except Exception as e:
            raise HTTPBadRequest("An error occurred", str(e))

# Initialize Falcon app
app = ASGIApp()
# Add resource
app.add_route("/sort", SortingService())

# Run the ASGI application
if __name__ == "__main__":
    import asyncio
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)