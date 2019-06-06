import operator
import math
import datetime as dt
import workdays as wd
import calendar
from ordered_set import OrderedSet

# def get_date():
# client_arr = [600, 320, 176, 174, 143, 80, 70]
# hero_num=5
# weekday_hrs=8
# total_days=300
# month_num=12

# if math.ceil  [400, 200, 110, 109, 90, 50, 44]
# if math.floor [399, 199, 109, 108, 89, 49, 43]


# import numpy as np
# start = dt.date( 2019, 6, 5)
# end = dt.date( 2019, 6, 6)
#
# test how many days betweeen date


# day_id from 0 - 6 means Monday - Sunday
# test_day_id = calendar.weekday(start_year, start_month, start_day)
# print("tested date id is :{}\n".format(test_day_id))


# get the day of the date in this month
# last_date_this_month = calendar.monthrange(2019, 6)[1]
# print(last_date_this_month)
# last_date_start_month = calendar.monthrange(start_year, start_month)[1]


# function to how many workdays between start date and end date
# return total_weekdays_num, month_num, workdays_month_plan
def get_weekdays_num_month(start_year, start_month, start_day, end_year, end_month, end_day):
    weekdays_num_month_list = []

    total_workdays_num = wd.networkdays(dt.date(start_year, start_month, start_day), dt.date(end_year, end_month, end_day))

    print("total weekdays between is: {}".format(total_workdays_num))

    for now_year in range(start_year, end_year + 1):
        if start_year < end_year:
            first_month_year = 1
            last_month_year = 12

            if now_year == start_year:
                begin_month = start_month
            else:
                begin_month = first_month_year

            if now_year == end_year:
                finish_month = end_month
            else:
                finish_month = last_month_year
        else:
            begin_month = start_month
            finish_month = end_month

        for now_month in range(begin_month, finish_month + 1):
            print("month is {}".format(now_month))

            first_day_month = 1
            last_day_month = calendar.monthrange(now_year, now_month)[1]

            if now_year == start_year and now_month == start_month:
                begin_day = start_day
            else:
                begin_day = first_day_month

            if now_year == end_year and now_month == end_month:
                finish_day = end_day
            else:
                finish_day = last_day_month

            # how many weekdays in this month
            month_num_weekdays = wd.networkdays(dt.date(now_year, now_month, begin_day), dt.date(now_year, now_month, finish_day))

            # data structure is: current year, current month and total weekdays in this month of the year
            now_month_plan = [now_year, now_month, month_num_weekdays]

            # a list, show the month and how many weekdays
            weekdays_num_month_list.append(now_month_plan)

            print("The number of weekdays in this month is: {}\n".format(month_num_weekdays))

    # how many months in during the time
    month_num = len(weekdays_num_month_list)

    return total_workdays_num, month_num, weekdays_num_month_list


# make the new client list every month by scaling factor
# every client list is the same
# return scaled_client_list
def get_scaled_client_list(client_list, month_num, total_days, hero_num, weekday_hrs):
    scaled_client_list = []
    available_heroes_total = hero_num * total_days * weekday_hrs

    client_month_request = sum(client_list)
    client_total_request = month_num * client_month_request

    # get the scale_factor
    if available_heroes_total < client_total_request:
        scale_factor = available_heroes_total / client_total_request

        print("scale factor is: ")
        print(scale_factor)
        for each_client in client_list:
            # use math.floor to find the right request
            new_each_client = math.ceil(scale_factor * each_client)
            scaled_client_list.append(new_each_client)
    else:
        scaled_client_list = client_list

    print("scaled client list is : {}\n".format(scaled_client_list))

    return scaled_client_list


# filter and get the final client list
# trimmed the client array is workload is more than heroes availability
# trimmed the client list for specific month
# return final_client_list_now_month
def get_final_client_list_now_month(scaled_client_list, hero_num, day_num_month, weekday_hrs):
    final_client_list_now_month = []

    available_load = hero_num * day_num_month * weekday_hrs

    client_request = sum(scaled_client_list)

    if available_load >= client_request:
        final_client_list_now_month = scaled_client_list
    else:
        for each_client in scaled_client_list:
            if available_load >= each_client:
                final_client_list_now_month.append(each_client)
                available_load -= each_client
            else:
                final_client_list_now_month.append(available_load)
                break

    # print(sum(final_client_list_now_month))

    return final_client_list_now_month


# print(get_weekdays_num_month(start_year, start_month, start_day, end_year, end_month, end_day))

