// Implements a dictionary's functionality
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 1000;

// Hash table
node *table[N];

unsigned int size_of_dictionary = 0;
bool dictionary_is_loaded = false;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int n = strlen(word);
    char word_copy[n + 1];
    
    for (int i = 0; i < n; i++)
    {
        word_copy[i] = tolower(word[i]);
    }
    word_copy[n] = '\0';
    
    int index = hash(word_copy);
    
    if (table[index] != NULL)
    {
        for (node *cursor = table[index]; cursor != NULL; cursor = cursor->next)
        {
            if (strcmp(cursor->word, word_copy) == 0)
            {
                return true;
            }
        }
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int hash = 0;
    int n;
    for (int i = 0; word[i] != '\0'; i++)
    {
        if (isalpha(word[i]))
        {
            n = word[i] - 'a' + 1;
        }
        else 
        {
            n = 27;
        }
        
        hash = ((hash << 3) + n) % N;
        
    }
    return hash;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("File opening issue");
        return false;
    }
    
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    char word[LENGTH + 1];
    
    while (fscanf(file, "%s", word) != EOF)
    {
        size_of_dictionary++;

        node *n = malloc(sizeof(node));

        if (n == NULL)
        {
            printf("Not enough memory\n");
            unload();
            return false;
        }
        
        strcpy(n->word, word);

        int index = hash(word);

        if (table[index] == NULL)
        {
            n->next = NULL;
            table[index] = n;
        }
        else
        {
            n->next = table[index];
            table[index] = n;
        }
        
    }

    fclose(file);
    dictionary_is_loaded = true;
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (dictionary_is_loaded)
    {
        return size_of_dictionary;
    }
    else
    {
        return 0;
    }
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    if (!dictionary_is_loaded)
    {
        return false;
    }
    else
    {
        for (int i = 0; i < N; i++)
        {
            if (table[i] != NULL)
            {
                node *cursor = table[i];
                while (cursor != NULL)
                {
                    node *temp = cursor;
                    cursor = cursor->next;
                    free(temp);
                }
            }
        }
        return true;
    }

    
}
