import operator
import math
import datetime as dt
import workdays as wd
import calendar

# filter and get the final client list
# trimmed the client array is workload is more than heroes availability
# def filter_client_arr(input_list, hero_num, week_num, days_per_week, weekday_hrs):
#     output_list = []
#
#     available_load = hero_num * week_num * days_per_week * weekday_hrs
#
#     client_request = sum(input_list)
#
#     if available_load >= client_request:
#         output_list = input_list
#     else:
#         for each_client in input_list:
#
#             if available_load >= each_client:
#                 output_list.append(each_client)
#                 available_load -= each_client
#             else:
#                 output_list.append(available_load)
#                 break
#
#     # print(sum(output_list))
#
#     return output_list


# get the total work plan


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
def get_total_work_plan(client_arr, hero_num, week_num, days_per_week, weekday_hrs):
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
    total_each_hero = weekday_hrs * days_per_week * week_num

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

            # if rest < client_tuple_list[total_client_num - finished_client_num - flag - 1][0]:
            #     small_one = [rest, hero_id]
            #     small_heroes.append(small_one)
            #     break


            # here should push the small available work to the list


            # if rest >= remain_request:
            #     rest -= remain_request
            #     # finishd one client
            #     flag += 1
            #
            #     ########## very important #2nd client id#####
            #     one_work = []
            #     one_work.append(client_tuple_list[i][0])
            #     one_work.append(client_tuple_list[i][1])
            #
            #     work_plan[hero_id].append(one_work)
            #
            #     # rest_client_arr[i] = 0
            #     client_tuple_list[i][0] = 0
            #
            # # here should push the small available work to the list
            # elif rest < remain_request and rest < client_tuple_list[total_client_num - finished_client_num - 1][0]:
            #     small_one = [rest, hero_id]
            #     small_heroes.append(small_one)
            #     break

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


# input the total work plan to get the detailed work
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


# input the total work plan and get the hero-client relation
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


# generate excel table
# def generate_table(file_name, list1, list2, week_num):
#     titles = 'Monday\tTuesday\tWednesday\tThursday\tFriday\t' * week_num
#
#     output = open(file_name, 'w', encoding='gbk')
#
#     output.write('Detailed work allocation for this month: \n')
#
#     output.write('\t')
#     output.write(titles)
#     output.write('\n')
#
#     for i in range(len(list1)):
#             for j in range(len(list1[i])):
#                 pass
#                 output.write(str(list1[i][j]))    #write函数不能写int类型的参数，所以使用str()转化
#                 output.write('\t')   #相当于Tab一下，换一个单元格
#             output.write('\n')       #写完一行立马换行
#
#     output.write('\n')  # 写完一行立马换行
#
#     # print the table for Hero-client relation
#     output.write('\nHero-Client relation is: \n')
#
#     for m in range(len(list2)):
#             for n in range(len(list2[m])):
#                 output.write(str(list2[m][n]))    #write函数不能写int类型的参数，所以使用str()转化
#                 output.write('\t')   #相当于Tab一下，换一个单元格
#             output.write('\n')       #写完一行立马换行
#
#     output.close()


def calculate(client_task, hero_num, week_num, day_per_week, weekday_hrs):
    filtered_client_arr = filter_client_arr(client_task, hero_num, week_num, day_per_week, weekday_hrs)
    total_work_plan = get_total_work_plan(filtered_client_arr, hero_num, week_num, day_per_week, weekday_hrs)
    
    print(total_work_plan)

    # get the work plan for each hero
    detailed_work_plan = get_full_allocation_list(total_work_plan, weekday_hrs)
    print(detailed_work_plan)

    hero_client_relation = get_hero_client_relation(total_work_plan)
    print(hero_client_relation)

    return (detailed_work_plan, hero_client_relation)



if __name__ == '__main__':
    # very good test case, since all 960 960 but in the end algo can'e solve 18 more hrs
    # client_arr = [179, 160, 150, 80, 70, 60, 50, 42, 40, 32, 28, 25, 18, 16, 10]
    # hero_num = 6
    # week_num = 4
    # days_per_week = 5
    # weekday_hrs = 8

    # too little client request

    # client_arr = [179, 160, 150, 80, 70, 62, 50, 45, 39, 32, 28, 25, 16, 10]
    # hero_num = 10
    #
    # week_num = 5
    # days_per_week = 5
    # weekday_hrs = 6
    #


    # lots of clients with only little work test case
    client_arr = [25, 22, 20, 18, 18, 18, 18, 18, 18, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 16, 10]
    # used to be no good
    hero_num = 6
    week_num = 4
    days_per_week = 5
    weekday_hrs = 8

    # allocation is good
    # hero_num = 6
    # week_num = 4
    # days_per_week = 5
    # weekday_hrs = 6


    # exceeded workload should
    # more than heroes can handle, just crop the client list to be the same as heroes
    # client_arr = [320, 190, 179, 160, 150, 80, 70, 60, 50, 42, 40, 32, 28, 25, 18, 16, 10]
    # hero_num = 6
    # week_num = 4
    # days_per_week = 5
    # weekday_hrs = 8

    # good test case, finally still have 19 hrs need to be done but no one allocated, hero6 hero7 should do the rest of them
    # client_arr = [176, 174, 143, 80, 70]
    # hero_num = 8
    # week_num = 4
    # days_per_week = 5
    # weekday_hrs = 4

    # hero_num = 6
    # week_num = 4
    # days_per_week = 5
    # weekday_hrs = 8

    file_name = 'results.xls'

    filtered_client_arr = filter_client_arr(client_arr, hero_num, week_num, days_per_week, weekday_hrs)

    total_work_plan = get_total_work_plan(filtered_client_arr, hero_num, week_num, days_per_week, weekday_hrs)
    print(total_work_plan)

    # get the work plan for each hero
    detailed_work_plan = get_full_allocation_list(total_work_plan, weekday_hrs)
    print(detailed_work_plan)

    hero_client_relation=get_hero_client_relation(total_work_plan)
    print(hero_client_relation)

    print()
    print()

    # print(calculate(client_arr, hero_num, week_num, days_per_week, weekday_hrs))

    # generate excel file
    generate_table(file_name, detailed_work_plan, hero_client_relation, week_num)