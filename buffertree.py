import math

class BufferTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.child = []
        self.buffer=[]


class BufferTree:
    def __init__(self, t):
        self.root = BufferTreeNode(True)
        self.t = t
        self.nodeswithbuffer = dict()    

    def bufferinsert(self, b):
        b = [b]
        x = self.root 
        self.nodeswithbuffer[0] = {x}
        for i in b:
            if len(x.buffer) >= 3:
                self.bufferempty(x)
                x=self.root
            x.buffer.append(i)


    # clear current node's buffer  
    # if it has child, then push down these keys in its buffer to children's buffer  
    # if it is leaf, then call insert() or delete() function to update these keys from buffer to keys.
    def bufferempty(self, x):  
        if x.child != []:
            for i in x.buffer:
                flag_be = False
                for j in range(len(x.keys)):
                    if flag_be:  break
                    if i[0] < x.keys[j][0]:  
                        if len(x.child[j].buffer) >= 3: 
                            self.bufferempty(x.child[j])
                        x.child[j].buffer.append(i)
                        flag_be = True
                        for k in self.nodeswithbuffer:
                            if x in self.nodeswithbuffer[k]:
                                if k+1 in self.nodeswithbuffer:
                                    self.nodeswithbuffer[k+1].add(x.child[j])
                                    break
                                else:
                                    self.nodeswithbuffer[k+1] = {x.child[j]}
                                    break
                    elif j == len(x.keys) - 1:
                        if len(x.child[j+1].buffer) >= 3: 
                            self.bufferempty(x.child[j+1])
                        j = len(x.keys) - 1
                        x.child[j+1].buffer.append(i)
                        flag_be = True
                        for k in self.nodeswithbuffer:
                            if x in self.nodeswithbuffer[k]:
                                if k+1 in self.nodeswithbuffer:
                                    self.nodeswithbuffer[k+1].add(x.child[j+1])
                                    break
                                else:
                                    self.nodeswithbuffer[k+1] = {x.child[j+1]}
                                    break
            x.buffer = []
            self.removefromdict(x) 
        else:
            while x.buffer != []:
                a = x.buffer.pop(0)
                if a[1] == "i":
                    self.insert((a[0],))
                elif a[1] == "d":
                    self.delete(self.root, (a[0],))
            self.removefromdict(x)


############################### insert ###############################

    # 每次插入从root开始，先检查root是否满了，若满了需要创建新的root。
    def insert(self, k):
        root = self.root
        # if len(root.keys) == (4 * self.t) - 1:
        if len(root.keys) == self.t - 1:
            temp = BufferTreeNode()
            self.root = temp
            temp.child.insert(0, root)
            self.split_child(temp, 0)
            self.insert_non_full(temp, k)
        else:
            self.insert_non_full(root, k)

    # 如果是leaf node，就插入到keys[]中相应的位置；否则向下遍历孩子结点。
    def insert_non_full(self, x, k):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append((None, None))
            while i >= 0 and k[0] < x.keys[i][0]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            while i >= 0 and k[0] < x.keys[i][0]:
                i -= 1
            i += 1
            # 如果孩子结点满了，就进行分裂。
            # if len(x.child[i].keys) == (4 * self.t) - 1:
            if len(x.child[i].keys) == self.t - 1:
                self.split_child(x, i)
                if k[0] > x.keys[i][0]:
                    i += 1
            self.insert_non_full(x.child[i], k)

    def split_child(self, x, i):
        t = self.t
        y = x.child[i]
        z = BufferTreeNode(y.leaf)
        x.child.insert(i + 1, z)

        half_idx = math.ceil(t/2.0) - 1
        x.keys.insert(i, y.keys[half_idx])
        z.keys = y.keys[half_idx + 1: t - 1]
        y.keys = y.keys[0: half_idx]
        if not y.leaf:
            z.child = y.child[half_idx + 1: t]
            y.child = y.child[0: half_idx + 1]        
        # x.keys.insert(i, y.keys[t - 1])
        # z.keys = y.keys[t: (4 * t) - 1]
        # y.keys = y.keys[0: t - 1]
        # if not y.leaf:
        #     z.child = y.child[t: 4 * t]
        #     y.child = y.child[0: t]
        return 

