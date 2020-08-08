#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int average = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width / 2); j++)
        {
            int tempRed = image[i][j].rgbtRed;
            int tempGreen = image[i][j].rgbtGreen;
            int tempBlue = image[i][j].rgbtBlue;
            image[i][j].rgbtRed = image[i][width - 1 - j].rgbtRed;
            image[i][j].rgbtGreen = image[i][width - 1 - j].rgbtGreen;
            image[i][j].rgbtBlue = image[i][width - 1 - j].rgbtBlue;
            image[i][width - 1 - j].rgbtRed = tempRed;
            image[i][width - 1 - j].rgbtGreen = tempGreen;
            image[i][width - 1 - j].rgbtBlue = tempBlue;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            copy[h][w] = image[h][w];
        }
    }
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int avgR = 0;
            int avgG = 0;
            int avgB = 0;
            int counter = 0;
            
            for (int row = -1; row < 2; row++)
            {
                for (int column = -1; column < 2; column++)
                {
                    if (row + i < 0 || column + j < 0 || row + i >= height || column + j >= width)
                    {
                        
                    } 
                    else
                    {
                        avgR += copy[row + i][column + j].rgbtRed;
                        avgG += copy[row + i][column + j].rgbtGreen;
                        avgB += copy[row + i][column + j].rgbtBlue;
                        counter++;
                    }
                }
            }
            
            int R = round(avgR / (float) counter);
            int G = round(avgG / (float) counter);
            int B = round(avgB / (float) counter);
            
            if (R > 255)
            {
                R = 255;
            }
            if (G > 255)
            {
                G = 255;
            }
            if (B > 255)
            {
                B = 255;  
            } 
            
            image[i][j].rgbtRed = R;
            image[i][j].rgbtGreen = G;
            image[i][j].rgbtBlue = B;
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            copy[h][w] = image[h][w];
        }
    }
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int GX_red = 0;
            int GY_red = 0;
            int GX_green = 0;
            int GY_green = 0;
            int GX_blue = 0;
            int GY_blue = 0;
            for (int row = -1; row < 2; row++)
            {
                for (int column = -1; column < 2; column++)
                {
                    if (row + i < 0 || column + j < 0 || row + i >= height || column + j >= width)
                    {
                        
                    } 
                    else
                    {
                        if (row == -1 && column == -1)
                        {
                            GX_red += (copy[row + i][column + j].rgbtRed * (-1));
                            GY_red += (copy[row + i][column + j].rgbtRed * (-1));
                            GX_green += (copy[row + i][column + j].rgbtGreen * (-1));
                            GY_green += (copy[row + i][column + j].rgbtGreen * (-1));
                            GX_blue += (copy[row + i][column + j].rgbtBlue * (-1));
                            GY_blue += (copy[row + i][column + j].rgbtBlue * (-1));
                        } 
                        else if (row == -1 && column == 0)
                        {
                            
                            GY_red += (copy[row + i][column + j].rgbtRed * (-2));
                            
                            GY_green += (copy[row + i][column + j].rgbtGreen * (-2));

                            GY_blue += (copy[row + i][column + j].rgbtBlue * (-2));
                        } 
                        else if (row == -1 && column == 1)
                        {
                            GX_red += (copy[row + i][column + j].rgbtRed * (1));
                            GY_red += (copy[row + i][column + j].rgbtRed * (-1));
                            GX_green += (copy[row + i][column + j].rgbtGreen * (1));
                            GY_green += (copy[row + i][column + j].rgbtGreen * (-1));
                            GX_blue += (copy[row + i][column + j].rgbtBlue * (1));
                            GY_blue += (copy[row + i][column + j].rgbtBlue * (-1));
                        } 
                        else if (row == 0 && column == -1)
                        {
                            GX_red += (copy[row + i][column + j].rgbtRed * (-2));

                            GX_green += (copy[row + i][column + j].rgbtGreen * (-2));

                            GX_blue += (copy[row + i][column + j].rgbtBlue * (-2));

                        }
                        else if (row == 0 && column == 0)
                        {

                        }
                        else if (row == 0 && column == 1)
                        {
                            GX_red += (copy[row + i][column + j].rgbtRed * (2));

                            GX_green += (copy[row + i][column + j].rgbtGreen * (2));

                            GX_blue += (copy[row + i][column + j].rgbtBlue * (2));

                        }
                        else if (row == 1 && column == -1)
                        {
                            GX_red += (copy[row + i][column + j].rgbtRed * (-1));
                            GY_red += (copy[row + i][column + j].rgbtRed);
                            GX_green += (copy[row + i][column + j].rgbtGreen * (-1));
                            GY_green += (copy[row + i][column + j].rgbtGreen);
                            GX_blue += (copy[row + i][column + j].rgbtBlue * (-1));
                            GY_blue += (copy[row + i][column + j].rgbtBlue);
                        }
                        else if (row == 1 && column == 0)
                        {

                            GY_red += (copy[row + i][column + j].rgbtRed * (2));

                            GY_green += (copy[row + i][column + j].rgbtGreen * (2));

                            GY_blue += (copy[row + i][column + j].rgbtBlue * (2));
                        }
                        else if (row == 1 && column == 1)
                        {
                            GX_red += copy[row + i][column + j].rgbtRed;
                            GY_red += copy[row + i][column + j].rgbtRed;
                            GX_green += copy[row + i][column + j].rgbtGreen;
                            GY_green += copy[row + i][column + j].rgbtGreen;
                            GX_blue += copy[row + i][column + j].rgbtBlue;
                            GY_blue += copy[row + i][column + j].rgbtBlue;
                        }
                        
                        
                        
                    }
                }
            }
            
            int finalRed = round(sqrt(pow(GX_red, 2) + pow(GY_red, 2)));
            int finalGreen = round(sqrt(pow(GX_green, 2) + pow(GY_green, 2)));
            int finalBlue = round(sqrt(pow(GX_blue, 2) + pow(GY_blue, 2)));
                        
            if (finalRed > 255)
            {
                finalRed = 255;
            }
            if (finalGreen > 255)
            {
                finalGreen = 255;
            }
            if (finalBlue > 255)
            {
                finalBlue = 255;
            } 
            
            image[i][j].rgbtRed = finalRed;
            image[i][j].rgbtGreen = finalGreen;
            image[i][j].rgbtBlue = finalBlue;
        }
    }
    return;
}
