# 类型特征转换之1-of-k(哑编码）
# *************************************************************************
# 定性：博主很胖 博主很瘦
# 定量：博主有 80kg 博主有 60kg（ps：好难啊）
# 一般定性都会有相关的描述词，定量的描述都是可以用数字来量化处理
# 现在假设给你的一个病人的病情描述，一般病情的描述包含以下几个方面，将病情严重程度划分：
# 非常严重，严重，一般严重，轻微
# 现在有个病人过来了，要为他构造一个病情的特征，假设他的病情是严重情况，我们可以给他的哑编码是
# 0 1 0 0

# 文本数据抽取的方式：词袋法；TF-IDF
# *************************************************************************