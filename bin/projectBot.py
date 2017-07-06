import os, sys, argparse, json, sys, re, shutil, datetime, logging, subprocess
from collections import namedtuple

### Global Project defaults ###
zeros=4

Contributor = namedtuple('Contributor', ['name', 'email', 'rank'])


### Default options are created in an object and returned ###
def genDefaultOptions():
    # logging.debug('Generating Default Options')
    logThis('debug', 'Generating Default Options')

    cont = Contributor('Broseph Peet', 'bro@unrulyrecursion.com', '1')
    script_path = getScriptPath()

    o = {'name': 'Example Project',
            'template_name' : 'Generic',
            'scm'           : 'git',
            'scm_init'      : False,
            'contributors'  : [cont],
            'info'          : 'This is a sample description of a project',
            'directory'     : '../',
            'script_path'   : script_path + '/',
            'template_path' : os.path.join(script_path, 'templates/')}
    return o


### Generates an example output based on default options/template ###
def genExampleFolder():
    # This is where the example folder is generated
    # logging.info('Generating Example Folders')
    logThis('info', 'Generating Example Folders')

    # TODO consider allowing the generation of just one template (nondestructive to entire example folder) for when people have tons of templates

    defExampleFolder = getDefaultExamplesFolder()

    # Remove old example folder
    existing_dirs = getProjectDirs("./")
    if (len(existing_dirs) > 0):
        for d in existing_dirs:
            # TODO improve this to check for the exact folder, and delete if present
            if (d.lower().find("generatedExamples".lower()) >= 0):
                # logging.info('Removing old example folder: ' + d)
                logThis('info', 'Removing old example folder: ' + str(d))
                shutil.rmtree(d)

    os.mkdir(defExampleFolder)

    # TODO switch back to get template list
#    t = getTemplateList()
    t = getBuiltInTemplates()
    # logging.info('Template List : ' + t)
    logThis('info', 'Template List : ' + str(t))

    for d in t: #TODO make this also include any custom folder from config
        o = genDefaultOptions()

        # logging.debug('Processing template:  ' + d)
        logThis('debug', 'Processing template:  ' + str(d))
        o['template_name'] = d
        o['name'] = o['name'] + " (" + d + ")"
        o['directory'] = os.path.join("./", defExampleFolder)
        o['scm'] = '_stop_'

        # Create Example how you would a normal project
        create_project(o)

    return o


### Wrapper for full template check that simply returns true or false ###
def templateCheck(dir):
    # logging.info('Template check wrapper')
    logThis('info', 'Template check wrapper')
    c = os.getcwd()
    os.chdir(os.path.join(getScriptPath(), 'templates/'))
    ftc = fullTemplateCheck(dir)
    # logging.debug('Is success : ' + str(ftc['success']))
    logThis('debug', 'Is success : ' + str(ftc['success']))
    os.chdir(c)
    return ftc['success']


### Full template check that looks at multiple things as well as validity. Returns overall success as well as some errors that occurred while generating template files. ###
def fullTemplateCheck(dir):
    # logging.info('Full template check starting : ' + os.path.join(os.getcwd(), dir))
    logThis('info', 'Full template check starting : ' + str(os.path.join(os.getcwd(), dir)))
    results = {}
    results['simple'] = simpleTemplateCheck(dir)

    # TODO implement full checking logic
    results['success'] = results['simple']

    return results


### A simple check for a template. Only looks to see if there exists a generic.json file ###
def simpleTemplateCheck(dir):
    gen_file = 'generic.json'
    # logging.info('Doing simple check')
    logThis('info', 'Doing simple check')

    if not os.path.isfile(os.path.join(dir, gen_file)):
        # logging.debug('generic.json not found')
        logThis('debug', 'generic.json not found')
        return False


    return True


### Get all templates (built in and custom) as a list ###
def getTemplateList():
    l = getTemplates()
