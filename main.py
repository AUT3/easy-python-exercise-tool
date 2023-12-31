import program
import argparse
import configparser
import shutil

portable_available = True
try:
    import PyInstaller.__main__
except ImportError:
    portable_available = False
# file mainly for handling arguments

exercise_path: str
solution_path: str
portable = False

def make_portable():
        # if PyInstaller is installed
        if(not portable_available):
            print("To use -p parameter PyInstaller needs to be available!")
            return

        PyInstaller.__main__.run([
            "program.py",
            "--onefile",
            "--distpath=%s" % portable_path + "dist",
            "--workpath=%s" % portable_path + "work",
            "--specpath=%s" % portable_path + "spec",
            "--log-level=ERROR",
            "-n=output"
        ])
        
        if(not keep_debug):
            shutil.rmtree(portable_path + "work")
            shutil.rmtree(portable_path + "spec")

        # make configuration file
        config = configparser.ConfigParser()
        config["PARAMETERS"] = {
            "ExercisePath": exercise_path,
            "SolutionPath": (solution_path or "none"),
            "Eval": eval_mode
        }

        config_file = open(portable_path + "dist/" + "config.ini", "a")
        config.write(config_file)
        config_file.close()

        # copy exercise file, any solution files will be created automatically by the program
        shutil.copyfile(exercise_path, portable_path + "dist/" + exercise_path)

if __name__ == "__main__":
    # parsing arguments
    parser = argparse.ArgumentParser(description="Software to make creating Python exercises easier")

    parser.add_argument("-f", "--file", type=str, help="Specify the default solution file (otherwise the code will have to be typed inside the program input)", default="")
    parser.add_argument("-p", "--portable_path", type=str, help="Output to .exe file (for portability). Remember to end with /")
    parser.add_argument("-d", "--debug", action="store_true", help="Keep the debug files (only relevant for -p)")
    parser.add_argument("-e", "--eval", action="store_true", help="Set this if it is supposed to be a test (answering incorrectly won't give another chance)")
    parser.add_argument("exercise-file", type=str, help="Specify the exercise (json) file")

    args = parser.parse_args()
    arg_config = vars(args)

    # print(config)
    exercise_path = arg_config["exercise-file"]
    solution_path = arg_config["file"]
    portable_path = arg_config["portable_path"]
    keep_debug = arg_config["debug"]
    eval_mode = arg_config["eval"]

    if(portable_path):
        make_portable()
    else:
        # runs the program normally
        exe = program.exercise(exercise_path, solution_path, eval_mode)
        exe.loop()