# new_arr = get_scaled_client_list(client_arr, total_days, hero_num, weekday_hrs, month_num)

# for i in range(6):
#     print(new_arr[i] / client_arr[i])


# for small cases
def allocation_for_small_heroes(client_tuple_list, small_heroes, work_plan):

    while client_tuple_list[0][0] > 0 and len(small_heroes) > 0:
        current_client_need = client_tuple_list[0][0]
        current_cliend_id = client_tuple_list[0][1]
        current_hero_load = small_heroes[0][0]
        current_hero_id = small_heroes[0][1]

        smaller_one = current_client_need if current_client_need <= current_hero_load else current_hero_load
        client_tuple_list[0][0] -= smaller_one
        client_tuple_list.sort(key=operator.itemgetter(0), reverse=True)

        work_plan[current_hero_id].append([smaller_one, current_cliend_id])

        if smaller_one == current_hero_load:
            del small_heroes[0]
        else:
            small_heroes[0][0]-=smaller_one
            small_heroes.sort(key=operator.itemgetter(0), reverse=True)

    return work_plan


# use allocation_for_small_heroes to calculate
# the total work plan is for the month
# roughly list of [hero_name, [1hrs, client1], [2hrs, client2],...]
def get_total_work_plan(client_arr, hero_num, day_num_month, weekday_hrs):
    current_hero_id = 0

    total_client_num = len(client_arr)
    total_hero_num = hero_num

    # set final returned plan
    work_plan = []
    # ways to generate
    for i in range(hero_num):
        work_plan.append([])

    # set the correlation list to the clients and hours
    client_tuple_list = []
    for i in range(len(client_arr)):
        client_tuple_list.append([])
        client_tuple_list[i].append(client_arr[i])
        client_tuple_list[i].append(i)

    # test to print tuple list
    # print(client_tuple_list)

    print("Clients task is : {}".format(client_arr))
    print("We have in total {} heroes".format(hero_num))
    total_goal = sum(client_arr)
    print("\nTotal required hrs is: {}".format(total_goal))

    # test case if there's too little work, we need to
    # total_each_hero = 5 * 8 * weeks_num * (541 / 960)
    total_each_hero = weekday_hrs * day_num_month

    total_available = hero_num * total_each_hero

    print("Total available hrs is: {}".format(total_available))

    if total_available > total_goal:
        total_each_hero = math.ceil(total_each_hero * (total_goal / total_available))

    print("each hero should spend no more than: {} hours".format(total_each_hero))
    ########## very important #########

    # first round, to filter the task with less than 160 hrs and get the rest of them
    # after this round, each task can be done

    finished_client_num = 0

    for client_id in range(len(client_arr)):
        each_client = client_arr[client_id]

        num_of_hero = each_client // total_each_hero

        ########## very important ##########
        if num_of_hero == 0:
            # rest_client_arr.append(each_client)
            pass
        else:
            hero_num -= num_of_hero

            print("\n-------{} heroes has been been fully allocated-------".format(num_of_hero))

            while num_of_hero > 0:
                work_plan[current_hero_id].append('Hero {}'.format(current_hero_id))

                # client_tuple_list[client_id][0] = 160
                ########## very important #1st client id#####
                work_plan[current_hero_id].append([total_each_hero, client_id])

                print("\nHero id is: {}".format(current_hero_id))

                print("Individual allocation is: {}".format(work_plan[current_hero_id]))

                num_of_hero -= 1

                current_hero_id += 1

            rest_work = each_client % total_each_hero

            if rest_work >= 0:
                ########## very important ##########
                # rest_client_arr.append(rest_work)
                client_tuple_list[client_id][0] = rest_work

                if rest_work == 0:
                    finished_client_num += 1

    client_tuple_list.sort(key=operator.itemgetter(0), reverse=True)
    ########## very important #####1st sort#####


    # second round , for every hero
    print("\n-----The rest of clients task is: {} ------".format(client_tuple_list))
    print("We still have {} heroes".format(hero_num))
    print()

    small_heroes = []

    # for every hero
    for hero_id in range(total_hero_num - hero_num, total_hero_num):
        print("Hero id is: {}".format(hero_id))
        rest = total_each_hero

        # for every hero's work plan
        work_plan[hero_id].append('Hero {}'.format(hero_id))

        # flag is to calculate in this iteration how many clients has been finished
        flag = 0

        for i in range(total_client_num - finished_client_num):
            # remain_request = rest_client_arr[i]

            remain_request = client_tuple_list[i][0]
            # print("least client is: {}".format(client_tuple_list[total_client_num - finished_client_num - 1][0]))

            # when it's has 8 more but [2, 1] finished still have 6 to push into smalled heroes

            if rest >= remain_request > 0:
                rest -= remain_request
                # finishd one client
                flag += 1

                ########## very important #2nd client id#####
                one_work = []
                one_work.append(client_tuple_list[i][0])
                one_work.append(client_tuple_list[i][1])

                work_plan[hero_id].append(one_work)

                # rest_client_arr[i] = 0
                client_tuple_list[i][0] = 0

            if rest > 0 and i == total_client_num - finished_client_num - 1:
                small_one = [rest, hero_id]
                small_heroes.append(small_one)

        finished_client_num += flag

        # ########## very important ####2nd sort######
        client_tuple_list.sort(key=operator.itemgetter(0), reverse=True)

        print("Individual allocation is: {}".format(work_plan[hero_id]))
        print("Smaller heroes is: {}".format(small_heroes))
        print("The rest clients need to be allocated is: {}".format(client_tuple_list))
        print()

    # test
    print("small heroes list is: ")

    small_heroes.sort(key=operator.itemgetter(0), reverse=True)
    print(small_heroes)

    # print(finished_client_num)
    print("client_tuple_list is : ")
    print(client_tuple_list)

    updated_work_plan = allocation_for_small_heroes(client_tuple_list, small_heroes, work_plan)

    return updated_work_plan


