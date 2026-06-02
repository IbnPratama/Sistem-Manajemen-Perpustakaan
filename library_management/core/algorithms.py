def merge_sort(data, key_func):
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    left = merge_sort(data[:mid], key_func)
    right = merge_sort(data[mid:], key_func)
    return _merge(left, right, key_func)


def _merge(left, right, key_func):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key_func(left[i]) <= key_func(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def binary_search(data, target, key_func):
    low, high = 0, len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        val = key_func(data[mid])
        if val == target:
            return mid
        elif val < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def linear_search(data, target, key_func):
    results = []
    for item in data:
        if target.lower() in str(key_func(item)).lower():
            results.append(item)
    return results


def quick_sort(data, key_func):
    if len(data) <= 1:
        return data
    pivot = data[len(data) // 2]
    left = [x for x in data if key_func(x) < key_func(pivot)]
    middle = [x for x in data if key_func(x) == key_func(pivot)]
    right = [x for x in data if key_func(x) > key_func(pivot)]
    return quick_sort(left, key_func) + middle + quick_sort(right, key_func)


def bubble_sort(data, key_func):
    arr = list(data)
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if key_func(arr[j]) > key_func(arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
