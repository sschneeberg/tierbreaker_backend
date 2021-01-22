def quick_sort(totals_dict, dict_arr=[]):
    if len(dict_arr) == 0: 
        for key in totals_dict:
            dict_arr.append({ key: totals_dict[key]})
    # dict_arr is an array of dictionaries in form {option : total_votes}
    # sort by total_votes
    if len(dict_arr) == 0: return dict_arr
    pivot = dict_arr[-1]
    pivot_value = ''
    for key in pivot: pivot_value = pivot[key]
    lower, upper = [],[]
    for i in range(len(dict_arr) - 1):
        for key in dict_arr[i]:
            if dict_arr[i][key] > pivot_value: upper.append(dict_arr[i])
            else: lower.append(dict_arr[i])
    return quick_sort({},upper) + [pivot] + quick_sort({},lower)
        
# test_dict = {"key1": 1, "key2" : 4, "key6" : 0}
# print(quick_sort(test_dict))
# print([{'key6': 0}, {'key1': 1}, {'key2': 4}])