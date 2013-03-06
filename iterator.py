import itertools

def begin():
    input_values = {}
    
    textPrompt = 'Enter the text you would like to iterate over with #\'s in the place of increasing numbers and @\'s in the place of iterating phrases/letters: '
    lowerPrompt = 'Enter your starting number: '
    upperPrompt = 'Enter your ending number: '
    wordsPrompt = 'Enter the words you would like to iterate over (separated by commas): '
        
    input_values['text'] = getRegChoice(textPrompt, split=True)
    input_values['lower'] = getIntChoice(lowerPrompt)
    input_values['upper'] =  getIntChoice(upperPrompt)
    input_values['words'] = getRegChoice(wordsPrompt, split=False)
    
    return input_values
    
def getRegChoice(text, split):
    return raw_input(text).split(', ') if split else raw_input(text)
    
def getIntChoice(text):
    try:
        return int(raw_input(text))
    except ValueError:
        print "That is not a number."
        return getIntChoice(text)
    
def makedict(input):
    c = getChoice()
    if c == 1:
        return output_permutations(input, numbers_first=False)
    elif c == 2:
        return output_permutations(input, numbers_first=True)
    else:
        print "That is not a valid choice."
        makedict(input)
            
def getChoice():
    try:
        return int(raw_input('1 for word-first iteration, 2 for number-first: '))
    except ValueError:
        print "That is not a number."
        return getChoice()
    
def output_permutations(dict, numbers_first):
    text, lower, upper, words = input_sort(dict)
    numbers = range(lower, upper + 1)

    data = (numbers, words) if numbers_first else (words, numbers)
    for n, w in itertools.product(*data):
        if not numbers_first: n, w = w, n
        print("Player %d likes %s." % (n, w))
        
# def make_format(template, subs):
#     text.replace('#', str(num)).replace('@', i)

def input_sort(dict):
    return dict['text'], dict['lower'], dict['upper'], dict['words']

def prompt():
    return raw_input("Press enter to see the next set (1 if you'd like to cancel): ")

def nav():
    input_values = begin()
    output_values = makedict(input_values)
    return output_values
        
nav()