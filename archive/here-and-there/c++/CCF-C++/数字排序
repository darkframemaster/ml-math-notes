#include<iostream>
#include<queue>
using namespace std;
#define N 1000
void input(int n,int* arr){
    int i=0;
    for(i=0;i<n;i++){
        cin>>arr[i];
    }
}
void output(int n,int* arr){
    int icount=1;
    int i=0,j=0;
    int arr2[N];

    for(i=0;i<n;i++){
        for(j=i+1;j<n;j++){
            if(arr[i]==arr[j]){
                icount++;
                arr[j]=-1;
                arr2[j]=-1;
            }
        }
        arr2[i]=icount;
        icount=1;
    }
    int temp=0;
    for(i=0;i<n;i++){
            for(j=i;j<n;j++){
                   if(arr2[i]<arr2[j]&&arr2[i]!=-1&&arr2[j]!=-1){
                        temp=arr2[i];
                        arr2[i]=arr2[j];
                        arr2[j]=temp;
                        temp=arr[i];
                        arr[i]=arr[j];
                        arr[j]=temp;
                   }
                   if(arr2[i]==arr2[j]&&arr2[i]!=-1&&arr2[j]!=-1&&arr[i]>arr[j]){
                        temp=arr2[i];
                        arr2[i]=arr2[j];
                        arr2[j]=temp;
                        temp=arr[i];
                        arr[i]=arr[j];
                        arr[j]=temp;
                   }
            }
    }

    for(i=0;i<n;i++){
        if(arr[i]!=-1){
            cout<<arr[i]<<" "<<arr2[i]<<endl;
        }
    }
}
int main(){
    int n;
    int arr[N];
    cin>>n;
    input(n,arr);
    output(n,arr);
    return 0;
}
