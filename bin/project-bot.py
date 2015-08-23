import os, sys, argparse, json, sys, re, shutil, datetime, logging, subprocess
from collections import namedtuple

### Global Project defaults ###
zeros=4

Contributor = namedtuple('Contributor', ['name', 'email', 'rank'])


### Default options are created in an object and returned ###
def genDefaultOptions():
    logging.debug('Generating Default Options')
    
    cont = Contributor('Broseph Peet', 'bro@unrulyrecursion.com', '1')
    script_path = getScriptPath()
    
    o = {'name': 'Example Project', 
               'template_name': 'Generic',
               'scm': 'git', 
               'scm_init': False,
               'contributors': [cont],
               'info': 'This is a sample description of a project',
               'directory': '../',
               'script_path': script_path + '/',
               'template_path': os.path.join(script_path, 'templates/')}
    return o
    

### Generates an example output based on default options/template ###
def genExampleFolder():
    # This is where the example folder is generated
    logging.info('Generating Example Folders')

    # TODO consider allowing the generation of just one template (nondestructive to entire example folder) for when people have tons of templates

    defExampleFolder = getDefaultExamplesFolder()

    # Remove old example folder
    existing_dirs = getProjectDirs("./")
    if (len(existing_dirs) > 0):
        for d in existing_dirs:
            # TODO improve this to check for the exact folder, and delete if present
            if (d.lower().find("generatedExamples".lower()) >= 0):
                logging.info('Removing old example folder: ' + d)
                shutil.rmtree(d)

    os.mkdir(defExampleFolder)
    
#    t = getTemplateList()
    t = getBuiltInTemplates()
    logging.info('Template List : ' + t)

    for d in t: #TODO make this also include any custom folder from config

        o = genDefaultOptions()

        logging.debug('Processing template:  ' + d)
        o['template_name'] = d
        o['name'] = o['name'] + " (" + d + ")"
        o['directory'] = os.path.join("./", defExampleFolder)
        o['scm'] = '_stop_'
        
        # Create Example how you would a normal project
        create_project(o)

    return o
    
   
def getTemplateList():
    l = getTemplates()
#    return [item for sublist in l for item in sublist] # TODO ignore empty lists
    return getBuiltInTemplates()


def getTemplates():
    tmp = {}
    tmp['builtin'] = getBuiltInTemplates()


def getBuiltInTemplates():
    return getProjectDirs(os.path.join(getScriptPath(), 'templates/'))


# TODO implement this based on config file etc
def getCustomTemplates():
    return []

### Get Default Examples folder
def getDefaultExamplesFolder():
    return "generatedExamples"


### Get Config file values as a map
def parseConfig():
    pass


### Heart of this program: Creates a project with the given options ###
def create_project(o):
    c = os.getcwd()
    
    global options
    options = o
    
    if options['name'] == '':
        options['name'] = raw_input("Project name, sir: ")
        
    logging.info('Creating project: ' + options['name'] + "\n   CWD: " + os.getcwd())

    existing_dirs = getProjectDirs(options['directory'])
    existing_dirs = weedOutNonNumberedDirs(existing_dirs)

    num = 0
    if (len(existing_dirs) > 0):
        last_proj = existing_dirs[len(existing_dirs)-1]
        if (last_proj.find('-') > -1):
            num = int(last_proj.split("-")[0]) + 1
        logging.debug(last_proj)
    
    options['path'] = os.path.join(options['directory'], (str(num).zfill(zeros) + "-" + options['name']))
    logging.info("Making dir: " + options['path'])
    os.mkdir(options['path'])
    os.chdir(options['path'])
    
    parseTemplate(options)
    os.chdir(c)

    
### Returns list of directories within the given directory ###
def getProjectDirs(d):
    logging.debug("Project Dir: " + str(os.listdir(d)))
    existing_dirs = [x for x in os.listdir(d) if not os.path.isfile(os.path.join(d, x)) and x[0] != '.' and x != 'bin']
    existing_dirs = sorted(existing_dirs)
    logging.debug("Narrowed Dirs: " + str(existing_dirs))
    return existing_dirs


def weedOutNonNumberedDirs(d):
    logging.debug("Weeding out non-numbered directories")
    logging.debug("Before: \n" + str(d))

    d = [x for x in d if x[0].isdigit()]

    logging.debug("After: \n" + str(d))
    return d

    
### Path where this script resides ###
def getScriptPath():
    return os.path.dirname(os.path.realpath(__file__))
    
    
