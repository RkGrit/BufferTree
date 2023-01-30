from buffertree import *

def main():
    B = BufferTree(8)
    
    # 插入操作写入到buffer
    array = [8, 9, 10, 11, 15, 16, 17, 18, 19, 20, 21, 1, 7, 5, 3, 6, 2, 4, 14, 12, 13]
    for i in array:
        B.bufferinsert((i, "i"))
    print("After write insert operators into buffers, the tree looks like:")
    B.print_tree(B.root)
    print()
    
    # 清空buffer
    B.emptyallbuffers()
    print("After emptying all buffers, the tree looks like:")
    B.print_tree(B.root)
    print()
    
    # 查询        
    print("key 4   in BufferTree:", B.search(4,B.root))
    print("key 4.5 in BufferTree:", B.search(4.5,B.root))
    print()

    # 顺序输出        
    sorted_array = []
    B.inorder(B.root, sorted_array)
    print("keys in sort are:",sorted_array)
    print()
    
    # 删除操作写入buffer
    array = [8, 9, 10, 11, 15, 16, 17, 18, 19, 20, 21, 1, 7, 5, 3, 6, 2, 4, 14, 12, 13]
    for i in array:
        B.bufferinsert((i, "d"))
    B.emptyallbuffers()
    print("After deletion, the tree looks like:")
    B.print_tree(B.root)
    print()
    
    print("key 4 in BufferTree:", B.search(4,B.root))    

if __name__ == "__main__":
     main()