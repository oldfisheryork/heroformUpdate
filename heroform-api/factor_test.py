import operator
import math
import datetime as dt
import workdays as wd
import calendar

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
# days = np.busday_count(start, end)
# print("June in 2019 business days is: ")

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
    weekdays_num_month = []

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

            month_workdays = wd.networkdays(dt.date(now_year, now_month, begin_day), dt.date(now_year, now_month, finish_day))

            # data structure is: current year, current month and total weekdays in this month of the year
            now_month_plan = [now_year, now_month, month_workdays]
            weekdays_num_month.append(now_month_plan)

            print("The number of workdays this month is: {}\n".format(month_workdays))

    month_num = len(weekdays_num_month)

    return total_workdays_num, month_num, weekdays_num_month


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


# also will allocation_for_small_heroes
# the total work plan is for the month
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
            print("least client is: {}".format(client_tuple_list[total_client_num - finished_client_num - 1][0]))

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


# generate excel table
def generate_table(file_name, list1):
    week_num = math.ceil(len(list1[0][0]) / 5)
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

    # # print the table for Hero-client relation
    # output.write('\nHero-Client relation is: \n')
    #
    # for m in range(len(list2)):
    #         for n in range(len(list2[m])):
    #             output.write(str(list2[m][n]))    #write函数不能写int类型的参数，所以使用str()转化
    #             output.write('\t')   #相当于Tab一下，换一个单元格
    #         output.write('\n')       #写完一行立马换行

    output.close()


if __name__ == '__main__':
    start_year = 2019
    start_month = 6
    start_day = 1

    end_year = 2019
    end_month = 7
    end_day = 31

    client_list = [320, 190, 179, 160, 150, 80, 70, 60, 50, 42, 40, 32, 28, 25, 18, 16, 10]

    print("total original client request is: {}".format(sum(client_list)))

    hero_num=6
    weekday_hrs=8

    total_weekdays, month_num, weekdays_month_plan = get_weekdays_num_month(start_year, start_month, start_day, end_year, end_month, end_day)

    # fixed, during the time scaled
    scaled_client_list=get_scaled_client_list(client_list, month_num, total_weekdays, hero_num, weekday_hrs)

    detailed_allocation_now_month = []

    for every_month_details in weekdays_month_plan:
        now_year = every_month_details[0]
        now_month = every_month_details[1]
        day_num_month = every_month_details[2]

        final_client_list_now_month = get_final_client_list_now_month(scaled_client_list, hero_num, day_num_month, weekday_hrs)

        print("year: {}".format(now_year))
        print("month: {}".format(now_month))
        print("final client list this month is :{}\n".format(final_client_list_now_month))

        work_plan_now_month = get_total_work_plan(final_client_list_now_month, hero_num, day_num_month, weekday_hrs)

        detailed_allocation_now_month = get_full_allocation_list(work_plan_now_month, weekday_hrs)

        print("work plan this month is:\n {}\n".format(work_plan_now_month))
        print("detailed allocation this month is:\n {}\n".format(detailed_allocation_now_month))

        # print(work_plan_now_month)
        print("----------------------------\n")



