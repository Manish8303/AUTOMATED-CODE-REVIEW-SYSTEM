// test.c - Intentionally bad C code for analyzer testing

#include <stdio.h>
#include <string.h>

int main()
{
  char name[10];
  printf("Enter your name: ");
  gets(name); // SECURITY ISSUE: unsafe function (buffer overflow risk)

    printf("Hello, %s\n", name)

  int i;
  for (i = 0; i < 10; i++)
   printf("%d ", i)   // Missing semicolon
  printf("\n");

  int unused = 42; // Unused variable
  undeclared_var = 100; // ERROR: undeclared variable

  return 0
}