# get the detailed allocation list
# each month plan rough plan as input
# to the every day
def get_full_allocation_list(total_work_plan, weekday_hrs):
    list_middle_output = []

    for list_value in total_work_plan:
        print(list_value)
        list_output_value = []
        remain_hours = 0
        day = 0
        for i in range(len(list_value)):
            if i == 0:
                list_output_value.append(list_value[i])
            else:
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
        list_middle_output.append(list_output_value)

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
                    remove_element = list_output_value.pop()
                    combine_element.append(remove_element)
                    combine_element.append([set_second, set_third])
                    list_output_value.append(combine_element)
                else:
                    list_output_value.append([set_second, set_third])
                pre_day = set_first
        list_output.append(list_output_value)

    return list_output


# only the function be used when it's the first period of time to deal with
# if it's the starting month of the whole period
def add_front_start_date(first_day_id, final_final_allocation_list):
    if first_day_id > 4:
        return final_final_allocation_list

    num_blank = first_day_id

    for each_hero_plan in final_final_allocation_list:
        for _ in range(num_blank):
            each_hero_plan.insert(1, [])

    print('Updated total work plan is: \n', final_final_allocation_list)

    return final_final_allocation_list


# add [] to the back
def add_back_boring_days(full_allocation_list, weekdays_num):
    for each_hero_plan in full_allocation_list:
        hero_now_total_real_weekdays = len(each_hero_plan) - 1
        boring_day_num = weekdays_num - hero_now_total_real_weekdays

        while boring_day_num > 0:
            # add [] if it's boring days
            each_hero_plan.append([])
            boring_day_num -= 1

    return full_allocation_list


# generate excel table
def generate_table(file_name, list1, list2):
    week_num = math.ceil((len(list1[0]) - 1) / 5)

    titles = 'Monday\tTuesday\tWednesday\tThursday\tFriday\t' * week_num

    output = open(file_name, 'w', encoding='gbk')

    output.write('Detailed work allocation for this month: \n')

    output.write('\t')
    output.write(titles)
    output.write('\n')

    for i in range(len(list1)):
            for j in range(len(list1[i])):
                pass
                output.write(str(list1[i][j]))    #write函数不能写int类型的参数，所以使用str()转化
                output.write('\t')   #相当于Tab一下，换一个单元格
            output.write('\n')       #写完一行立马换行

    output.write('\n')  # 写完一行立马换行

    # print the table for Hero-client relation
    output.write('\nHero-Client relation is: \n')

    for m in range(len(list2)):
            for n in range(len(list2[m])):
                output.write(str(list2[m][n]))    #write函数不能写int类型的参数，所以使用str()转化
                output.write('\t')   #相当于Tab一下，换一个单元格
            output.write('\n')       #写完一行立马换行

    output.close()


