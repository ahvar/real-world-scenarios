class Container:
    """
    A container of integers that should support
    addition, removal, and search for the median integer
    """

    def __init__(self):
        self._values = []
        self._idx = {}

    def add(self, value: int) -> None:
        """
        Adds the specified value to the container

        :param value: int
        """
        if len(self._values) == 0:
            self._values.append(value)
            return
        last_val = self._values[-1]
        self._values.append(value)

    def delete(self, value: int) -> bool:
        """
        Attempts to delete one item of the specified value from the container

        :param value: int
        :return: True, if the value has been deleted, or
                 False, otherwise.
        """
        # TODO: implement this method
        if value not in self._values:
            return False
        left = 0
        right = len(self._values) - 1
        while left <= right:
            mid = (left + right) // 2
            if self._values[mid] == value:
                self._values.pop(mid)
                return True
            elif self._values[mid] < value:
                left = mid + 1
            else:
                right = mid - 1
        return False

    def get_median(self) -> int:
        """
        Finds the container's median integer value, which is
        the middle integer when the all integers are sorted in order.
        If the sorted array has an even length,
        the leftmost integer between the two middle
        integers should be considered as the median.

        :return: The median if the array is not empty, or
        :raise:  a runtime exception, otherwise.
        """
        left, right = 0, len(self._values) - 1
        mid = (right + left) // 2
        if len(self._values) // 2 == 0:
            mid -= 1
        return self._values[mid]
