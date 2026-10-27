#include<iostream>
using namespace std;
#define imax=500
int main(){
    int n;
    cin>>n;
    int arr[500][500];
    int i=0,j=0;
    for(i=0;i<n;i++){
        for(j=0;j<n;j++){
            cin>>arr[i][j];
        }
    }

    bool flag=0;//zuo bian wei 0
    int left=0;
    int right=0;

    if(n==1){
        cout<<arr[0][0];
        return 0;
    }

    cout<<arr[0][0]<<" ";

    for(j=1;j<n;j++){
            if(flag==0){
                flag=1;
                left=0;
                right=j;
                while(left>=0&&right>=0){
                    cout<<arr[left][right]<<" ";
                    left++;
                    right--;
                }
                continue;
            }
            if(flag==1){
                flag=0;
                left=j;
                right=0;
                  while(left>=0&&right>=0){
                    cout<<arr[left][right]<<" ";
                    left--;
                    right++;
                  }
                continue;
            }
    }


        if(n%2==0){
        flag=0;//n-1 zai zuo
        for(i=1;i<n-1;i++){
            if(flag==0){
                flag=1;
                left=n-1;
                right=i;
                while(left>=i&&right>=i){
                    cout<<arr[left][right]<<" ";
                    left--;
                    right++;
                }
                continue;
            }
            if(flag==1){
                  flag=0;
                left=i;
                right=n-1;
                while(left>=i&&right>=i){
                    cout<<arr[left][right]<<" ";
                    left++;
                    right--;
                }
                continue;
            }
        }
        }
        if(n%2==1){
            flag=1;
            for(i=1;i<n-1;i++){
            if(flag==0){
                flag=1;
                left=n-1;
                right=i;
                while(left>=i&&right>=i){
                    cout<<arr[left][right]<<" ";
                    left--;
                    right++;
                }
                continue;
            }
            if(flag==1){
                  flag=0;
                left=i;
                right=n-1;
                while(left>=i&&right>=i){
                    cout<<arr[left][right]<<" ";
                    left++;
                    right--;
                }
                continue;
            }
        }
        }
        cout<<arr[n-1][n-1]<<" ";
    return 0;
}
