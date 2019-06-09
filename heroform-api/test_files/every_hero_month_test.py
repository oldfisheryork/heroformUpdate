# every hero


def each_hero_now_month_list(each_hero_list, weekday_hrs):
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


total_work_plan = ['Hero 4', [57, 4], [34, 6], [24, 0], [5, 1]]
print(each_hero_now_month_list(total_work_plan, 8))




