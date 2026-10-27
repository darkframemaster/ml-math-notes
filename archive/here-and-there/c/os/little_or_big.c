#include<stdio.h>
#include<stdlib.h>
typedef unsigned char BYTE;

int checkCPU(){
	union w{
	int a;
	char b;
	}c;
	c.a = 1;
	if(c.b == 1){
		printf("The endian of cpu is litte\n");
	}	
	else{
		printf("The endian of cpu is big\n");
	}
}

int litte_or_big(){
	unsigned int num,*p;
	p = &num;
	num = 1;
	*(BYTE *)p = 0xff;	// make p to a BYTE* pointer
	if(num == 0xff){
		printf("The endian of cpu is litte,And the num is %d\n",num);
	}
	else{
		printf("The endian of cpu is big,And the num is %d\n",num);		
	}
	return 0;
}

int main(){
	litte_or_big();
	checkCPU();
	return 0;
}
