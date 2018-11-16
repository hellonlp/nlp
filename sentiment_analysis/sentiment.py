# -*- coding: utf-8 -*-
"""
Created on Thu Jun  17 12:33:42 2018
@author: cm
"""


import os
import re
import jieba
import numpy as np



pwd = os.path.dirname(os.path.abspath(__file__))
jieba.load_userdict( os.path.join(pwd, 'dict','jieba_sentiment.txt'))



def cut_sentence(text):
    patterns = "。|；|！|!|？|\?|\t|\n"
    sentences = filter(None, re.split(patterns, text))
    return [l for l in sentences]


# 打开词典文件，返回列表
def load_dict(Dict):
    f = os.path.join(pwd, 'dict', Dict)
    with open(f, 'r', encoding='utf-8') ad fp:
        lines = fp.readlines()
    dictionary = [word.strip() for word in lines]
    return set(dictionary)
   
   
# 加载词典
deny_word = load_dict(Dict='not.txt')
posdict = load_dict(Dict='positive.txt')
negdict = load_dict(Dict = 'negative.txt')
pos_neg_dict = posdict|negdict
# 程度级别词语
mostdict = load_dict(Dict='most.txt')
verydict = load_dict(Dict='very.txt')
moredict = load_dict(Dict='more.txt')
ishdict = load_dict(Dict='ish.txt')
insufficientlydict = load_dict(Dict='insufficiently.txt')
overdict = load_dict(Dict='over.txt')
inversedict = load_dict(Dict='inverse.txt')


def is_odd(num):
    if num % 2 == 0:
        return 'even'
    else:
        return 'odd'
        
def sentiment_score_list(dataset):
    seg_sentence=cut_sentence(dataset)
    count1 = []
    count2 = []
    for sen in seg_sentence: # 循环遍历每一个评论
        segtmp = jieba.lcut(sen, cut_all=False) # 把句子进行分词，以列表的形式返回             
        i = 0 #记录扫描到的词的位置
        a = 0 #记录情感词的位置
        poscount = 0 # 积极词的第一次分值
        poscount2 = 0 # 积极反转后的分值
        poscount3 = 0 # 积极词的最后分值（包括叹号的分值）
        negcount = 0
        negcount2 = 0
        negcount3 = 0
        for word in segtmp:
            if word in posdict: # 判断词语是否是情感词
                poscount +=1
                c = 0
                for w in segtmp[a:i]: # 扫描情感词前的程度词
                    if w in mostdict:
                        poscount *= 4
                    elif w in verydict:
                        poscount *= 3 
                    elif w in moredict:
                        poscount *= 2 
                    elif w in ishdict:
                        poscount *= 0.5#
                    elif w in insufficientlydict:
                        poscount *= -0.3 #-0.3
                    elif w in overdict:
                        poscount *= -0.5#-0.5
                    elif w in inversedict: 
                        c+= 1
                    else:
                        poscount *= 1
                if is_odd(c) == 'odd': # 扫描情感词前的否定词数
                    poscount *= -1.0
                    poscount2 += poscount
                    poscount = 0
                    poscount3 = poscount + poscount2 + poscount3
                    poscount2 = 0
                else:
                    poscount3 = poscount + poscount2 + poscount3
                    poscount = 0
                a = i+1
            elif word in negdict: # 消极情感的分析，与上面一致
                negcount += 1
                d = 0
                for w in segtmp[a:i]:
                    if w in mostdict:
                        negcount *= 4
                    elif w in verydict:
                        negcount *= 3
                    elif w in moredict:
                        negcount *= 2
                    elif w in ishdict:
                        negcount *= 0.5
                    elif w in insufficientlydict:
                        negcount *= -0.3#-0.3
                    elif w in overdict:
                        negcount *= -0.5#-0.5
                    elif w in inversedict:
                        d += 1
                    else:
                        negcount *= 1
                if is_odd(d) == 'odd':
                    negcount *= -1.0
                    negcount2 += negcount
                    negcount = 0
                    negcount3 = negcount + negcount2 + negcount3
                    negcount2 = 0
                else:
                    negcount3 = negcount + negcount2 + negcount3
                    negcount = 0
                a = i + 1         
            elif word == '！' or word == '!':# or  word == '?' or word == '？' : # 判断句子是否有感叹号
                for w2 in segtmp[::-1]: # 扫描感叹号前的情感词，发现后权值+2，然后退出循环
                    if w2 in posdict or negdict:
                        poscount3 += 2
                        negcount3 += 2
                        break
            elif  word == '?' or word == '？' : # 判断句子是否有问好
                for w2 in segtmp[::-1]: # 有问号情感值为负
                        poscount3 =  0
                        negcount3 =  2#1
             
            i += 1
            pos_count = poscount3
            neg_count = negcount3
            count1.append([pos_count,neg_count])
        count2.append(count1)
        count1=[]
    return count2


