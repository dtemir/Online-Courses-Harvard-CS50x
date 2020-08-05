#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int main(void)
{
    string text = get_string("Text: ");

    int letters = 0;
    int words = 0;
    int sentences = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        char c = text[i];
        if ((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z'))
        {
            letters++;
        }
        else if (c == ' ')
        {
            words++;
        }
        else if (c == '.' || c == '!' || c == '?')
        {
            sentences++;
        }
    }
    words++;
    //printf("letters: %i\n", letters);
    //printf("words: %i\n", words);
    //printf("sentences: %i\n", sentences);
    float L = ((float) letters * 100) / (float) words;
    
    //printf("l: %f\n", L);

    float S = ((float) sentences * 100) / (float) words;

    //printf("s: %f\n", S);

    float index = 0.0588 * L - 0.296 * S - 15.8;
    index = round(index);

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    } 
    else 
    {
        printf("Grade %i\n", (int)index);
    }

}