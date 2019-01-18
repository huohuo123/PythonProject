from sklearn.neighbors import KNeighborsClassifier

def main():
    X=[[0],[1],[2],[3]]
    y=[0,0,1,1]
    neigh=KNeighborsClassifier(n_neighbors=3)
    neigh.fit(X,y)


if __name__ == '__main__':
    main()