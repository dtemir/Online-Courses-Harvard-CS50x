#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    long n;
    do 
    {
        n = get_long("Number: ");
    } 
    while (n < 1);
    
    int length = 0;
    int first = 0;
    int second = 0;
    int firstDigit = 0;
    int secondDigit = 0;
    while (n > 0)
    {
        int curr = n % 10;
        n = n / 10;
        length++;
        
        if (length % 2 == 0)
        {
            int temp = curr * 2;
            if (temp > 9)
            {
                first += temp - 10;
                first += (temp / 10) % 10;
            } 
            else 
            {
                first += temp;
            }
            
        } 
        else 
        {
            second += curr;
        }
        
        if (firstDigit != secondDigit)
        {
            secondDigit = firstDigit;
        }
        
        firstDigit = curr;
        
    }
    
    
    
    if ((first + second) % 10 == 0)
    { 
        if (length == 15 && (firstDigit == 3 && (secondDigit == 4 || secondDigit == 7)))
        {
            printf("AMEX\n");
        } 
        else if (length == 16 && (firstDigit == 5 && (secondDigit == 1 || secondDigit == 2 || secondDigit == 3 || secondDigit == 4
                                  || secondDigit == 5)))
        {
            printf("MASTERCARD\n");
        } 
        else if ((length == 13 || length == 16) && firstDigit == 4) 
        {
            printf("VISA\n");
        } 
        else 
        {
            printf("INVALID\n");
        }
    } 
    else 
    {
        printf("INVALID\n");
    }
   
}