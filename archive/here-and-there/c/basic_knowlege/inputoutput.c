#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main() {
	int i = 4;
	double d = 4.0;
	char s[] = "HackerRank ";
	
	int a;
	double b;
	char c[50];
	scanf("%d\n%lf\n%s", &a, &b, c);
	printf("%d\n%.1f\n%s%s\n", i+a, d+b, s, c);
}
