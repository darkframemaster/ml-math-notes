#include<stdio.h>
#include<time.h>

#define CLOCK_PER_SEC ((clock_t)1000)


int find_sub_str(char* father, char* son){
	printf("substring:  ");
	for( ;*father != '\0'; father++){
		char* tmp = son;
		for(;*father==*tmp && *father != '\0' ;){
			printf("%c",*father);
			if(*tmp=='\0'){
				return 1;	
			}
			father++;
			tmp++;
		}		
	}
	return 0;
}

int find_sub_str_(char* father, char* son){
	printf("substring:  ");
	for(int i=0; father[i] != '\0'; i++){
		for(int j=0; father[i]==son[j]; ){
			printf("%c",father[i]);
			if(son[j] == '\0'){
				return 1;	
			}
			j++;
			i++;
		}
	}
	return 0;
}

int main(){
	char* father="iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiwei shen me hui zhe yang ,wo ye bu zhidao ,zhe ta ma  he zen me hui zhe yang ,bu kexue a ,wo dou da le zheme duo de zila , mei men neng bu neng gei dian mian zi, zhenshi de ,pian yao ang wo ba shuo you de zi quan buda wna cai ke yi shi ma?e this willl be a little bit hard ,wo shi xuehao";
	char* son="wo shi";
	clock_t start_time, finish_time;
	double cost  = 0;
	int ans = 0;

	start_time = clock();
	ans = find_sub_str_(father,son);
	finish_time = clock();
	cost = (double)(finish_time - start_time) / CLOCK_PER_SEC;
	printf("\ncost %f seconds\n", cost);
	printf("%d \n",ans);
	
	start_time = clock();
	ans = find_sub_str(father,son);
	finish_time  = clock();
	cost = (double)(finish_time - start_time) / CLOCK_PER_SEC;
	printf("\ncost %f seconds\n",cost);
	printf("%d \n",ans);

	start_time = clock();
	ans = find_sub_str_(father,son);
	finish_time = clock();
	cost = (double)(finish_time - start_time) / CLOCK_PER_SEC;
	printf("\ncost %f seconds\n", cost);
	printf("%d \n",ans);

	return 0;
}
