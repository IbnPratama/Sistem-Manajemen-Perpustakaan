def merge_sort(arr, key_field):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid], key_field)
    right_half = merge_sort(arr[mid:], key_field)

    return _merge(left_half, right_half, key_field)


def _merge(left, right, key_field):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        val_left = str(left[i][key_field]).lower() if isinstance(left[i][key_field], str) else left[i][key_field]
        val_right = str(right[j][key_field]).lower() if isinstance(right[j][key_field], str) else right[j][key_field]

        if val_left <= val_right:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
            
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def binary_search(arr, key_field, target):
    sorted_arr = merge_sort(arr, key_field)
    
    low = 0
    high = len(sorted_arr) - 1
    target_val = str(target).lower()

    while low <= high:
        mid = (low + high) // 2
        mid_val = str(sorted_arr[mid][key_field]).lower()

        if mid_val == target_val:
            return sorted_arr[mid] 
        elif mid_val < target_val:
            low = mid + 1
        else:
            high = mid - 1
            
    return None 


def linear_search_partial(arr, key_field, keyword):
    results = []
    keyword = str(keyword).lower()
    
    for item in arr:
        if keyword in str(item[key_field]).lower():
            results.append(item)
            
    return results