#include <stdio.h>
#include <string.h>
#define SIZE_NAME 16
#define SIZE_CHARECTERS 21
void sort(char sortedArr[][SIZE_CHARECTERS], int wordNum){
    char temp[SIZE_CHARECTERS];
    const int ONE = 1;
    for(int k = 0; k < wordNum - ONE; k++){
        for(int j = k + ONE; j < wordNum; j++){
            if(strcmp(sortedArr[k], sortedArr[j]) > 0){
                strcpy(temp, sortedArr[k]);
                strcpy(sortedArr[k], sortedArr[j]);
                strcpy(sortedArr[j], temp);
            }
        }
    }
}
int strList(char sortedArr[][SIZE_CHARECTERS], char mainStr[], char hint[], char sep[]){
    const char start = ':';
    for(int i = 0; mainStr[i] != start; i++){
        hint[i] = mainStr[i];
    }
    char *token;
    token = strchr(mainStr, start);
    token += sizeof(char);
    token = strtok(token, sep);
    int wordNum = 0;
    while (token != NULL){
        strcpy(sortedArr[wordNum], token);
        token = strtok(NULL, sep);
        wordNum++;
    }
    return wordNum;
}
void shape(int stage){
    const int ZERO = 0, ONE = 1, TWO = 2, THREE = 3, FOUR = 4, FIVE = 5, SIX = 6;
    if(stage == ONE){
        printf(" _________________\n");
        for(int t = 0; t < FIVE; t++){
            printf("|                |\n");
        }
        printf("|________________|\n");
    }
    else if(stage == TWO){
        printf(" _________________\n");
        for(int t = 0; t < FIVE; t++){
            if(t == ONE || t == TWO){
                printf("|  **            |\n");
            }
            else{
                printf("|                |\n");
            }
        }
        printf("|________________|\n");
    }
    else if(stage == THREE){
        printf(" _________________\n");
        for(int t = 0; t < FIVE; t++){
            if(t == ONE || t == TWO){
                printf("|  **        **  |\n");
            }
            else{
                printf("|                |\n");
            }
        }
        printf("|________________|\n");
    }
    else if(stage == FOUR){
        printf(" _________________\n");
        for(int t = 0; t < FIVE; t++){
            if(t == ZERO){
                printf("|  --            |\n");
            }
            else if(t == ONE || t == TWO){
                printf("|  **        **  |\n");
            }
            else{
                printf("|                |\n");
            }
        }
        printf("|________________|\n");
    }
    else if(stage == FIVE){
        printf(" _________________\n");
        for(int t = 0; t < FIVE; t++){
            if(t == ZERO){
                printf("|  --        --  |\n");
            }
            else if(t == ONE || t == TWO){
                printf("|  **        **  |\n");
            }
            else{
                printf("|                |\n");
            }
        }
        printf("|________________|\n");
    }
    else if(stage == SIX){
        printf(" _________________\n");
        for(int t = 0; t < FIVE; t++){
            if(t == ZERO){
                printf("|  --        --  |\n");
            }
            else if(t == ONE || t == TWO){
                printf("|  **        **  |\n");
            }
            else if(t == FOUR){
                printf("| \\/\\/\\/\\/\\/\\/\\  |\n");
            }
            else{
                printf("|                |\n");
            }
        }
        printf("|________________|\n");
    }

}
void game(char sortedArr[][SIZE_CHARECTERS], int option, int lenOfOption, char hint[]){
    int stage = 1;
    int hintFlag = 1;
    int outFlag = 1;
    int correctFlag = 1;
    char answers[SIZE_CHARECTERS];
    int letIndex = 0;
    char choice = 0;
    char enter;
    const char UNDERLINE = '_', SPACE = ' ', ASTERISK = '*' ;
    char line[lenOfOption];
    for(int i = 0; i < lenOfOption; i++){
        if(sortedArr[option][i] != SPACE){
            line[i] = UNDERLINE;
        }
        else{
            line[i] = SPACE;
        }
    }
    const int ZERO = 0, ONE = 1, SIX = 6;
    while(ONE){
        shape(stage);
        if (strcmp(line, sortedArr[option]) == ZERO){
            printf("The word is %s, good job!", sortedArr[option]);
            break;
        }
        for(int i = 0; i < lenOfOption; i++){
            printf("%c", line[i]);
        }
        if(hintFlag == ONE){
            printf("\ndo you want a clue? press -> *");
        }
        printf("\nThe letters that you already tried:");
        for(int k = 0; k < letIndex;k++){
            if(k == letIndex - ONE){
                printf(" %c", answers[k]);
            }
            else{
                printf(" %c,", answers[k]);
            }
        }
        printf("\nplease choose a letter:\n");
        scanf("%*[^\n]");
        scanf("%*[^\n]%*c");
        scanf("%c %c", &enter, &choice);
        if(choice == ASTERISK && hintFlag == ONE){
            printf("the clue is: ");
            for(int i = 0; i < strlen(hint); i++){
                printf("%c", hint[i]);
            }
            printf(".\n");
            hintFlag = 0;
        }
        else if(choice != ASTERISK){
            for(int i = 0; i < letIndex; i++){
                if(choice == answers[i]){
                    outFlag = 0;
                }
            }
            if(outFlag == ONE){
                answers[letIndex] = choice;
                letIndex++;
                for(int i = 0; i < lenOfOption; i++){
                    if(sortedArr[option][i] == choice){
                        line[i] = choice;
                        correctFlag = 0;
                    }
                }
                if(correctFlag == ONE){
                    stage++;
                    if(stage == SIX){
                        shape(stage);
                        printf("The word is %s, GAME OVER!", sortedArr[option]);
                        break;
                    }
                }
            }
            else{
                printf("You've already tried that letter.\n");
            }
        }
        outFlag = 1;
        correctFlag = 1;
    }
}

int main() {
    char mainStr[SIZE_NAME*SIZE_CHARECTERS];
    char sortedArr[SIZE_NAME][SIZE_CHARECTERS];
    char hint[SIZE_CHARECTERS] = {0};
    printf("Enter your words:\n");
    scanf("%[^\n]", mainStr);
    int wordNum = strList(sortedArr, mainStr,hint, ",");
    sort(sortedArr, wordNum);
    const int ONE = 1;
    printf("choose an option:\n");
    for(int i = 0; i < wordNum; i++){
        printf("%d: %s\n", (i + ONE), sortedArr[i]);
    }
    int option;
    scanf("%d", &option);
    option -= ONE;
    int lenOfOption = strlen(sortedArr[option]);
    game(sortedArr, option, lenOfOption, hint);
    return 0;
}
