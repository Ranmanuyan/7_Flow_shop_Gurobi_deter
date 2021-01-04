# -*- coding: utf-8 -*-
# @Author: Lei Liu
# @Date:   2020-09-19 15:54:57
# @Last Modified by:   Lei Liu
# @Last Modified time: 2020-09-19 16:13:03



# Location to schedule

def schedule(var_list):

	num_job =3

	location =[]

	for i in range(len(var_list)):
		if(var_list[i] == 1):
			location.append(i%num_job)

	schedule_list =[]
	schedule_list= location_schedule(location)


	print (schedule_list)

	return schedule_list





def location_schedule(location):




	temp =[]
	for i in range (len(location)):
		temp.append(0)


	for i in range (len(location)):
		temp[location[i]]=i


	# print (temp)


	return temp



if __name__ == '__main__':
	var_list =[0,1,0,1,0,0,0,0,1]
	schedule(var_list)