#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    if (argc != 2) //argument check
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    
    for (int i = 0; i < strlen(argv[1]); i++) //positive decimal check
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    
    int k = atoi(argv[1]); // assign key to the variable
    if (k > 26) //return to the range of 0 - 26
    {
        k %= 26;    
    }
    //printf("%i\n", k);
    
    string plain = get_string("plaintext: ");
    printf("ciphertext: ");
    for (int i = 0; i < strlen(plain); i++)
    {
        char c = plain[i];
        if (c >= 'A' && c <= 'Z')
        {
            c -= 65;
            c += k;
            c %= 26;
            c += 65;
        } 
        else if (c >= 'a' && c <= 'z')
        {
            c -= 97;
            c += k;
            c %= 26;
            c += 97;
        }
        printf("%c", c);
    }
    printf("\n");
    
}