#    return [item for sublist in l for item in sublist] # TODO ignore empty lists
    return getBuiltInTemplates()


### Retrieve all templates { 'builtin' : [], 'custom' : [] } ###
def getTemplates():
    tmp = {}
    tmp['builtin'] = getBuiltInTemplates()


def getBuiltInTemplates():
    return [x for x in getProjectDirs(os.path.join(getScriptPath(), 'templates/')) if templateCheck(x)]


### Returns all custom templates based on location in config file ###
# TODO implement this based on config file etc
def getCustomTemplates():
    return []

### Get Default Examples folder ###
def getDefaultExamplesFolder():
    return "generatedExamples"


### Get Config file values as a map ###
def parseConfig():
    pass


### Heart of this program: Creates a project with the given options ###
def create_project(o):
    c = os.getcwd()

    global options
    options = o

    # if options['name'] == '':
    #     options['name'] = raw_input("Project name, sir: ")

    # logging.info('Creating project: ' + options['name'] + "\n   CWD: " + os.getcwd())
    logThis('info', 'Creating project: ' + str(options['name']) + "\n   CWD: " + str(os.getcwd()))

    existing_dirs = getProjectDirs(options['directory'])
    existing_dirs = weedOutNonNumberedDirs(existing_dirs)

    num = 0
    if (len(existing_dirs) > 0):
        last_proj = existing_dirs[len(existing_dirs)-1]
        if (last_proj.find('-') > -1):
            num = int(last_proj.split("-")[0]) + 1
        # logging.debug(last_proj)
        logThis('debug', last_proj)

    options['path'] = os.path.join(options['directory'], (str(num).zfill(zeros) + "-" + options['name']))
    # logging.info("Making dir: " + options['path'])
    logThis('info', 'Making dir: ' + str(options['path']))
    os.mkdir(options['path'])
    os.chdir(options['path'])

    parseTemplate(options)

    # TODO change dir then parse template

    os.chdir(c)

    # logging.info('Completed creation of : ' + options['name'] + '\n     Template used : ' + options['template_name'])
    logThis('info', 'Completed creation of : ' + str(options['name']) + '\n     Template used : ' + str(options['template_name']))


### Returns list of directories within the given directory ###
def getProjectDirs(d):
    # logging.debug("Project Dir: " + str(os.listdir(d)))
    logThis('debug', 'Project Dir: ' + str(os.listdir(d)))
    existing_dirs = [x for x in os.listdir(d) if not os.path.isfile(os.path.join(d, x)) and x[0] != '.' and x != 'bin']
    existing_dirs = sorted(existing_dirs)
    # logging.debug("Narrowed Dirs: " + str(existing_dirs))
    logThis('debug', 'Narrowed Dirs: ' + str(existing_dirs))
    return existing_dirs


### List comprehension to remove non-numbered directories from list ###
def weedOutNonNumberedDirs(d):
    # logging.debug("Weeding out non-numbered directories")
    logThis('debug', 'Weeding out non-numbered directories')
    # logging.debug("Before: \n" + str(d))
    logThis('debug', 'Before: \n' + str(d))

    d = [x for x in d if x[0].isdigit()]

    # logging.debug("After: \n" + str(d))
    logThis('debug', 'After: \n' + str(d))
    return d


### Path where this script resides ###
def getScriptPath():
    return os.path.dirname(os.path.realpath(__file__))


