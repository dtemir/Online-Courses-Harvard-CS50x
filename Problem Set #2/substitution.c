#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    if (argc != 2) //argument check
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    for (int i = 0; i < strlen(argv[1]); i++) 
    {
        if (!isalpha(argv[1][i]))
        {
            printf("This character is not a letter: %c\n", argv[1][i]);
            return 1;
        }
        
        for (int j = 0; j < i; j++)
        {
            if (argv[1][j] == argv[1][i])
            {
                printf("This character is repeated: %c\n", argv[1][j]);
                return 1;
            }
        }
    }
    
    if (strlen(argv[1]) != 26)
    {
        printf("The provided argument is not 26 chars long\n");
        return 1;
    }
    
    string k = argv[1]; // assign key to the variable
    
    //printf("%i\n", k);
    
    string plain = get_string("plaintext: ");
    printf("ciphertext: \n");
    for (int i = 0; i < strlen(plain); i++)
    {
        char c = plain[i];
        int valueOfC = (int) c;
        if (c >= 'A' && c <= 'Z')
        {
            char k1 = k[valueOfC - 65];
            //printf("k1: %c", k1);
            if (k1 >= 'A' && k1 <= 'Z')
            {
                c = k1;
            }
            else
            {

                c = k1 - 32;
                
            }
        }
        else if (c >= 'a' && c <= 'z')
        {
            char k1 = k[valueOfC - 97];
            //printf("k1: %c", k1);
            if (k1 >= 'A' && k1 <= 'Z')
            {
                c = k1;
                c += 32;
            }
            else
            {
                c = k1;
            }
        
        }
        printf("%c", c);
    }
    printf("\n");
    
}