### Method that does the high level parsing for templates ###
def parseTemplate(options):
    logging.info('Parsing template: ' + options['template_name'] + ' for project: ' + options['name'])
    global gen
    global val
    
    try:
        logging.info('Attempting to load: ' + os.path.join(options['template_path'], options['template_name'], 'generic.json'))
        gen_file = open(os.path.join(options['template_path'], options['template_name'], 'generic.json'), 'r')
        gen = json.load(gen_file)
        gen_file.close()
    except IOError as e:
        logging.error("I/O error({0}) loading generic.json: {1}".format(e.errno, e.strerror))
        sys.exit()
    except:
        logging.error("Unexpected error loading generic.json: " + sys.exc_info()[0])
        raise
        sys.exit()
    logging.info('..loaded')
    
    # generic.json File loaded and parsed correctly
    
    try:
        logging.info('Attempting to load: ' + os.path.join(options['template_path'], options['template_name'], 'values.json'))
        val_file = open(os.path.join(options['template_path'], options['template_name'], 'values.json'), 'r')
        val = json.load(val_file)
        val_file.close()
    except IOError as e:
        logging.error("I/O error({0}) loading values.json: {1}".format(e.errno, e.strerror))
        sys.exit()
    except:
        logging.error("Unexpected error loading values.json: " + sys.exc_info()[0])
        raise
        sys.exit()
    logging.info('..loaded')

    # values.json File loaded and parsed correctly
    
    logging.info('Creating Structure')
    for s in gen['structure']:
        logging.debug('Current Working Directory: ' + os.getcwd())
        if s['type'] == 'folder':
            logging.debug('Type: Folder \n  Location: ' + os.path.join(s['path'], s['name']))
            os.mkdir(os.path.join(s['path'], s['name']))
        elif s['type'] == 'file':
            logging.debug('Type: ' + s['type'] + ', Strategy: ' + s['strategy'] + ', Template: ' + s['template'])
            if s['strategy'] == 'generate':
                if s['name'] == 'readme.md':
                    generateReadme(options, s)
            elif s['strategy'] == 'copy':
                shutil.copy(os.path.join(options['template_path'], options['template_name'], s['template']), os.path.join(s['path'], s['name']))
                # TODO catch error here and handle gracefully
        elif s['type'] == 'git' and options['scm'] == 'git':
            logging.debug('Type: Git \n  Location: ' + os.path.join(s['path'], s['name']))
            initGit(os.path.join(s['path'], s['name']))
            
    # TODO Confirm this is the right was to handle the scm flag
    if not options['scm_init'] and not options['scm'] == '_stop_':
        # TODO logic for which scm to init
        initGit(os.path.join(os.getcwd(), "scm"))
    
    
### Special Case file generation for readme ###
# Consider generalizing
def generateReadme(options, structure):
    logging.info('Loading readme files')
    # Try to load src file
    try:
        logging.info('Attempting to load: ' + os.path.join(options['template_path'], options['template_name'], structure['template']))
        src_file = open(os.path.join(options['template_path'], options['template_name'], structure['template']), 'r')
    except IOError as e:
        logging.error("I/O error({0}) loading readme template: {1}".format(e.errno, e.strerror))
        sys.exit()
    except:
        logging.error("Unexpected error loading readme template: " + sys.exc_info()[0])
        sys.exit()
        raise
    logging.info('..loaded')
    # Src file loaded properly (at least we hope)
    
    # Open destination file for writing!
    try:
        logging.info('Attempting to load: ' + os.path.join(structure['path'], structure['name']))
        temp_file = open(os.path.join(structure['name']), 'w')
    except IOError as e:
        logging.error("I/O error({0}) creating readme: {1}".format(e.errno, e.strerror))
        sys.exit()
    except:
        logging.error("Unexpected error creating readme: " + sys.exc_info()[0])
        sys.exit()
        raise
    logging.info('..loaded')
    # Opened successfully
    
    logging.info('Replacing variables with values')
    # Now just to go through line by line and substitute variables in src
    pat = re.compile(r'<(.+)>',re.I)
    
    for line in src_file:
        # substitute variable names for values
        l = re.sub(pat,readmeSub,line)
      
        temp_file.write(l)
    logging.info('..done')
    
    temp_file.close()
    src_file.close()


### Sub Method called by regex convention - Performs the replacement ###
def readmeSub(matchObj):
    pat = matchObj.group(0)
    vr = pat[2:len(pat)-1]
    scope = pat[1]
    
    # Use dictionary to relate the scope and the src the data should come from
    scopeList = {'i' : options, 'v' : val, 'l' : gen, 't' : gen}
    
    logging.debug('Substituting variable: ' + vr + ' - Scope: ' + pat[1])
    
    # Special cases can return sooner
    if scope == 'i': # Input Value
        if (vr.lower() == 'createddate'):
            return str(datetime.date.today())
        else:
            return str(options[vr.lower()])

    elif scope == "a": # Array based value
        return readmeArraySub(scopeList[vr[0]], vr)
    
    elif scope not in scopeList:
        logging.warning('Scope was not recognized: ' + scope)
        return pat
    
    # General purpose case
    return str(scopeList[scope][vr.lower()])
    
    
