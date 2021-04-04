# alphabet-guessing-game
The alphabet guessing game web-application that using MongoDB.

## How to clone the alphabet guessing game
* Access to a command-line/terminal window.
    * Linux:
        ```
        CTRL-ALT-T or CTRL-ALT-F2
        ``` 
    * Windows: 
        ``` 
        WIN+R > type powershell > Enter/OK or Type in search tap "cmd"
        ```
    * MacOS: 
        ```
        Finder > Applications > Utilities > Terminal
        ```
* Change directory to the directory that the user wants to run the application.
    ```
    cmd> cd directory name
    ```
* Use git clone in the command line. (Link to clone the alphabet guessing game `https://github.com/PitchapaSaelim/alphabet-guessing-game.git`)
    ```
    cmd> git clone https://github.com/PitchapaSaelim/alphabet-guessing-game.git
    ```
## Getting Started
> Install [Docker](https://docs.docker.com/desktop/) and [Docker Compose](https://docs.docker.com/compose/install/)

- Clone the alphabet guessing game to your machine. [*See how to clone the web-application.*](https://github.com/PitchapaSaelim/alphabet-guessing-game#how-to-clone-the-alphabet-guessing-game)
- Access to a command-line/terminal window.
    * Change directory to the directory that contain `alphabet-guessing-game` folder.
        ```
        cmd> cd alphabet-guessing-game
        ```        
    * 
        ```
        cmd> docker-compose up -d
        ```        
    * 
        ```
        cmd> docker-compose logs -f --tail 10 web
        ```     

- Follows the link  http://localhost/   

- Follows this command when you want to close the web-application.
    ```
    cmd> docker-compose down -v
    ```     

## How to play the alphabet guessing game
1. Create the question by choose A or B or C or D to add the character to the question.
2. The web-application will let you guess the correct answer. You can choose A or B or C or D to guess the character.
3. When you guess wrongly, the number of failures will increase. But when you guessed it right, the character X will appear instead of the correct one. 
4. When you answer them all correctly, the web-application will shows you won and tells you the number of failures.
5. Press `Play Again?` button to restart the game.