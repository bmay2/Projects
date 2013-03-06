import random

total = random.randint(200000,1000000)
print "Your total is $%d." % total

print "Looking through your rather large wallet to see how much change you have..."
change = [random.choice([1,5,10,20,50]) for i in xrange(0,random.randint(1500000,2500000))]
print "\nDone looking!\n"

if total > sum(change):
    print "You're $%d short!" % (total-sum(change))

pretotal = total

# print change

def num(change, total):
    set = []
    num_count = {}
    numbers = [50,20,10,5,1]
    words = ['fifty','twenty', 'ten', 'five', 'one']
    
    for i in numbers:
        num_count[i] = change.count(i)
        print "You have %d %s-dollar bill(s)." % (num_count[i], words[numbers.index(i)])
    
    for i in numbers:
        num_in_total = total / i # check number of certain bill in total
        for j in range(0, min(num_in_total, num_count[i])): # use max number of bills available
            set.append(i) # add to set for final combo
        total = total - min(num_in_total, num_count[i])*i # take $x-bills out of total
    
    print "\nYou decide to pay with:"
    for i in numbers:
         print "\t%d %s-dollar bill(s)." % (set.count(i), words[numbers.index(i)])
    
    return set, sum(set)-pretotal
    
    # python -m cProfile at5.py
    
print num(change, total)