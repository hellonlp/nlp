# 一、引言
目前情感分析主要分为三个方向，第一个是由情感词典和句法结构来做的、第二个是根据机器学习来做的、第三个是用深度学习的方法来做的（例如LSTM、CNN、LSTM+CNN、BERT+CNN等）。三种方法中，第一种和第三种在不同的情况下使用，第二种方法现在的位置有点尴尬。
本片文章主要介绍下如何使用情感字典来做情感分析。

# 二、情感字典
出来分词词典和停用词词典外，一共还包含9个词典：
1、否定词：not.txt
2、正面情感词：positive.txt
3、负面情感词：negative.txt
4、程度副词：
1) most.txt
2) very.txt
3) more.txt
4) ish.txt
5) insufficiently.txt
6) over.txt
7) inverse.txt

# 三、算法流程设计
一共有8个步骤：
第一步：读取评论数据，对评论进行分句（分句主要以特定的标点符号为主）。
第二步：将结巴词典和所有情感词典做并集，得出新的切词用地结巴词典。
第三步：查找对分句的情感词，记录正面还是负面，以及位置。
第四步：往情感词前查找程度词，找到就停止搜寻。为程度词设权值，乘以情感值。
第五步：往情感词前查找否定词，找完全部否定词，若数量为奇数，乘以-1，若为偶数， 乘以 1。
第六步：找出感叹号和问好等重要标点符合

判断分句结尾是否有感叹号，有叹号则往前寻找情感词，有则相应的情感值+2。
判断分句结尾是否有问好，有问号该句判断为负面值+2。
第七步：计算完一条评论所有分句的情感值（[正面分值, 负面分值]），用数组（list） 记录起来。
第八步：计算每条评论中每一个分句的的正面情感均值与负面情感均值，然后比较正面情感总和与负面情感总和，较大的一个即为所得情感倾向。

# 四、举例分析
例子：“我特别喜欢武汉这个城市！因为武汉有非常多好看的景点。但是，我不喜欢武汉的天气，因为武汉的天气有点差，热的时候让人感觉不爽。”

1、 情感词分为 2 种， 一种是正面的，另外一种是负面的。
要分析一句话是正面的还是负面的，首先需要找出句子里面的情感词，然后再找出程度副词和否定词等。
正面的情感词比如：好，孝顺，高性能，一心一意等。 负面情感词比如：差，郁闷，小心眼，一毛不拔等。 出现一个积极词就+1，出现一个消极词就-1。 在这句话里面，有“好看”和“喜欢”两个正面情感词，“差”和“不爽”两个负面情感词。
2、 情感词 “喜欢”、“好看”和‘差“前面都有一个程度副词。”极好“就比”较好“和”好“的情感更强烈，”太差“也比”有点差“情感强一些。 所以需要在找到情感词后往前找一下有没有程度副词，在这里不同的程度副词有不同的权重。 程度词我们分为 6 种，分别为：most，very，more，ish，insufficient 和 over 通过测试计算，给上面 6 种情感词的打分分别为 4，3，2，0.5，-0.3 和-0.5。
3、 ” 我特别喜欢武汉这个城市“后面有感叹号，叹号意味着情感强烈。因此发现叹号可以为情 感值+2.
4、 否定词 在找到情感词的时候，需要往前找否定词。比如”不“，”不能“这些词。而且还要数这些否 定词出现的次数，如果是单数，情感分值就*-1，但如果是偶数，那情感就没有反转，还 是1。在这句话里面，可以看出”喜欢“前面只有一个”不“，所以”喜欢“的情感值应该反 转，-1。
5、 正面和负面需要分别独立计算，很明显就可以看出，这句话里面有褒有贬，不能用一个分值来表示它的情感倾 向。而且这个权值的设置也会影响最终的情感分值，敏感度太高了。因此对这句话的最终的正确的处理，是得出这句话的一个正面分值，一个负面分值（这样消极分值也是正数， 无需使用负数了）。
6、 以分句的情感为基础，加权求和，从而得到一条评论的情感分值。

这条例子评论有五个分句， 因此其结构如下（[正面分值, 负面分值]）： 下面是对每个分句的打分: [正面分值, 负面分值]
① 我 特别 喜欢 武汉这个城市 ！ [正面分值, 负面分值] : [3x1+2,0]
② 因为武汉有 非常 多 好看 的景点。 [正面分值, 负面分值] : [4x1,0]
③ 但是， [正面分值, 负面分值] : [0,0]
④ 我 不 喜欢 武汉的天气， [正面分值, 负面分值] : [-1x1,0]
⑤ 因为武汉的天气 有点 差， [正面分值, 负面分值] : [0,0.5x1]
⑥ 热的时候让人感觉 不爽。 [正面分值, 负面分值] : [0,1]

最后，这句话的得分为： [31+2,0] + [41,0] + [0,0] + [-11,0] + [0,0.51] + [0,1] = [8,1.5]，即为： [正面分值, 负面分值] = [8,1.5]。
因为 8>1.5，所以整句话的情感判断为正面。

# 五、总结
如果我们仅仅使用情感词典的方法，准确率可以达到 73%左右。这种比较通用，不需要训练，对于不同类型的数据都可以进行情感分析。唯一的缺点就是准确率不是非常高。