import program
import argparse
import configparser

# file mainly for handling arguments

exercise_path: str
solution_path: str
portable = False

if __name__ == "__main__":
    # parsing arguments: src, (-F, -o)
    parser = argparse.ArgumentParser(description="Software to make creating Python exercises easier")

    parser.add_argument("-f", "--file", type=str, help="Specify the solution file (if applicable)", default="")
    parser.add_argument("-p", "--portable", action="store_true", help="Output to .exe file named after the exercise file (for easier portability)")
    parser.add_argument("exercise-file", type=str, help="Specify the exercise (json) file")
    
    args = parser.parse_args()
    arg_config = vars(args)

    # print(config)
    exercise_path = arg_config["exercise-file"]
    solution_path = arg_config["file"]
    portable = arg_config["portable"]


    exe = program.exercise(exercise_path, solution_path)
    program.loop(exe)