def score(s):
    senti_score_list = sentiment_score_list(s)
    negatives=[]
    positives=[]
    for review in senti_score_list:
        score_array =  np.array(review)
        AvgPos = np.sum(score_array[:,0])
        AvgNeg = np.sum(score_array[:,1])        
        negatives.append(AvgNeg)
        positives.append(AvgPos)   
    pos_score = np.mean(positives) 
    neg_score = np.mean(negatives)
    if pos_score >=0 and  neg_score<=0:
        pos_score = pos_score
        neg_score = abs(neg_score)
    elif pos_score >=0 and  neg_score>=0:
        pos_score = pos_score
        neg_score = neg_score    
    return pos_score,neg_score


def norm_score(sent):
    score1,score0 = score(sent)
    if score1 > 4 and score0 > 4:
        if score1 >= score0:
            _score1 = 1
            _score0 = score0/score1    
        elif score1 < score0:
            _score0 = 1
            _score1 = score1/score0  
    else :
        if score1 >= 4 :
            _score1 = 1
        elif score1 < 4 :
            _score1 = score1/4
        if score0 >= 4 :
            _score0 = 1
        elif score0 < 4 :
            _score0 = score0/4 
    #return (_score1-_score0+1)/2
    return _score1,_score0
        


def final(sent):
    score1,score0 = norm_score(sent)
    if score1 == score0:
        result = 0
    elif score1 > score0:
        result = 1
    elif score1 < score0:
        result = -1
    return result
    
    
    
if __name__ =='__main__':
    text = '我爱武汉'
    text = '好讨厌'
    text = '好喜欢'
    text = '我真的好讨厌你'
    text = '真伤心'
    text = '越南共产党对于中国共产党做出的一些行为表示这是背信弃义的行为'
    text = '真不错'
    text = '实在是无语'
    text = '连招待所都不如'
    text = '性价比不高'
    text = '花园式的酒店，在城中，有点旧，但靠花园的房间不错！'
    text = '不值房价，早餐太糟，也许我去的比较晚，九点左右，没东西吃'
    text = '我9号入住行政层（28楼），设施还好，服务不错，但电梯太老了。'
    text = '酒店门口时条单行道，外出有些不方便！其他还行'
    text = '其他还行'
    text = '外出有些不方便！'
    text = '很牛。'
    text = '我不同意这位小姐的说法'
    text = '热情奔放，创意无限，燃气了我心中的一把火'
    text = '真不知道该说什么好'
    text = '没什么意思'
    text = '哎哟喂'
    text = '这个系统简直太垃圾了'
    text = '越南共产党对于中国共产党做出的一些行为表示这是背信弃义的行为'
    text = '实在是无语'
    text = '我不是很喜欢你'
    text = '我很酷'
    text = '我太酷'
    text = '我太牛了'
    text = '你太牛了'
    text = '真的超级不爽'
    text = '看错你了'
    text = '没看错你了'
    print(final(text))


        