### Method that does the high level parsing for templates ###
def parseTemplate(options):
    # logging.info('Parsing template: ' + options['template_name'] + ' for project: ' + options['name'])
    logThis('info', 'Parsing template: ' + str(options['template_name']) + ' for project: ' + str(options['name']))

    global gen
    global val

    genPath = os.path.join(options['template_path'], options['template_name'], 'generic.json')
    gen = loadGenFile(genPath)

    valPath = os.path.join(options['template_path'], options['template_name'], 'values.json')
    val = loadValFile(valPath)

    logging.info('Creating Structure')
    for s in gen['structure']:
        # logging.debug('Current Working Directory: ' + os.getcwd())
        logThis('debug', 'Current Working Directory: ' + str(os.getcwd()))
        if s['type'] == 'folder':
            # logging.debug('Type: Folder \n  Location: ' + os.path.join(s['path'], s['name']))
            logThis('debug', 'Type: Folder \n  Location: ' + str(os.path.join(s['path'], s['name'])))
            os.mkdir(os.path.join(s['path'], s['name']))
        elif s['type'] == 'file':
            # logging.debug('Type: ' + s['type'] + ', Strategy: ' + s['strategy'] + ', Template: ' + s['template'])
            logThis('debug', 'Type: ' + str(s['type']) + ', Strategy: ' + str(s['strategy']) + ', Template: ' + str(s['template']))
            if s['strategy'] == 'generate':
                if s['name'] == 'readme.md':
                    generateReadme(options, s)
            elif s['strategy'] == 'copy':
                shutil.copy(os.path.join(options['template_path'], options['template_name'], s['template']), os.path.join(s['path'], s['name']))
                # TODO catch error here and handle gracefully
        elif s['type'] == 'git' and options['scm'] == 'git':
            # logging.debug('Type: Git \n  Location: ' + os.path.join(s['path'], s['name']))
            logThis('debug', 'Type: Git \n  Location: ' + str(os.path.join(s['path'], s['name'])))
            initGit(os.path.join(s['path'], s['name']))


    # logging.info('Looking for template extensions')
    logThis('info', 'Looking for template extensions')
    # TODO add existence check for gen['extends']
    # logging.info('...found')
    logThis('info', '...found')
    try:
        for e in gen['extends']:
            # TODO null checks for both with gracious error
            # logging.debug('Loading ' + e['name'] + ' template')
            logThis('debug', 'Loading ' + str(e['name']) + ' template')
            # logging.debug('Subdirectory: ' + e['root'])
            logThis('debug', 'Subdirectory: ' + str(e['root']))

            subOptions = loadSubTemplate(e)
    except KeyError as e:
        pass


    # TODO Confirm this is the right was to handle the scm flag (need to respect the scm flag in the generic files)
    if not options['scm_init'] and not options['scm'] == '_stop_':
        # TODO logic for which scm to init
        initGit(os.path.join(os.getcwd(), "scm"))

    for t in gen['extends']:
        cwd = os.getcwd()

        # TODO fill out this conditional with input from user
        continueWithCollision = true
        try:
            os.mkdir(t['root'])
        except OSError as e:
            pass

        if continueWithCollision:
            os.chdir(t['root'])

        os.chdir(cwd)


### Load generic file
def loadGenFile(tp):
    gen = null
    try:
        # logging.info('Attempting to load: ' + tp)
        logThis('info', 'Attempting to load: ' + str(tp))
        gen_file = open(tp, 'r')
        gen = json.load(gen_file)
        gen_file.close()
    except IOError as e:
        # logging.error('I/O error({0}) loading generic.json: {1}'.format(e.errno, e.strerror))
        logThis('error', 'I/O error({0}) loading generic.json: {1}'.format(e.errno, e.strerror))
        sys.exit()
    except:
        # logging.error('Unexpected error loading generic.json: ' + sys.exc_info()[0])
        logThis('error', 'Unexpected error loading generic.json: ' + str(sys.exc_info()[0]))
        raise
        sys.exit()
    # logging.info('..loaded')
    logThis('info', '..loaded')
    # generic.json File loaded and parsed correctly
    return gen


