#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define BUFFER_SIZE 512

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argv[1] == NULL)
    {
        printf("./recover image\n");
        return 1;
    }

    FILE *file = fopen(argv[1], "r");
    FILE *img;
    char name[7];

    if (file == NULL)
    {
        printf("Unable to read file");
    }

    BYTE buffer[BUFFER_SIZE];
    
    int counter = 0;

    while (fread(buffer, BUFFER_SIZE, 1, file) == 1)
    {
        if (buffer[0] == 0xff  && buffer[1] == 0xd8 && buffer[2] == 0xff && ((buffer[3] & 0xf0) == 0xe0))
        {
            
            if (counter > 0)
            {
                fclose(img);
                sprintf(name, "%03d.jpg", counter);
                img = fopen(name, "w");
                fwrite(buffer, BUFFER_SIZE, 1, img);
                counter++;
            }
            if (counter == 0)
            {
                sprintf(name, "%03d.jpg", counter);
                img = fopen(name, "w");
                fwrite(buffer, BUFFER_SIZE, 1, img);
                counter++;
            } 

        }
        else if (counter > 0)
        {
            fwrite(buffer, BUFFER_SIZE, 1, img);
        }
    }
    printf("%i\n", counter);

    fclose(img);
    fclose(file);

}