############################### delete ###############################

    # 每次删除从root开始
    def delete(self, x, k):
        t = self.t
        i = 0
        while i < len(x.keys) and k[0] > x.keys[i][0]:  # 寻找所在位置
            i += 1
        if x.leaf:  # 如果是leaf node，直接删除相应的key
            if i < len(x.keys) and x.keys[i][0] == k[0]:
                x.keys.pop(i)
                return x
            else:  # 这种情况说明要删的k不存在，直接return
                return x 
        else :  
            if i < len(x.keys) and x.keys[i][0] == k[0]:  # 要删除的k在非叶结点上
                self.delete_internal_node(x, k, i)
                return x
            elif len(x.child[i].keys) >= math.ceil(t/2.0):  # 该结点的key足够多
                self.delete(x.child[i], k)
            else:
                if i != 0 and i + 1 < len(x.child):
                    if len(x.child[i - 1].keys) >= math.ceil(t/2.0):
                        self.delete_sibling(x, i, i - 1)
                        self.delete(x.child[i], k)
                    elif len(x.child[i + 1].keys) >= math.ceil(t/2.0):
                        self.delete_sibling(x, i, i + 1)
                        self.delete(x.child[i], k)
                    else:
                        self.delete_merge(x, i, i + 1)
                        self.delete(x.child[i], k)
                elif i == 0:
                    if len(x.child[i + 1].keys) >= math.ceil(t/2.0):
                        self.delete_sibling(x, i, i + 1)
                        self.delete(x.child[i], k)
                    else:
                        self.delete_merge(x, i, i + 1)
                        self.delete(x.child[i], k)
                elif i + 1 == len(x.child):
                    if len(x.child[i - 1].keys) >= math.ceil(t/2.0):
                        self.delete_sibling(x, i, i - 1)
                        self.delete(x.child[i], k)
                    else:
                        self.delete_merge(x, i, i - 1)
                        self.delete(x.child[i-1], k)
                # self.delete(x.child[i], k)
            return x

    # Delete internal node
    def delete_internal_node(self, x, k, i):
        t = self.t
        if x.leaf:
            if x.keys[i][0] == k[0]:
                x.keys.pop(i)
                return
            return
        if len(x.child[i].keys) > math.ceil(t/2.0) - 1 :  
            x.keys[i] = self.delete_predecessor(x.child[i])
        elif len(x.child[i + 1].keys) > math.ceil(t/2.0) - 1 :
            x.keys[i] = self.delete_successor(x.child[i + 1])
        else:
            self.delete_merge(x, i, i + 1)
            self.delete_internal_node(x.child[i], k, math.ceil(t/2.0) - 1)
        return

    # Delete the predecessor
    def delete_predecessor(self, x):
        if x.leaf:
            return x.keys.pop()
        n = len(x.keys) - 1
        if len(x.child[n].keys) > math.ceil(self.t/2.0) -1 :
            self.delete_sibling(x, n + 1, n)
        else:
            self.delete_merge(x, n, n + 1)
        self.delete_predecessor(x.child[n])

    # Delete the successor
    def delete_successor(self, x):
        if x.leaf:
            return x.keys.pop(0)
        if len(x.child[1].keys) > math.ceil(self.t/2.0) - 1 :
            self.delete_sibling(x, 0, 1)
        else:
            self.delete_merge(x, 0, 1)
        self.delete_successor(x.child[0])

    # Delete resolution
    def delete_merge(self, x, i, j):
        cnode = x.child[i]
        if j > i:
            rsnode = x.child[j]
            cnode.keys.append(x.keys[i])  # 
            for k in range(len(rsnode.keys)):
                cnode.keys.append(rsnode.keys[k])
                if len(rsnode.child) > 0:
                    cnode.child.append(rsnode.child[k])
            if len(rsnode.child) > 0:
                cnode.child.append(rsnode.child.pop())
            for k in range(len(rsnode.buffer)):
                cnode.buffer.append(rsnode.buffer[k])
            new = cnode
            x.keys.pop(i)
            x.child.pop(j)
        else:
            lsnode = x.child[j]
            lsnode.keys.append(x.keys[j])
            for k in range(len(cnode.keys)):
                lsnode.keys.append(cnode.keys[k])
                if len(lsnode.child) > 0:
                    lsnode.child.append(cnode.child[k])
            if len(lsnode.child) > 0:
                lsnode.child.append(cnode.child.pop())
            for k in range(len(cnode.buffer)):
                lsnode.buffer.append(cnode.buffer[k])
            new = lsnode
            x.keys.pop(j)
            x.child.pop(i)
        if x == self.root and len(x.keys) == 0:
            self.root = new
            x =  new
        return x

    # 从兄弟结点借key
    def delete_sibling(self, x, i, j):
        cnode = x.child[i]
        if i < j:
            rsnode = x.child[j]
            cnode.keys.append(x.keys[i])
            x.keys[i] = rsnode.keys[0]
            if len(rsnode.child) > 0:
                cnode.child.append(rsnode.child[0])
                rsnode.child.pop(0)
            rsnode.keys.pop(0)
        else:
            lsnode = x.child[j]
            cnode.keys.insert(0, x.keys[i - 1])
            x.keys[i - 1] = lsnode.keys.pop()
            if len(lsnode.child) > 0:
                cnode.child.insert(0, lsnode.child.pop())


    def search(self, b, x):
        if (b,) in x.keys or (b,"i") in x.buffer or (b,"d") in x.buffer:
                return True
        if x.child != []:
            for i in range(len(x.keys)):
                if b < x.keys[i][0]:
                    return self.search(b, x.child[i])
                elif i == len(x.keys) - 1:
                    return self.search(b, x.child[i+1])
        return False

    # Print the tree
    def print_tree(self, x, l=0):
        print("Level_{}".format(l), ", children num is", len(x.child), ", key num is", len(x.keys), end=" : ")
        for i in x.keys:
            print(i[0], end=" ")
        print()
        l += 1
        if len(x.child) > 0:
            for i in x.child:
                self.print_tree(i, l)
        return
    
    def inorder(self,x, topr):
        if not x.leaf:
            for i in range(len(x.child)):
                self.inorder(x.child[i], topr)
                if i < len(x.keys):
                    topr.append(x.keys[i][0])#, end=", ")
        else:
            for k in x.keys:
                topr.append(k[0])#, end=", ")

        return
    
    def emptyallbuffers(self):
        while not self.checkifbufferempty():
            for i in self.nodeswithbuffer.copy():
                for j in self.nodeswithbuffer[i].copy():
                    self.bufferempty(j)
                    # self.nodeswithbuffer[i].remove(j)

    def checkifbufferempty(self):
        for i in self.nodeswithbuffer:
            for j in self.nodeswithbuffer[i]:
                if j.buffer != []:
                    return False
        return True

    def removefromdict(self, x):
        for ii in self.nodeswithbuffer.copy():
            for jj in self.nodeswithbuffer[ii].copy():
                if jj == x:
                    self.nodeswithbuffer[ii].remove(jj)    
                    return         