### load values file
def loadValFile(tp):
    val = null
    try:
        # logging.info('Attempting to load: ' + tp)
        logThis('info', 'Attempting to load: ' + str(tp))
        val_file = open(tp, 'r')
        val = json.load(val_file)
        val_file.close()
    except IOError as e:
        # logging.error('I/O error({0}) loading values.json: {1}'.format(e.errno, e.strerror))
        logThis('error', 'I/O error({0}) loading values.json: {1}'.format(e.errno, e.strerror))
        sys.exit()
    except:
        # logging.error('Unexpected error loading values.json: ' + sys.exc_info()[0])
        logThis('error', 'Unexpected error loading values.json: ' + str(sys.exc_info()[0]))
        raise
        sys.exit()
    # logging.info('..loaded')
    logThis('info', '..loaded')

    # values.json File loaded and parsed correctly
    return val


### Load the options for a subtemplate ###
def loadSubTemplate(subTemplate):
    # logging.info('Loading subtemplate options')
    logThis('info', 'Loading subtemplate options')
    # TODO generate options here with sub template thoughts, such as the changed root, and no project name
    return {}


### Special Case file generation for readme ###
# Consider generalizing
def generateReadme(options, structure):
    # logging.info('Loading readme files')
    logThis('info', 'Loading readme files')
    # Try to load src file
    try:
        # logging.info('Attempting to load: ' + os.path.join(options['template_path'], options['template_name'], structure['template']))
        logThis('info', 'Attempting to load: ' + str(os.path.join(options['template_path'], options['template_name'], structure['template'])))
        src_file = open(os.path.join(options['template_path'], options['template_name'], structure['template']), 'r')
    except IOError as e:
        # logging.error('I/O error({0}) loading readme template: {1}'.format(e.errno, e.strerror))
        logThis('error', 'I/O error({0}) loading readme template: {1}'.format(e.errno, e.strerror))
        sys.exit()
    except:
        # logging.error('Unexpected error loading readme template: ' + sys.exc_info()[0])
        logThis('error', 'Unexpected error loading readme template: ' + str(sys.exc_info()[0]))
        sys.exit()
        raise
    # logging.info('..loaded')
    logThis('info', '..loaded')
    # Src file loaded properly (at least we hope)

    # Open destination file for writing!
    try:
        # logging.info('Attempting to load: ' + os.path.join(structure['path'], structure['name']))
        logThis('info', 'Attempting to load: ' + str(os.path.join(structure['path'], structure['name'])))
        temp_file = open(os.path.join(structure['name']), 'w')
    except IOError as e:
        # logging.error('I/O error({0}) creating readme: {1}'.format(e.errno, e.strerror))
        logThis('error', 'I/O error({0}) creating readme: {1}'.format(e.errno, e.strerror))
        sys.exit()
    except:
        # logging.error('Unexpected error creating readme: ' + sys.exc_info()[0])
        logThis('error', 'Unexpected error creating readme: ' + str(sys.exc_info()[0]))
        sys.exit()
        raise
    logging.info('..loaded')
    # Opened successfully

    # logging.info('Replacing variables with values')
    logThis('info', 'Replacing variables with values')

    # Now just to go through line by line and substitute variables in src
    pat = re.compile(r'<(.+)>',re.I)

    for line in src_file:
        # substitute variable names for values
        l = re.sub(pat,readmeSub,line)

        temp_file.write(l)
    # logging.info('..done')
    logThis('info', '..done')

    temp_file.close()
    src_file.close()