# get extreme final allocation list
# relation list
def calculate(client_list, hero_num, weekday_hrs,
              start_year, start_month, start_day, end_year, end_month, end_day):
    # for example
    # [43, 2, [[2019, 6, 20], [2019, 7, 23]]]
    total_weekdays, month_num, weekdays_month_plan = get_weekdays_num_month(start_year, start_month, start_day,
                                                                            end_year, end_month, end_day)

    # fixed, during the time scaled
    scaled_client_list = get_scaled_client_list(client_list, month_num, total_weekdays, hero_num, weekday_hrs)

    detailed_allocation_now_month = []

    # this is the merged plan
    final_final_allocation_list = []

    relation_set_list = []
    for i in range(hero_num):
        sub_set = OrderedSet()
        relation_set_list.append(sub_set)

    # every_month_details such as [2019, 7, 23]
    for every_month_details in weekdays_month_plan:
        now_year = every_month_details[0]
        now_month = every_month_details[1]
        day_num_month = every_month_details[2]

        # scaled and trimmed and trimed
        final_client_list_now_month = get_final_client_list_now_month(scaled_client_list, hero_num, day_num_month,
                                                                      weekday_hrs)

        print("year: {}".format(now_year))
        print("month: {}".format(now_month))

        print("final client list this month is :{}\n".format(final_client_list_now_month))

        # roughly allocation each month
        work_plan_now_month = get_total_work_plan(final_client_list_now_month, hero_num, day_num_month, weekday_hrs)
        print("work plan this month is:\n {}\n".format(work_plan_now_month))

        for i in range(hero_num):
            hero_name = work_plan_now_month[i][0]
            relation_set_list[i].add(hero_name)

            client_num = len(work_plan_now_month[i]) - 1

            if client_num <= 0:
                continue

            for client_id in range(client_num):
                relation_set_list[i].add(work_plan_now_month[i][client_id + 1][1])


        # detailed allocation each month
        detailed_allocation_now_month = get_full_allocation_list(work_plan_now_month, weekday_hrs)

        # for each month add blank if it's boring days
        back_added_allocation_list = add_back_boring_days(detailed_allocation_now_month, day_num_month)
        print("detailed allocation this month is:\n {}\n".format(back_added_allocation_list))

        final_final_allocation_list.append(back_added_allocation_list)

        # print(work_plan_now_month)
        print("----------------------------\n")

    final_relation_list = []
    for hero_id in range(hero_num):
        sub_list = []
        current_sub_set = relation_set_list[hero_id]
        for ele in current_sub_set:
            sub_list.append(ele)
        final_relation_list.append(sub_list)

    print("\nfinal relation list is: \n")
    print(final_relation_list)

    print("\n most complete allocation plan is : \n")
    print(final_final_allocation_list)

    first_month_allocation_list = final_final_allocation_list[0]

    if month_num > 1:
        # in every month
        for month_id in range(1, month_num):
            now_month_allocation_list = final_final_allocation_list[month_id]

            for hero_id in range(len(now_month_allocation_list)):
                total_allocation_days = len(now_month_allocation_list[hero_id])

                for each_allocation_id in range(1, total_allocation_days):
                    first_month_allocation_list[hero_id].append(now_month_allocation_list[hero_id][each_allocation_id])

    # day_id from 0 - 6 means Monday - Sunday
    # test_day_id = calendar.weekday(start_year, start_month, start_day)
    # print("tested date id is :{}\n".format(test_day_id))
    first_day_id = calendar.weekday(start_year, start_month, start_day)

    extreme_final_list = add_front_start_date(first_day_id, first_month_allocation_list)

    print("\n extreme_final_list is :\n")
    print(extreme_final_list)

    return extreme_final_list, final_relation_list


def add_dates_to_extreme_final_list(extreme_final_list, start_year, start_month, start_day, end_year, end_month, end_day):
    pass


if __name__ == '__main__':
    start_year = 2019
    start_month = 7
    start_day = 1

    end_year = 2020
    end_month = 6
    end_day = 30

    client_list = [240, 50, 25, 22, 20, 18, 18, 18, 18, 18, 18, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 16, 10]

    print("total original client request is: {}".format(sum(client_list)))

    hero_num=5
    weekday_hrs=6

    extreme_final_list, hero_client_list = calculate(client_list, hero_num, weekday_hrs,
                                                     start_year, start_month, start_day, end_year, end_month, end_day)

    # hero_client_list = get_hero_client_relation(extreme_final_list)

    file_name = 'results.xls'

    generate_table(file_name, extreme_final_list, hero_client_list)
