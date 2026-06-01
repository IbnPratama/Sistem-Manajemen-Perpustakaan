def merge_sort(arr, key_func):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid], key_func)
    right_half = merge_sort(arr[mid:], key_func)

    return _merge(left_half, right_half, key_func)

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

def binary_search(arr, target, key_func):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        current_val = str(key_func(arr[mid])).lower()
        target_val = str(target).lower()

        if current_val == target_val:
            return arr[mid]
        elif current_val < target_val:
            low = mid + 1
        else:
            high = mid - 1

    return None