### Sub Method called by regex convention - Performs the replacement ###
def readmeSub(matchObj):
    pat = matchObj.group(0)
    vr = pat[2:len(pat)-1]
    scope = pat[1]

    # Use dictionary to relate the scope and the src the data should come from
    scopeList = {'i' : options, 'v' : val, 'l' : gen, 't' : gen}

    # logging.debug('Substituting variable: ' + vr + ' - Scope: ' + pat[1])
    logThis('debug', 'Substituting variable: ' + str(vr) + ' - Scope: ' + str(pat[1]))

    # Special cases can return sooner
    if scope == 'i': # Input Value
        if (vr.lower() == 'createddate'):
            return str(datetime.date.today())
        else:
            return str(options[vr.lower()])

    elif scope == 'a': # Array based value
        return readmeArraySub(scopeList[vr[0]], vr)

    elif scope not in scopeList:
        # logging.warning('Scope was not recognized: ' + scope)
        logThis('warning', 'Scope was not recognized: ' + str(scope))
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
    # logging.debug('Key is: ' + key)
    logThis('debug', 'Key is: ' + str(key))
    # Virgin structure of the line so each entry of data can start fresh
    struct = vr[space:]
    out = ''

    # Loop over data returned by the key
    for a in file[key.lower()]:
        # logging.debug('Json is: \n' + str(a))
        logThis('debug', 'Json is: \n' + str(a))
        tmp = struct

        # Go through the line and make replacements as you can
        # TODO make more error tolerant (currently surfaces list entry errors and dies)
        while tmp.find('{{') > -1:
            fr = tmp.find('{{')
            la = tmp.find('}}')

            # logging.debug('Current Source: ' + tmp + ', Fr: ' + str(fr) + ', La: ' + str(la))
            logThis('debug', 'Current Source: ' + str(tmp) + ', Fr: ' + str(fr) + ', La: ' + str(la)) # TODO refactor to string formatter
            # logging.debug('Replacing: ' + tmp[fr+2:la])
            logThis('debug', 'Replacing: ' + str(tmp[fr+2:la]))

            # the offending line with the possible errors \/
            tmp = tmp[0:fr] + str(a[tmp[fr+2:la].lower()]) + tmp[la+2:]
        out = out + tmp + '\n'
    return out

### Instance to generalize logging to different methods
logThisStruct = {
    'error' : logging.error,
    'warning' : logging.warning,
    'info' : logging.info,
    'debug' : logging.debug
}

### Generalization of logging so it can go to several output methods
def logThis(level, message):
    logThisStruct[level.lower()](message)


### Initialize a bare repo at the given directory ###
# TODO null check and directory existence check
def initGit(d):

    # Only support Linux and Mac for git at the moment
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'): # https://docs.python.org/2/library/sys.html#sys.platform

        c = os.getcwd()
        os.mkdir(d)
        os.chdir(d)
        # logging.info('Initializing git repo at: ' + d)
        logThis('info', 'Initializing git repo at: ' + str(d))

        subprocess.call(['git', 'init'])
        options['scm_init'] = True
        os.chdir(c)
    else:
        # logging.info('Git repo not initialized')
        logThis('info', 'Git repo not initialized')


### Respond to call from command line ###
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
    parser.add_argument('-s', '--scm', dest='scm', help='Which source control management you would like initialized', choices=['git', 'None'])
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
        # logging.debug('Defaults: ' + str(o))
        logThis('debug', 'Defaults: ' + str(o))
        # logging.debug('Args: ' + str(args))
        logThis('debug', 'Args: ' + str(args))

        o['name'] = args.name # This will either be true, or get a default value that won't reach this point
        o['contributors'] = o['contributors'] if getattr(args, 'contributors') is None else args.contributors
        o['directory'] = o['directory'] if getattr(args, 'directory', o['directory']) is None else args.directory
        o['example'] = args.example # This always gets either true or false, no need for default here
        o['info'] = o['info'] if getattr(args, 'info') is None else args.info

        # TODO might need to catch an except here..
        scmtmp = getattr(args, 'scm', o['scm'])
        if scmtmp is None:
            o['scm'] = '_stop_'
        elif scmtmp == 'None':
            o['scm'] = '_stop_'
        else:
            o['scm'] = args.scm

        o['template_name'] = o['template_name'] if getattr(args, 'template') is None else args.template
        # logging.info('Args with Defaults: ' + str(o))
        logThis('info', 'Args with Defaults: ' + str(o))

        # Call Project Creation
        create_project(o)

    ### Reset working directory to original ###
    os.chdir(cwd)
