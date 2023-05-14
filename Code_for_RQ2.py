import pandas as pd
from compare_name import comparing
import csv

input_data = pd.read_csv("data/different_author_information.csv")

author_information = []
author_comparision_result = []

only_dauthor_list = [] #only_dauthor_list存储的是那些名字只在data paper中出现的作者的信息

for i in range(1,1566):
    ddoi = input_data.iloc[i, 0]  # ddoi是data paper的doi
    rdoi = input_data.iloc[i,1] #rdoi是research paper的doi,这一段是比较research paper中出现的每一位作者在data paper中获得了什么样的排位
    dauthor = input_data.iloc[i,2]
    rauthor = input_data.iloc[i,3]
    subject = input_data.iloc[i,7]

    DPaperNumber = input_data.iloc[i,4]
    RPaperNumber = input_data.iloc[i, 5]

    m = dauthor[2:(len(dauthor)) - 2]  # 输入的是字符串形式的列表，以下几行的目的是把字符串形式的列表数据转换回字符串
    dauthor_list = m.split("', '") #dauthor_list 是每一篇data paper的作者的名字组成的list
    n = rauthor[2:(len(rauthor)) - 2]  # 输入的是字符串形式的列表，以下几行的目的是把字符串形式的列表数据转换回字符串
    rauthor_list = n.split("', '") #rauthor_list 是每一篇research paper的作者的名字组成的list

    for rranking in range(0, len(rauthor_list)):
        for dranking in range(0, len(dauthor_list)):
            if comparing(rauthor_list[rranking],dauthor_list[dranking]):
                ranking_difference = rranking - dranking
                author_comparision_result.append([rdoi,ddoi,rauthor_list[rranking],
                                                  rranking + 1, dranking + 1, ranking_difference,
                                                  RPaperNumber,DPaperNumber,subject])
                break

    for dranking in range(0, len(dauthor_list)):
        find_the_author = 0
        for rranking in range(0, len(rauthor_list)):
            if comparing(dauthor_list[dranking],rauthor_list[rranking]):
                find_the_author += 1
                break
        if find_the_author == 0:
            only_dauthor_list.append([ddoi,dauthor_list[dranking],dranking + 1,subject])



file = open("data/ResearchPaper_Comparing_DataPaper.csv", 'a+', encoding='utf-8-sig', newline='')
csv_writer = csv.writer(file) #这一部分提取的是每一篇文章的作者全名
for item in author_comparision_result:
    csv_writer.writerow(item)
file.close()

file = open("data/Only_DataPaper_Author.csv", 'a+', encoding='utf-8-sig', newline='')
csv_writer = csv.writer(file) #这一部分提取的是每一篇文章的作者全名
for item in only_dauthor_list:
    csv_writer.writerow(item)
file.close()

total_author_number = len(author_comparision_result) #在ResearchPaper中出现的作者的总人次
Dpaper_higher = 0 #记录在DataPaper中获得更高排位的作者的数量
Dpaper_same = 0 #记录在DataPaper中获得同ResearchPaper相同排位的作者的数量
Ranking_list = ["a","b","c","d","l"]

author_ranking_change = []

for item in author_comparision_result:
    if item[5] > 0:
        Dpaper_higher += 1
    elif item[5] == 0:
        Dpaper_same += 1

    if item[3] == 1:
        Rlevel = "a"
    elif item[3] == item[6]:
        Rlevel = "l"
    else:
        middle_author_number = item[6] - 2
        if item[3] - 1<= middle_author_number//3 :
            Rlevel = "b"
        elif item[3] - 1<= middle_author_number*2//3:
            Rlevel = "c"
        else:
            Rlevel = "d"

    if item[4] == 1:
        Dlevel = "a"
    elif item[4] == item[7]:
        Dlevel = "l"
    else:
        middle_author_number = item[7] - 2
        if item[4] - 1<= middle_author_number//3 :
            Dlevel = "b"
        elif item[4] - 1<= middle_author_number*2//3:
            Dlevel = "c"
        else:
            Dlevel = "d"

    author_ranking_change.append([item[2],item[3],item[4],Rlevel,Dlevel,item[6],item[7],item[8]])

file = open("data/Author_Ranking_Change.csv", 'a+', encoding='utf-8-sig', newline='')
csv_writer = csv.writer(file) #这一部分提取的是每一篇文章的作者全名
for item in author_ranking_change:
    csv_writer.writerow(item)
file.close()

final_output = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]] #计算作者在Dpaper和Rpaper中，落在哪个顺序区间
for item in author_ranking_change:
    for i in range(len(Ranking_list)):
        for j in range(len(Ranking_list)):
            if item[3] == Ranking_list[i] and item[4] == Ranking_list[j]:
                final_output[i][j] += 1

print(final_output)

rp_credit_change = [0.0,0.0,0.0,0.0,0.0]

sum = [0,0,0,0,0]
for i in range(len(Ranking_list)):
    for j in range(len(Ranking_list)):
        sum[i] = sum[i] + final_output[i][j]

print(sum)

def calculate_credit(ranking,total_number): #Proportional   credit-assignment   schemas   (Credit03).Because  the  equal  credit-assignment  schemas  do  not  takecoauthor position into account, Van Hooydonk (1997) pro-posed a proportional schema to credit coauthors.
    # credits = 2*(1-ranking/(total_number+1))/total_number
    if total_number > 60:
        total_number = 60
    credits = (2**(total_number-ranking))/(2**total_number - 1)
    return credits

for item in author_ranking_change:
    for i in range(len(Ranking_list)):
        for j in range(len(Ranking_list)):
            if item[3] == Ranking_list[i] and item[4] == Ranking_list[j]:
                credits_difference= calculate_credit(item[2],item[6]) - calculate_credit(item[1],item[5])
                rp_credit_change[i] += credits_difference

print(rp_credit_change)

average_credit_change = [0.0,0.0,0.0,0.0,0.0]

for i in range(len(Ranking_list)):
    average_credit_change[i] = rp_credit_change[i]/sum[i]

print(average_credit_change)
