# 代码生成时间: 2025-08-10 11:04:31
# sort_algorithm_service.py
# This Python program uses the Falcon framework to provide a service
# that implements sorting algorithms.

import falcon

class SortService:
    """
    This class provides a sorting service.
    It exposes methods to sort a list of integers.
    """

    def on_get(self, req, resp):
        """
        Handles GET requests to the /sort endpoint.
        Returns a sorted list of numbers provided as a query parameter.
        """
        try:
            numbers = req.get_param('numbers')
            if not numbers:
                raise falcon.HTTPBadRequest('Missing query parameter: numbers')

            try:
                numbers = [int(num) for num in numbers.split(',')]
            except ValueError:
                raise falcon.HTTPBadRequest('Invalid number in query parameter: numbers')

            sorted_numbers = self.sort_numbers(numbers)
            resp.media = {'sorted_numbers': sorted_numbers}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {'error': str(e)}

    def sort_numbers(self, numbers):
        """
        Sorts a list of numbers using the quicksort algorithm.
        Args:
            numbers (list): A list of integers to sort.
        Returns:
            list: The sorted list of integers.
        """
        self.quicksort(numbers, 0, len(numbers) - 1)
        return numbers

    def quicksort(self, arr, low, high):
        """
        The quicksort algorithm.
        Args:
            arr (list): The array to sort.
            low (int): The starting index.
            high (int): The ending index.
        """
        if low < high:
            partition_index = self.partition(arr, low, high)
            self.quicksort(arr, low, partition_index - 1)
            self.quicksort(arr, partition_index + 1, high)

    def partition(self, arr, low, high):
        """
        The partition function for the quicksort algorithm.
        Args:
            arr (list): The array to partition.
            low (int): The starting index.
            high (int): The ending index.
        Returns:
            int: The index at which the array is partitioned.
        """
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

# Instantiate the Falcon API
api = falcon.API()

# Add the SortService to the API at the /sort endpoint
api.add_route('/sort', SortService())
