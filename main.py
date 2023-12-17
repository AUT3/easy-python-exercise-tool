import program
import argparse
import configparser
import PyInstaller.__main__
import shutil

# file mainly for handling arguments

exercise_path: str
solution_path: str
portable = False

if __name__ == "__main__":
    # parsing arguments: src, (-F, -o)
    parser = argparse.ArgumentParser(description="Software to make creating Python exercises easier")

    parser.add_argument("-f", "--file", type=str, help="Specify the default solution file (otherwise default will be dynamic inside the program)", default="")
    parser.add_argument("-p", "--portable_path", type=str, help="Output to .exe file (for portability). Remember to end with /")
    parser.add_argument("-d", "--debug", action="store_true", help="Keep the debug files (only relevant for -p)")
    parser.add_argument("exercise-file", type=str, help="Specify the exercise (json) file")

    args = parser.parse_args()
    arg_config = vars(args)

    # print(config)
    exercise_path = arg_config["exercise-file"]
    solution_path = arg_config["file"]
    portable_path = arg_config["portable_path"]
    keep_debug = arg_config["debug"]

    if(portable_path):
        # makes the program portable

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
            "SolutionPath": (solution_path or "none")
        }

        config_file = open(portable_path + "dist/" + "config.ini", "a")
        config.write(config_file)
        config_file.close()

        # copy exercise file, any solution files will be created automatically by the program
        shutil.copyfile(exercise_path, portable_path + "dist/" + exercise_path)

    else:
        # runs the program normally

        exe = program.exercise(exercise_path, solution_path)
        program.loop(exe)
