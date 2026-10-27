#include<iostream>
using namespace std;
#define begin_year 1850
#define begin_day_date 2

int first_day_month(int year,int month){
        bool runyear;
        int i=0;
        int days=0;
        int firstdate_ofthis_year=0;
        for(i=begin_year;i<year;i++){
            if(i==2000||(i%4==0&&i%100!=0)){
                days+=366;
            }
            else{
                days+=365;
            }
        }
          if(year==2000||(year%4==0&&year%100!=0)){
                runyear=true;
       }
       else{
                runyear=false;
       }
        for(i=1;i<month;i++){
            if(i==1||i==3||i==5||i==7||i==8||i==10||i==12){
                days+=31;
            }
            else if(i==2&&runyear==true){
                days+=29;
            }
            else if(i==2&&runyear==false){
                days+=28;
            }
            else{
                days+=30;
            }
        }
        firstdate_ofthis_year=(days+2)%7;
        if(firstdate_ofthis_year==0){
            firstdate_ofthis_year=7;
        }
        return firstdate_ofthis_year;
}
void output(int year,int month,int number,int date,int first_date){
    int answer=0;
    if(date==first_date){
        answer=(number-1)*7+1;
    }
    else{
        if(date>first_date){
            answer=date-first_date+(number-1)*7+1;
        }
        if(date<first_date){
            answer=7-first_date+date+(number-1)*7+1;
        }
    }
    //cout<<first_date<<" "<<answer<<endl;
    bool runyear;
       if(year==2000||(year%4==0&&year%100!=0)){
                runyear=true;
       }
       else{
                runyear=false;
       }
  //     cout<<runyear<<endl;
       if(month==1||month==3||month==5||month==7||month==8||month==10||month==12){
                if(answer>31){
                    cout<<"none";
                    return;
                }
       }
        else if(month==2&&runyear==true){
                if(answer>29){
                    cout<<"none";
                    return;
                }
        }
        else if(month==2&&runyear==false){
                if(answer>28){
                    cout<<"none";
                    return;
                }
        }
        else{
            if(answer>30){
                cout<<"none";
                return;
            }
        }

        if(month<10){
            if(answer<10){
                cout<<year<<'/'<<0<<month<<'/'<<0<<answer;
            }
            else
                cout<<year<<'/'<<0<<month<<'/'<<answer;
        }
        else{
              if(answer<10){
                cout<<year<<'/'<<month<<'/'<<0<<answer;
            }
            else
                cout<<year<<'/'<<month<<'/'<<answer;
        }
}
int main(){
    int a;//month
    int b;//
    int c;//date
    cin>>a>>b>>c;
    int year_one;
    int year_two;
    cin>>year_one>>year_two;
    int temp;
    if(year_two<year_one){
        temp=year_one;
        year_one=year_two;
        year_two=temp;
    }
    int year_one_date=first_day_month(year_one, a);
    int year_two_date=first_day_month(year_two, a);



    output(year_one,a,b,c,year_one_date);
    cout<<endl;
    output(year_two,a,b,c,year_two_date);

    return 0;
}