### Special case for replacement when arrays are involved ###
def readmeArraySub(file, vr):
    scope = vr[0]
    # Should always be a space separating scope/name from the rest of the line
    space = vr.find(' ')
    # Key for the array from the data file
    key = vr[1:space]
    logging.debug('Key is: ' + key)
    # Virgin structure of the line so each entry of data can start fresh
    struct = vr[space:]
    out = ''
    
    # Loop over data returned by the key
    for a in file[key.lower()]:
        logging.debug('Json is: \n' + str(a))
        tmp = struct
        
        # Go through the line and make replacements as you can
        # TODO make more error tolerant (currently surfaces list entry errors and dies)
        while tmp.find('{{') > -1:
            fr = tmp.find('{{')
            la = tmp.find('}}')
            logging.debug('Current Source: ' + tmp + ', Fr: ' + str(fr) + ', La: ' + str(la))
            logging.debug('Replacing: ' + tmp[fr+2:la])
            # the offending line with the possible errors \/
            tmp = tmp[0:fr] + str(a[tmp[fr+2:la].lower()]) + tmp[la+2:]
        out = out + tmp + '\n'
    return out
    
        
### Initialize a bare repo at the given directory ###
# TODO null check and directory existence check
def initGit(d):
    c = os.getcwd()
    os.mkdir(d)
    os.chdir(d)
    logging.info('Initializing git repo at: ' + d)

    # Only support Linux and Mac for git at the moment
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'): # https://docs.python.org/2/library/sys.html#sys.platform
        subprocess.call(['git', 'init'])
        options['scm_init'] = True
    else:
        logging.info('Git repo not initialized')
    os.chdir(c)
    

if __name__ == "__main__":
    global cwd
    cwd = os.getcwd()
    
    
    ### Arg Parsing ###
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='Name of the project (and folder) to create', nargs='?', default='_stop_')
    parser.add_argument('-c', '--contributors', dest='contributors', help='Contributors to the project', nargs=3, action='append', metavar=('cName', 'cEmail', 'cRank'))
    parser.add_argument('-d', '--directory', dest='directory', help='Custom directory location for new project')
    parser.add_argument('-e', '--example', dest='example', help='Generate example folder', action='store_true')
    parser.add_argument('-i', '--info', dest='info', help='Very short description of the project')
    parser.add_argument('-s', '--scm', dest='scm', help='Which source control management you would like initialized', choices=['git'])
    parser.add_argument('-t', '--template', dest='template', help="Template name (also used as the name of the template's enclosing folder)", default='Generic')
    parser.add_argument('-v', '--verbose', dest='verbosity', help='Increase verbosity (off/on/firehose)', action='count', default=0)
    args = parser.parse_args()
    
    ### Initialize Logging ###
    if args.verbosity == 0:
        l = logging.WARNING
    elif args.verbosity == 1:
        l = logging.INFO
    else:
        l = logging.DEBUG
        
    logging.basicConfig(level=l, format='%(asctime)s - %(levelname)s - %(message)s')
    
    
    if ((args.name == '_stop_') or args.example):
        ### Generate Example Project/Folder ###
        genExampleFolder()
    else:
        ### Generate Project/Folder ###
        
        os.chdir(cwd)
        
        # Set arguments with default options
        o = genDefaultOptions();
        logging.debug('Defaults: ' + str(o))
        logging.debug('Args: ' + str(args))
        o['name'] = args.name # This will either be true, or get a default value that won't reach this point
        o['contributors'] = o['contributors'] if getattr(args, 'contributors') is None else args.contributors
        o['directory'] = o['directory'] if getattr(args, 'directory', o['directory']) is None else args.directory
        o['example'] = args.example # This always gets either true or false, no need for default here
        o['info'] = o['info'] if getattr(args, 'info') is None else args.info
        o['scm'] = '_stop_' if getattr(args, 'scm', o['scm']) is None else args.scm
        o['template_name'] = o['template_name'] if getattr(args, 'template') is None else args.template
        logging.info('Args with Defaults: ' + str(o))
        # Call Project Creation
        create_project(o)
        
    ### Reset working directory to original ###
    os.chdir(cwd)


