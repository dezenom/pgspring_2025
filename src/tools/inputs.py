import umath

keyboard = {}
keybinds = {}

# checkKeyPress can take either string or integers , integers are pygame values ie pygame.K_a, strings are keybind values that have been set

def checkKeyPress(key)->bool:
    return (isinstance(key,int) and str(key) in keyboard and keyboard[str(key)]) or (isinstance(key,str) and str(keybinds[key]) in keyboard and keyboard[str(keybinds[key])])


# #  parameters
#     name - name of the keybind to be used in the map
#     key - what pygame key value it is to be asocciated with
def addKeybind(name,key):
    keybinds[name] = key

# give key values for certain directions and it will return a 2 dimensional vector depending on whether those key values are active or not
def getDirection(up=None,down=None,left=None,right=None)->list:
    allinputs = [up,down,left,right]
    output = [0,0,0,0]
    direction = [0,0]


    for i,inputs in enumerate(allinputs):
        cresult = inputs and checkKeyPress(inputs)
        if cresult:
            output[i] = 1

    for i,out in enumerate(output):
        if i < 2 and out:
            direction[1] += 1 if i == 1 else -1
        if i >= 2 and out:
            direction[0] += 1 if i == 3 else -1

    if direction[0] and direction[1]:
        hyp = umath.hyp(direction)
        direction[0] = direction[0] / hyp
        direction[1] = direction[1] / hyp

    return direction

