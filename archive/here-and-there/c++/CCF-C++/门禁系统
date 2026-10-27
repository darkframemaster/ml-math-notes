#include<iostream>
using namespace std;

int main(){
    int n=0;
    cin>>n;
    int* arr=new int[n];
    for(int i=0;i<n;i++){
            cin>>arr[i];
    }

    int icount=0;
    for(int i=0;i<n;i++){
        for(int j=i;j>=0;j--){
            if(arr[i]==arr[j]){
                icount++;
            }
            if(j==0){
                cout<<icount<<" ";
            }
        }
        icount=0;
    }
    return 0;
}
