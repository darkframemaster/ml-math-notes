#include<iostream>
#define imax 1000
using namespace std;
void input(int n,int m,int arr[imax][imax]){
    int i=0,j=0;
    for(i=0;i<n;i++){
        for(j=0;j<m;j++){
            cin>>arr[i][j];
        }
    }
}
void output(int n,int m,int arr[imax][imax]){
    int i=0,j=0;
    for(i=m;i>0;i--){
        for(j=0;j<n;j++){
            cout<<arr[j][i-1]<<" ";
        }
        cout<<endl;
    }
}
int main(){
    int n=0,m=0;
    cin>>n>>m;
    int arr[imax][imax];
    input(n,m,arr);
    output(n,m,arr);
    return 0;
}
