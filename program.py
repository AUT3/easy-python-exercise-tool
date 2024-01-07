import json
import subprocess
import configparser
import sys
import re

# file with the actual program

# TODO: ADD POINTS

class exercise:
    def __init__(self, path, solution_path, eval_mode) -> None:
        self.path = path
        file = open(path, "r")
        self.ex = json.loads(file.read())
        file.close()
        self.clear_file = True
        self.solution_path = solution_path
        self.points = 0
        self.max_points = 0
        self.eval_mode = eval_mode

    def handle_solution_file(self, path):
        # create or clear file (works, weirdly enough)
        print(f"{self.clear_file}, {path}")
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

        # separate questions
        if(num != 0):
            print("\n")

        print(q["title"], end=" ")

        if(self.eval_mode): 
            print(f"({q.get('pts', 0)})", end="")
        
        print(f"\n{q['question']}")
        
        if(q["type"] == "sc" or q["type"] == "mc"):
            # single-choice / multiple-choice (same thing code wise, might merge them in json to "c" for choice)
            try:
                ans = input("Type your answer here:\n>").lower()
            except KeyboardInterrupt:
                sys.exit()

            regex_res = re.search("[a-z0-9]+", ans)

            if(not regex_res): output = False
            else: output = (regex_res.group() == q["answer"])
        elif(q["type"] == "e"):
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

            # print(f"Your result: {result}\nExpected result: {expected}")
            
            output = (result == expected)
        else:
            print(f"Error! Probably wrong type in question {num}!!!")
            output = False

        if(len(q.get('file', '')) != 0):
            self.clear_file = output

        # if correct, add points
        if(self.eval_mode):
            self.points += q.get('pts', 0) * output
            self.max_points += q.get('pts', 0)

        return output

    def loop(self):
        i = 0
        while(i < len(self.ex)):
            if(not self.eval_mode):
                # 'practice' mode
                if(self.show_question(i)):
                    i += 1
            else:
                # eval mode
                self.show_question(i)
                i += 1

        print(f"You did it!", end="")
        print(f"Points: ({self.points}/{self.max_points})")

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")

    exe = exercise(config["PARAMETERS"]["exercisepath"], config["PARAMETERS"]["solutionpath"], config["PARAMETERS"]["eval"])
    exe.loop()
