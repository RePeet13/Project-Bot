import os, sys, argparse, json, sys, re

### Global Project defaults ###
project_dir = "../"
zeros=4
template_dir = ""


if __name__ == "__main__":
    
    global args
    
    ### Generate Example Project/Folder ###
    
    genExampleFolder()
    
    
    ### Arg Parsing ###
    
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='Name of the project (and folder) to create')
    parser.add_argument('-t', '--template', dest='template', help="Template name (also used as the name of the template's enclosing folder)", default='Generic')
    parser.add_argument('-s', '--scm', dest='scm', help='Which source control management you would like initialized', choices=['git'])
    parser.add_argument('-c', '--contributor', dest='contributor', help='A contributor to the project', nargs=3, action='append', metavar=('cName', 'cEmail', 'cRank'))
    parser.add_argument('-i', '--info', dest='info', help='Very short description of the project')
    parser.add_argument('-d', '--directory', dest='directory', help='Custom directory location for new project')
    args = parser.parse_args()





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


    
   
def create_project():

    global project_name
    global project_dir
    global project_path
    
    if project_name == '':
        project_name = raw_input("Project name, sir: ")

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
    project_path = new_path
    os.mkdir(new_path)
    
def getScriptPath ():
    return os.path.dirname(os.path.realpath(__file__))
    # return os.path.dirname(os.path.realpath(sys.argv[0])) # previous solution

def getDefaultProjectDir ():
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
    # est='template', dest='scm', dest='contributor', dest='info', dest='directory'
    args.template = 'Generic'
    args.scm = 'git'
    args.contributor = []
    args.info = ''
    args.directory = ''
    
    ### Call normal create_project ###
    
    create_project()
    
    
def parseTemplate(template_path):
    
    global gen
    global val
    
    try:
        gen_file = open(template_path + 'generic.json', 'r')
        gen = json.load(gen_file)
        gen_file.close()
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        sys.exit()
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
        sys.exit()

    # generic.json File loaded and parsed correctly
    
    try:
        val_file = open(template_path + 'values.json', 'r')
        val = json.load(gen_file)
        val_file.close()
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

    # values.json File loaded and parsed correctly
    
    for s in gen['structure']:
        if s['type'] == "folder":
            os.mkdir(project_dir + s['path'])
        elif s['type'] == "file":
            if s['name'] == 'readme.md':
                generateReadme(template_path + s['template'])
    

def generateReadme(file_template_path):
    
    # Try to load src file
    try:
        src_file = open(file_template_path, 'r')
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        sys.exit()
    except:
        print "Unexpected error:", sys.exc_info()[0]
        sys.exit()
        raise
    # Src file loaded properly (at least we hope)
    
    
    # Open destination file for writing!
    try:
        temp_file = open(project_path + 'readme.md', 'w')
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        sys.exit()
    except:
        print "Unexpected error:", sys.exc_info()[0]
        sys.exit()
        raise
    # Opened successfully
    
    # Now just to go through line by line and substitute variables in src
    
    pat = re.compile(r'<([a-z]+)>',re.I)
    
    for line in src_file:
        # substitute variable names for values
        l = re.sub(pat,readmeSub,line)
      
        #perform operation and substitution on line into l
      
        temp_file.write(l)# + "\n") # TODO uncomment if no new lines in output
    
    temp_file.close()
    src_file.close()


def readmeSub(matchObj):
    scope = matchObj[0]
    
    # Gigantic Else If statement
    if scope == "i":    # Input Value
        pass
    elif scope == "l":  # Local Values (generic.json)
        return gen[matchObj[1:]]
    elif scope == "v":  # Values.json
        out = ""
        arr = matchObj[1:].split("-")
        if len(arr) > 1:
            # TODO handle
            print("length of array more than 2: " + str(arr))
            sys.exit()
        out = out + val[arr[0][1:]][arr[1]]
        return out
    elif scope == "t":  # Template Values
        return gen[matchObj[1:]]
    else:
        pass
        # something's wrong, need to error out gracefully

""" Actual Execution """
# create_project()