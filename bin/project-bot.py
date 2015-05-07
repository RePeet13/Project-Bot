import os, sys, argparse

### Global Project defaults ###
project_dir = "../"
project_name = ''
zeros=4

### Arg Parsing ###

parser = argparse.ArgumentParser()
parser.add_argument("name", help="Name of the project (and folder) to create")
args = parser.parse_args()
print args.name





# def main(argv):
#     in_project_name = ''
#     in_dir_name = ''

#     """ Help Text """
#     help = 'project-bot.py -p "Project Name"'

#     try:
#         opts, args = getopt.getopt(argv, "hp:d:", ["project=","directory="])
#     except getopt.GetoptError:
#         print help
#         sys.exit(2)
#     for opt, arg in opts:
#         if opt == '-h':
#             print help
#             sys.exit()
#         elif opt in ("-p", "--project"):
#             in_project_name = arg
#             print(in_project_name)
#         elif opt in ("-d", "--directory"):
#             in_dir_name = arg
#             print(in_dir_name)
#     if in_project_name != '':
#         global project_name 
#         project_name = in_project_name

# if __name__ == "__main__":
#     main(sys.argv[1])
    
   
def create_project():

    global project_name
    if project_name == '':
        project_name = input("Project name, sir: ")

    project_dir = getDefaultProjectDir()
    print("Project Dir: " + str(os.listdir(project_dir)))
    
    existing_dirs = [x for x in os.listdir(project_dir) if not os.path.isfile(os.path.join(project_dir,x)) and x[0] != '.' and x != "bin"]
    existing_dirs = sorted(existing_dirs)
    print("Narrowed Dirs: "+ str(existing_dirs))
    
    if len(existing_dirs) == 0:
        num = 0
    else:
        last_proj = existing_dirs[len(existing_dirs)-1]
        num = int(last_proj.split("-")[0]) + 1
        
    # print(last_proj)
    
    new_path = project_dir + str(num).zfill(zeros) + "-" + project_name
    print("Making dir: " + new_path)
    os.mkdir(new_path)
    
def getScriptPath():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def getDefaultProjectDir():
    dirs_tmp = getScriptPath().split("/")
    dirs = []
    for d in dirs_tmp:
        if d == "bin":
            break
        else:
            dirs.append(d)
    print("Default Project Dir: " + "/".join(dirs)+"/")
    return "/".join(dirs) + "/"
    
def genExampleFolder():
    # This is where the example folder will be generated
    
    ### Set global options and what not
    
    create_project()

""" Actual Execution """
# create_project()