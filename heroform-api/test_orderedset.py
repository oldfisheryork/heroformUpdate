# from ordered_set import OrderedSet
# letters = OrderedSet()
# string_a = "aaabbbccaaaeeeaaaf"
#
# for char in string_a:
#     letters.add(char)
# print(letters)
#
# list = []
#
# for ele in letters:
#     list.append(ele)
# print(list)


# def get_hero_client_relation(extreme_fiinal_list):
#     list_output = []
#
#     for hero_id in range(len(extreme_fiinal_list)):
#         sub_list = []
#         sub_set = OrderedSet()
#
#         hero_name = extreme_fiinal_list[hero_id][0]
#         sub_set.add(hero_name)
#
#         client_num = len(extreme_fiinal_list[hero_id]) - 1
#
#         if client_num <= 0:
#             continue
#
#         for i in range(client_num):
#
#             if extreme_fiinal_list[hero_id][i + 1]:
#
#                 client_id = extreme_fiinal_list[hero_id][i + 1][1]
#
#                 sub_set.add(client_id)
#
#         for ele in sub_set:
#             sub_list.append(ele)
#
#
#         list_output.append(sub_list)
#
#     return list_output


def get_hero_client_relation(total_work_plan):
    list_output = []
    for hero_id in range(len(total_work_plan)):
        sub_list = []
        hero_name = total_work_plan[hero_id][0]
        sub_list.append(hero_name)

        client_num = len(total_work_plan[hero_id]) - 1

        if client_num <= 0:
            continue

        for i in range(client_num):
            client_id = total_work_plan[hero_id][i+1][1]
            sub_list.append(client_id)

        list_output.append(sub_list)
    return list_output