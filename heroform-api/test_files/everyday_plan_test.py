def get_each_hero_now_month_list(each_hero_list, weekday_hrs):
    print("\n every hero month rough plan is : \n")
    print(each_hero_list)

    collected_day_client_list = []
    remain_hrs = weekday_hrs

    now_month_day_id = 0

    # 对每个client
    for i in range(len(each_hero_list)):
        # i = 0 , hero name
        if i == 0:
            collected_day_client_list.append(each_hero_list[0])
            continue

        # real work
        now_client_request = each_hero_list[i][0]
        now_client_id = each_hero_list[i][1]

        if now_client_request >= remain_hrs:
            while now_client_request >= remain_hrs:
                collected_day_client_list.append([now_month_day_id, remain_hrs, now_client_id])
                now_client_request -= remain_hrs
                remain_hrs = weekday_hrs
                now_month_day_id += 1

        if now_client_request > 0:
            collected_day_client_list.append([now_month_day_id, now_client_request, now_client_id])
            remain_hrs -= now_client_request

    return collected_day_client_list


def get_full_allocation_list(total_work_plan, weekday_hrs):
    print("\n input total work plan is : \n")
    print(total_work_plan)

    list_middle_output = []

    for each_hero_list in total_work_plan:
        collected_day_client_list = get_each_hero_now_month_list(each_hero_list, weekday_hrs)
        list_middle_output.append(collected_day_client_list)

    print("\n list middle output is : \n")
    print(list_middle_output)

    merged_by_day_allocation_list = []

    # every hero work list
    for each_hero_list in list_middle_output:
        pre_day = -1

        merged_day_client_list = []

        # i is each chunk of work id
        for i in range(len(each_hero_list)):
            if i == 0:
                merged_day_client_list.append(each_hero_list[0])
            # all the real work
            else:
                now_day_id = each_hero_list[i][0]
                task_load = each_hero_list[i][1]
                client_id = each_hero_list[i][2]

                if pre_day == now_day_id:

                    new_element = [task_load, client_id]

                    last_ele = merged_day_client_list[-1]

                    test_ele = last_ele[0]
                    # already a list
                    if isinstance(test_ele, (list,)):
                        merged_day_client_list[-1].append(new_element)
                    # not a list
                    else:
                        del merged_day_client_list[-1]
                        combined_list = []
                        combined_list.append(last_ele)
                        combined_list.append(new_element)
                        merged_day_client_list.append(combined_list)
                # different day_id
                else:
                    merged_day_client_list.append([task_load, client_id])

                pre_day = now_day_id

        print("\n list output value is : \n")
        print(merged_day_client_list)

        merged_by_day_allocation_list.append(merged_day_client_list)

    print("\nmerged to everyday allocation list is : \n")
    print(merged_by_day_allocation_list)

    return merged_by_day_allocation_list


# [144, 129, 121, 65, 57, 50, 34]
# total_work_plan = ['Hero 4', [57, 4], [34, 6], [24, 0], [5, 1]]


weekday_hrs = 8
get_full_allocation_list(total_work_plan, weekday_hrs)
