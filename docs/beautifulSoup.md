#### https://cuiqingcai.com/1319.html

#### Beautiful 解析 html 页面
```
res = requests.get(url)
res.encoding = 'gb18030'
soup = BeautifulSoup(res.text, 'html.parser')
Beautiful Soup将复杂HTML文档转换成一个复杂的树形结构,每个节点都是Python对象,所有对象可以归纳为4种:
1. Tag
2. NavigableString 用于获取标签里面的内容
3. BeautifulSoup BeautifulSoup 对象表示的是一个文档的全部内容.大部分时候,可以把它当作 Tag 对象，是一个特殊的 Tag，我们可以分别获取它的类型，名称，以及属性
4. Comment 是一个特殊类型的 NavigableString 对象
```

#### Tag 对象
```
通俗点讲就是 HTML 中的一个个标签,对于 Tag
soup.p.get('class')
它有两个重要的属性，是 name 和 attrs
取值 class = "el" 标签的对象
soup.find(name='div', attrs={'class': 'dw_page'})
```

#### beautifulSoup class 精确匹配问题
```
在BS中, class属于多值属性, 它的值存储在list中 {'class': ['navi']} ，
在匹配class的时候, 它使用的逻辑是 A in B, 所以就会出现模糊匹配的情况，
可以使用 lambda 表达式进行过滤 soup.find_all(lambda tag: tag.name=='div' and tag.get('class')==['el'])
```

#### find_all( name , attrs , recursive , text , **kwargs )
```
find_all() 方法搜索当前 tag 的所有 tag 子节点,并判断是否符合过滤器的条件
1）name 参数
name 参数可以查找所有名字为 name 的tag,字符串对象会被自动忽略掉

```
#### text 参数
```
通过 text 参数可以搜搜文档中的字符串内容.与 name 参数的可选值一样, text 参数接受字符串 , 正则表达式 , 列表, True
soup.find_all(text="Elsie")
```
#### recursive 参数
```
调用tag的 find_all() 方法时,Beautiful Soup会检索当前tag的所有子孙节点,如果只想搜索tag的直接子节点,可以使用参数 recursive=False
```

#### select 用法
```
组合查找
组合查找即和写 class 文件时，标签名与类名、id名进行的组合原理是一样的，例如查找 p 标签中，id 等于 link1的内容，二者需要用空格分开
print soup.select('p #link1')

直接子标签查找
print soup.select("head > title")
```

#### beautiful 要点
```
.contents
tag 的 .content 属性可以将tag的子节点以列表的方式输出 soup.head.contents 输出方式为列表，我们可以用列表索引来获取它的某一个元素 soup.head.contents[0]

.children
它返回的不是一个 list，不过我们可以通过遍历获取所有子节点

.descendants
.contents 和 .children 属性仅包含tag的直接子节点，.descendants 属性可以对所有tag的子孙节点进行递归循环，和 children类似
for child in soup.descendants:
    print child

.string 属性
如果tag只有一个 NavigableString 类型子节点,那么这个tag可以使用 .string 得到子节点。如果一个tag仅有一个子节点,那么这个tag也可以使用 .string 方法,输出结果与当前唯一子节点的 .string 结果相同
也就是如果一个标签里面没有标签了，那么 .string 就会返回标签里面的内容。如果标签里面只有唯一的一个标签了，那么 .string 也会返回最里面的内容
print soup.head.string

.strings
获取多个内容，不过需要遍历获取
for string in soup.strings:
    print(repr(string))

.stripped_strings 
输出的字符串中可能包含了很多空格或空行,使用 .stripped_strings 可以去除多余空白内容

.parent 属性
获取父节点

.parents 属性
通过元素的 .parents 属性可以递归得到元素的所有父辈节点

.next_sibling  .previous_sibling 属性
.next_sibling 属性获取了该节点的下一个兄弟节点，.previous_sibling 则与之相反，如果节点不存在，则返回 None
注意：实际文档中的tag的 .next_sibling 和 .previous_sibling 属性通常是字符串或空白，因为空白或者换行也可以被视作一个节点，所以得到的结果可能是空白或者换行


```

