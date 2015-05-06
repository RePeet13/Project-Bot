import os, sys, getopt

# Global Project defaults
project_dir = "../"
project_name = ''
zeros=4

def main(argv):
    in_project_name = ''
    try:
        opts, args = getopt.getopt(argv, "hp:", ["project="])
    except getopt.GetoptError:
        print 'project-bot.py -p "Project Name"'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'project-bot.py -p "Project Name"'
            sys.exit()
        elif opt in ("-p", "--project"):
            in_project_name = arg
            print(in_project_name)
    if in_project_name == '':
        project_name = input("Project name, sir: ")
    else:
        project_name = in_project_name

if __name__ == "__main__":
    main(sys.argv[1])
    
   
def create_project():
    
    existing_dirs = [x for x in os.listdir(project_dir) if not os.path.isfile(os.path.join(project_dir,x)) and x[0] != '.' and x != "bin"]
    # print(existing_dirs)
    existing_dirs = sorted(existing_dirs)
    # print(existing_dirs)
    
    if len(existing_dirs) == 0:
        num = 0
    else:
        last_proj = existing_dirs[len(existing_dirs)-1]
        num = int(last_proj.split("-")[0]) + 1
        
    # print(last_proj)
    
    new_path = project_dir + str(num).zfill(zeros) + "-" + project_name
    os.mkdir(new_path)
    

""" Actual Execution """
create_project()