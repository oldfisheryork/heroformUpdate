# get the detailed allocation list


def get_full_allocation_list(total_work_plan, weekday_hrs):
    list_middle_output = []

    for list_value in total_work_plan:
        print(list_value)

        list_output_value = []
        remain_hours = 0
        day = 0
        for i in range(len(list_value)):
            # i == 0 is the hero name
            if i == 0:
                list_output_value.append(list_value[i])

            else:
                # pair_first is the total amount time
                # pair_second is the client id
                pair_first = list_value[i][0]
                pair_second = list_value[i][1]

                while pair_first >= weekday_hrs - remain_hours:
                    list_output_value.append([day, weekday_hrs - remain_hours, pair_second])
                    pair_first = pair_first - (weekday_hrs - remain_hours)
                    remain_hours = 0
                    day += 1
                if pair_first != 0:
                    list_output_value.append([day, pair_first, pair_second])
                    remain_hours = pair_first

        print("list_output_value is : {}\n".format(list_output_value))
        list_middle_output.append(list_output_value)

    print("list_middle_output_value is : {}\n".format(list_middle_output))

    list_output = []

    for list_value in list_middle_output:
        pre_day = -1
        list_output_value = []

        for i in range(len(list_value)):
            if i == 0:
                list_output_value.append(list_value[i])
            else:
                set_first = list_value[i][0]
                set_second = list_value[i][1]
                set_third = list_value[i][2]

                if pre_day == set_first:
                    combine_element = []
                    # remove_element is the first [hrs, client] pair belongs to this day
                    remove_element = list_output_value.pop()

                    combine_element.append(remove_element)
                    combine_element.append([set_second, set_third])

                    list_output_value.append(combine_element)
                else:
                    list_output_value.append([set_second, set_third])

                pre_day = set_first

        list_output.append(list_output_value)

    print("list output is : {}\n".format(list_output))
    return list_output


# add [] to the back
def add_back_boring_days(full_allocation_list, weekdays_num):

    for each_hero_plan in full_allocation_list:
        hero_now_total_real_weekdays = len(each_hero_plan) - 1
        boring_day_num = weekdays_num - hero_now_total_real_weekdays

        while boring_day_num > 0:
            # add [] if it's boring days
            each_hero_plan.append([])
            boring_day_num -= 1

        # print("real weekdays is; {}".format(hero_now_total_real_weekdays))
        #
        # print(each_hero_plan)
        # print("---------------------------\n")

    # for i in full_allocation_list:
    #     print("modified allocation is : \n")
    #     print(i)
    #     print('\n')

    return full_allocation_list


# only the function be used when it's the first period of time to deal with
# if it's the starting month of the whole period
def add_front_start_date(first_day_id, total_work_plan):
    num_blank = first_day_id

    for each_hero_plan in total_work_plan:
        for _ in range(num_blank):
            each_hero_plan.insert(1, [])
    print('Updated total work plan is: ', total_work_plan)


# merge to the final list
def merge_final_allocation_list():


total_work_plan_2 =[['Hero 0', [174, 0]],
                   ['Hero 1', [134, 1], [36, 8], [4, 16]],
                   ['Hero 2', [126, 2], [43, 7], [5, 15]],
                   ['Hero 3', [113, 3], [57, 5], [4, 15]],
                   ['Hero 4', [106, 4], [51, 0], [13, 14], [4, 16]],
                   ['Hero 5', [50, 6], [30, 9], [29, 10], [23, 11], [20, 12], [18, 13], [3, 15]]]
#
# total_work_plan_1 = [['Hero 0', [160, 0]],
#                     ['Hero 1', [134, 1], [11, 11], [15, 10]],
#                     ['Hero 2', [126, 2], [30, 9], [4, 10]],
#                     ['Hero 3', [113, 3], [43, 7], [4, 10]],
#                     ['Hero 4', [106, 4], [50, 6], [4, 10]],
#                     ['Hero 5', [65, 0], [57, 5], [36, 8], [2, 10]]

# final_work_plan = [total_work_plan_1, total_work_plan_2]

weekday_hrs = 8
weekdays_num2 = 23
first_day_id = 2
# weekdays_num1 = 20

full_allocation_list = get_full_allocation_list(total_work_plan_2, weekday_hrs)
formulated_allocation_list = add_back_boring_days(full_allocation_list, weekdays_num2)

add_front_start_date(first_day_id, formulated_allocation_list)
