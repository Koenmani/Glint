def read_feature_file(input):
    f = open(input,"r")
    return f.readlines()

def parse_scenarios(input):
    scenarios = []
    single_line = ''
    when = False
    linecount = 1
    for line in input: 
        if str.lower(line.split(' ')[0]) == 'then':
            #could be the last line, but not sure yet
            when = True
            single_line = single_line + ' ('+str(linecount)+') ' + line.strip()
            linecount+=1
        elif when == True and (line == '' or len(line)<=5):
            #if this was the last line of the scenario
            scenarios.append(single_line)
            single_line = ''
            when = False
            linecount+=1
        else:
            #append the current line to the single line
            #including the line numer in []
            single_line = single_line + ' ('+str(linecount)+') ' + line.strip()
            linecount+=1
    return scenarios

def parse_quality_checks(scenario):
    debuglog(scenario)
    check_givenwhenthen(scenario)
    check_too_long(scenario)
    check_multiple_andors(scenario)
    check_and_after_given(scenario)
    check_single_example(scenario)
    check_user_reference(scenario)
    check_pseudo_code(scenario)

def debuglog(txt):
    if debug:
        print('%s' % (txt,))

####quality checks####
#All functions check for a specific pattern in the given input
#The will append the global objects: warning and errors with the given findings
#

def check_givenwhenthen(scenario):
    #Checks for a proper given, when then pattern in the given scenario
    x = re.search("given.*when.*then.*", str.lower(scenario))
    line_number = scenario.split(" ")[1]
    if not x:
        errors.append('[ERROR] ' + str(line_number) + " Can not identify a solid given, when, then construct")
    else:
        if x.pos > 0:
            errors.append('[ERROR] ' + str(line_number) + " Can not identify a solid given, when, then construct")

def check_too_long(scenario):
    #Checks if the scenario is too long. 6 or more lines is a bad practise and should be split
    x = re.findall("given|when|then|and|or|but not",str.lower(scenario))
    if x:
        line_number = scenario.split(" ")[1]
        if len(x) > 5:
            debuglog(scenario)
            warnings.append('[WARNING] ' + str(line_number) + " Scenario too long. Better split into more scenarios")

def check_multiple_andors(scenario):
    #Checks if this scenario has multiple consequative and/or's after eachother. This is very bad practise and should be better designed
    lines = re.split("\(\d*\)",scenario)
    andcount = 0 #counts the number of consequative ANDs or ORs
    for l in lines:
            if str.lower("and") in str.lower(l) or str.lower("or") in str.lower(l):
                andcount = andcount + 1
            else:
                andcount = 0
            if andcount >= 3:
                line_number = scenario.split(" ")[1]
                errors.append('[ERROR] ' + str(line_number) + " Too many consequative AND or OR statements, making Gherkin more complex then needed. Better split into more scenarios")
    
    
def check_and_after_given(scenario):
    #check if there are no AND or OR after the given. This is bad practise as the starting point should be crisp and clear
    lines = re.split("\(\d*\)",scenario)
    given = False
    for l in lines:
        if given:
            if str.lower("and") in str.lower(l) or str.lower("or") in str.lower(l):
                line_number = scenario.split(" ")[1]
                errors.append('[ERROR] ' + str(line_number) + " Given should be crisp, clear and in one line (no ANDs)")
                return
            else:
                given = False
        if str.lower("given") in str.lower(l):
            given = True

def check_single_example(scenario):
    #checks if the example indeed contain more than one. Else it throws a warning
    if "examples" in str.lower(scenario):
        examples = str.lower(scenario).split("examples:")[1]
        exampelines = re.split("\(\d*\)",examples)
        if len(exampelines) <= 3:
            line_number = scenario.split(" ")[1]
            warnings.append('[WARNING] ' + str(line_number) + " Scenario outline contains only one example. Add more or change to scenario")

def check_user_reference(scenario):
    #check and warns if the description is mostly referring to me, myself and i rather than and actor (end-user or stakeholder)
    #given i ...
    #when i
    x = re.findall(" i *| me *| we *|",str.lower(scenario))
    if x:
        line_number = scenario.split(" ")[1]
        debuglog(scenario)
        warnings.append('[WARNING] ' + str(line_number) + " It is generally bad practise to refer to yourself in BDD. Refer to an actor.")

def check_pseudo_code(scenario):
    x = re.findall("-|\+|\*|\/|=",str.lower(scenario))
    if x:
        line_number = scenario.split(" ")[1]
        debuglog(scenario)
        warnings.append('[WARNING] ' + str(line_number) + " Usage of +-\/= indicates pseudo code. Reformulate it to better BDD")

####imports####
import sys
import getopt
import re
import json

####global variables####
warnings = []
errors = []
score = 0.0 #(total scenarios in file - (warnings*0,5) - errors) / total scenarios in file    (8 - (3/2)-3) / 8
debug = False

####mainline####
if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:],"vhm:i:",["m=","i=","v="])
    except getopt.GetoptError:
        print('Invalid arguments. Please run python glint.py -h for help')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python glint.py -m <mode> -i <inputfile>')
            print('     Mode can be either file, object or api')
            print('     In case of mode file, you will need to specify -i with the full path to the file you want to parse')
            print('     In case of mode object, you will need to specify -i the json formatted object you wish to parse')
            print('     -v for verbose logging')
            sys.exit()
        elif opt in ("-m", "--mode"):
            mode = arg.strip()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-v", "--verbose"):
            debug = True
    
    if mode == 'file' or mode == 'object':
        debuglog('Running in mode: %s' % (mode,))
        if mode == 'file':
            try:
                scenarios = read_feature_file(inputfile)
                debuglog('%s lines from scenarios read into memory' % (len(scenarios),))
            except:
                print('Can not read inputfile, please run python glint.py -h for help')
            single_line_scenarios = parse_scenarios(scenarios)
        else:
            single_line_scenarios = json.loads(inputfile)
        
        
        debuglog('%s scenarios read into memory' % (len(single_line_scenarios),))

        for s in single_line_scenarios:
            if len(s.strip())>0:
                parse_quality_checks(s)

    elif mode == 'api':
        #start a flask app to listen to input
        pass
    else:
        print('Invalid mode: %s, please run python glint.py -h for help' % (mode,))
    
    #calculate score
    score = round((len(single_line_scenarios) - (len(warnings)*0.5) - len(errors)) / len(single_line_scenarios)*100,0) 
    print("Total errors found: %s" % (len(errors),))
    print("Total warnings found: %s" % (len(warnings),))
    v="%"
    print("Total quality score: %s%s" % (score,v))
    
    #print errors
    for e in errors:
        print(e)
    for w in warnings:
        print(w)

