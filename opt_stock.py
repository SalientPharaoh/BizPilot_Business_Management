
def process(W,n,a,z=0):
    for i in a:
        z+=i[0]
    g=W//z 
    #print(f"Each item quantity bought is:{W//z}")
    W-=int((W//z)*z)
    m=[[0 for i in range(W+1)] for j in range(n+1)]
    w=[]
    v=[]
    for i in a:
        w.append(i[0])
    w.sort()
    for i in w:
        for j in a:
            if i==j[0]:
                v.append(j[1])
    def knapsack(w, v, W, n):
        for i in range(1,n+1):
            for j in range(1,W+1):
                if w[i-1] <= j:
                    m[i][j] = max(v[i-1] + m[i-1][j-w[i-1]],m[i-1][j])
                elif w[i-1] > j:
                    m[i][j] = m[i-1][j]
    o=[]
    def pat():
        a=n
        b=W
        while(a!=0):
            if m[a][b]!=m[a-1][b]:
                o.append(a)
                b-=w[a-1]
            a-=1 
    knapsack(w,v,W,4)
    #print(m[n][W])
    pat()
    r=[]

    for i in range(n):
        r.append(g)
    for i in range(n):
        for j in o:
            if i==j-1:
                r[i]+=1
    for i in range(n):
        print(f"Quantity for item {a[i][2]}  :  {r[i]}")