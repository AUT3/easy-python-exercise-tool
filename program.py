import json
import subprocess
import configparser
import sys
import re

# file with the actual program

# TODO: ADD POINTS

class exercise:
    def __init__(self, path, solution_path) -> None:
        self.path = path
        file = open(path, "r")
        self.ex = json.loads(file.read())
        file.close()
        self.clear_file = True
        self.solution_path = solution_path

    def handle_solution_file(self, path):
        # create or clear file (works, weirdly enough)
        if(self.clear_file):
            open(path, "w").close()

        input(f"Write your answer in {path} and press Enter when done\n>")

        ans_file = open(path, "r")
        ans = ans_file.read()
        ans_file.close()

        return ans

    def show_question(self, num) -> bool:
        q = self.ex[num]
        output = False

        if(num != 0):
            print("\n")

        print(q["title"])
        print(q["question"])
        
        if(q["type"] == "sc" or q["type"] == "mc"):
            # single-choice / multiple-choice (same thing code wise, might merge them in json to "c" for choice)
            try:
                ans = input("Type your answer here:\n>").lower()
            except KeyboardInterrupt:
                sys.exit()

            regex_res = re.search("[a-z0-9]+", ans)

            if(not regex_res): output = False
            else: output = (regex_res.group() == q["answer"])
        elif(q["type"]=="e"):
            # executable exercise (placeholder name) - requires code to be written

            if(len(q.get('file', '')) == 0):
                if(len(self.solution_path) == 0):
                    try:
                        ans = input("Type your code here:\n>")
                    except KeyboardInterrupt:
                        sys.exit()
                else:
                    ans = self.handle_solution_file(self.solution_path)
            else:
                ans = self.handle_solution_file(q["file"])

            result = subprocess.run(["python3", "-c", ans], capture_output=True).stdout
            expected = subprocess.run(["python3", "-c", q["answer"]], capture_output=True).stdout

            print(f"Your result: {result}\nExpected result: {expected}")
            
            output = (result == expected)
        else:
            print(f"Error! Probably wrong type in question {num}!!!")
            output = False

        self.clear_file = output

        return output

def loop(e: exercise):
    i = 0
    while(i < len(e.ex)):
        if(e.show_question(i)):
            i += 1

    print("Congratulations!")

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")

    exe = exercise(config["PARAMETERS"]["exercisepath"], config["PARAMETERS"]["solutionpath"])
    loop(exe)
