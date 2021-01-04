# -*- coding: utf-8 -*-
# @Author: Lei Liu
# @Date:   2020-08-25 15:54:17
# @Last Modified by:   Lei Liu
# @Last Modified time: 2020-08-26 15:45:21

#  have a known schedule, calculate its obj, such as total completion time.
#  no disjunctive constraints




num_job = 6
num_machine= 5 
process_T= [
             [63, 23, 69, 36, 30, 10],
             [34, 9, 46, 13, 19, 26],
             [5, 21, 29, 40, 10, 70],
             [0, 0,  0, 0, 0,  0],
             [0, 0,  0, 0, 0,  0]
             ]
# schedule = [5,0,3,4,2,1]
schedule = [3,5,0,4,2,1]


def calTotal_C():
	start = []
	completion = []
	totalC =0
	

	for i in range(len(schedule)):
		start1 = []
		completion1 = []
		
		if(i==0):
			for j in range(num_machine):
				if(j==0):
					start1.append(0)
					completion1.append(start1[j]+process_T[j][schedule[i]])
				else:
					start1.append(completion1[j-1])
					completion1.append(start1[j]+process_T[j][schedule[i]])
		else:
			for j in range(num_machine):
				if(j==0):
					start1.append(completion[i-1][j])
					completion1.append(start1[j]+process_T[j][schedule[i]])
				else:
					start1.append(max(completion[i-1][j], completion1[j-1]))
					completion1.append(start1[j]+process_T[j][schedule[i]])

		start.append(start1)
		completion.append(completion1)

	print(start)
	print('-------------------------------')
	print(completion)

	for i in range(len(schedule)):
		totalC += completion[i][num_machine-1]

	print('total completion time is : ', totalC)




if __name__ == '__main__':
	calTotal_C()

